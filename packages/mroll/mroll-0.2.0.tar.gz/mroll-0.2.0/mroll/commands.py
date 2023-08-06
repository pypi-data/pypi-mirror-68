#!/usr/bin/env python3

import click
import os
import shutil
import configparser
from datetime import datetime
import importlib.util
import importlib.machinery
from mroll.config import *
from mroll.migration import Revision, MigrationContext, WorkDirectory


def load_module_py(module_id, path):
    spec = importlib.util.spec_from_file_location(module_id, path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module

def get_templates_dir():
    dir_ = os.path.dirname(__file__)
    return os.path.join(dir_, 'templates')

def get_env():
    config = Config.from_file(MROLL_CONFIG_FILE)
    path = os.path.join(config.work_dir, 'env.py')
    env = load_module_py('env', path)
    return env

def rev_id():
    import uuid
    return uuid.uuid4().hex[-12:]
    

# ----------------------------------

@click.group(chain=True)
@click.pass_context
def cli(ctx):
    ctx.ensure_object(dict)

@cli.command(name='setup')
@click.option('-d', '--dir', 'dir_', default='migrations', help='name of the work directory')
@click.option('-p', '--path', help='path to work directory')
def setup(dir_, path):
    """
    Set up work directory. Should be run once.
    """
    directory = path or os.path.join(os.getcwd(), dir_)
    if os.access(directory, os.F_OK) and os.listdir(directory):
        raise ValueError("Directory %s already exists and is not empty" % directory)
    versions = os.path.join(directory, 'versions')
    os.mkdir(directory)
    os.mkdir(versions)
    tmpl_dir = get_templates_dir()
    shutil.copy(os.path.join(tmpl_dir, 'mroll.ini'), directory)
    shutil.copy(os.path.join(tmpl_dir, 'env.py'), directory)
    #  setup config file
    if not os.path.exists(SYS_CONFIG):
        os.mkdir(SYS_CONFIG)
    if not os.path.exists(MROLL_CONFIG_DIR):
        os.mkdir(MROLL_CONFIG_DIR)
    config = configparser.ConfigParser()
    config['mroll'] = dict(work_dir=directory)
    with open(MROLL_CONFIG_FILE, 'w') as configfile:
        config.write(configfile)
    assert os.path.exists(MROLL_CONFIG_FILE)
    print('ok')

@cli.command(name='config')
@click.option('-p', '--path', help='path to work directory')
def config(path):
    """
    Set up mroll configuration under $HOME/.config/mroll
    """
    directory = path or os.path.join(os.getcwd(), 'migrations')
    dir_list = os.listdir(directory)
    check = ('mroll.ini' in dir_list) and ('versions' in dir_list)
    if not check:
        raise ValueError("specified path {} is not valid mroll working directory!")
    #  setup config file
    if not os.path.exists(SYS_CONFIG):
        os.mkdir(SYS_CONFIG)
    if not os.path.exists(MROLL_CONFIG_DIR):
        os.mkdir(MROLL_CONFIG_DIR)
    config = configparser.ConfigParser()
    config['mroll'] = dict(work_dir=directory)
    with open(MROLL_CONFIG_FILE, 'w') as configfile:
        config.write(configfile)
    assert os.path.exists(MROLL_CONFIG_FILE)
    print('ok')

@cli.command(name='init')
def init():
    """
    Creates mroll_revisions tbl. Should be run once.
    """
    env = get_env()
    try:
        # if following succeeds then mroll revisons tbl exist.
        env.get_head()
        return print("Nothing to do! Mroll revisions table already exist.")
    except:
        pass
    try:
        env.create_revisions_table() and print('{} created'.format(env.tbl_name))
    except Exception as e:
        print(e)
        raise SystemExit('init failed')
    print('Done')
    
@cli.command(name='revision')
@click.option('-m', '--message', help='gets added to revision name')
def revision(message):
    """
    Creates new revision from a template.
    """
    config = Config.from_file(MROLL_CONFIG_FILE)
    wd = WorkDirectory(config.work_dir)
    ts = datetime.now().isoformat()
    id_ = rev_id()
    description = message or ''
    file_ = os.path.join(get_templates_dir(), 'revision_template.txt')
    with open(file_, 'r') as f:
        template = f.read()
        kebab = description.strip().replace(' ', '_')
        fn = os.path.join(wd.path, 'versions', '{}_{}.sql'.format(id_, kebab))
        with open(fn, 'w+') as fw:
            fw.write('-- identifiers used by mroll\n')
            header = "-- id={}\n-- description={}\n-- ts={}\n".format(id_, description, ts)
            fw.write(header)
            fw.write(template)
        assert os.path.exists(fn)
    print('ok')

@cli.command(name='history')
def history():
    """
    Shows applied revisions.
    """
    return applied_revisions()
    
def all_revisions():
    config = Config.from_file(MROLL_CONFIG_FILE)
    wd = WorkDirectory(config.work_dir)
    for rev in wd.revisions:
        print(rev)

def applied_revisions():
    migr_ctx = MigrationContext.from_env(get_env())
    for r in migr_ctx.revisions:
        print(r)

def pending_revisions():
    """
    Shows pending revisions not yet applied.
    """
    config = Config.from_file(MROLL_CONFIG_FILE)
    wd = WorkDirectory(config.work_dir)
    env = get_env()
    migr_ctx = MigrationContext.from_env(env)
    working_set = wd.revisions
    if migr_ctx.head is not None:
        def filter_fn(rev):
            return datetime.fromisoformat(rev.ts) > migr_ctx.head.ts
        working_set = list(filter(filter_fn, working_set))
    for r in working_set:
        print(r)

@cli.command(name="show")
@click.argument('subcmd', nargs=1)
def show(subcmd):
    """
    Shows revisions information.\n
    mroll show [ all | pending | applied ]
    """
    if subcmd not in ['all', 'pending', 'applied']:
        raise SystemExit("Invalid sub command!")
    if subcmd == 'pending':
        return pending_revisions()
    if subcmd == 'applied':
        return applied_revisions()
    return all_revisions()

@cli.command(name="upgrade")
@click.option('-n', '--num', help="run n number of pending revisions")
def upgrade(num):
    """
    Applies all revisions not yet applied in work dir.
    """
    config = Config.from_file(MROLL_CONFIG_FILE)
    wd = WorkDirectory(config.work_dir)
    env = get_env()
    migr_ctx = MigrationContext.from_env(env)
    working_set = wd.revisions
    if migr_ctx.head is not None:
        print('adjusting working set ...')
        def filter_fn(rev):
            return datetime.fromisoformat(rev.ts) > migr_ctx.head.ts
        working_set = list(filter(filter_fn, working_set))
    ptr = num or len(working_set)
    for rev in working_set[:ptr]:
        try:
            env.add_revision(rev.id, rev.description, rev.ts, rev.upgrade_sql)
        except Exception as e:
            print(e)
            raise SystemExit('Upgrade failed at revision id={} description={}'.format(rev.id, rev.description))
    print('Done')

@cli.command(name='rollback')
@click.option('-n', '--num', help="rollbacks n number applied revisions")
def rollback(num):
    """
    Downgrades to previous revision by default. 
    """
    config = Config.from_file(MROLL_CONFIG_FILE)
    wd = WorkDirectory(config.work_dir)
    count = num or 1
    while count:
        env = get_env()
        migr_ctx = MigrationContext.from_env(env)
        if migr_ctx.head is None:
            print("Nothing to do!")
            return
        print('Rolling back id={} description={} ...'.format(migr_ctx.head.id, migr_ctx.head.description)) 
        downgrade_sql = ''
        for rev in reversed(wd.revisions):
            if rev.id == migr_ctx.head.id:
                downgrade_sql = rev.downgrade_sql
                break
        try:
            env.remove_revision(migr_ctx.head.id, downgrade_sql)
        except Exception as e:
            print(e)
            raise SystemExit('Rollback failed!')
        count-=1
    print('Done')

@cli.command(name='version')
def version():
    """
    Shows current version
    """
    from . import __version__
    print(__version__)

if __name__ == '__main__':
    cli()
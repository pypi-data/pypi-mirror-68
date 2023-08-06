from invoke import task
from mundi import cli
from mundi import fix


@task
def test(ctx):
    ctx.run("pytest tests/ --cov")
    ctx.run("black --check .")
    ctx.run("pycodestyle")


@task
def prepare_data(ctx, compile_only=False, fast=False):
    """
    Prepare data from .data/ folder and include the processed results into
    .mundi_healthcare/databases/
    """
    pkg = 'mundi_healthcare'

    if compile_only or not fast:
        ctx.run("rm mundi_healthcare/databases/* -rfv")
        cli.prepare(pkg)
        print('-' * 40, end='\n\n')

    if not compile_only:
        for db in ['capacity']:
            cli.compile(pkg, db, f'{db}.pkl.gz', fix=[fix.sum_children])
            print('-' * 40, end='\n\n')


@task
def publish(ctx, which="minor"):
    """
    Publish package.
    """
    # Do not publish broken code!
    test(ctx)

    ctx.run("git status")
import click

@click.command(name="hello")
@click.option('--name', required=True, help='Your name')
def hello(name):
    click.echo("Hello {}!".format(name))

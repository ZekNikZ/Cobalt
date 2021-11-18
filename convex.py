import click
import convex_encoding

@click.group()
@click.option('--debug/--no-debug', default=False)
def runGroup(debug):
    click.echo(f"Debug mode is {'on' if debug else 'off'}")

@runGroup.command()
def run():
    click.echo('Run')

@runGroup.command()
def shell():
    click.echo('Shell')


@click.group()
@click.option('--debug/--no-debug', default=False)
def encodeGroup(debug):
    click.echo(f"Debug mode is {'on' if debug else 'off'}")

@encodeGroup.command()
@click.argument('input', type=click.Path(exists=True))
@click.argument('output', type=click.Path(), default='')
def encode(input, output):
    convex_encoding.encode(input, output=output or None)

@encodeGroup.command()
@click.argument('input', type=click.Path(exists=True))
@click.argument('output', type=click.Path(), default='')
def decode(input, output):
    convex_encoding.decode(input, output=output or None)

cli = click.CommandCollection(sources=[runGroup, encodeGroup])

if __name__ == '__main__':
    cli()
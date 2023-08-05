import click
from autoxlsx import process
from pathlib import Path


@click.command()
@click.argument('excelmap', type=click.Path(exists=True))
@click.argument('parameters', type=click.Path(exists=True))
@click.argument('excelfile', type=click.Path(exists=True))
def cli(excelfile, excelmap, parameters):
    """Apply update parameters to excelfile using update file """
    process.process(Path(excelmap),
                    Path(parameters),
                    Path(excelfile))


if __name__ == '__main__':
    cli()

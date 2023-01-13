import click
from cli_pack.dataparser import commands as reader
from cli_pack.train import commands as trainer
from loguru import logger

@click.group()
@click.pass_context
def cli(ctx):
    pass

cli.add_command(reader.data)
cli.add_command(trainer.magik)

if __name__ == "__main__":
    logger.add("log.log", format="{time} {level} {message}", rotation="1 month")
    cli()
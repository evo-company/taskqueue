import sys
import asyncio
import logging

import click
import strictconf.yaml

from .config import Config
from .logging import configure_logging


log = logging.getLogger(__name__)


@click.group()
@click.argument('config')
@click.pass_context
def cli(ctx, config):
    path, _, section = config.partition('@')
    if not section:
        print('Config section is not provided')
        ctx.exit(1)

    cfg = Config()
    strictconf.yaml.init(cfg, [path], section)
    configure_logging(__package__, cfg.main)
    ctx.obj = cfg


@cli.command(name='worker')
@click.pass_obj
def worker_command(cfg: Config):
    from .worker import main

    if not cfg.main.kafka_hosts:
        log.error('No Kafka servers specified in config')
        sys.exit(1)

    asyncio.run(main(cfg))


@cli.command(name='rpc')
@click.option('--port', type=int)
@click.pass_obj
def rpc_command(cfg: Config, port):
    from .service import main

    if not cfg.main.kafka_hosts:
        log.error('No Kafka servers specified in config')
        sys.exit(1)

    asyncio.run(main(cfg, port=port))


if __name__ == '__main__':
    cli.main(prog_name=f'python -m {__package__}')

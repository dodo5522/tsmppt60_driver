from argparse import ArgumentParser
from json import dumps

from .api import TsMppt60
from .util import DEBUG, INFO, Logger


def main():
    parser = ArgumentParser(description="TS-MPPT-60 driver CLI tool")
    parser.add_argument(
        "--host",
        type=str,
        default="localhost",
        help="TS-MPPT-60 host name or IP address (default: localhost)",
    )
    parser.add_argument(
        "--port",
        type=int,
        default=80,
        help="TS-MPPT-60 port number (default: 80)",
    )
    parser.add_argument(
        "--debug",
        action="store_true",
        default=False,
        help="Enable debug mode (default: False)",
    )
    args = parser.parse_args()
    driver = TsMppt60(args.host, port=args.port)

    logger = Logger(
        "TS-MPPT-60",
        DEBUG if args.debug else INFO,
        full_log=args.debug,
    )
    logger.info(dumps(driver.get()))

import argparse
import configparser
import logging
import os
import sys
from pathlib import Path

from gandi import __version__, commands
from gandi.auth import GandiAuth, MissingApiKeyError


def run():
    """Command line entry point"""
    args = parse_args()
    setup_logging(args)
    config = read_config(args.config)

    auth = GandiAuth(os.environ.get("GANDI_API_KEY", config.get("apikey")))
    try:
        # Not all subcommands need the API key, so we won't know whether or not we need
        # it until we actually run the subcommand function
        ret = args.func(config, auth, args)
        sys.exit(0 if ret else 1)
    except MissingApiKeyError:
        print("Missing API key")
        sys.exit(1)


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("-c", "--config", type=Path, help="path to config file")
    parser.add_argument(
        "-v", "--verbose", action="store_true", help="increase output verbosity",
    )
    parser.add_argument(
        "-V",
        "--version",
        action="version",
        version="%(prog)s {version}".format(version=__version__),
    )

    subparsers = parser.add_subparsers(title="available commands")
    commands.setup.create_command(subparsers)
    commands.alias.create_command(subparsers)
    commands.mbox.create_command(subparsers)

    args = parser.parse_args()
    if "func" not in args:
        parser.print_help()
        sys.exit(1)

    return args


def setup_logging(args):
    """Setup logging"""
    level = logging.INFO if args.verbose else logging.WARNING
    logging.basicConfig(format="%(message)s", level=level)


def read_config(conf_file=None):
    """Find and read configuration file"""
    if not conf_file:
        xdg_config_home = os.environ.get("XDG_CONFIG_HOME", "~/.config")
        conf_file = Path(xdg_config_home).expanduser() / "gandi" / "config"

    config = configparser.ConfigParser()
    try:
        with conf_file.open("r") as fil:
            config.read_file(fil)
    except FileNotFoundError:
        config.read_dict({"gandi": {}})

    return config["gandi"]

import os
from pathlib import Path


def create_command(parser):
    subparser = parser.add_parser("setup", help="setup your Gandi account")
    subparser.set_defaults(func=setup)


def setup(config, *args):
    api_key = config.get("apikey", "")
    api_key = input("Gandi v5 API key [{}]: ".format(api_key)) or api_key
    if not api_key:
        print("API key is required")
        return False

    domain = config.get("domain", "")
    domain = input("Default domain [{}]: ".format(domain)) or domain

    mailbox_id = config.get("mailboxid", "")
    mailbox_id = input("Default mailbox ID [{}]: ".format(mailbox_id)) or mailbox_id

    xdg_config_home = os.environ.get("XDG_CONFIG_HOME", "~/.config")
    conf_file = Path(xdg_config_home).expanduser() / "gandi" / "config"
    conf_file.parent.mkdir(parents=True, exist_ok=True)

    with conf_file.open("w") as fil:
        lines = ["[gandi]", "apikey = {}".format(api_key)]
        if domain:
            lines += ["domain = {}".format(domain)]

        if mailbox_id:
            lines += ["mailboxid = {}".format(mailbox_id)]

        fil.write(os.linesep.join(lines) + os.linesep)

    return True

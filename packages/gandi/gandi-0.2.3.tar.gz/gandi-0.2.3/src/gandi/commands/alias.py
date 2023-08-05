import json
import os

import requests


def create_command(parser):
    subparser = parser.add_parser("alias", help="manage email aliases")
    subparser.add_argument("-m", "--mailbox", metavar="MAILBOX_ID", type=str)
    subparser.add_argument("-d", "--domain", type=str)

    actions = subparser.add_mutually_exclusive_group(required=True)
    actions.add_argument("-l", "--list", action="store_true")
    actions.add_argument("-a", "--add", metavar="ALIAS", type=str)
    actions.add_argument("-r", "--remove", metavar="ALIAS", type=str)

    subparser.set_defaults(func=alias)


def alias(config, auth, args):
    domain = (
        args.domain
        if args.domain is not None
        else os.environ.get("GANDI_DOMAIN", config.get("domain"))
    )

    if not domain:
        print("Missing domain")
        return False

    mailbox_id = (
        args.mailbox
        if args.mailbox is not None
        else os.environ.get("GANDI_MAILBOX_ID", config.get("mailboxid"))
    )

    if not mailbox_id:
        print("Missing mailbox ID")
        return False

    url = f"https://api.gandi.net/v5/email/mailboxes/{domain}/{mailbox_id}"

    aliases = get_aliases(url, auth)
    if aliases is None:
        return False

    if args.list:
        print(os.linesep.join(sorted(aliases)))
        return True

    if args.add:
        return add_alias(url, auth, args.add, aliases)

    if args.remove:
        return remove_alias(url, auth, args.remove, aliases)

    # Unreachable
    raise AssertionError


def get_aliases(url, auth):
    res = requests.get(url, auth=auth)
    if res.status_code != 200:
        return None

    data = json.loads(res.text)
    return set(data["aliases"])


def add_alias(url, auth, alias, aliases):
    if alias in aliases:
        print(f"Alias '{alias}' already exists")
        return False

    if not update_aliases(url, auth, aliases | {alias}):
        return False

    print(f"Created alias '{alias}'")
    return True


def remove_alias(url, auth, alias, aliases):
    if alias not in aliases:
        print(f"Alias '{alias}' does not exist")
        return False

    if not update_aliases(url, auth, aliases - {alias}):
        return False

    print(f"Removed alias '{alias}'")
    return True


def update_aliases(url, auth, aliases):
    res = requests.patch(url, json={"aliases": list(aliases)}, auth=auth)
    try:
        res.raise_for_status()
    except requests.HTTPError as e:
        print("Error occurred while updating aliases")
        print(e.args)
        return False

    return True

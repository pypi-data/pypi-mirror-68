import json
import os

import requests


def create_command(parser):
    subparser = parser.add_parser("mbox", help="manage email mailboxes")
    subparser.add_argument("-d", "--domain", type=str)

    actions = subparser.add_mutually_exclusive_group(required=True)
    actions.add_argument("-l", "--list", action="store_true")

    subparser.set_defaults(func=mbox)


def mbox(config, auth, args):
    domain = (
        args.domain
        if args.domain is not None
        else os.environ.get("GANDI_DOMAIN", config.get("domain"))
    )

    if not domain:
        print("Missing domain")
        return False

    url = f"https://api.gandi.net/v5/email/mailboxes/{domain}"

    mboxes = get_mailboxes(url, auth)
    if mboxes is None:
        return False

    if args.list:
        fmt = "{:<30} {:<16} {:<8} {:>12}   {}"
        header = fmt.format("Address", "Domain", "Type", "Quota Used", "Mailbox ID")
        rows = [
            fmt.format(
                mbox["address"],
                mbox["domain"],
                mbox["mailbox_type"],
                mbox["quota_used"],
                mbox["id"],
            )
            for mbox in mboxes
        ]

        print(header)
        print(os.linesep.join(rows))

    return True


def get_mailboxes(url, auth):
    res = requests.get(url, auth=auth)
    if res.status_code != 200:
        return None

    data = json.loads(res.text)
    return data

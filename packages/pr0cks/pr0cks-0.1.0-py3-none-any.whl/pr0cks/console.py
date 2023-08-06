"""
Author: Nicolas VERDIER (contact@n1nj4.eu)
This file is part of pr0cks.

pr0cks is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

pr0cks is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with pr0cks.  If not, see <http://www.gnu.org/licenses/>.
"""

import argparse
import asyncore
import logging
import sys
import traceback
from typing import List

from pr0cks_extension.cli import Pr0cksCommand, iter_extensible_commands

from pr0cks import socks
from pr0cks.server import Pr0cks5Server


class ProxyTypes:
    SOCKS5 = socks.PROXY_TYPE_SOCKS5
    SOCKS4 = socks.PROXY_TYPE_SOCKS4
    HTTP = socks.PROXY_TYPE_HTTP

    def __iter__(self):
        return (member for member in dir(self) if not member.startswith('_'))

    def __getitem__(self, item):
        res = getattr(self, item, None)
        if res is None:
            raise KeyError(item)
        return res


ProxyTypes = ProxyTypes()


# pylint:disable=too-many-statements
def main():
    logging.basicConfig(stream=sys.stderr, level=logging.INFO)

    parser = argparse.ArgumentParser(
        prog='procks',
        description="Transparent SOCKS5/SOCKS4/HTTP_CONNECT Proxy"
    )
    parser.add_argument(
        '--type', default=ProxyTypes.SOCKS5,
        choices=list(ProxyTypes),
        help="The type of proxy to forward the traffic to"
    )
    parser.add_argument('-p', '--port', type=int, default=10080,
                        help="port to bind the transparent proxy on the local socket "
                             "(default 10080)")
    parser.add_argument('-n', '--nat', action='store_true',
                        help="set bind address to 0.0.0.0 to make pr0cks work "
                             "from a netfilter FORWARD rule instead of OUTPUT")
    parser.add_argument('-v', '--verbose', action="store_true",
                        help="print all the connections requested through the proxy")
    parser.add_argument('-c', '--no-cache', action="store_true", help="don't cache dns requests")
    parser.add_argument('--username', default=None,
                        help="Username to authenticate with to the server. "
                             "The default is no authentication.")
    parser.add_argument('--password', default=None,
                        help="Only relevant when a username has been provided")

    parser.add_argument("proxy_addr")
    parser.add_argument("proxy_port", type=int)

    commands = add_extensible_commands(parser)

    args = parser.parse_args()

    if args.verbose:
        logging.getLogger().setLevel(logging.DEBUG)

    bind_address = "127.0.0.1"
    if args.nat:
        bind_address = "0.0.0.0"

    try:
        proxy_type = ProxyTypes[args.type]
    except KeyError:
        logging.error("[-] --proxy : unknown proxy type %s", args.type)
        sys.exit(1)
    proxy_addr = args.proxy_addr
    proxy_port = args.proxy_port

    if args.username:
        if not args.password:
            sys.exit("username provided but without password !")
        logging.info(
            "[+] Provided credentials are %s:%s",
            args.username,
            args.password[0:3] + "*" * (len(args.password) - 3)
        )

    for command in commands:
        command.execute(args, bind_address)

    socks.setdefaultproxy(
        proxytype=proxy_type,
        addr=proxy_addr,
        port=proxy_port,
        username=args.username,
        password=args.password
    )

    logging.info(
        "[+] Forwarding all TCP traffic received on %s:%s through the %s proxy on %s:%s",
        bind_address, args.port, args.type, proxy_addr, proxy_port
    )
    logging.info("[i] example of rule you need to have:")
    logging.info(
        "iptables "
        "-t nat "
        "-A OUTPUT "
        "-o eth0 "
        "-p tcp "
        "-m tcp !-d <proxy_server> "
        "-j REDIRECT "
        "--to-ports %s",
        args.port
    )
    logging.info(
        "iptables "
        "-t nat "
        "-A OUTPUT "
        "-o eth0 "
        "-p udp -m udp "
        "--dport 53 "
        "-j REDIRECT --to-ports %s",
        args.dns_port
    )
    logging.info(
        "[i] Tip to avoid leaks : Block IPv6. "
        "For ipv4 put a DROP policy on OUTPUT and only allow TCP to your socks proxy. "
        "cf. the iptables.rules example file"
    )

    try:
        Pr0cks5Server(bind_address, args.port)
        asyncore.loop()
    except KeyboardInterrupt:
        sys.stdout.write("\n")
        sys.exit(0)
    except Exception:  # pylint:disable=broad-except
        sys.stderr.write(traceback.format_exc())
        sys.exit(1)


def add_extensible_commands(parser: argparse.ArgumentParser) -> List[Pr0cksCommand]:
    """
    Adds extensible commands to the given parser in groups of the Command's name

    @return: Instantiated commands to be executed
    """
    commands: List[Pr0cksCommand] = []
    # pylint:disable=invalid-name
    for Command in iter_extensible_commands():
        group = parser.add_argument_group(Command.NAME)
        commands.append(Command(group))
    return commands


if __name__ == '__main__':
    main()

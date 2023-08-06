"""
pr0cks
Copyright (C) 2020 LoveIsGrief

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <http://www.gnu.org/licenses/>.
"""
import asyncore
import logging
import socket
import struct
import sys

from pr0cks import socks

# Python socket module does not have this constant
SO_ORIGINAL_DST = 80


class ErrorHandler:

    # pylint:disable=no-self-use
    def handle_error(self):
        _type, value, traceback = sys.exc_info()
        logging.error("[-] Socks5conn Error: %s : %s\n%s", _type, value, traceback)


class Socks5Conn(ErrorHandler, asyncore.dispatcher):
    def __init__(self, sock=None, _map=None, conn=True):
        self.out_buffer = b""
        self.allsent = False
        self.log = logging.getLogger(self.__class__.__name__)
        if conn is True:
            # get the original dst address and port
            odestdata = sock.getsockopt(socket.SOL_IP, SO_ORIGINAL_DST, 16)
            _, port, addr1, addr2, addr3, addr4 = struct.unpack("!HHBBBBxxxxxxxx", odestdata)
            address = "%d.%d.%d.%d" % (addr1, addr2, addr3, addr4)
            self.log.debug(
                '[+] Forwarding incoming connection from %s to %s through the proxy',
                repr(sock.getpeername()),
                (address, port)
            )
            # connect to the original dst :
            self.conn_sock = socks.socksocket()
            # self.conn_sock.settimeout(15)
            self.conn_sock.connect((address, port))

            self.sock_class = Socks5Conn(
                sock=self.conn_sock,
                conn=self
            )  # add a dispatcher to handle the other side
        else:
            self.sock_class = conn
            self.conn_sock = None
        asyncore.dispatcher.__init__(self, sock, _map)

    def initiate_send(self):
        num_sent = 0
        num_sent = asyncore.dispatcher.send(self, self.out_buffer[:4096])
        self.out_buffer = self.out_buffer[num_sent:]

    def handle_write(self):
        self.initiate_send()

    def writable(self):
        return self.allsent or len(self.out_buffer) > 0

    def send(self, data):
        # if self.debug:
        #    self.log_info('sending %s' % repr(data))
        if data:
            self.out_buffer += data
        else:
            self.allsent = True
        # self.initiate_send()

    def handle_read(self):
        data = self.recv(8192)
        self.sock_class.send(data)

    def handle_close(self):
        leftover_size = len(self.sock_class.out_buffer)
        while leftover_size > 0:
            logging.debug("sending %s leftover data", leftover_size)
            self.sock_class.initiate_send()
            leftover_size = len(self.sock_class.out_buffer)

        self.sock_class.close()
        self.close()


class Pr0cks5Server(ErrorHandler, asyncore.dispatcher):
    """
    The server accepting connections on a specified port.

    Accepted connections are handled in a new async channel by Socks5Conn
    """

    def __init__(self, host, port):
        asyncore.dispatcher.__init__(self)
        self.create_socket(socket.AF_INET, socket.SOCK_STREAM)
        self.set_reuse_addr()
        self.bind((host, port))
        self.listen(20)
        self.sock = None

    def handle_accept(self):
        pair = self.accept()
        if pair is None:
            return
        sock, addr = pair  # pylint: disable=unused-variable

        # TODO is this necessary?
        self.sock = sock

        # Handle the connection
        Socks5Conn(sock)

    def handle_close(self):
        self.sock.close()
        self.close()

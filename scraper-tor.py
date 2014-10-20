import socket
import socks
import stem

import urllib
import random

class ScraperTor():
    socks_port = 7000
    socks_address = '127.0.0.1'
    tor_config = {}
    tor_process = None

    def set_socks_port(self, port):
        """ Set the port for SOCKS
        """
        self.socks_port = port

    def set_socks_address(self, address):
        """ Set the address for SOCKS
        """
        self.socks_address = address

    def _getaddrinfo(*args):
        """ Perfomrs DNS resolution
        """
        return [(socket.AF_INET, socket.SOCK_STREAM, 6, '', (args[0], args[1]))]

    def set_socks_proxy(self, address = None, port = None):
        """ Set socks proxy
        """
        port = port or self.socks_port
        address = address or self.socks_address
        socks.setdefaultproxy(socks.PROXY_TYPE_SOCKS5, address, port)
        socket.socket = socks.socksocket
        socket.getaddrinfo = self._getaddrinfo

    def _tor_print(self, line):
        """ Print tor bootstrap info
        """
        if "Bootstrapped" in line:
            print "%s" % (line)

    def set_tor_config(self, config):
        """ Set tor configuration
        """
        self.tor_config = config

    def start_tor_process(self):
        """ Start a tor process
        """
        self.tor_process = stem.process.launch_tor(init_msg_handler = self._tor_print)

    def start_tor_process_with_config(self, config = None):
        """ Start a tor process with configuration
        """
        config = config or self.tor_config

        if not config:
            config = {
                    'SocksPort': str(self.socks_port)
                    }

        self.tor_process = stem.process.launch_tor_with_config(config, init_msg_handler = self._tor_print)

    def stop_tor_process(self,):
        """ Stop tor process
        """
        self.tor_process.kill()



if __name__ == '__main__':

    tor = ScraperTor()

    tor.set_socks_proxy()

    print('SOCKS Address: %s Port: %s' % (tor.socks_address, tor.socks_port))

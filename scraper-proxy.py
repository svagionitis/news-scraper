import urllib
import random

class ScraperProxy():
    proxy = None
    _proxy_list = []

    def set_proxy(self, proxy):
        """ Set the proxy
        """
        self.proxy = proxy

    def load_proxies(self, filename):
        """ Load proxies from a file to a list
        """
        with open(filename) as f:
            for line in f:
                line = line.strip()
                if line:
                    self._proxy_list.append(line)

    def set_random_proxy(self, filename):
        """ Set proxy randomly from a file
        """
        # If the proxy list is populated, then get the random one
        # Else load the proxies from the file first and then choose one randomly
        if self._proxy_list:
            set_proxy(random.choice(self._proxy_list))
        else:
            self.load_proxies(filename)
            self.set_proxy(random.choice(self._proxy_list))

    def check_proxy(self, proxy = None, test_url='https://www.google.com'):
        """ Check if a proxy is dead (False) or alive (True)
        """
        # See http://stackoverflow.com/questions/16738525/python-default-values-for-class-member-function-parameters-set-to-member-variabl
        proxy = proxy or self.proxy

        try:
            urllib.urlopen(test_url, proxies={'http':'http://'+proxy,
                                              'https':'http://'+proxy})
        except IOError:
            print('Connection error! Proxy %s possibly dead...' % proxy)
            return False
        else:
            print('Proxy %s is alive...' % proxy)
            return True

    def get_external_ip(self, with_proxy = False, proxy = None):
        """ Get the external ip using dnsdynamic.org
            enabling or disabling proxy
        """
        dnsdynamic_url = 'http://myip.dnsdynamic.org/'
        myexternalip_url = 'http://myexternalip.com/raw'
        proxy = proxy or self.proxy
        try:
            if with_proxy:
                response = urllib.urlopen(dnsdynamic_url, proxies={'http':'http://'+proxy,
                                                                   'https':'http://'+proxy})
            else:
                response = urllib.urlopen(dnsdynamic_url)

            try:
                ip = response.read()
            finally:
                response.close()

        except IOError:
            print('Connection error for %s with proxy %s' % (dnsdynamic_url, proxy))
            return None
        else:
            print('IP returned is %s' % ip)
            return ip


if __name__ == '__main__':

    proxy = ScraperProxy()

    test_proxy = '58.215.142.208:80'

    print('Set proxy to %s' % test_proxy)
    proxy.set_proxy(test_proxy)

    print('Test proxy %s' % proxy.proxy)
    proxy.check_proxy()

    proxy.set_random_proxy('proxies.txt')
    print('Set random proxy from file %s' % proxy.proxy)

    proxy.set_proxy(test_proxy)
    print('External IP with no proxy: %s' % proxy.get_external_ip())
    print('External IP with proxy (%s): %s' % (proxy.proxy, proxy.get_external_ip(with_proxy = True)))


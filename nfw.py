import re
import requests
import getpass
import atexit
import threading
import time
import logging as log
import coloredlogs
coloredlogs.install()
log.basicConfig(level=log.INFO)

from requests.packages.urllib3.exceptions import InsecureRequestWarning
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

p_magic = re.compile('\"magic\" value=\"(?P<magic>.+)\"', re.MULTILINE)
p_login_failed = re.compile('Authentication Failed', re.MULTILINE)
p_refresh = re.compile(
    'location.href=\"(?P<url>.+keepalive.+)\"', re.MULTILINE)
p_logout = re.compile('location.href=\"(?P<url>.+logout.+)\"', re.MULTILINE)


class NetAccess(object):

    def __init__(self):
        super(NetAccess, self).__init__()
        self.loggedIn = False

    def input_credentials(self):
        log.info('Requesting credentials')
        self.username = input('username: ')
        self.passwd = getpass.getpass()
        return self.setup()

    def refresh(self):
        if self.loggedIn:
            r_refresh = requests.get(self.refresh_url, verify=False)
            if r_refresh.status_code == 200:
                log.info('Refreshing with %s', self.refresh_url)
            else:
                log.error('Refresh failed with %s at %s',
                          r_refresh.status_code, self.refresh_url)

    def logout(self):
        if self.loggedIn:
            r_logout = requests.get(self.logout_url, verify=False)
            if r_logout.status_code == 200:
                log.warning('Logged out with %s', self.logout_url)
                self.loggedIn = False
            else:
                log.error('Logout failed with %s at %s',
                          r_logout.status_code, self.logout_url)

    def setup(self):
        try:
            r_bing = requests.get('http://www.bing.com', allow_redirects=False)
        except Exception as e:
            #raise e
            log.critical(e)
            return False
        else:
            log.info('Test status code is %s', r_bing.status_code)
            if r_bing.status_code == 303:
                log.warning('Internet not authorized yet')
                r_rdr = requests.get('http://www.bing.com', verify=False)
                log.info('Logging in from %s', r_rdr.url)
                match_netaccess = p_magic.search(r_rdr.text)
                self.magic = match_netaccess.group('magic')
                r_auth = requests.post('https://nfw.iitm.ac.in:1003',
                                       data={
                                           'magic': self.magic,
                                           '4Tredir': 'archlinux.org',
                                           'username': self.username,
                                           'password': self.passwd
                                       },
                                       headers={
                                           'Referer': r_rdr.url
                                       }, verify=False)

                if p_login_failed.search(r_auth.text) is not None:
                    log.error('Wrong credentials')
                    return False
                self.refresh_url = p_refresh.search(r_auth.text).group('url')
                self.logout_url = p_logout.search(r_auth.text).group('url')
                self.loggedIn = True
                log.info('KeepAlive from %s', p_refresh.search(
                    r_auth.text).group('url'))
                log.info('Logout from %s', p_logout.search(
                    r_auth.text).group('url'))
                return True
            elif r_bing.status_code == 200:
                log.warning('Internet works already!')
            else:
                log.error('Error')
            return False


def periodic_refresh(_netaccess):
    _netaccess.refresh()


def clean_exit(_netaccess):
    _netaccess.logout()
    #_timerthread.cancel()


def main():
    netaccess = NetAccess()
    if netaccess.input_credentials():
        #timer = threading.Timer(5.0, periodic_refresh, [netaccess])
        atexit.register(clean_exit, netaccess)
        while True:
            periodic_refresh(netaccess)
            time.sleep(9*60)
    return

if __name__ == '__main__':
    main()

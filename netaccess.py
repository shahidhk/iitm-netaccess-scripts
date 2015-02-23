import requests
import re

class Netaccess:

    def __init__(self, username, password, duration):
        self.session = requests.Session()
        self._username = username
        self._password = password
        self._duration = duration
        self._base_url = 'https://netaccess.iitm.ac.in/account/'

        self._USERNAME_PASSWORD_ERR_MSG_ = 'Invalid username/password'
        self._AUTH_SUCCESS_MSG_ = 'Netaccess authenticated successfully'
        self._ERROR_MSG_ = 'Unidentifiable error occured. Please try again'
        self._IP_ADDR_REGEX_ = r'Your present IP address is <strong>(\d{1,3}.\d{1,3}.\d{1,3}.\d{1,3})</strong>'
        self._AUTH_VERIFY_STR_ = 'Login failed'
        self._LOGIN_VERIFY_STR_PREFIX_ = '/account/revoke/'

    def authenticate(self):
        auth_data = {'userLogin': self._username, 'userPassword': self._password}
        try:
            auth_response = self.session.post(self._base_url + 'login', data=auth_data)
            if self._AUTH_VERIFY_STR_ in auth_response.text:
                return (False, self._USERNAME_PASSWORD_ERR_MSG_)
            else:
                current_ip = re.search(self._IP_ADDR_REGEX_, auth_response.text).group(1)
                approve_data = {'duration': self._duration, 'approveBtn': ''}
                try:
                    approve_response = self.session.post(self._base_url + 'approve', data=approve_data)
                    if self._LOGIN_VERIFY_STR_PREFIX_ + current_ip in approve_response.text:
                        return (True, self._AUTH_SUCCESS_MSG_)
                    else:
                        return (False, self._ERROR_MSG_)
                except Exception, e:
                    return (False, e.message)
                else:
                    return (False, self._ERROR_MSG_)
        except Exception, e:
            return (False, e.message)
        else:
            return (False, self._ERROR_MSG_)

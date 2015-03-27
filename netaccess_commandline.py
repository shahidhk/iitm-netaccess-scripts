#!/usr/bin/env python

import netaccess
import getpass

def auth():
    username = raw_input('Username: ')
    password = getpass.getpass()
    duration = int(raw_input("Duation (1:60 mins/2: 1 day)? "))
    handle = netaccess.Netaccess(username, password, duration)
    (status, msg) = handle.authenticate()
    if status:
        print msg
    else:
        print msg, '.', 'Try again?'
        auth()

if __name__=='__main__':
    auth()

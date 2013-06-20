#-------------------------------------------------------------------------------
# Name:        goo_gl
# Purpose:     Provides access to the Goo.gl URL shortener API
#
# Author:      Christopher Koch
#
# Created:     20/06/2013
# Copyright:   (c) Christopher Koch 2013
# Licence:     GPL 3.0
#-------------------------------------------------------------------------------

from re import match
import urllib.request as u
from urllib.parse import quote
from urllib.error import *
from json import loads

g_url = 'http://goo.gl/api/url'
g_agent = {'User-Agent': 'toolbar'}

def shorten(url):
    if not match('http://', url) and not match('https://', url):
        return ''
    g_arg = b'url={}' + bytes(url, 'utf-8')
    g_req = u.Request(g_url, g_arg, g_agent)
    try:
        e = u.urlopen(g_req)
    except HTTPError as er:
        j = loads(er.read().decode())
        if 'short_url' not in j:
            return j
        return j['short_url']
    except ValueError:
        return url
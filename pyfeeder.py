#-------------------------------------------------------------------------------
# Name:        pyfeeder
# Purpose:     Read RSS feeds and send updates to a phone via
#              Google Voice's SMS features
# Author:      Christopher Koch
#
# Created:     19/06/2013
# Copyright:   (c) Christopher Koch 2013
# Licence:     GPL 3.0
#-------------------------------------------------------------------------------

from googlevoice import *
from googlevoice.util import ValidationError
import feedparse as f
from time import sleep
from goo_gl import shorten

print("Logging in...")
v = voice.Voice()
v.login(b'yourusername@gmail.com', b'yourpassword')
num = 'your10digitphonenumber'

print("Reading feeds list...")
url_list = open('.feeds')
feeds_list = list()
for line in url_list:
    print(line, end='')
    feeds_list.append(f.Feed(line.strip('\n\r\\')))
url_list.close()

while True:
    for f in feeds_list:
        new_items = f.update()
        if new_items is not None:
            print("{} has new items".format(f.name))
            for i in new_items:
                #print("Getting short link...")
                #link = shorten(i.link)
                link = i.link
                msg = "From {}: {}... {}".format(f.name, i.title, link)
                print("Sending SMS '{}'".format(msg))
                for z in range(5):
                    try:
                        v.send_sms(num, msg)
                        print("Sent")
                        break
                    except ValidationError:
                        #Try different values here if your messages aren't sending
                        sleep(60)
                sleep(60)
    sleep(60*5)

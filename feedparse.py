#-------------------------------------------------------------------------------
# Name:        feedparse
# Purpose:     Parse RSS feed XML files
#
# Author:      Christopher Koch
#
# Created:     20/06/2013
# Copyright:   (c) Christopher Koch 2013
# Licence:     GPL 3.0
#-------------------------------------------------------------------------------

import xml.etree.ElementTree as et
import urllib.request as u
from datetime import datetime as dt
from datetime import timezone as tz
from dateutil.parser import parse

class FeedItem:
    def __init__(self, item_xml):
        self.title = item_xml.findtext('title')
        self.link = item_xml.findtext('link')
        self.published = parse(item_xml.findtext('pubDate'))

class Feed:
    def __init__(self, url):
        self.url = url
        self.last_updated = None
        self.update()

    def update(self):
        req = u.Request(self.url)
        f = u.urlopen(req)
        rss = et.fromstring(f.read())
        rss = rss.find('channel')

        feed_updated = parse(rss.findtext('lastBuildDate'))

        if self.last_updated is not None and self.last_updated > feed_updated:
            return None
        if self.last_updated is None:
            self.last_updated = dt.utcnow().replace(tzinfo = tz.utc)
            
        self.name = rss.findtext('title')

        all_items = list()
        new_items = list()

        # Each item is an object containing a datetime, title, and link

        for i in rss.iter('item'):
            this_item = FeedItem(i)
            all_items.append(this_item)
            if this_item.published > self.last_updated:
                new_items.append(this_item)

        self.items = all_items
        self.last_updated = dt.utcnow().replace(tzinfo = tz.utc)
        
        return new_items

## File download helpers ##

##def url_to_name(url):
##    return basename(urlsplit(url)[2])
##
##def download(url, local_file_name=None):
##    local_name = url2name(url)
##    req = u.Request(url)
##    r = u.urlopen(req)
##    if r.info().has_key('Content-Disposition'):
##        # get the file name
##        local_name = r.info()['Content-Disposition'].split('filename=')[1]
##        if local_name[0] == '"' or local_name[0] == "'":
##            local_name = local_name[1:-1]
##    elif r.url != url:
##        # redirected
##        local_name = url2name(r.url)
##    if local_file_name:
##        # local name user-specified
##        local_name = local_file_name
##    f = open(local_name, 'wb')
##    f.write(r.read())
##    f.close()
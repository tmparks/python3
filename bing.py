#!/usr/bin/env python3
# Download recent images from the Bing archive.
# Through trial and error, it has been determined that
# no more than 15 recent images are available for download.
#
# The XML and RSS responses provide links to 1366x768 images.
# The JSON response provides links to 1920x1080 images.
#
# Copyright 2017-2019 Thomas M. Parks <tmparks@yahoo.com>

import json, posixpath, urllib.parse, urllib.request

request_urls = [
    'https://www.bing.com/HPImageArchive.aspx?format=js&idx=0&n=7&mkt=en-US',
    'https://www.bing.com/HPImageArchive.aspx?format=js&idx=7&n=8&mkt=en-US'
    ]
    
for url in request_urls:
    with urllib.request.urlopen(url) as response:
       obj = json.load(response)
       for image in obj['images']:
           image_url = urllib.parse.urljoin(url, image['url'])
           qs = urllib.parse.urlparse(image['url']).query
           local_file = ''.join(urllib.parse.parse_qs(qs)['id'])
           print(local_file)
           urllib.request.urlretrieve(image_url, local_file)

#!/usr/bin/env python3
# Copyright 2017 Thomas M. Parks <tmparks@yahoo.com>
# Download recent Bing images.

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
           local_file = posixpath.basename(image_url)
           urllib.request.urlretrieve(image_url, local_file)
           print(local_file)

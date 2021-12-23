#!/usr/bin/env python3
# Download recent images from the Bing archive.
# Through trial and error, it has been determined that
# no more than 15 recent images are available for download.
#
# The XML and RSS responses provide links to 1366x768 images.
# The JSON response provides links to 1920x1080 images.
#
# Copyright 2017-2021 Thomas M. Parks <tmparks@yahoo.com>
# Additional contributors: Benjamin Parks

import json, os, PIL.Image, sys, tempfile, urllib.parse, urllib.request

# The screen dimensions for the 2021 16-inch MacBook Pro are 3456x2234.
# The screen area below the menu bar is 3456x2160, so that the height of the
# menu bar is 74 pixels. Thus we add 37 pixels to the top of a 1920x1080 image.
def add_menu_bar(in_file, out_file, height=37):
    input = PIL.Image.open(in_file)
    output = PIL.Image.new(input.mode, (input.size[0], input.size[1] + height))
    output.paste(input, (0, height, output.size[0], output.size[1]))
    output.save(out_file)

here = os.path.dirname(sys.argv[0])

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
            id = ''.join(urllib.parse.parse_qs(qs)['id'])
            (root, ext) = os.path.splitext(id)
            local_file = os.path.join(here, root + '.png')
            if not os.path.exists(local_file):
                print(local_file)
                temp_file = tempfile.mktemp(suffix=ext)
                urllib.request.urlretrieve(image_url, temp_file)
                add_menu_bar(temp_file, local_file)
                os.remove(temp_file)

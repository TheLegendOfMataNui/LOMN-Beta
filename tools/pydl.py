#!/usr/bin/env python
"""
Copyright (c) 2020 JrMasterModelBuilder
Licensed under MPL-2.0 <https://mozilla.org/MPL/2.0/>
"""

import os
import sys
import math
import argparse
try:
	from urllib.request import urlopen
except ImportError:
	from urllib2 import urlopen

def get_headers(req):
	r = {}
	if hasattr(req, 'getheaders'):
		for header in req.getheaders():
			r[header[0].lower()] = header[1]
	else:
		for header in req.info().headers:
			header = header.rstrip('\r\n').split(': ', 1)
			r[header[0].lower()] = header[1]
	return r

def main():
	parser = argparse.ArgumentParser()
	parser.add_argument(
		'url',
		nargs=1,
		help='URL'
	)
	parser.add_argument(
		'file',
		nargs=1,
		help='FILE'
	)
	options = parser.parse_args()
	downloading = options.url[0]
	destination = options.file[0]
	partial = '%s.part' % (destination)
	if os.path.exists(destination):
		os.remove(destination)

	#print('Downloading: %s' % (downloading))
	#print('Destination: %s' % (destination))
	#print('Partial: %s' % (partial))

	req = urlopen(downloading)
	headers = get_headers(req)
	content_length = None
	try:
		content_length = int(headers['content-length'])
	except:
		pass

	total = 0
	last_percent = -1
	with open(partial, 'wb') as f:
		while True:
			d = req.read(1024)
			if not d or not len(d):
				break
			f.write(d)
			total += len(d)

			percent = math.floor(total / float(content_length) * 100)
			if percent % 10 == 0 and percent != last_percent:
				last_percent = percent
				if content_length is not None:
					output = '%2.0f%%' % (percent)
				else:
					output = '?'
				sys.stdout.write('\t' + output + '\n')
				sys.stdout.flush()

	#print('')

	os.rename(partial, destination)

	return 0

if __name__ == '__main__':
	sys.exit(main())

#!/usr/bin/env python
"""
LOMN release packaging tool
Version: 0.1.0

Copyright (c) 2018 benji
Licensed under the Mozilla Public License, v. 2.0
"""

import argparse
import hashlib
import os
import shutil
import sys

# Case insensitive dictionary that preserves key casing, from https://stackoverflow.com/a/51083318
class CaseInsensitiveDict(dict):

	class Key(str):
		def __init__(self, key):
			str.__init__(key)
		def __hash__(self):
			return hash(self.lower())
		def __eq__(self, other):
			return self.lower() == other.lower()

	def __init__(self, data=None):
		super(CaseInsensitiveDict, self).__init__()
		if data is None:
			data = {}
		for key, val in data.items():
			self[key] = val
	def __contains__(self, key):
		key = self.Key(key)
		return super(CaseInsensitiveDict, self).__contains__(key)
	def __setitem__(self, key, value):
		key = self.Key(key)
		super(CaseInsensitiveDict, self).__setitem__(key, value)
	def __getitem__(self, key):
		key = self.Key(key)
		return super(CaseInsensitiveDict, self).__getitem__(key)

# Computes the MD5 hash of the given file, from https://stackoverflow.com/a/44873382
def md5file(filename):
	h  = hashlib.md5()
	b  = bytearray(128*1024)
	mv = memoryview(b)
	with open(filename, 'rb', buffering=0) as f:
		for n in iter(lambda : f.readinto(mv), 0):
			h.update(mv[:n])
	return h.hexdigest()

# 
# Snapshot functions
#
# (A snapshot is just a CaseInsensitiveDict of filename to md5 hash as a hex string.)
# 
def create_snapshot(directory):
	result = CaseInsensitiveDict()
	for dirname, dirnames, filenames in os.walk(directory):
		dirname_relative = os.path.relpath(dirname, directory)
		for filename in filenames:
			result [os.path.normpath(os.path.join(dirname_relative, filename))] = md5file(os.path.join(dirname, filename))
	return result

def write_snapshot(snapshot, filename):
	file = open(filename, "w")
	for filename, contentshash in snapshot.items():
		file.write(filename + ":" + contentshash + "\n")
	file.close()

def read_snapshot(filename):
	result = CaseInsensitiveDict()

	file = open(filename, "r")
	for line in file:
		if len(line) > 0:
			parts = line.strip().split(":")
			result[parts[0]] = parts[1]
	file.close()

	return result

def print_snapshot(snapshot):
	for filename, contentshash in snapshot.items():
		print(filename + ":" + contentshash)

# 
# CLI functions
# 
# 
# 
def package():
	# TODO: Package the darn thing!
	parser = argparse.ArgumentParser(
		description='Copy all files in <directory> into <outdirectory> which are modified or added relative to <snapshot>',
		usage='releasetool.py package <directory> <snapshot> <outdirectory>'
	)
	parser.add_argument('directory', help='Directory whose files are to be packaged')
	parser.add_argument('snapshot', help='Filename of the snapshot to compare the directory with')
	parser.add_argument('outdirectory', help='Directory where packaged files will be copied')
	args = parser.parse_args(sys.argv[2:])

	new_snapshot = create_snapshot(args.directory)
	old_snapshot = read_snapshot(args.snapshot)

	if os.path.isdir(args.outdirectory):
		shutil.rmtree(args.outdirectory)

	modified = 0
	for filename, contentshash in new_snapshot.items():
		if not filename in old_snapshot or old_snapshot[filename] != contentshash:
			# Added or modified
			modified += 1
			print('ADD/MODIFIED: ' + filename)
			if not os.path.isdir(os.path.dirname(os.path.join(args.outdirectory, filename))):
				os.makedirs(os.path.dirname(os.path.join(args.outdirectory, filename)))
			shutil.copyfile(os.path.join(args.directory, filename), os.path.join(args.outdirectory, filename.replace("LEGOBionicle.exe", "LEGO Bionicle.exe")))
		else:
			print('NOT MODIFIED: ' + filename)
			pass

	removed = 0
	for filename in old_snapshot:
		if not filename in new_snapshot:
			removed += 1
			print('REMOVED:      ' + filename)
	print('Added / Modified: {0:d} ({1:.1f}%), Removed: {2:d}'.format(modified, (modified * 100.0 / len(old_snapshot)), removed))
	return 0

def snapshot():
	parser = argparse.ArgumentParser(
		description='Take a snapshot of <directory> for use packaging and save it in <filename>',
		usage='releasetool.py snapshot <directory> <filename>'
	)
	parser.add_argument('directory', help='Directory to snapshot')
	parser.add_argument('filename', help='Filename to store the output snapshot in')
	args = parser.parse_args(sys.argv[2:])

	snapshot = create_snapshot(args.directory)
	write_snapshot(snapshot, args.filename)

	return 0

commands = {
	'package': package,
	'snapshot': snapshot
}

def main():
	parser = argparse.ArgumentParser(
		description=os.linesep.join([
			'LOMN release packaging tool',
			'Version: 0.1.0'
		]),
		epilog=os.linesep.join([
			'Copyright (c) 2018 benji',
			'Licensed under the Mozilla Public License, v. 2.0'
		]),
		usage=os.linesep.join([
			'releasetool.py <command> [args]',
			'',
			'Available commands are:',
			'  package <directory> <snapshot> <outdirectory>    Copy all files in <directory> into <outdirectory> which are modified or added relative to <snapshot>',
			'  snapshot <directory> <filename>                  Take a snapshot of <directory> for use packaging and save it in <filename>'
		]),
		formatter_class=argparse.RawTextHelpFormatter
	)
	parser.add_argument('command', help='Subcommand to run')
	command_args = parser.parse_args(sys.argv[1:2])
	if not command_args.command in commands:
		print('Unrecognized command.')
		parser.print_help()
		return 1
	
	return commands.get(command_args.command)()

if __name__ == '__main__':
	sys.exit(main())

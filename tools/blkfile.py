#!/usr/bin/env python
"""
SAGE BLK file tool
Version: 2.2.0

Copyright (c) 2018 JrMasterModelBuilder
Licensed under the Mozilla Public License, v. 2.0

LZSS code based on LZSS.C 4/6/1989 Haruhiko Okumura
"""

import io
import os
import sys
import struct
import json
import argparse

file_extension = '.blk'
dir_extension = '.dir'
byte_alignment = 4

def class_str(instance):
	return class_repr(instance)

def class_repr(instance):
	return '<%s: %s>' % (instance.__class__, instance.__dict__)

def getc(b):
	d = b.read(1)
	if len(d) < 1: return None
	return struct.unpack('<B', d)[0]

def putc(v, b):
	b.write(struct.pack('<B', v))




class BLKLZSS():
	def __str__(self):
		return class_str(self)

	def __repr__(self):
		return class_repr(self)

	def __init__(
		self,
		N = 4096,
		F = 18,
		THRESHOLD = 2
	):
		self.N = N
		self.F = F
		self.THRESHOLD = THRESHOLD
		self.text_buf = bytearray(N + F - 1)
		self.lson = [0] * (N + 1)
		self.rson = [0] * (N + 257)
		self.dad = [0] * (N + 1)
		self.match_length = 0
		self.match_position = 0

	def init_tree(self):
		N = self.N
		rson = self.rson
		dad = self.dad

		for i in range(N + 1, N + 256 + 1):
			rson[i] = N
		for i in range(N):
			dad[i] = N

	def insert_node(self, r):
		F = self.F
		N = self.N
		text_buf = self.text_buf
		lson = self.lson
		rson = self.rson
		dad = self.dad

		cm = 1
		key = r
		p = N + 1 + text_buf[key]
		rson[r] = N
		lson[r] = N
		self.match_length = 0

		while True:
			if cm >= 0:
				if rson[p] != N:
					p = rson[p]
				else:
					rson[p] = r
					dad[r] = p
					return
			else:
				if lson[p] != N:
					p = lson[p]
				else:
					lson[p] = r
					dad[r] = p
					return

			i = 1
			while i < F:
				cm = text_buf[key + i] - text_buf[p + i]
				if cm != 0:
					break
				i += 1

			if i > self.match_length:
				self.match_position = p
				self.match_length = i
				if i >= F:
					break

		dad[r] = dad[p]
		lson[r] = lson[p]
		rson[r] = rson[p]
		dad[lson[p]] = r
		dad[rson[p]] = r
		if rson[dad[p]] == p:
			rson[dad[p]] = r
		else:
			lson[dad[p]] = r
		dad[p] = N

	def delete_node(self, p):
		N = self.N
		lson = self.lson
		rson = self.rson
		dad = self.dad

		q = 0
		if dad[p] == N:
			return

		if rson[p] == N:
			q = lson[p]
		elif lson[p] == N:
			q = rson[p]
		else:
			q = lson[p]
			if rson[q] != N:
				while True:
					q = rson[q]
					if not (rson[q] != N):
						break
				rson[dad[q]] = lson[q]
				dad[lson[q]] = dad[q]
				lson[q] = lson[p]
				dad[lson[p]] = q
			rson[q] = rson[p]
			dad[rson[p]] = q

		dad[q] = dad[p]
		if rson[dad[p]] == p:
			rson[dad[p]] = q
		else:
			lson[dad[p]] = q
		dad[p] = N

	def encode(self, data, allocate = 0):
		F = self.F
		N = self.N
		THRESHOLD = self.THRESHOLD
		text_buf = self.text_buf

		infile = io.BytesIO(data)
		outfile = io.BytesIO(bytearray(allocate))
		code_buf = bytearray(17)

		self.init_tree()
		code_buf[0] = 0

		mask = 1
		code_buf_ptr = 1
		s = 0
		r = N - F
		i = s
		for i in range(i, r):
			text_buf[i] = 0x20

		l = 0
		while l < F:
			c = getc(infile)
			if c is None: break
			text_buf[r + l] = c
			l += 1

		if l == 0:
			return b''

		i = 1
		for i in range(i, F + 1):
			self.insert_node(r - i)

		self.insert_node(r)
		while True:
			if self.match_length > l:
				self.match_length = l

			if self.match_length <= THRESHOLD:
				self.match_length = 1
				code_buf[0] |= mask
				code_buf[code_buf_ptr] = text_buf[r]
				code_buf_ptr += 1
			else:
				mp = self.match_position
				code_buf[code_buf_ptr] = mp & 0xFF
				code_buf_ptr += 1
				code_buf[code_buf_ptr] = (
					((mp >> 4) & 0xf0) |
					(self.match_length - (THRESHOLD + 1))
				) & 0xFF
				code_buf_ptr += 1

			mask <<= 1
			mask &= 0xFF
			if mask == 0:
				i = 0
				for i in range(i, code_buf_ptr):
					putc(code_buf[i], outfile)
				code_buf[0] = 0
				code_buf_ptr = 1
				mask = 1

			last_match_length = self.match_length
			i = 0
			while i < last_match_length:
				c = getc(infile)
				if c is None: break
				self.delete_node(s)
				text_buf[s] = c
				if s < F - 1:
					text_buf[s + N] = c
				s = (s + 1) & (N - 1)
				r = (r + 1) & (N - 1)
				self.insert_node(r)
				i += 1

			while i < last_match_length:
				i += 1
				self.delete_node(s)
				s = (s + 1) & (N - 1)
				r = (r + 1) & (N - 1)
				l -= 1
				if l:
					self.insert_node(r)
			i += 1

			if not (l > 0):
				break

		if code_buf_ptr > 1:
			i = 0
			for i in range(i, code_buf_ptr):
				putc(code_buf[i], outfile)

		end = outfile.tell()
		outfile.seek(0)
		return outfile.read(end)

	def decode(self, data, allocate = 0):
		F = self.F
		N = self.N
		THRESHOLD = self.THRESHOLD
		text_buf = self.text_buf

		infile = io.BytesIO(data)
		outfile = io.BytesIO(bytearray(allocate))

		for i in range(N - F):
			text_buf[i] = 0x30

		r = N - F
		flags = 0
		while True:
			flags >>= 1
			if (flags & 256) == 0:
				c = getc(infile)
				if c is None: break
				flags = c | 0xFF00

			if flags & 1:
				c = getc(infile)
				if c is None: break

				putc(c, outfile)
				text_buf[r] = c
				r += 1
				r &= N - 1
			else:
				i = getc(infile)
				if i is None: break
				j = getc(infile)
				if j is None: break

				i |= (j & 0xf0) << 4
				j = (j & 0x0f) + THRESHOLD

				for k in range(j + 1):
					c = text_buf[(i + k) & (N - 1)]
					putc(c, outfile)
					text_buf[r] = c
					r += 1
					r &= N - 1

		end = outfile.tell()
		outfile.seek(0)
		return outfile.read(end)




class BLKError(Exception):
	pass

class BLKTypeError(BLKError):
	pass

class BLKFileReadError(BLKError):
	pass

class BLKFileWriteError(BLKError):
	pass

class BLKFileEntryError(BLKError):
	pass

class BLKEntryReadError(BLKError):
	pass




class BLKEntry():
	def __str__(self):
		return class_str(self)

	def __repr__(self):
		return class_repr(self)

	struct_entry = struct.Struct(''.join([
		'<',
		'40s', # name
		'I', # size_c
		'I', # size_d
		'I', # flags
		'I'  # offset
	]))

	def __init__(
		self,
		name = None,
		size_c = 0,
		size_d = 0,
		flags = 0,
		offset = 0
	):
		self.name = b'\x00' * 40
		if not name is None:
			self.set_name(name)
		self.size_c = size_c
		self.size_d = size_d
		self.flags = flags
		self.offset = offset

	def get_name(self):
		return self.name.split(b'\x00')[0]

	def set_name(self, name):
		self.name = struct.pack('<40s', name)

	def get_is_compressed(self):
		return self.flags & 1

	def get_block_size(self):
		if self.get_is_compressed():
			return self.size_c
		return self.size_d

class BLKEntryRead(BLKEntry):
	def __init__(
		self,
		name = None,
		size_c = 0,
		size_d = 0,
		flags = 0b10,
		offset = 0
	):
		BLKEntry.__init__(self, name, size_c, size_d, flags, offset)

	def from_read(self, read):
		[
			name,
			size_c,
			size_d,
			flags,
			offset
		] = read.read_struct(self.struct_entry)
		self.name = name
		self.size_c = size_c
		self.size_d = size_d
		self.flags = flags
		self.offset = offset

	def read_from(self, read):
		size_d = self.size_d
		compressed = self.get_is_compressed()
		block_size = self.get_block_size()
		read.seek(self.offset)
		data = read.read(block_size)
		if compressed:
			lzss = BLKLZSS()
			data = lzss.decode(data, size_d)
			data_l = len(data)
			if data_l != size_d:
				raise BLKEntryReadError(
					'Decoded size not expected: %s != %s' % (
						data_l,
						size_d
					)
				)
		return data

class BLKEntryWrite(BLKEntry):
	def __init__(
		self,
		name = None,
		size_c = 0,
		size_d = 0,
		flags = 0b10,
		offset = 0
	):
		BLKEntry.__init__(self, name, size_c, size_d, flags, offset)

	def to_write(self, write):
		write.write_struct(
			self.struct_entry,
			self.name,
			self.size_c,
			self.size_d,
			self.flags,
			self.offset
		)

	def write_to(self, write, data, compress = None):
		compressed = False
		decompressed_len = len(data)

		# If not force uncompressed, compress data.
		if not compress is False:
			# Compress data, using size as rough estimate of compressed size.
			lzss = BLKLZSS()
			data_comp = lzss.encode(data, decompressed_len)

			# If forced or smaller, use the compressed data.
			if compress is True or len(data_comp) < decompressed_len:
				data = data_comp
				compressed = True

		# Write compressed or uncompressed.
		if compressed:
			self.flags = 0b11
			self.size_c = len(data)
		else:
			self.flags = 0b10
			self.size_c = decompressed_len

		self.size_d = decompressed_len
		write.write(data)




class BLKFile():
	def __str__(self):
		return class_str(self)

	def __repr__(self):
		return class_repr(self)

	MAGIC = 0x464B4C42 # 'BLKF'
	VERSION = 1

	struct_header = struct.Struct(''.join([
		'<',
		'I', # magic
		'I', # version
		'I'  # count
	]))

	entries_offset = struct_header.size

	def __init__(self, fio, offset=None, size_max=None):
		# If offset set, use the current input offset.
		if offset is None:
			offset = fio.tell()

		# Set needed properties to use the reading methods.
		self.fio = fio
		self.__pos = 0
		self.offset = 0

		# Set size to the input limit, if specified.
		self.size = size_max

	def tell(self):
		return self.__pos

	def seek(self, offset, from_what=os.SEEK_SET):
		pos = None
		if from_what == os.SEEK_CUR:
			pos = self.__pos + offset
		elif from_what == os.SEEK_END:
			pos = self.__pos - offset
		elif from_what == os.SEEK_SET:
			pos = offset
		else:
			raise BLKTypeError('Invalid seek from type: %s' % (from_what))

		if pos < 0 or pos > self.size:
			raise BLKFileReadError('Cannot seek to: %s' % (pos))

		self.__pos = pos

	def can_read(self, size):
		return self.__pos + size < self.size

	def read(self, size):
		pos = self.__pos
		fio = self.fio
		before = fio.tell()
		seekto = self.offset + pos

		if seekto + size > self.size:
			raise BLKFileReadError('Cannot read past end of file')

		fio.seek(seekto, os.SEEK_SET)
		ret = fio.read(size)
		fio.seek(before, os.SEEK_SET)
		read_size = len(ret)

		if read_size != size:
			raise BLKFileReadError('Read an unexpected size %s' % (read_size))

		self.__pos = pos + read_size
		return ret

	def write(self, data):
		pos = self.__pos
		fio = self.fio
		before = fio.tell()
		seekto = self.offset + pos

		if seekto > self.size:
			raise BLKFileWriteError('Cannot seek past end of file')

		fio.seek(seekto, os.SEEK_SET)
		fio.write(data)
		fio.seek(before, os.SEEK_SET)

		self.__pos = pos + len(data)
		if self.__pos > self.size:
			self.size = self.__pos
			fio.seek(self.offset + self.size, os.SEEK_SET)

	def read_struct(self, structure):
		return structure.unpack_from(self.read(structure.size))

	def write_struct(self, structure, *args):
		self.write(structure.pack(*args))

class BLKFileRead(BLKFile):
	def __init__(self, fio, offset=None, size_max=None):
		# If offset set, use the current input offset.
		if offset is None:
			offset = fio.tell()

		# If maximum set, determine how much input available.
		if size_max is None:
			# Find how much data remains after input offset.
			before = fio.tell()
			fio.seek(0, os.SEEK_END)
			size_max = fio.tell() - offset
			fio.seek(before, os.SEEK_SET)

		BLKFile.__init__(self, fio, offset, size_max)

		# Check that files is large enough to read header.
		if not size_max is None and size_max < self.struct_header.size:
			raise BLKFileReadError('Input size too small: %s' % (size_max))

		[
			magic,
			version,
			count
		] = self.read_struct(self.struct_header)

		# Check the header magic.
		if magic != self.MAGIC:
			raise BLKFileReadError('Invalid input header magic: %s' % (magic))
		self.magic = magic

		# Check the header version.
		if version != self.VERSION:
			raise BLKFileReadError('Invalid header version number: %s' % (version))
		self.version = version

		# Set the count property.
		self.count = count

		# Find the last entry if present.
		last_entry = None
		for entry in self.entries():
			if not last_entry:
				last_entry = entry
			elif entry.offset > last_entry.offset:
				last_entry = entry

		# Calculate the file end, and update the size.
		size = self.entries_offset
		if last_entry:
			size = last_entry.offset + last_entry.get_block_size()
		self.size = size

		# Move the file IO to the file end.
		fio.seek(size, os.SEEK_CUR)

	def entries(self):
		entries_offset = self.entries_offset

		# Seek to entries offset.
		self.seek(entries_offset, os.SEEK_SET)

		# Loop over the entries.
		for i in range(self.count):
			# Read entry.
			entry = BLKEntryRead()
			entry.from_read(self)

			# Remember current file position, yield, then reset position.
			before = self.tell()
			yield entry
			self.seek(before, os.SEEK_SET)

	def entry_read(self, entry):
		return entry.read_from(self)

class BLKFileWrite(BLKFile):
	def __init__(self, fio, offset=None):
		BLKFile.__init__(self, fio, offset)

		self.size = 0
		self.entries = set()

	def add(self, entry):
		self.entries.add(entry)

	def save(self):
		self.seek(0, os.SEEK_SET)

		entries_ordered = sorted(
			list(self.entries),
			key=lambda entry: entry.get_name().lower()
		)
		count = len(entries_ordered)
		if count > 1:
			for i in range(count - 1):
				a = entries_ordered[i].get_name()
				b = entries_ordered[i + 1].get_name()
				if a == b:
					raise BLKFileEntryError('Duplicate entry name: %s', a)

		# Write the file header.
		self.write_struct(self.struct_header, self.MAGIC, self.VERSION, count)
		entries_offset = self.tell()

		# Write the entries table.
		for entry in entries_ordered:
			entry.to_write(self)

		# Write entry body.
		for entry in entries_ordered:
			entry.offset = self.tell()
			yield entry

			# Pad to byte alignment.
			unaligned = self.tell() % byte_alignment
			if unaligned:
				self.write(b'\x00' * (byte_alignment - unaligned))

		# Rewrite the entries table.
		before = self.tell()
		self.seek(entries_offset, os.SEEK_SET)
		for entry in entries_ordered:
			entry.to_write(self)
		self.seek(before, os.SEEK_SET)




def process_file(options, path):
	print('File: %s' % (path))

	outdir = None
	if path.lower().endswith(file_extension):
		outdir = path[0:-len(file_extension)]
	else:
		outdir = path + dir_extension
	
	if options.output != None:
		outdir = options.output

	# Open the file for binary reading.
	with open(path, 'rb') as fi:
		# Use the reader class.
		blk = BLKFileRead(fi)

		# File properties.
		print('  count: %i' % (blk.count))
		print('  size: 0x%08X' % (blk.size))

		# Create output directory unless just listing.
		if not options.list:
			if os.path.exists(outdir):
				raise BLKError(
					'Output directory already exists: %s' % (
						outdir
					)
				)
			os.mkdir(outdir)

		# Loop over the entries.
		print('  entries:')
		for entry_i, entry in enumerate(blk.entries()):
			name = entry.get_name().decode('ascii')

			# Output information on entry.
			print('  [%%%ii]: %s' % (
				len(str(blk.count)),
				(', '.join([
					'flags: 0x%08X',
					'offset: 0x%08X',
					'size_c: 0x%08X',
					'size_d: 0x%08X',
					'name: %s'
				]))
			) % (
				entry_i,
				entry.flags,
				entry.offset,
				entry.size_c,
				entry.size_d,
				json.dumps(name)
			))

			# If just listing skip extracting file.
			if options.list:
				continue

			# If name is empty, cannot extract.
			if not len(name):
				raise BLKError(
					'Name cannot be empty: %s' % (
						json.dumps(name)
					)
				)

			if '/' in name or '\\' in name:
				raise BLKError(
					'Name cannot contain slashes: %s' % (
						json.dumps(name)
					)
				)

			# Write the file to output directory.
			outfile = os.path.join(outdir, name)
			with open(outfile, 'wb') as fo:
				fo.write(blk.entry_read(entry))
				fo.close()

		fi.close()

def process_directory(options, path):
	print('Directory: %s' % (path))

	outfile = path.rstrip('/\\') + file_extension
	if options.output != None:
		outfile = options.output
	if os.path.exists(outfile):
		raise BLKError(
			'Output file already exists: %s' % (
				outfile
			)
		)

	# Check for compression option.
	compress = None
	if options.decompressed:
		compress = False
	elif options.compressed:
		compress = True

	# List files in directory.
	files = set()
	for direntry in os.listdir(path):
		# Skip any hidden files.
		if direntry.startswith('.'):
			continue
		# Only files.
		if not os.path.isfile(os.path.join(path, direntry)):
			continue
		files.add(direntry)

	# Open the file for binary writing.
	with open(outfile, 'wb') as fo:
		blk = BLKFileWrite(fo)

		# Add all the files.
		for fn in files:
			blk.add(BLKEntryWrite(fn.encode('ascii')))

		# Write it and close.
		for entry in blk.save():
			fn = entry.get_name().decode('utf8')
			print('Adding: %s' % (fn))
			with open(os.path.join(path, fn), 'rb') as f:
				entry.write_to(blk, f.read(), compress)
				f.close()
		fo.close()

def process(options):
	for path in options.paths:
		if os.path.isdir(path):
			process_directory(options, path)
		elif os.path.isfile(path):
			process_file(options, path)
		else:
			raise BLKError('Path is not valid: %s' % (path))
	return 0

def main():
	parser = argparse.ArgumentParser(
		description=os.linesep.join([
			'SAGE BLK file tool',
			'Version: 2.1.0'
		]),
		epilog=os.linesep.join([
			'Copyright (c) 2018 JrMasterModelBuilder',
			'Licensed under the Mozilla Public License, v. 2.0',
			'',
			'LZSS code based on LZSS.C 4/6/1989 Haruhiko Okumura'
		]),
		formatter_class=argparse.RawTextHelpFormatter
	)

	group_cd = parser.add_mutually_exclusive_group()
	group_cd.add_argument(
		'-c',
		'--compressed',
		action='store_true',
		help='Force all file data to be compressed (defaults to smaller option)'
	)
	group_cd.add_argument(
		'-d',
		'--decompressed',
		action='store_true',
		help='Force all file data to be decompressed (defaults to smaller option)'
	)

	parser.add_argument(
		'-l',
		'--list',
		action='store_true',
		help='Just list archived files'
	)
	parser.add_argument(
		'-o',
		'--output',
		action='store',
		help='Override the default output path'
	)
	parser.add_argument(
		'paths',
		nargs='+',
		help='Paths to run on'
	)
	return process(parser.parse_args())

if __name__ == '__main__':
	sys.exit(main())

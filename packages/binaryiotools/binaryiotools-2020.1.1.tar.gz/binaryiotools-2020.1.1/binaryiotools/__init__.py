#!/usr/bin/env python3
"""
Base binary I/O helper.

Does boilerplate things like reading the next uint32 from a file or binary stream

Create a new IO object and initialize/ set data

Example
```python
f = open(fileName, 'rb')
data = f.read()
f.close()
io = IO(data)
width = io.u32
height = io.u32
```

The example above reads a file in binary and sets the variables width and height
as the first two unsigned integer 32s

For a file starting with the bytes:

```none
00 00 00 C8 00 01 90
```

The values for width and height would be 200, 400
"""
import struct


class IO:
	"""
	Class to handle i/o to a byte buffer or file-like object
	"""
	def __init__(self, data=None, idx=0, littleEndian=False, boolSize=8, stringEncoding='U'):
		"""
		:param data: can be a data buffer or a file-like object
		:param idx: start reading/writing the data at the given index
		:param littleEndian: whether the default is big-endian or little-endian
		:param boolSize: how many default bits to use for a bool (8,16,32,or 64)
		:param stringEncoding: default string encoding A=Ascii, U=UTF-8, W-Unicode wide
		"""
		if data is None:
			data = bytearray()
		self._data = data
		self.index = idx
		self._contexts = []
		self.littleEndian = littleEndian
		self.boolSize = boolSize
		self.stringEncoding = stringEncoding # A=Ascii, U=UTF-8, W-Unicode wide

	@property
	def data(self):
		""" return data """
		return self._data

	@data.setter
	def data(self, data):
		""" set data """
		if not hasattr(data, "__getitem__"):
			raise Exception('ERR: incorrect type for data buffer' + str(type(data)))
		self._data = data

	def beginContext(self, newIndex):
		"""
		Start a new context where the index can be changed all you want,
		and when endContext() is called, it will be restored to the current position
		"""
		self._contexts.append(newIndex)

	def endContext(self):
		"""
		Restore the index to the previous location where it was when
		beginContext() was called
		"""
		self.index = self._contexts.pop()

	def _write(self, size, fmt, data):
		"""	general formatted write	"""
		if self.index + size >= len(self.data):
			self.data.extend(bytearray((self.index + size) - len(self.data)))
		try:
			struct.pack_into(fmt, self.data, self.index, data)
			self.index += size
		except (DeprecationWarning, struct.error):
			raise Exception(type(data), fmt, size, data)

	def _read(self, size, fmt):
		"""	general formatted read """
		try:
			data = struct.unpack(fmt, self.data[self.index:self.index + size])[0]
		except (DeprecationWarning, struct.error):
			raise Exception(str(fmt) + " " + str(size) + " " +
			str(self.index) + ' ' + str(len(self.data)) + ' ' +
			str(self.data[self.index:self.index + size]))
		# Move the pointer forward
		self.index += size
		return data

	@property
	def bool(self):
		""" return bool """
		if self.boolSize == 8:
			return self.bool8
		if self.boolSize == 16:
			return self.bool16
		if self.boolSize == 32:
			return self.bool32
		if self.boolSize == 64:
			return self.bool64
		raise Exception("Unknown bool size " + str(self.boolSize))

	@bool.setter
	def bool(self, ioBool):
		""" set bool """
		if self.boolSize == 8:
			self.bool8 = ioBool
		elif self.boolSize == 16:
			self.bool16 = ioBool
		elif self.boolSize == 32:
			self.bool32 = ioBool
		elif self.boolSize == 64:
			self.bool64 = ioBool
		else:
			raise Exception("Unknown bool size " + str(self.boolSize))

	@property
	def bool8(self):
		""" get bool8 """
		return self.u8 != 0

	@bool8.setter
	def bool8(self, ioBool):
		""" set a bool8 """
		self.u8 = ioBool

	@property
	def bool16(self):
		""" get bool16 """
		return self.u16 != 0

	@bool16.setter
	def bool16(self, ioBool):
		""" set bool16 """
		self.u16 = ioBool

	@property
	def bool32(self):
		""" get bool32 """
		return self.u32 != 0

	@bool32.setter
	def bool32(self, ioBool):
		""" set bool32 """
		self.u32 = ioBool

	@property
	def bool64(self):
		""" get bool64 """
		return self.u64 != 0

	@bool64.setter
	def bool64(self, ioBool):
		""" set bool64 """
		self.u64 = ioBool

	@property
	def byte(self):
		""" get byte """
		return self.i8

	@byte.setter
	def byte(self, byte):
		""" set byte """
		self.i8 = byte

	@property
	def unsignedByte(self):
		""" get unsigned byte """
		return self.u8

	@unsignedByte.setter
	def unsignedByte(self, byte):
		""" set unsigned byte """
		self.u8 = byte

	@property
	def word(self):
		""" get a word """
		return self.i16

	@word.setter
	def word(self, word):
		""" set a word """
		self.i16 = word

	@property
	def unsignedWord(self):
		""" get an unsigned word """
		return self.u16

	@unsignedWord.setter
	def unsignedWord(self, unsignedWord):
		""" set an unsigned word """
		self.u16 = unsignedWord

	@property
	def dword(self):
		""" get a dword """
		return self.i32

	@dword.setter
	def dword(self, dword):
		""" set a dword """
		self.i32 = dword

	@property
	def unsignedDword(self):
		""" get a unsigned dword """
		return self.u32

	@unsignedDword.setter
	def unsignedDword(self, unsignedDword):
		""" set an unsigned dword """
		self.u32 = unsignedDword

	@property
	def qword(self):
		""" get a qword """
		return self.i64

	@qword.setter
	def qword(self, qword):
		""" set a qword """
		self.i64 = qword

	@property
	def unsignedQword(self):
		""" get an unsigned qword """
		return self.u64

	@unsignedQword.setter
	def unsignedQword(self, unsignedQword):
		""" set an unsigned qword """
		self.u64 = unsignedQword

	@property
	def i8(self):
		""" get an int8 """
		if self.littleEndian:
			return self.i8le
		return self.i8be

	@i8.setter
	def i8(self, i8):
		""" set an int8 """
		if self.littleEndian:
			self.i8le = i8
		else:
			self.i8be = i8

	@property
	def u8(self):
		""" get an unsigned int """
		if self.littleEndian:
			return self.u8le
		return self.u8be

	@u8.setter
	def u8(self, u8):
		""" set an unsigned int """
		if self.littleEndian:
			self.u8le = u8
		else:
			self.u8be = u8

	@property
	def i16(self):
		""" get an int16 """
		if self.littleEndian:
			return self.i16le
		return self.i16be

	@i16.setter
	def i16(self, i16):
		""" set an int16 """
		if self.littleEndian:
			self.i16le = i16
		else:
			self.i16be = i16

	@property
	def u16(self):
		""" get an uint16 """
		if self.littleEndian:
			return self.u16le
		return self.u16be

	@u16.setter
	def u16(self, u16):
		""" set an unint16 """
		if self.littleEndian:
			self.u16le = u16
		else:
			self.u16be = u16

	@property
	def i32(self):
		""" get an int32 """
		if self.littleEndian:
			return self.i32le
		return self.i32be

	@i32.setter
	def i32(self, i32):
		"""set an int32 """
		if self.littleEndian:
			self.i32le = i32
		else:
			self.i32be = i32

	@property
	def u32(self):
		""" get a uint32 """
		if self.littleEndian:
			return self.u32le
		return self.u32be

	@u32.setter
	def u32(self, u32):
		""" set a unint32 """
		if self.littleEndian:
			self.u32le = u32
		else:
			self.u32be = u32

	@property
	def i64(self):
		""" get an int64 """
		if self.littleEndian:
			return self.i64le
		return self.i64be

	@i64.setter
	def i64(self, i64):
		""" set an int64 """
		if self.littleEndian:
			self.i64le = i64
		else:
			self.i64be = i64

	@property
	def u64(self):
		""" get a uint64 """
		if self.littleEndian:
			return self.u64le
		return self.u64be

	@u64.setter
	def u64(self, u64):
		""" set a uint64 """
		if self.littleEndian:
			self.u64le = u64
		else:
			self.u64be = u64

	@property
	def float32(self):
		""" get a float32 """
		if self.littleEndian:
			return self.float32le
		return self.float32be

	@float32.setter
	def float32(self, float32):
		""" set a float32 """
		if self.littleEndian:
			self.float32le = float32
		else:
			self.float32be = float32

	@property
	def float64(self):
		""" get a float64 """
		if self.littleEndian:
			return self.float64le
		return self.float64be

	@float64.setter
	def float64(self, float64):
		""" set a float64 """
		if self.littleEndian:
			self.float64le = float64
		else:
			self.float64be = float64

	@property
	def u8be(self):
		"""	read the next uint8 and advance the index """
		return self._read(1, ">B")

	@u8be.setter
	def u8be(self, u8be):
		""" set the uint8 """
		self._write(1, '>B', u8be)

	@property
	def u8le(self):
		"""	read the next uint8 and advance the index """
		return self._read(1, "<B")

	@u8le.setter
	def u8le(self, u8le):
		""" set the uint8 """
		self._write(1, '<B', u8le)

	@property
	def i8le(self):
		"""	read the next signed int8 and advance the index """
		return self._read(1, "<b")

	@i8le.setter
	def i8le(self, i8le):
		""" set the int8 """
		self._write(1, '<b', i8le)

	@property
	def i8be(self):
		"""	read the next signed int8 and advance the index """
		return self._read(1, ">b")

	@i8be.setter
	def i8be(self, i8be):
		""" set the int8 """
		self._write(1, '>b', i8be)

	@property
	def u16be(self):
		"""	read the next uint16 and advance the index """
		return self._read(2, ">H")

	@u16be.setter
	def u16be(self, u16be):
		""" set the uint16 """
		self._write(2, '>H', u16be)

	@property
	def u16le(self):
		"""	read the next uint16 and advance the index """
		return self._read(2, "<H")

	@u16le.setter
	def u16le(self, u16le):
		""" set the uint16 """
		self._write(2, '<H', u16le)

	@property
	def i16le(self):
		"""	read the next signed int16 and advance the index """
		return self._read(2, "<h")

	@i16le.setter
	def i16le(self, i16le):
		""" set the int16 """
		self._write(2, '<h', i16le)

	@property
	def i16be(self):
		""" read the next signed int16 and advance the index """
		return self._read(2, ">h")

	@i16be.setter
	def i16be(self, i16be):
		""" set the int16 """
		self._write(2, '>h', i16be)

	@property
	def u32be(self):
		"""	read the next uint32 and advance the index """
		return self._read(4, ">I")

	@u32be.setter
	def u32be(self, u32be):
		""" set the uint32 """
		self._write(4, '>I', int(u32be))

	@property
	def u32le(self):
		"""	read the next uint32 and advance the index """
		return self._read(4, "<I")

	@u32le.setter
	def u32le(self, u32le):
		""" set the uint32 """
		self._write(4, '<I', u32le)

	@property
	def i32le(self):
		"""	read the next signed int32 and advance the index """
		return self._read(4, "<i")

	@i32le.setter
	def i32le(self, i32le):
		""" set the int32 """
		self._write(4, '<i', i32le)

	@property
	def i32be(self):
		"""	read the next signed int32 and advance the index """
		return self._read(4, ">i")

	@i32be.setter
	def i32be(self, i32be):
		""" set the int32 """
		self._write(4, '>i', int(i32be))

	@property
	def u64be(self):
		"""	read the next uint64 and advance the index """
		return self._read(8, ">Q")

	@u64be.setter
	def u64be(self, u64be):
		""" set the uint64 """
		self._write(8, '>Q', u64be)

	@property
	def u64le(self):
		"""	read the next uint64 and advance the index """
		return self._read(8, "<Q")

	@u64le.setter
	def u64le(self, u64le):
		""" set the uint64 """
		self._write(8, '<Q', u64le)

	@property
	def i64le(self):
		""" read the next signed int64 and advance the index """
		return self._read(8, "<q")

	@i64le.setter
	def i64le(self, i64le):
		""" set the int64 """
		self._write(8, '<q', i64le)

	@property
	def i64be(self):
		"""	read the next signed int64 and advance the index """
		return self._read(8, ">q")

	@i64be.setter
	def i64be(self, i64be):
		""" set the int64 """
		self._write(8, '>q', i64be)

	@property
	def float(self):
		""" get a float """
		return self.float32

	@float.setter
	def float(self, f):
		""" set a float """
		self.float32 = f

	@property
	def double(self):
		""" get a double """
		return self.float64

	@double.setter
	def double(self, f):
		""" set a double """
		self.float64 = f

	@property
	def float32be(self):
		"""	read the next 32 bit float and advance the index """
		return self._read(4, ">f")

	@float32be.setter
	def float32be(self, float32be):
		""" set a 32 bit float """
		self._write(4, '>f', float32be)

	@property
	def float32le(self):
		"""	read the next 32 bit float and advance the index """
		return self._read(4, "<f")

	@float32le.setter
	def float32le(self, float32le):
		""" set a 32 bit float """
		self._write(4, '<f', float32le)

	@property
	def float64be(self):
		"""	read the next 64 bit float and advance the index """
		return self._read(8, ">d")

	@float64be.setter
	def float64be(self, float64be):
		""" set a 64 bit float """
		self._write(8, '>d', float64be)

	@property
	def float64le(self):
		"""	read the next 64 bit float and advance the index """
		return self._read(8, "<d")

	@float64le.setter
	def float64le(self, float64le):
		""" set a 64 bit float """
		self._write(8, '<d', float64le)

	def getBytes(self, nbytes):
		"""
		grab some raw bytes and advance the index
		"""
		d = self.data[self.index:self.index + nbytes]
		self.index += nbytes
		return d

	def addBytes(self, ioBytes):
		"""
		add some raw bytes and advance the index

		alias for setBytes()

		:param bytes: can be a string, bytearray, or another IO object
		"""
		self.setBytes(ioBytes)

	def setBytes(self, ioBytes):
		"""
		add some raw bytes and advance the index

		alias for addBytes()

		:param ioBytes: can be a string, bytearray, or another IO object
		"""
		if isinstance(ioBytes, IO):
			ioBytes = ioBytes.data
		if isinstance(ioBytes, str):
			ioBytes = bytearray(ioBytes, encoding="utf-8")
		if self.index >= len(self.data):
			# if we're at the end, simply extend the buffer
			self.data.extend(ioBytes)
			self.index += len(ioBytes)
		else:
			if self.index + len(ioBytes) >= len(self.data):
				self.data.extend(bytearray((self.index + len(ioBytes)) - len(self.data)))
			for b in ioBytes:
				self.data[self.index] = b
				self.index += 1

	def _sz754(self, encoding):
		"""
		Read the next string conforming to IEEE 754 and advance the index

		Note, string format is:
			uint32   n+1  Number of bytes that follow, including the zero byte
			byte[n]  ...  String data in Unicode, encoded using UTF-8
			byte     0    Zero marks the end of the string.
		or simply uint32=0 for empty string
		"""
		nchars = self.u32
		if nchars == 0:
			return ''
		d = self.data[self.index:self.index + nchars - 1]
		self.index += nchars
		if encoding == 'A':
			return d
		if encoding == 'U':
			return d.decode('UTF-8', errors='replace')
		if encoding == 'W':
			return d.decode('UTF-16', errors='replace')
		raise Exception()

	def _sz754set(self, sz754, _encoding):
		'''_sz754set'''
		self.u32 = len(sz754)
		self.setBytes(sz754)
		self.u8 = 0

	@property
	def sz754(self):
		'''sz754'''
		return self._sz754(self.stringEncoding)

	@sz754.setter
	def sz754(self, sz754):
		'''set sz754'''
		return self._sz754set(sz754, self.stringEncoding)

	@property
	def sz754A(self):
		'''sz754A'''
		return self._sz754('A')

	@sz754A.setter
	def sz754A(self, sz754):
		'''set sz754A'''
		return self._sz754set(sz754, 'A')

	@property
	def sz754W(self):
		'''sz754W'''
		return self._sz754('W')

	@sz754W.setter
	def sz754W(self, sz754):
		'''set sz754W'''
		return self._sz754set(sz754, 'W')

	@property
	def sz754U(self):
		'''sz754U'''
		return self._sz754('U')

	@sz754U.setter
	def sz754U(self, sz754):
		'''set sz754U'''
		return self._sz754set(sz754, 'U')

	def _readUntil(self, until, encoding='A'):
		"""
		Read a sequence of chars in a set encoding until a set char

		:param until: must be within the ascii character set
		:param encoding: one of A (ascii), U (UTF-8) or W (UCS-2)
		"""
		d = []
		if encoding == 'A':
			encoding = 'ascii'
		elif encoding == 'U':
			encoding = 'UTF-8'
		elif encoding == 'W':
			encoding = 'UCS-2'
		else:
			raise Exception('bogus encoding')
		until = until.encode('ascii')[0] # always ascii
		while True:
			c = self.data[self.index]
			self.index += 1
			if encoding == 'W': # get one more byte
				d.append(c)
				c = self.data[self.index]
				self.index += 1
			if c == until:
				break
			d.append(c)
		return bytes(d).decode(encoding, errors='replace')

	@property
	def textLine(self):
		'''Read a sequence of chars until the next new line char'''
		ret = self._readUntil('\n', self.stringEncoding)
		if ret[-1] == '\r':
			ret = ret[-1]
		return ret

	@textLine.setter
	def textLine(self, text):
		'''Set a sequence of chars until the next new line char'''
		self.setBytes(text)
		if text[-1] != '\n':
			self.setBytes('\n')

	@property
	def textLineA(self):
		'''Read a sequence of chars until the next new line char in ascii'''
		ret = self._readUntil('\n', 'A')
		if ret[-1] == '\r':
			ret = ret[-1]
		return ret

	@textLineA.setter
	def textLineA(self, text):
		'''Set a sequence of chars until the next new line char in ascii'''
		self.setBytes(text)
		if text[-1] != '\n':
			self.setBytes('\n')

	@property
	def textLineW(self):
		'''Read a sequence of chars until the next new line char in ucs-2'''
		ret = self._readUntil('\n', 'W')
		if ret[-1] == '\r':
			ret = ret[-1]
		return ret

	@textLineW.setter
	def textLineW(self, text):
		'''Set a sequence of chars until the next new line char in ucs-2'''
		self.setBytes(text)
		if text[-1] != '\n':
			self.setBytes('\0\n')

	@property
	def textLineU(self):
		'''Read a sequence of chars until the next new line char in utf-8'''
		ret = self._readUntil('\n', 'U')
		if ret[-1] == '\r':
			ret = ret[-1]
		return ret

	@textLineU.setter
	def textLineU(self, text):
		'''Set a sequence of chars until the next new line char in utf-8'''
		self.setBytes(text)
		if text[-1] != '\n':
			self.setBytes('\n')

	@property
	def cString(self):
		'''Read a sequence of chars until the next null byte'''
		return self._readUntil('\0', self.stringEncoding)

	@cString.setter
	def cString(self, text):
		"""Set a sequence of chars and add a null byte """
		self.setBytes(text)
		self.setBytes('\0')

	@property
	def cStringA(self):
		'''Read a sequence of chars until the next null byte in ascii'''
		return self._readUntil('\0', 'A')

	@cStringA.setter
	def cStringA(self, text):
		"""Set a sequence of chars and add a null byte in ascii"""
		self.setBytes(text)
		self.setBytes('\0')

	@property
	def cStringW(self):
		'''Read a sequence of chars until the next null byte in ucs-2'''
		return self._readUntil('\0', 'W')

	@cStringW.setter
	def cStringW(self, text):
		"""Set a sequence of chars and add a null byte in ucs-2"""
		self.setBytes(text)
		self.setBytes('\0\0')

	@property
	def cStringU(self):
		'''Read a sequence of chars until the next null byte in utf-8'''
		return self._readUntil('\0', 'U')

	@cStringU.setter
	def cStringU(self, text):
		"""Set a sequence of chars and add a null byte in utf-8"""
		self.setBytes(text)
		self.setBytes('\0')

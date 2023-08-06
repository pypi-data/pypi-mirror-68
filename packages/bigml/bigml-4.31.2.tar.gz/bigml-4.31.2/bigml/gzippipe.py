"""
Extracted from ActiveState Recipes

"""
from gzip import GzipFile

try:
    from io import StringIO
except ImportError:
    from StringIO import StringIO


class GZipPipe(file) :
    """This class implements a compression pipe suitable for asynchronous
    process.

    Only one buffer of data is read/compressed at a time.
    The process doesn't read the whole file at once : This improves performance
    and prevents hight memory consumption for big files."""

    # Size of the internal buffer
    CHUNCK_SIZE = 1024

    def __init__(self, path = None, name = "data") :
        """Constructor

        @param path   Path to the file name
        @param name     Name of the data within the zip file"""

        # Source file
        self = open(path, "rb")

        # OEF reached for source ?
        self.source_eof = False

        # Buffer
        self.buffer = StringIO


        # Init ZipFile that writes to us (the StringIO buffer)
        self.zipfile = GzipFile(name, 'wb', 9, self.buffer)

    def write(self, data) :
        """The write method shouldn't be called from outside.
        A GZipFile was created with this current object as a output buffer and it
        fills it whenever we write to it (calling the read method of this object will do it for you)
        """

        self.buffer.write(data)

    def read(self, size = -1) :
        """Calling read() on a zip pipe will suck data from the source stream.

        @param  size Maximum size to read - Read whole compressed file if not specified.
        @return Compressed data"""

        # Feed the zipped buffer by writing source data to the zip stream
        while ((len(self.buffer) < size) or (size == -1)) and not self.source_eof :

            # No source given in input
            if self.source == None: break

            # Get a chunk of source data
            chunk = self.source.read(GZipPipe.CHUNCK_SIZE)

            # Feed the source zip file (that fills the compressed buffer)
            self.zipfile.write(chunk)

            # End of source file ?
            if (len(chunk) < GZipPipe.CHUNCK_SIZE) :
                self.source_eof = True
                self.zipfile.flush()
                self.zipfile.close()
                break


        # We have enough data in the buffer (or source file is EOF): Give it to the output
        if size == 0:
            result = ""
        if size >= 1 :
            result = self.buffer.getvalue()[0:size]
            self.buffer = self.buffer[size:]
        else : # size < 0 : All requested
            result = self.buffer.getvalue()
            self.buffer = StringIO

        return result

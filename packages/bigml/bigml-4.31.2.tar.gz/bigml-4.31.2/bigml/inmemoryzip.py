import zipfile
try:
    from cStringIO import StringIO
except ImportError:
    from io import BytesIO as StringIO


class InMemoryZip(object):
    def __init__(self, zip_name, compression=zipfile.ZIP_DEFLATED):
        # Create the in-memory file-like object
        self.zip_name = zip_name
        self._zip_data_stream = StringIO()
        self._zip_handler = zipfile.ZipFile(self._zip_data_stream, "a",
                                            compression, False)

    def append(self, file_names, file_contents):
        '''Appends a list of files with name filename_in_zip and contents of
        file_contents to the in-memory zip.'''
        # Get a handle to the in-memory zip in append mode

        print file_names, file_contents
        if isinstance(file_names, basestring):
            self._zip_handler.writestr(file_names, file_contents)
        else:
            for index, file_name in enumerate(file_names):
                print index, file_name
                # Write the file to the in-memory zip
                self._zip_handler.writestr(file_name, file_contents[index])

        # Mark the files as having been created on Windows so that
        # Unix permissions are not inferred as 0000
        for zfile in self._zip_handler.filelist:
            zfile.create_system = 0

        return self

    def read(self):
        '''Returns a string with the contents of the in-memory zip.'''
        self._zip_data_stream.seek(0)
        return self._zip_data_stream.read()

    def write(self):
        '''Writes the in-memory zip to a file.'''
        f = file(self.zip_name, "wb")
        f.write(self._zip_data_stream.getvalue())
        f.close()

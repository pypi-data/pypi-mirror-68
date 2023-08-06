import io
import pathlib

import zstandard as zstd


class ZstandardFile(io.RawIOBase):
    """File like object interface of Zstanrard archive"""

    def __init__(
        self, filename_or_obj, mode="r", compresslevel=3, compressor_args=None, decompressor_args=None,
    ):
        super().__init__()
        self.ctx = None
        self.stream = None
        self.fileobj = None
        if mode == "w":
            if isinstance(filename_or_obj, (str, pathlib.Path)):
                self.fileobj = open(filename_or_obj, "wb")
            else:
                self.fileobj = filename_or_obj
            if not compressor_args:
                compressor_args = {}
            self.ctx = zstd.ZstdCompressor(level=compresslevel, **compressor_args)
            self.stream = self.ctx.stream_writer(self.fileobj)
        else:
            if isinstance(filename_or_obj, (str, pathlib.Path)):
                self.fileobj = open(filename_or_obj, "rb")
            else:
                self.fileobj = filename_or_obj
            if not decompressor_args:
                decompressor_args = {}
            self.ctx = zstd.ZstdDecompressor(**decompressor_args)
            self.stream = self.ctx.stream_reader(self.fileobj)

    def close(self):
        self.stream.close()
        self.fileobj.close()

    @property
    def closed(self):
        return self.fileobj.closed

    def flush(self):
        return self.stream.flush()

    def writable(self):
        return self.fileobj.writable()

    def readable(self):
        return self.fileobj.readable()

    def seekable(self):
        return self.stream.seekable()

    def tell(self, *args, **kwargs):
        return self.stream.tell(*args, **kwargs)

    def seek(self, *args, **kwargs):
        return self.stream.seek(*args, **kwargs)

    def truncate(self, size=None):
        return self.stream.truncate(size)

    def read(self, *args, **kwargs):
        return self.stream.read(*args, **kwargs)

    def readinto(self, *args, **kwargs):
        return self.stream.readinto(*args, **kwargs)

    def write(self, data):
        self.stream.write(data)
        return len(data)

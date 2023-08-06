import joblib
from joblib.compressor import CompressorWrapper

from .file import ZstandardFile

DEFAULT_COMPRESS_LEVELS = (1, 2, 3, 6, 9, 12, 15, 18, 20, 22)


class ZStandardCompressorWrapper(CompressorWrapper):
    """joblib CompressorWrapper for Zstandard format"""

    def __init__(self, compress_levels, compressor_args, decompressor_args):
        super().__init__(ZstandardFile, b"\x28\xb5\x2f\xfd", ".zst")
        self._comprss_levels = compress_levels or DEFAULT_COMPRESS_LEVELS
        self._compressor_args = compressor_args
        self._decompressor_args = decompressor_args

    def compressor_file(self, fileobj, compresslevel=None):
        """Returns an instance of a compressor file object."""
        return self._factory(fileobj, "w", compresslevel)

    def decompressor_file(self, fileobj):
        """Returns an instance of a decompressor file object."""
        return self._factory(fileobj, "r")

    def _factory(self, fileobj, mode, compresslevel=None):
        if compresslevel is None:
            compresslevel = 2
        level = self._comprss_levels[compresslevel]
        return self.fileobj_factory(
            fileobj,
            mode=mode,
            compresslevel=level,
            compressor_args=self._compressor_args,
            decompressor_args=self._decompressor_args,
        )


def register(compress_levels=None, compressor_args=None, decompressor_args=None, force=True):
    if compress_levels and (not isinstance(compress_levels, (list, tuple)) or len(compress_levels) != 10):
        raise ValueError("compress_levels L must be list or tuple, len(L) == 10, 1 <= L[i] <= 22.")
    joblib.register_compressor(
        "zstd", ZStandardCompressorWrapper(compress_levels, compressor_args, decompressor_args), force=force,
    )

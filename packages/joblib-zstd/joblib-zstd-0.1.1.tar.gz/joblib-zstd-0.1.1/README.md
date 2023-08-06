joblib-zstd is a plugin, which enables Zstandard (.zst) compression and decompression through joblib.dump and joblib.load.

# Prerequisites

You need [joblib](https://joblib.readthedocs.io/en/latest/).

# Install

```
pip install joblib-zstd
```

If you failed to install, update version of pip and setuptools:

```
pip install -U pip setuptools
```

# Usage

```python
import joblib
import joblib_zstd
joblib_zstd.register()

joblib.dump({'a': 1, 'b': 2}, 'obj.zst', compress=5)  # implicit compression
joblib.dump({'a': 1, 'b': 2}, 'obj.bin', compress=('zstd', 5))  # explicit compression

joblib.load('obj.zst')  # implicit decompression
```

# LISENCE

MIT

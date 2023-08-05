import sys

if sys.version_info < (3, 7):
    from ._rotation import Rotation
else:
    from _plotly_utils.importers import relative_import

    __all__, __getattr__, __dir__ = relative_import(
        __name__, [], ["._rotation.Rotation"]
    )

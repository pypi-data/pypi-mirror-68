import sys

if sys.version_info < (3, 7):
    from ._symbol import SymbolValidator
    from ._size import SizeValidator
    from ._outliercolor import OutliercolorValidator
    from ._opacity import OpacityValidator
    from ._line import LineValidator
    from ._color import ColorValidator
else:
    from _plotly_utils.importers import relative_import

    __all__, __getattr__, __dir__ = relative_import(
        __name__,
        [],
        [
            "._symbol.SymbolValidator",
            "._size.SizeValidator",
            "._outliercolor.OutliercolorValidator",
            "._opacity.OpacityValidator",
            "._line.LineValidator",
            "._color.ColorValidator",
        ],
    )

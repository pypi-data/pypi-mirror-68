import sys

if sys.version_info < (3, 7):
    from ._opacitysrc import OpacitysrcValidator
    from ._opacity import OpacityValidator
    from ._line import LineValidator
else:
    from _plotly_utils.importers import relative_import

    __all__, __getattr__, __dir__ = relative_import(
        __name__,
        [],
        [
            "._opacitysrc.OpacitysrcValidator",
            "._opacity.OpacityValidator",
            "._line.LineValidator",
        ],
    )

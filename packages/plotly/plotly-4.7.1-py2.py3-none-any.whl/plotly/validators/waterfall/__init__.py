import sys

if sys.version_info < (3, 7):
    from ._ysrc import YsrcValidator
    from ._yaxis import YaxisValidator
    from ._y0 import Y0Validator
    from ._y import YValidator
    from ._xsrc import XsrcValidator
    from ._xaxis import XaxisValidator
    from ._x0 import X0Validator
    from ._x import XValidator
    from ._widthsrc import WidthsrcValidator
    from ._width import WidthValidator
    from ._visible import VisibleValidator
    from ._uirevision import UirevisionValidator
    from ._uid import UidValidator
    from ._totals import TotalsValidator
    from ._texttemplatesrc import TexttemplatesrcValidator
    from ._texttemplate import TexttemplateValidator
    from ._textsrc import TextsrcValidator
    from ._textpositionsrc import TextpositionsrcValidator
    from ._textposition import TextpositionValidator
    from ._textinfo import TextinfoValidator
    from ._textfont import TextfontValidator
    from ._textangle import TextangleValidator
    from ._text import TextValidator
    from ._stream import StreamValidator
    from ._showlegend import ShowlegendValidator
    from ._selectedpoints import SelectedpointsValidator
    from ._outsidetextfont import OutsidetextfontValidator
    from ._orientation import OrientationValidator
    from ._opacity import OpacityValidator
    from ._offsetsrc import OffsetsrcValidator
    from ._offsetgroup import OffsetgroupValidator
    from ._offset import OffsetValidator
    from ._name import NameValidator
    from ._metasrc import MetasrcValidator
    from ._meta import MetaValidator
    from ._measuresrc import MeasuresrcValidator
    from ._measure import MeasureValidator
    from ._legendgroup import LegendgroupValidator
    from ._insidetextfont import InsidetextfontValidator
    from ._insidetextanchor import InsidetextanchorValidator
    from ._increasing import IncreasingValidator
    from ._idssrc import IdssrcValidator
    from ._ids import IdsValidator
    from ._hovertextsrc import HovertextsrcValidator
    from ._hovertext import HovertextValidator
    from ._hovertemplatesrc import HovertemplatesrcValidator
    from ._hovertemplate import HovertemplateValidator
    from ._hoverlabel import HoverlabelValidator
    from ._hoverinfosrc import HoverinfosrcValidator
    from ._hoverinfo import HoverinfoValidator
    from ._dy import DyValidator
    from ._dx import DxValidator
    from ._decreasing import DecreasingValidator
    from ._customdatasrc import CustomdatasrcValidator
    from ._customdata import CustomdataValidator
    from ._constraintext import ConstraintextValidator
    from ._connector import ConnectorValidator
    from ._cliponaxis import CliponaxisValidator
    from ._base import BaseValidator
    from ._alignmentgroup import AlignmentgroupValidator
else:
    from _plotly_utils.importers import relative_import

    __all__, __getattr__, __dir__ = relative_import(
        __name__,
        [],
        [
            "._ysrc.YsrcValidator",
            "._yaxis.YaxisValidator",
            "._y0.Y0Validator",
            "._y.YValidator",
            "._xsrc.XsrcValidator",
            "._xaxis.XaxisValidator",
            "._x0.X0Validator",
            "._x.XValidator",
            "._widthsrc.WidthsrcValidator",
            "._width.WidthValidator",
            "._visible.VisibleValidator",
            "._uirevision.UirevisionValidator",
            "._uid.UidValidator",
            "._totals.TotalsValidator",
            "._texttemplatesrc.TexttemplatesrcValidator",
            "._texttemplate.TexttemplateValidator",
            "._textsrc.TextsrcValidator",
            "._textpositionsrc.TextpositionsrcValidator",
            "._textposition.TextpositionValidator",
            "._textinfo.TextinfoValidator",
            "._textfont.TextfontValidator",
            "._textangle.TextangleValidator",
            "._text.TextValidator",
            "._stream.StreamValidator",
            "._showlegend.ShowlegendValidator",
            "._selectedpoints.SelectedpointsValidator",
            "._outsidetextfont.OutsidetextfontValidator",
            "._orientation.OrientationValidator",
            "._opacity.OpacityValidator",
            "._offsetsrc.OffsetsrcValidator",
            "._offsetgroup.OffsetgroupValidator",
            "._offset.OffsetValidator",
            "._name.NameValidator",
            "._metasrc.MetasrcValidator",
            "._meta.MetaValidator",
            "._measuresrc.MeasuresrcValidator",
            "._measure.MeasureValidator",
            "._legendgroup.LegendgroupValidator",
            "._insidetextfont.InsidetextfontValidator",
            "._insidetextanchor.InsidetextanchorValidator",
            "._increasing.IncreasingValidator",
            "._idssrc.IdssrcValidator",
            "._ids.IdsValidator",
            "._hovertextsrc.HovertextsrcValidator",
            "._hovertext.HovertextValidator",
            "._hovertemplatesrc.HovertemplatesrcValidator",
            "._hovertemplate.HovertemplateValidator",
            "._hoverlabel.HoverlabelValidator",
            "._hoverinfosrc.HoverinfosrcValidator",
            "._hoverinfo.HoverinfoValidator",
            "._dy.DyValidator",
            "._dx.DxValidator",
            "._decreasing.DecreasingValidator",
            "._customdatasrc.CustomdatasrcValidator",
            "._customdata.CustomdataValidator",
            "._constraintext.ConstraintextValidator",
            "._connector.ConnectorValidator",
            "._cliponaxis.CliponaxisValidator",
            "._base.BaseValidator",
            "._alignmentgroup.AlignmentgroupValidator",
        ],
    )

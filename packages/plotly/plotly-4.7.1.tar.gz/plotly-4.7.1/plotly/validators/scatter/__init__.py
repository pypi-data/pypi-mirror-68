import sys

if sys.version_info < (3, 7):
    from ._ysrc import YsrcValidator
    from ._ycalendar import YcalendarValidator
    from ._yaxis import YaxisValidator
    from ._y0 import Y0Validator
    from ._y import YValidator
    from ._xsrc import XsrcValidator
    from ._xcalendar import XcalendarValidator
    from ._xaxis import XaxisValidator
    from ._x0 import X0Validator
    from ._x import XValidator
    from ._visible import VisibleValidator
    from ._unselected import UnselectedValidator
    from ._uirevision import UirevisionValidator
    from ._uid import UidValidator
    from ._tsrc import TsrcValidator
    from ._texttemplatesrc import TexttemplatesrcValidator
    from ._texttemplate import TexttemplateValidator
    from ._textsrc import TextsrcValidator
    from ._textpositionsrc import TextpositionsrcValidator
    from ._textposition import TextpositionValidator
    from ._textfont import TextfontValidator
    from ._text import TextValidator
    from ._t import TValidator
    from ._stream import StreamValidator
    from ._stackgroup import StackgroupValidator
    from ._stackgaps import StackgapsValidator
    from ._showlegend import ShowlegendValidator
    from ._selectedpoints import SelectedpointsValidator
    from ._selected import SelectedValidator
    from ._rsrc import RsrcValidator
    from ._r import RValidator
    from ._orientation import OrientationValidator
    from ._opacity import OpacityValidator
    from ._name import NameValidator
    from ._mode import ModeValidator
    from ._metasrc import MetasrcValidator
    from ._meta import MetaValidator
    from ._marker import MarkerValidator
    from ._line import LineValidator
    from ._legendgroup import LegendgroupValidator
    from ._idssrc import IdssrcValidator
    from ._ids import IdsValidator
    from ._hovertextsrc import HovertextsrcValidator
    from ._hovertext import HovertextValidator
    from ._hovertemplatesrc import HovertemplatesrcValidator
    from ._hovertemplate import HovertemplateValidator
    from ._hoveron import HoveronValidator
    from ._hoverlabel import HoverlabelValidator
    from ._hoverinfosrc import HoverinfosrcValidator
    from ._hoverinfo import HoverinfoValidator
    from ._groupnorm import GroupnormValidator
    from ._fillcolor import FillcolorValidator
    from ._fill import FillValidator
    from ._error_y import Error_YValidator
    from ._error_x import Error_XValidator
    from ._dy import DyValidator
    from ._dx import DxValidator
    from ._customdatasrc import CustomdatasrcValidator
    from ._customdata import CustomdataValidator
    from ._connectgaps import ConnectgapsValidator
    from ._cliponaxis import CliponaxisValidator
else:
    from _plotly_utils.importers import relative_import

    __all__, __getattr__, __dir__ = relative_import(
        __name__,
        [],
        [
            "._ysrc.YsrcValidator",
            "._ycalendar.YcalendarValidator",
            "._yaxis.YaxisValidator",
            "._y0.Y0Validator",
            "._y.YValidator",
            "._xsrc.XsrcValidator",
            "._xcalendar.XcalendarValidator",
            "._xaxis.XaxisValidator",
            "._x0.X0Validator",
            "._x.XValidator",
            "._visible.VisibleValidator",
            "._unselected.UnselectedValidator",
            "._uirevision.UirevisionValidator",
            "._uid.UidValidator",
            "._tsrc.TsrcValidator",
            "._texttemplatesrc.TexttemplatesrcValidator",
            "._texttemplate.TexttemplateValidator",
            "._textsrc.TextsrcValidator",
            "._textpositionsrc.TextpositionsrcValidator",
            "._textposition.TextpositionValidator",
            "._textfont.TextfontValidator",
            "._text.TextValidator",
            "._t.TValidator",
            "._stream.StreamValidator",
            "._stackgroup.StackgroupValidator",
            "._stackgaps.StackgapsValidator",
            "._showlegend.ShowlegendValidator",
            "._selectedpoints.SelectedpointsValidator",
            "._selected.SelectedValidator",
            "._rsrc.RsrcValidator",
            "._r.RValidator",
            "._orientation.OrientationValidator",
            "._opacity.OpacityValidator",
            "._name.NameValidator",
            "._mode.ModeValidator",
            "._metasrc.MetasrcValidator",
            "._meta.MetaValidator",
            "._marker.MarkerValidator",
            "._line.LineValidator",
            "._legendgroup.LegendgroupValidator",
            "._idssrc.IdssrcValidator",
            "._ids.IdsValidator",
            "._hovertextsrc.HovertextsrcValidator",
            "._hovertext.HovertextValidator",
            "._hovertemplatesrc.HovertemplatesrcValidator",
            "._hovertemplate.HovertemplateValidator",
            "._hoveron.HoveronValidator",
            "._hoverlabel.HoverlabelValidator",
            "._hoverinfosrc.HoverinfosrcValidator",
            "._hoverinfo.HoverinfoValidator",
            "._groupnorm.GroupnormValidator",
            "._fillcolor.FillcolorValidator",
            "._fill.FillValidator",
            "._error_y.Error_YValidator",
            "._error_x.Error_XValidator",
            "._dy.DyValidator",
            "._dx.DxValidator",
            "._customdatasrc.CustomdatasrcValidator",
            "._customdata.CustomdataValidator",
            "._connectgaps.ConnectgapsValidator",
            "._cliponaxis.CliponaxisValidator",
        ],
    )

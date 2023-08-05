import _plotly_utils.basevalidators


class ColorscaleValidator(_plotly_utils.basevalidators.ColorscaleValidator):
    def __init__(self, plotly_name="colorscale", parent_name="mesh3d", **kwargs):
        super(ColorscaleValidator, self).__init__(
            plotly_name=plotly_name,
            parent_name=parent_name,
            edit_type=kwargs.pop("edit_type", "calc"),
            implied_edits=kwargs.pop("implied_edits", {"autocolorscale": False}),
            role=kwargs.pop("role", "style"),
            **kwargs
        )

import _plotly_utils.basevalidators


class AlignValidator(_plotly_utils.basevalidators.EnumeratedValidator):
    def __init__(self, plotly_name="align", parent_name="volume.hoverlabel", **kwargs):
        super(AlignValidator, self).__init__(
            plotly_name=plotly_name,
            parent_name=parent_name,
            array_ok=kwargs.pop("array_ok", True),
            edit_type=kwargs.pop("edit_type", "none"),
            role=kwargs.pop("role", "style"),
            values=kwargs.pop("values", ["left", "right", "auto"]),
            **kwargs
        )

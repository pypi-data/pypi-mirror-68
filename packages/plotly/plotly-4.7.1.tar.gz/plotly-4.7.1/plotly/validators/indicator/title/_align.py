import _plotly_utils.basevalidators


class AlignValidator(_plotly_utils.basevalidators.EnumeratedValidator):
    def __init__(self, plotly_name="align", parent_name="indicator.title", **kwargs):
        super(AlignValidator, self).__init__(
            plotly_name=plotly_name,
            parent_name=parent_name,
            edit_type=kwargs.pop("edit_type", "plot"),
            role=kwargs.pop("role", "info"),
            values=kwargs.pop("values", ["left", "center", "right"]),
            **kwargs
        )

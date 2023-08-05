import _plotly_utils.basevalidators


class SideValidator(_plotly_utils.basevalidators.EnumeratedValidator):
    def __init__(self, plotly_name="side", parent_name="layout.yaxis", **kwargs):
        super(SideValidator, self).__init__(
            plotly_name=plotly_name,
            parent_name=parent_name,
            edit_type=kwargs.pop("edit_type", "plot"),
            role=kwargs.pop("role", "info"),
            values=kwargs.pop("values", ["top", "bottom", "left", "right"]),
            **kwargs
        )

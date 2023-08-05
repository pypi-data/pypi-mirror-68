import _plotly_utils.basevalidators


class UsrcValidator(_plotly_utils.basevalidators.SrcValidator):
    def __init__(self, plotly_name="usrc", parent_name="cone", **kwargs):
        super(UsrcValidator, self).__init__(
            plotly_name=plotly_name,
            parent_name=parent_name,
            edit_type=kwargs.pop("edit_type", "none"),
            role=kwargs.pop("role", "info"),
            **kwargs
        )

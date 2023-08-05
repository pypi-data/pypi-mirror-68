import _plotly_utils.basevalidators


class DbValidator(_plotly_utils.basevalidators.NumberValidator):
    def __init__(self, plotly_name="db", parent_name="carpet", **kwargs):
        super(DbValidator, self).__init__(
            plotly_name=plotly_name,
            parent_name=parent_name,
            edit_type=kwargs.pop("edit_type", "calc"),
            role=kwargs.pop("role", "info"),
            **kwargs
        )

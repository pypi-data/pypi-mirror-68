import _plotly_utils.basevalidators


class ValuesValidator(_plotly_utils.basevalidators.DataArrayValidator):
    def __init__(self, plotly_name="values", parent_name="splom.dimension", **kwargs):
        super(ValuesValidator, self).__init__(
            plotly_name=plotly_name,
            parent_name=parent_name,
            edit_type=kwargs.pop("edit_type", "calc+clearAxisTypes"),
            role=kwargs.pop("role", "data"),
            **kwargs
        )

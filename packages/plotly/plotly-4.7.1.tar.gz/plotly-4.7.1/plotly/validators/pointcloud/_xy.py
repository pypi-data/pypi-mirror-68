import _plotly_utils.basevalidators


class XyValidator(_plotly_utils.basevalidators.DataArrayValidator):
    def __init__(self, plotly_name="xy", parent_name="pointcloud", **kwargs):
        super(XyValidator, self).__init__(
            plotly_name=plotly_name,
            parent_name=parent_name,
            edit_type=kwargs.pop("edit_type", "calc"),
            role=kwargs.pop("role", "data"),
            **kwargs
        )

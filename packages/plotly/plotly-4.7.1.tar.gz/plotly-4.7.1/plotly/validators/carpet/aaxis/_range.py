import _plotly_utils.basevalidators


class RangeValidator(_plotly_utils.basevalidators.InfoArrayValidator):
    def __init__(self, plotly_name="range", parent_name="carpet.aaxis", **kwargs):
        super(RangeValidator, self).__init__(
            plotly_name=plotly_name,
            parent_name=parent_name,
            edit_type=kwargs.pop("edit_type", "calc"),
            items=kwargs.pop(
                "items",
                [
                    {"valType": "any", "editType": "calc"},
                    {"valType": "any", "editType": "calc"},
                ],
            ),
            role=kwargs.pop("role", "info"),
            **kwargs
        )

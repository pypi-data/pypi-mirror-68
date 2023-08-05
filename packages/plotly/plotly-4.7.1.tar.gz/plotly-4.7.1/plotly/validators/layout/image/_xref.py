import _plotly_utils.basevalidators


class XrefValidator(_plotly_utils.basevalidators.EnumeratedValidator):
    def __init__(self, plotly_name="xref", parent_name="layout.image", **kwargs):
        super(XrefValidator, self).__init__(
            plotly_name=plotly_name,
            parent_name=parent_name,
            edit_type=kwargs.pop("edit_type", "arraydraw"),
            role=kwargs.pop("role", "info"),
            values=kwargs.pop("values", ["paper", "/^x([2-9]|[1-9][0-9]+)?$/"]),
            **kwargs
        )

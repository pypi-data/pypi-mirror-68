import _plotly_utils.basevalidators


class LineValidator(_plotly_utils.basevalidators.CompoundValidator):
    def __init__(self, plotly_name="line", parent_name="parcats", **kwargs):
        super(LineValidator, self).__init__(
            plotly_name=plotly_name,
            parent_name=parent_name,
            data_class_str=kwargs.pop("data_class_str", "Line"),
            data_docs=kwargs.pop(
                "data_docs",
                """
            autocolorscale
                Determines whether the colorscale is a default
                palette (`autocolorscale: true`) or the palette
                determined by `line.colorscale`. Has an effect
                only if in `line.color`is set to a numerical
                array. In case `colorscale` is unspecified or
                `autocolorscale` is true, the default  palette
                will be chosen according to whether numbers in
                the `color` array are all positive, all
                negative or mixed.
            cauto
                Determines whether or not the color domain is
                computed with respect to the input data (here
                in `line.color`) or the bounds set in
                `line.cmin` and `line.cmax`  Has an effect only
                if in `line.color`is set to a numerical array.
                Defaults to `false` when `line.cmin` and
                `line.cmax` are set by the user.
            cmax
                Sets the upper bound of the color domain. Has
                an effect only if in `line.color`is set to a
                numerical array. Value should have the same
                units as in `line.color` and if set,
                `line.cmin` must be set as well.
            cmid
                Sets the mid-point of the color domain by
                scaling `line.cmin` and/or `line.cmax` to be
                equidistant to this point. Has an effect only
                if in `line.color`is set to a numerical array.
                Value should have the same units as in
                `line.color`. Has no effect when `line.cauto`
                is `false`.
            cmin
                Sets the lower bound of the color domain. Has
                an effect only if in `line.color`is set to a
                numerical array. Value should have the same
                units as in `line.color` and if set,
                `line.cmax` must be set as well.
            color
                Sets thelinecolor. It accepts either a specific
                color or an array of numbers that are mapped to
                the colorscale relative to the max and min
                values of the array or relative to `line.cmin`
                and `line.cmax` if set.
            coloraxis
                Sets a reference to a shared color axis.
                References to these shared color axes are
                "coloraxis", "coloraxis2", "coloraxis3", etc.
                Settings for these shared color axes are set in
                the layout, under `layout.coloraxis`,
                `layout.coloraxis2`, etc. Note that multiple
                color scales can be linked to the same color
                axis.
            colorbar
                :class:`plotly.graph_objects.parcats.line.Color
                Bar` instance or dict with compatible
                properties
            colorscale
                Sets the colorscale. Has an effect only if in
                `line.color`is set to a numerical array. The
                colorscale must be an array containing arrays
                mapping a normalized value to an rgb, rgba,
                hex, hsl, hsv, or named color string. At
                minimum, a mapping for the lowest (0) and
                highest (1) values are required. For example,
                `[[0, 'rgb(0,0,255)'], [1, 'rgb(255,0,0)']]`.
                To control the bounds of the colorscale in
                color space, use`line.cmin` and `line.cmax`.
                Alternatively, `colorscale` may be a palette
                name string of the following list: Greys,YlGnBu
                ,Greens,YlOrRd,Bluered,RdBu,Reds,Blues,Picnic,R
                ainbow,Portland,Jet,Hot,Blackbody,Earth,Electri
                c,Viridis,Cividis.
            colorsrc
                Sets the source reference on Chart Studio Cloud
                for  color .
            hovertemplate
                Template string used for rendering the
                information that appear on hover box. Note that
                this will override `hoverinfo`. Variables are
                inserted using %{variable}, for example "y:
                %{y}". Numbers are formatted using d3-format's
                syntax %{variable:d3-format}, for example
                "Price: %{y:$.2f}".
                https://github.com/d3/d3-3.x-api-
                reference/blob/master/Formatting.md#d3_format
                for details on the formatting syntax. Dates are
                formatted using d3-time-format's syntax
                %{variable|d3-time-format}, for example "Day:
                %{2019-01-01|%A}".
                https://github.com/d3/d3-3.x-api-
                reference/blob/master/Time-Formatting.md#format
                for details on the date formatting syntax. The
                variables available in `hovertemplate` are the
                ones emitted as event data described at this
                link https://plotly.com/javascript/plotlyjs-
                events/#event-data. Additionally, every
                attributes that can be specified per-point (the
                ones that are `arrayOk: true`) are available.
                variables `count` and `probability`. Anything
                contained in tag `<extra>` is displayed in the
                secondary box, for example
                "<extra>{fullData.name}</extra>". To hide the
                secondary box completely, use an empty tag
                `<extra></extra>`.
            reversescale
                Reverses the color mapping if true. Has an
                effect only if in `line.color`is set to a
                numerical array. If true, `line.cmin` will
                correspond to the last color in the array and
                `line.cmax` will correspond to the first color.
            shape
                Sets the shape of the paths. If `linear`, paths
                are composed of straight lines. If `hspline`,
                paths are composed of horizontal curved splines
            showscale
                Determines whether or not a colorbar is
                displayed for this trace. Has an effect only if
                in `line.color`is set to a numerical array.
""",
            ),
            **kwargs
        )

'''
To run:

    python plot.py

in this directory, and navigate to:

    http://localhost:5000

'''
#!/usr/bin/env python

from __future__ import print_function

import flask

import numpy as np
import pandas as pd
import datetime
import urllib
import ijson

from bokeh.embed import components
from bokeh.plotting import *
from bokeh.models import CustomJS,HoverTool,ColumnDataSource, PrintfTickFormatter
from bokeh.models.widgets import Slider, TextInput
from bokeh.resources import INLINE
from bokeh.util.string import encode_utf8

from collections import OrderedDict

app = flask.Flask(__name__)

url_default='http://msi.mcgill.ca/GSoC_NANOGrav/pulsar_data_test.json'

def getitem(obj, item, default):
    if item not in obj:
        return default
    else:
        return obj[item]

@app.route("/")
def polynomial():
    """ Very simple embedding of a polynomial chart

    """

    # Grab the inputs arguments from the URL
    # This is automated by the button
    args = flask.request.args

    # Get all the form arguments in the url with defaults
    _source=getitem(args,'_source',url_default)
    _size=int(getitem(args,'size','5'))
    favcolor=getitem(args,'favcolor','#1F77B4')
    bcolor=getitem(args,'bcolor','#F5F5DC')
    _shape=getitem(args,'_shape','circle')
    lcolor=getitem(args,'lcolor','#FCB938')
    toggle=bool(getitem(args,'toggle',''))


    #Parsing json

    DEFAULT_TICKERS = ['TOAs','RawProfiles', 'Period', 'PeriodDerivative', 'DM', 'RMS', 'Binary']
    TOOLS = "tap,resize,crosshair,pan,wheel_zoom,box_zoom,reset,box_select,lasso_select,previewsave,hover"

    Pulsar,TOAs,RawProfiles, Period, PeriodDerivative, DM, RMS, Binary=[],[],[],[],[],[],[],[]
    url_location=urllib.urlopen(_source)
    for item in ijson.items(url_location,"item"):
        Pulsar.append(str(item["Pulsar"]))
        TOAs.append(float(item["TOAs"]))
        RawProfiles.append(int(item["Raw Profiles"]))
        Period.append(float(item["Period"]))
        PeriodDerivative.append(float(item["Period Derivative"]))
        DM.append(str(item["DM"]))
        RMS.append(str(item["RMS"]))
        if (item["Binary"]=="Y"):
            Binary.append("Yes")
        else:
            Binary.append("No")


    #Create a plot periodvs period derivative

    s1 = ColumnDataSource(
    data=dict(
        Pulsar=Pulsar,
        TOAs=TOAs,
        RawProfiles=RawProfiles,
        Period=Period,
        PeriodDerivative=PeriodDerivative,
        DM=DM,
        RMS=RMS,
        Binary=Binary,
        )
    )

    p1 = figure(plot_width=600, plot_height=600,
               title="Period vs Period Derivative", y_axis_type="log" ,y_range=[min(PeriodDerivative)-min(PeriodDerivative)/5, max(PeriodDerivative)+max(PeriodDerivative)/5],x_range=[min(Period)-min(Period)/5, max(Period)+max(Period)/5],x_axis_label='Period[s]', y_axis_label='Period Derivative[s/s]',tools=TOOLS)
    p1.background_fill_color = bcolor
    p1.background_fill_alpha = "0.5"
    getattr(p1,_shape)('Period', 'PeriodDerivative', legend="period deri",color=favcolor,size=_size, source=s1)
    #p1.circle('Period', 'PeriodDerivative', legend="period deri",color=favcolor,size=_size, source=s1)
    p1.xaxis.axis_label_text_font_size = "15pt"
    p1.yaxis.axis_label_text_font_size = "15pt"
    #p1.xaxis[0].formatter = PrintfTickFormatter(format="s")
    #p1.yaxis[0].formatter = PrintfTickFormatter(format=" s/s")    

    #Toggle Line
    #if getattr(p1,line,None):
    #   getattr(p1,line)('Period', 'PeriodDerivative',legend="period deri",line_dash=[4, 4], line_color=lcolor, line_width=1,source=s1)
    p1.line('Period', 'PeriodDerivative',legend="period deri",line_dash=[4, 4], line_color=lcolor, line_width=1,source=s1,visible=toggle)

    # Custom data source for selected points
    s2 = ColumnDataSource(
        data=dict(
            Pulsar=[],
            TOAs=[],
            RawProfiles=[],
            Period=[],
        PeriodDerivative=[],
        DM=[],
        RMS=[],
        Binary=[],
        )
    )

    p2= figure(plot_width=600, plot_height=600,
               title=" Selected points from Period vs Period Derivative", y_axis_type="log" ,y_range=[min(PeriodDerivative)-min(PeriodDerivative)/10, max(PeriodDerivative)+max(PeriodDerivative)/10],x_range=[min(Period)-min(Period)/10, max(Period)+max(Period)/10],x_axis_label='Period[s]', y_axis_label='Period Derivative[s/s]',tools=TOOLS)
    p2.xaxis.axis_label_text_font_size = "15pt"
    p2.yaxis.axis_label_text_font_size = "15pt"

    p2.circle('Period', 'PeriodDerivative', legend="period deri",alpha=1.2, source=s2)

    s1.callback = CustomJS(args=dict(s2=s2), code="""
            var inds = cb_obj.get('selected')['1d'].indices;
            var d1 = cb_obj.get('data');
            var d2 = s2.get('data');
            d2['Pulsar'] = []
            d2['TOAs'] = []
            d2['RawProfiles'] = []
            d2['Period'] = []
            d2['PeriodDerivative'] = []
            d2['DM'] = []
            d2['RMS'] = []
            d2['Binary'] = []
            for (i = 0; i < inds.length; i++) {
                d2['Pulsar'].push(d1['Pulsar'][inds[i]])
                d2['TOAs'].push(d1['TOAs'][inds[i]])
                d2['RawProfiles'].push(d1['RawProfiles'][inds[i]])
                d2['Period'].push(d1['Period'][inds[i]])
                d2['PeriodDerivative'].push(d1['PeriodDerivative'][inds[i]])
                d2['DM'].push(d1['DM'][inds[i]])
                d2['RMS'].push(d1['RMS'][inds[i]])
                d2['Binary'].push(d1['Binary'][inds[i]])

            }
            s2.trigger('change');
      """  )


    hover = p1.select(dict(type=HoverTool))
    hover.tooltips = OrderedDict([
        ("Pulsar's Name", '@Pulsar'),
        ('TOAs', '@TOAs'),
        ('RawProfiles', '@RawProfiles'),
        ('Period[s]', '@Period'),
        ('PeriodDerivative[s/s]', '@PeriodDerivative'),
        ('DM[pc/cc]', '@DM'),
        ('RMS[us]', '@RMS'),
        ('Binary', '@Binary'),
    ])

    js_resources = INLINE.render_js()
    css_resources = INLINE.render_css()

    #Setting up layout
    layout = hplot(p1, p2)

    script, div = components(layout,INLINE)
    html = flask.render_template(
        'embed.html',
        plot_script=script,
        plot_div=div,
        js_resources=js_resources,
        css_resources=css_resources,
        _source=_source,
        Pulsar=Pulsar,
        _shape=_shape,
        favcolor=favcolor,
        bcolor=bcolor,
        _size=_size,
        lcolor=lcolor,
        toggle=toggle
    )
    return encode_utf8(html)

if __name__ == "__main__":
    print(__doc__)
    app.run()

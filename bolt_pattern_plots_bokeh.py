#%% Imports

# scientific imports
import numpy as np
import pandas as pd

# plotting imports
from bokeh.models import LinearColorMapper, ColorBar, ColumnDataSource, Span, Arrow, NormalHead, Range1d
from bokeh.transform import transform

# importing figure and show for creating
# and showing plots from bokeh.plotting
# interface
from bokeh.plotting import figure, show

# output to jupyter
from bokeh.io import output_notebook
output_notebook()

#%% function plotboltloads

def plotboltloads(df, centroid):

    # convert centroid to xc, yc coordinates
    xc, yc = centroid

    # color mapper
    low_color_val = 0
    high_color_val = round(max(df.Paxial.max(), df.PshearMag.max()))

    color_mapper = LinearColorMapper(palette = "Viridis256",
                                    low = low_color_val,
                                    high = high_color_val)


    # create tooltips for plot
    TOOLTIPS = [
        ("Bolt ID", "$index"),
        ("x, y coordinates", "(@x{0.0}, @y{0.0})"),
        ("Axial Load", "@Paxial{1} N"),
        ("Shear Load", "@PshearMag{1} N"),
        ("Centroid", "({}, {})".format(round(xc,1), round(yc, 1)))
    ]

    # create figure 
    p = figure(width=600, height=600, match_aspect = True, tooltips = TOOLTIPS)

    # vline
    vline = Span(location=xc, 
                dimension='height',
                line_color='grey', 
                line_width=1)
    vline.level = 'underlay'        # set vline to the plot background
    p.add_layout(vline)

    # hline
    hline = Span(location=yc, 
                dimension='width',
                line_color='grey', 
                line_width=1)
    hline.level = 'underlay'        # set hline to the plot background
    p.add_layout(hline)

    # scatter plot with hex glyph
    p.hex('x', 'y', size=20,
        line_color = "grey",
        fill_color = transform('Paxial', color_mapper),
        alpha = 1,
		source = df)
    
    # color bar (axial load)
    color_bar = ColorBar(color_mapper = color_mapper,
					label_standoff = 12,
					location = (0,0),
					title = '\u2B21 Axial Load (N) / \u25B7 Shear Load (N)')

      

    # plot circle at the xc, yc centroid
    p.circle(xc, yc, size = 10, 
            line_color = 'grey',
            fill_color = 'white')

    # define the position of the color bar (i.e. to the right of the 'hex' scatter axes)
    p.add_layout(color_bar, 'below')
  

    # get axis limits
    xrng = df.x.max() - df.x.min()
    yrng = df.y.max() - df.y.min()
    plotrng = np.max([xrng, yrng])

    # find maximum PshearMag
    Pshearmax = df.PshearMag.max()

    # scale arrow length to be maximum of 1/5 of axis length
    arrowscale = plotrng * (1/5) / Pshearmax

    x_start = df.x
    y_start = df.y
    x_end = df.x + arrowscale * df.Vx
    y_end = df.y + arrowscale * df.Vy

    

    # plot arrows one by one on the exisiting plot
    for i in range(len(x_start)):

        source_P = ColumnDataSource({'PshearMag':[df.PshearMag[i]]})
        
        p.add_layout(Arrow(
                    end=NormalHead(fill_color=transform('PshearMag', color_mapper),
                                    line_color = "grey", 
                                    size =15),
                    line_color = "grey",
                    line_width = 2,
                    x_start=x_start[i], 
                    y_start=y_start[i], 
                    x_end=x_end[i], 
                    y_end=y_end[i],
                    source = source_P),
                    )
    
    # update plot range now that arrow coordinates are known
    xb = np.min([x_start.min(), x_end.min()])
    xt = np.max([x_start.max(), x_end.max()])
    yb = np.min([y_start.min(), y_end.min()])
    yt = np.max([y_start.max(), y_end.max()])

    # update plot axis limits to include 10% padding (i.e. all data observable in plot + padding)
    p.x_range = Range1d(xb - 0.1*(xt-xb), xt + 0.1*(xt-xb))
    p.y_range = Range1d(yb - 0.1*(yt-yb), yt + 0.1*(yt-yb))
    
    # return figure object for plot
    # to plot -> need to use show(p)
    return p

#%% function plotboltpoints

def plotboltpoints(points, centroid):
    
    # convert points to x, y coordinates
    x, y = points

    # convert centroid to xc, yc coordinates
    xc, yc = centroid

    # create tooltips for plot
    TOOLTIPS = [
        ("Bolt ID", "$index"),
        ("x, y coordinates", "(@x{0.0}, @y{0.0})"),
        ("Centroid", "({}, {})".format(round(xc,1), round(yc, 1)))
    ]

    # create figure
    p = figure(width=600, height=400, match_aspect = True, tooltips = TOOLTIPS)

    # vline
    vline = Span(location=xc, 
                dimension='height',
                line_color='grey', 
                line_width=1)
    vline.level = 'underlay'        # set vline to the plot background
    p.add_layout(vline)

    # hline
    hline = Span(location=yc, 
                dimension='width',
                line_color='grey', 
                line_width=1)
    hline.level = 'underlay'        # set hline to the plot background
    p.add_layout(hline)

    # scatter plot with hex glyph
    p.hex(x, y, size=20,
        line_color = "grey",
        fill_color = "pink",
        alpha = 1,
		)

    # show the plot
    show(p)

    
# %% Testing

# from bolt_pattern_points import bolt_centroid

# def circle(r, N, theta_start_deg = 0, plot = True, A = 1, udf_pivot = False):

#     alpha = np.deg2rad(theta_start_deg)
#     theta = np.linspace(np.pi/2, -3*np.pi/2 + 2*np.pi/N, N)
#     points = r*np.cos(-alpha + theta), r*np.sin(-alpha + theta)
#     if plot:
#         centroid = bolt_centroid(points, A, False, udf_pivot)
#         plotboltpoints(points, centroid)
#     return points

# # circle
# p3 = circle(100, 8)
# #p4 = circle(100, 6, theta_start_deg=25, udf_pivot=(25, 40))



# this file need to be tested from bolt_pattern_analysis to avoid cyclic references

# %%

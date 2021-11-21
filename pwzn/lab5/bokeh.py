from bokeh.plotting import figure, row, column
from bokeh.io import curdoc
from bokeh.util.hex import hexbin
from bokeh.transform import linear_cmap
from bokeh.palettes import all_palettes
from bokeh.layouts import layout
from bokeh.models import Slider
import numpy as np

n_points = 10000
alpha = 666
beta = 666

def generate_data():
    x = np.random.beta(alpha, beta, n_points)
    y = np.random.beta(alpha, beta, n_points)
    data = {'x': x, 'y': y}
    counts_x, temp_bins_x = np.histogram(x, bins=100, density=True)
    bins_x = []
    for i in range(len(temp_bins_x)-1):
        bins_x.append((temp_bins_x[i]+temp_bins_x[i+1])/2)
    max_x = max(counts_x)
    counts_y, temp_bins_y = np.histogram(y, bins=100, density=True)
    bins_y = []
    for i in range(len(temp_bins_y)-1):
        bins_y.append((temp_bins_y[i]+temp_bins_y[i+1])/2)
    max_y = max(counts_y)
    hist = {'bins_x': bins_x, 'counts_x': counts_x/(10*max_x), 'bins_y': bins_y, 'counts_y': counts_y/(10*max_y)}
    return data, hist

def callback(attr, old, new):
    global n_points, alpha, beta
    n_points = points_slider.value
    alpha = scale_slider.value
    beta = scale_b_slider.value
    data, hist = generate_data()
    g1.data_source.data = data
    binned_data = hexbin(data['x'], data['y'], 0.001)
    cmap = linear_cmap('counts', 'Turbo256', 0, max(binned_data['counts']))
    g2.glyph.fill_color = cmap
    g2.data_source.data = binned_data

data, hist = generate_data()
points_slider = Slider(start=1000, end=100000, step=100, value=n_points, title='points', width=300)
scale_slider = Slider(start=1, end=1000, step=1, value=alpha, title='alpha', width=300)
scale_b_slider = Slider(start=1, end=1000, step=1, value=beta, title='beta', width=300)
points_slider.on_change('value_throttled', callback)
scale_slider.on_change('value_throttled', callback)
scale_b_slider.on_change('value_throttled', callback)
f1 = figure(match_aspect=True)
g1 = f1.circle('x', 'y', source=data, alpha=0.1)
binned_data = hexbin(data['x'], data['y'], 0.001)
cmap = linear_cmap('counts', 'Turbo256', 0, max(binned_data['counts']))
f2 = figure(match_aspect=True)
f2.background_fill_color = all_palettes['Turbo'][256][0]
f2.grid.visible = False
g2 = f2.hex_tile(size=0.01, source=binned_data, fill_color=cmap, line_color=None)
h1 = figure(match_aspect=True)
g3 = h1.vbar(x=hist['bins_x'], top=hist['counts_x'], width=0.001)
h2 = figure(match_aspect=True)
g4 = h2.vbar(x=hist['bins_y'], top=hist['counts_y'], width=0.001)
l = layout([column(points_slider, scale_slider, scale_b_slider), row(f1, f2), row(h1, h2)], sizing_mode='stretch_width')
curdoc().add_root(l)

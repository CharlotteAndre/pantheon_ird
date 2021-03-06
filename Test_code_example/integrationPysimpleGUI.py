import PySimpleGUI as sg

from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import tkinter as Tk

"""
Demonstrates one way of embedding Matplotlib figures into a PySimpleGUI window.

Basic steps are:
 * Create a Canvas Element
 * Layout form
 * Display form (NON BLOCKING)
 * Draw plots onto convas
 * Display form (BLOCKING)
"""


#------------------------------- PASTE YOUR MATPLOTLIB CODE HERE -------------------------------

import numpy as np
import matplotlib.pyplot as plt

from matplotlib.ticker import NullFormatter  # useful for `logit` scale

# Fixing random state for reproducibility
np.random.seed(19680801)

# make up some data in the interval ]0, 1[
y = np.random.normal(loc=0.5, scale=0.4, size=1000)
y = y[(y > 0) & (y < 1)]
y.sort()
x = np.arange(len(y))

# plot with various axes scales
plt.figure(1)

# linear
plt.subplot(221)
plt.plot(x, y)
plt.yscale('linear')
plt.title('linear')
plt.grid(True)


# log
plt.subplot(222)
plt.plot(x, y)
plt.yscale('log')
plt.title('log')
plt.grid(True)


# symmetric log
plt.subplot(223)
plt.plot(x, y - y.mean())
plt.yscale('symlog', linthreshy=0.01)
plt.title('symlog')
plt.grid(True)

# logit
plt.subplot(224)
plt.plot(x, y)
plt.yscale('logit')
plt.title('logit')
plt.grid(True)
plt.gca().yaxis.set_minor_formatter(NullFormatter())
plt.subplots_adjust(top=0.92, bottom=0.08, left=0.10, right=0.95, hspace=0.25,
                    wspace=0.35)
fig = plt.gcf()      # if using Pyplot then get the figure from the plot
figure_x, figure_y, figure_w, figure_h = fig.bbox.bounds

#------------------------------- END OF YOUR MATPLOTLIB CODE -------------------------------

#------------------------------- Beginning of Matplotlib helper code -----------------------


def draw_figure(canvas, figure, loc=(0, 0)):
    """ Draw a matplotlib figure onto a Tk canvas

    loc: location of top-left corner of figure on canvas in pixels.

    Inspired by matplotlib source: lib/matplotlib/backends/backend_tkagg.py
    """
    figure_canvas_agg = FigureCanvasTkAgg(figure,master=canvas)
    figure_canvas_agg.draw()
    figure_canvas_agg.get_tk_widget().pack(side=Tk.TOP, fill=Tk.BOTH, expand=1)
    figure_x, figure_y, figure_w, figure_h = figure.bbox.bounds
    figure_w, figure_h = int(figure_w), int(figure_h)

    return

#------------------------------- Beginning of GUI CODE -------------------------------
layout = [[sg.Button('Launch visualisation'), sg.Button('Launch visualisation 2')]]

window = sg.Window('Have some Matplotlib....', layout)

while True :
    for i in range(2):
        event, values = window.read(timeout=100)
        if event == "Launch visualisation":
# define the window layout
            layout = [[sg.Text('Plot test', font='Any 18')],
                      [sg.Canvas(key='canvas')],
                      [sg.OK(pad=((figure_w / 2, 0), 3), size=(4, 2))]]

            # create the form and show it without the plot
            window_graph = sg.Window('Demo Application - Embedding Matplotlib In PySimpleGUI', force_toplevel=False).Layout(layout).Finalize()

            # add the plot to the window
            # fig_photo = draw_figure(window_graph.FindElement('canvas').TKCanvas, fig)

            # show it all again and get buttons
            event_graph, values_graph = window_graph.Read()

        if event == "Launch visualisation 2":
            layout = [[sg.Text('Plot test', font='Any 18')],
                      [sg.Canvas(key='canvas')],
                      [sg.OK(pad=((figure_w / 2, 0), 3), size=(4, 2))]]

            # create the form and show it without the plot
            window_graph_2 = sg.Window('Demo Application - Embedding Matplotlib In PySimpleGUI', force_toplevel=False).Layout(layout).Finalize()

            # add the plot to the window
            # fig_photo = draw_figure(window_graph_2.FindElement('canvas').TKCanvas, fig)

            # show it all again and get buttons
            event_graph_2, values_graph_2 = window_graph_2.Read()

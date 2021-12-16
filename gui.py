import numpy as np
import PySimpleGUI as sg
import matplotlib, time, threading
matplotlib.use('TkAgg')
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

sg.theme('SystemDefault')
font = ('Helvetica', 12)
titlefont = ('Helvetica', 14, "bold")

def draw_figure(canvas, figure, loc=(0, 0)):
    figure_canvas_agg = FigureCanvasTkAgg(figure, canvas)
    figure_canvas_agg.draw()
    figure_canvas_agg.get_tk_widget().pack(side='top', fill='both', expand=1)
    return figure_canvas_agg

main_left_layout = [
    [sg.Text("Simulation Parameters",font=titlefont)],
]

main_right_layout = [
    [sg.Canvas(size=(10,10),key="plot")],
]
main_layout = [
    [sg.Column(main_left_layout), sg.Column(main_right_layout)]
]
window = sg.Window("Cell simulation",main_layout, finalize=True,font=font,resizable=True)

def main():
    while True: 
        event, values = window.read()
        if event == sg.WIN_CLOSED:
            break
    window.close()


if __name__ == '__main__':
    main()


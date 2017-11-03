import ipywidgets as widgets
from ipywidgets import IntSlider
from IPython.display import display

from cruiser.inputfiles import INPUTS, load


SIMULATION = None
CURRENT_CASE_WIDGETS = []


def close_open_case_widgets():
    for widget in CURRENT_CASE_WIDGETS:
        widget.close()
    CURRENT_CASE_WIDGETS.clear()


def on_param_value_change(change):
    param = change['owner'].param
    setattr(SIMULATION, param, change['new'])


def on_case_change(change):
    global SIMULATION
    close_open_case_widgets()
    case_name = change['new']
    if not case_name:
        return
    sim = SIMULATION = load(case_name)
    for param in sim.params:
        inp = getattr(sim.__class__, param)
        widget_cls = getattr(widgets, inp.widget)
        w = widget_cls(value=getattr(sim, param),
                       description=param + ':',
                       **inp.widget_kwargs)
        w.param = param
        w.observe(on_param_value_change, names='value')
        CURRENT_CASE_WIDGETS.append(w)
        display(w)


def input_ui():
    case = widgets.Dropdown(
        options=('',) + INPUTS,
        description='Case:',
        disabled=False,
    )
    case.observe(on_case_change, names='value')
    return case



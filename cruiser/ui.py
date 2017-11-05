"""Input UI constructor for cruiser.""""
import json
import tempfile
import subprocess

import ipywidgets as widgets
from IPython.display import display

from cruiser.inputfiles import INPUTS, load


SIMULATION = None
CURRENT_RUN_WIDGETS = []
CURRENT_CASE_WIDGETS = []


def close_open_widgets(open_widgets):
    """Closes existing widgets for input file building"""
    for widget in open_widgets:
        widget.close()
    open_widgets.clear()


def on_param_value_change(change):
    """Updates an input parameter"""
    param = change['owner'].param
    setattr(SIMULATION, param, change['new'])


def on_case_change(change):
    """Switches between input parameter settings."""
    global SIMULATION
    close_open_widgets(CURRENT_CASE_WIDGETS)
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


def run_simulation():
    """Runs and analyzes a Cyclus Simulation."""
    close_open_widgets(CURRENT_RUN_WIDGETS)
    # get output from cyclus
    out = widgets.Output()
    CURRENT_RUN_WIDGETS.append(out)
    display(out)
    rundir = tempfile.mkdtemp(prefix='cyclus')




def input_ui():
    """Builds the top-level user interface structure."""
    # selector for simulation case
    case = widgets.Dropdown(
        options=('',) + INPUTS,
        description='Case:',
        disabled=False,
    )
    case.observe(on_case_change, names='value')
    display(case)
    # run sim button
    run = widgets.Button(
        description='Run Simulation',
        button_style='',
        tooltip='Run the current Cyclus simulation',
        )
    run.on_click(run_simulation)
    display(run)



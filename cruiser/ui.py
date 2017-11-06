"""Input UI constructor for cruiser."""
import os
import sys
import json
import time
import tempfile
import subprocess

import ipywidgets as widgets
from IPython.display import display

from cruiser.inputfiles import SCENARIOS, load
from cruiser.streams import stream_output
from cruiser.analysis import stock_analysis


SIMULATION = None
CURRENT_RUN_WIDGETS = []
CURRENT_SCENARIO_WIDGETS = []


def close_open_widgets(open_widgets):
    """Closes existing widgets for input file building"""
    for widget in open_widgets:
        widget.close()
    open_widgets.clear()


def on_param_value_change(change):
    """Updates an input parameter"""
    param = change['owner'].param
    setattr(SIMULATION, param, change['new'])


def on_scenario_change(change):
    """Switches between input parameter settings."""
    global SIMULATION
    close_open_widgets(CURRENT_SCENARIO_WIDGETS)
    scenario_name = change['new']
    if not scenario_name:
        return
    sim = SIMULATION = load(scenario_name)
    for param in sim.params:
        inp = getattr(sim.__class__, param)
        widget_cls = getattr(widgets, inp.widget)
        w = widget_cls(value=getattr(sim, param),
                       description=param + ':',
                       **inp.widget_kwargs)
        w.param = param
        w.observe(on_param_value_change, names='value')
        CURRENT_SCENARIO_WIDGETS.append(w)
        display(w)


def run_simulation(button):
    """Runs and analyzes a Cyclus Simulation."""
    close_open_widgets(CURRENT_RUN_WIDGETS)
    # get output from cyclus
    out = widgets.Output()
    CURRENT_RUN_WIDGETS.append(out)
    display(out)
    rundir = tempfile.mkdtemp(prefix='cyclus-')
    # create input file
    infile = os.path.join(rundir, SIMULATION.scenario + '.json')
    with open(infile, 'w') as f:
        json.dump(SIMULATION.sim, f)
    with out:
        print('Wrote Cyclus input file to {0}'.format(infile))
    # run cyclus simulation
    outfile = os.path.join(rundir, SIMULATION.scenario + '.h5')
    with out:
        print('Starting Cyclus Simulation')
        stream_output(['cyclus', '-o', outfile, infile])
    # perform analysis
    stock_analysis(outfile)


def input_ui():
    """Builds the top-level user interface structure."""
    # selector for simulation case
    scenario = widgets.Dropdown(
        options=('',) + SCENARIOS,
        description='Case:',
        disabled=False,
    )
    scenario.observe(on_scenario_change, names='value')
    display(scenario)
    # run sim button
    run = widgets.Button(
        description='Run Simulation',
        button_style='',
        tooltip='Run the current Cyclus simulation',
        )
    run.on_click(run_simulation)
    display(run)

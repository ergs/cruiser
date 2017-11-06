"""Provides analyis utilities for Cruiser"""
import warnings

from IPython.display import display
from ipywidgets.widgets.interaction import interact
import matplotlib.pyplot as plt

with warnings.catch_warnings():
    warnings.simplefilter("ignore")
    import cymetric as cym
    import cymetric.fco_metrics


FIGS = []
EVALER = None


def plot_fco_egen(evaler=None):
    evaler = EVALER if evaler is None else evaler
    frame = evaler.eval('FcoElectricityGenerated')
    fig = plt.figure()
    plt.plot(frame['Year'], frame['Energy'])
    plt.xlabel('Years')
    plt.ylabel('Energy Generated [GWe-years]')
    plt.title('Energy Generated')


def plot_fco_umined(evaler=None):
    evaler = EVALER if evaler is None else evaler
    frame = evaler.eval('FcoUMined')
    fig = plt.figure()
    plt.plot(frame['Year'], frame['UMined'])
    plt.xlabel('Years')
    plt.ylabel('Uranium Mined [tonnes]')
    plt.title('Uranium Mined')


def plot_builds(evaler=None):
    evaler = EVALER if evaler is None else evaler
    frame = evaler.eval('BuildSeries')
    fig = plt.figure()
    protos = sorted(set(frame['Prototype']))
    width = 1.0 / len(protos)
    for i, proto in enumerate(protos):
        mask = frame['Prototype'] == proto
        plt.bar(frame['EnterTime'][mask]/12.0 + i*width, frame['Count'][mask],
                label=proto, width=width)
    plt.xlabel('Years')
    plt.ylabel('Count')
    plt.title('Number of Facilities Built')
    plt.legend(loc=0)


def stock_analysis(filename):
    """Runs stock analysis utilities."""
    global EVALER
    for fig in FIGS:
        fig.close()
    FIGS.clear()
    db = cym.dbopen(filename)
    evaler = EVALER = cym.Evaluator(db)
    plot_fco_egen()
    #plot_fco_umined()
    plot_builds()
    #db.close()
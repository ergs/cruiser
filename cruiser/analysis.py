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


def stock_analysis(filename):
    """Runs stock analysis utilities."""
    global EVALER
    for fig in FIGS:
        fig.close()
    FIGS.clear()
    db = cym.dbopen(filename)
    evaler = EVALER = cym.Evaluator(db)
    display(plot_fco_egen())
    #db.close()
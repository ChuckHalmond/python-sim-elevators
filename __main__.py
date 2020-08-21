import yaml
import simpy
import click
import math
import numpy as np
import matplotlib.pyplot as plt
import itertools
import random
import sys

from src.model.utils.io import line, progressBar, appendToStreamLineStartingWith
from src.model.system import System
from src.model.config import Config
from src.model.registries.scheduling_registry import SchedulingRegistry
from src.model.registries.idle_registry import IdleRegistry
from src.model.behaviours.scheduling import SchedulingFCFS, SchedulingLS, SchedulingSSTF
from src.model.behaviours.idle import IdleBottom, IdleMiddle, IdleOnPlace, IdleYoyo

def readYamlConfig(filename):
    with open(filename, 'r') as stream:
        try:
            return yaml.load(stream, Loader = yaml.FullLoader)
        except yaml.YAMLError as error:
            print(error)
            return {}

def writeDefaultYamlConfig():
    config = DEFAULT_CONFIG

    with open(DEFAULT_CONFIG_FILE_NAME, 'w+') as stream:
        try:
            yaml.dump(config, stream)
            
            # add comments to the config file
            appendToStreamLineStartingWith(
                stream,
                {
                    'idle': ' #[' + '|'.join(IdleRegistry.keys()) + ']',
                    'scheduling': ' #[' + '|'.join(SchedulingRegistry.keys()) + ']'
                }
            )

        except yaml.YAMLError as error:
            print(error)

def registerBehaviours():
    SchedulingRegistry.register('fcfs', SchedulingFCFS())
    SchedulingRegistry.register('sstf', SchedulingSSTF())
    SchedulingRegistry.register('ls', SchedulingLS())

    IdleRegistry.register('bottom', IdleBottom())
    IdleRegistry.register('middle', IdleMiddle())
    IdleRegistry.register('onplace', IdleOnPlace())
    IdleRegistry.register('yoyo', IdleYoyo())

DEFAULT_CONFIG_FILE_NAME = 'config.yaml'
DEFAULT_CONFIG = Config(
    live = True,
    liveDelay = 0.25,
    recap = True,
    steps = 100,
    randSeed = 12,
    mu = 0.5,
    lbda = 60.0,
    floors = 7,
    elevators = 2,
    capacity = 8,
    scheduling = 'sstf',
    idle = 'yoyo'
)

@click.command()
@click.option('--yaml', is_flag = True, show_default = True, help = 'Configures the simulation with the \'' + DEFAULT_CONFIG_FILE_NAME + '\' configuration file.' \
    ' To load another YAML configuration file, use this option along with the --configfile option.' \
    ' NB: The type of the parameters are not safe-check, please follow the default values.')
@click.option('--configfile', default = 'config.yaml', show_default = True, help = 'The filename of the YAML configuration file.')
@click.option('--resetconfigfile', is_flag = True, show_default = True, help = 'Creates a default YAML configuration file, \'' + DEFAULT_CONFIG_FILE_NAME + '\', and does not run any simulation.')
@click.option('--plot', is_flag = True, show_default = True, help = 'Creates a plot of the average user times from the simulation.')
def parseArgs(run = False, yaml = False, configfile = 'config.yaml', resetconfigfile = False, plot = False):
    """
    Runs a simulation from the given optionnal YAML configuration file.
    """
    if (resetconfigfile):
        writeDefaultYamlConfig()
        return
    
    config = DEFAULT_CONFIG

    if (yaml):
        yamlConfig = readYamlConfig(configfile)
        config.partialOverride(yamlConfig)

    if (plot):
        runSimAndPlot(config)
    else:
        runSim(config)

def runSim(config):
    env = simpy.Environment()
    system = System(env, config)
    system.start()

def runSimAndPlot(config):

    print(line)
    print('Plot')
    print(line)

    # 0. removes the live and recap parameters

    config.live = False
    config.liveDelay = 0
    config.recap = False

    # 1. computes every pair of behaviours

    behavioursPairs = list(itertools.product(SchedulingRegistry.keys(), IdleRegistry.keys()))
    nbPairs = len(behavioursPairs)

    # 2. runs the simulation with each pair of behaviours
    #   and store the total user waiting and serving times

    labels = nbPairs * [0]
    waitingTimes = nbPairs * [0]
    servingTimes = nbPairs * [0]

    for i in range(nbPairs):
        config.scheduling = behavioursPairs[i][0]
        config.idle = behavioursPairs[i][1]

        env = simpy.Environment()
        system = System(env, config)
        system.start()

        waitingTimes[i] += system.memo.waitingTimeDone
        servingTimes[i] += system.memo.servingTimeDone

        progressBar(i, nbPairs)
    progressBar(1, 1)

    # 3. transforms the total times as times per worker

    for i in range(nbPairs):
        labels[i] = behavioursPairs[i][0] + '\n' + behavioursPairs[i][1]
        waitingTimes[i] /= max(system.memo.workersDone, 1)
        servingTimes[i] /= max(system.memo.workersDone, 1)

    # 4. plots the times as a bar chart

    fig, ax = plt.subplots()

    x = np.arange(nbPairs) # the label locations
    width = 0.3 # the width of the bars

    waitingTimesBars = ax.bar(x - width / 2, waitingTimes, width, label = 'Waiting Time')
    servingTimesBars = ax.bar(x + width / 2, servingTimes, width, label = 'Serving Time')

    # autolabel the bars
    for bars in [waitingTimesBars, servingTimesBars]:
        for rect in bars:
            height = rect.get_height()
            ax.annotate(
                '{:.1f}'.format(height),
                xy = (rect.get_x() + rect.get_width() / 2, height),
                xytext = (0, 3),  # 3 points of vertical offset
                textcoords = 'offset points',
                ha = 'center',
                va = 'bottom'
            )

    # labels the chart
    ax.set_xticks(x)
    ax.set_xticklabels(labels)
    ax.set_ylabel('User Time (minutes)')
    ax.set_title(
        'Average user time by scheduling and idle behaviour' \
        '\nruns = %d, λ = %.2f, μ = %.2f, elevators = %d, capacity = %d, floors = %d'
        % (config.steps, config.lbda, config.mu, config.elevators, config.capacity, config.floors)
    )
    ax.legend()
    fig.tight_layout() # fixes the layout

    # plots the chart
    plt.show()
    
if __name__== '__main__':
    registerBehaviours()
    parseArgs()

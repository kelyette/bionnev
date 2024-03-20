import eel
import atexit
import json

from classes.simulation import Simulation
from parameters import plot_rules

LOG_ERR = '\033[91m[ERR]\033[0m '
LOG_WARN = '\033[93m[WARN]\033[0m '
LOG_DEBUG = '\033[96m[DEBUG]\033[0m '

print(LOG_DEBUG + "Starting Eel")

eel.init('web')

with open("parameters/config.json", "r") as f:
    config = json.load(f)
    
    default_envrule = config["default_envrule"]
    default_cellrule = config["default_cellrule"]
    default_plotrule = config["default_plotrule"]

sim = Simulation(default_envrule, default_cellrule, local=True)
plot_stgs = getattr(plot_rules, default_plotrule)()
last_time = 0.0

class State:
    def __init__(self):
        self.started = False
        self.paused = False
    
    def to_dict(self):
        return [i for i in self.__dict__ if i[0] != '_']

state = State()

@eel.expose
def sim_start():
    print(LOG_DEBUG + "jsmod:sim_start()")

    if state.started:
        sim.restart()
        
    state.started ^= True
    state.paused = not state.started
    
    return state.started

@eel.expose
def sim_pause():
    print(LOG_DEBUG + "jsmod:sim_pause()")
    
    state.paused ^= True
    
    return state.paused

@eel.expose
def sim_stop():
    print(LOG_DEBUG + "jsmod:sim_stop()")
    
    state.started = False

@eel.expose
def get_state():
    print(LOG_DEBUG + "jsmod:get_state()")

    return state.to_dict()

@eel.expose
def sim_launch():
    print(LOG_DEBUG + "jsmod:sim_launch()")

    state.started ^= True
    if state.started:
        state.paused = False 
    else: 
        state.sim.restart()
        state.paused = True

@eel.expose
def sim_get_state():
    """ print(LOG_DEBUG + "jsmod:sim_update()") """

    frame = sim.env.get_state()
    stats = [f"{stat}: {plot_stgs.stats[stat](sim):0.{plot_stgs.stats_pres}f}" for stat in list(plot_stgs.stats.keys())]
    return frame, stats

@eel.expose
def sim_get_size():
    print(LOG_DEBUG + "jsmod:sim_get_size()")

    return sim.env.grid_size

if __name__ == '__main__':
    sim.env.x = []
    eel.start('index.html', size=(1000, 700), cmdline_args=['--auto-open-devtools-for-tabs'], block=False)

    while True:
        eel.sleep(0.05)
        print(sim.env.clock, end='\r')
        if state.started and not state.paused:
            sim.next()
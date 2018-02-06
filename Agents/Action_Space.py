'''
This contains a class designed to limit the action space for training purposes,
as well as the functions needed to exicute the actions allowed in this space.
'''
import os
import sys
from absl import flags
from absl.flags import FLAGS

from pysc2.env import sc2_env
from pysc2.env import environment
from pysc2.lib import actions
from pysc2.maps import ladder

class Action_Space:

    # define the units and their actions
    valid_units = {126: ("Move_screen", "Effect_InjectLarva_screen"), #queen
       104: ("Move_screen", "Harvest_Gather_screen", "Build_Hatchery_screen", "Build_SpawningPool_screen"), #drone
       151: ("Train_Drone_quick", "Train_Overlord_quick"), #larva
       86: ("Train_Queen_quick")}  # hatchery
    busy_units = {}
    
    def __init__(self):
        return

    # compare the provided ID number to the ID of the units allowed
    def get_actions(self, unit_id):
        # return the valid actions for the given unit 
        if unit_id in self.valid_units:
            return self.valid_units[unit_id]
        return "Unit not defined in action space"

    def drone_busy(drone_id):
        if drone_id in busy_units:
            return True
        return False
  
    
# Action space functions
def inject_Larva(queen_id):
    return
def harvest_Minerals(drone_id):
    return
def harvest_Gas(drone_id):
    return
def build_Hatchery(drone_id):
    return
def build_Gas_Gyser(drone_id):
    return
def train_Drone():
    actions.select_larva()
    actions.FUNCTIONS[467]
    return
def train_Queen():
    actions.select_unit(actions.sc_ui.ActionMultiPanel.SelectAllOfType, 86)
    actions.FUNCTIONS[486]
    return
# I was thinking thats since you only need overlords when supply capped this function might be better as part of train_drone
# the same as the train queen tests for the spawning pool
def train_Overlord():
    actions.select_larva()
    actions.FUNCTIONS[483]
    return

# Auxilary functions
def move_Screen(unit_id):
    return
def build_Spawning_Pool(drone_id):
    return



# testing and debuging
def main():
    t1 = Action_Space
    print("getting drone actions")
    print (t1.get_actions(t1, 151))
    print("test for a unit not in the action space (112-zerg_Corruptor)")
    print (t1.get_actions(t1, 112))

    map_name = FLAGS.map_name
    print('Initializing Testing Enviroment')
    act_spec = sc2_env.SC2Env(map_name=map_name).action_spec()
    env = sc2_env.SC2Env(map_name=map_name, agent_race='Z')
    env.step(act_spec)
    #train_Queen()
    train_Drone()


if __name__ == '__main__':
    flags.DEFINE_string("map_name", "AbyssalReef", "Name of the map/minigame")
    FLAGS(sys.argv)
    main()

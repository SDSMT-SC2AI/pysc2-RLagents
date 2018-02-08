'''
This contains a class designed to limit the action space for training purposes,
as well as the functions needed to exicute the actions allowed in this space.
'''
import os
import sys
from absl import flags
from absl.flags import FLAGS

from pysc2.env import sc2_env
from pysc2.agents import base_agent
from pysc2.lib import actions
from pysc2.maps import ladder
from pysc2.lib import features
from pysc2.lib import point

_SELECT_ARMY = actions.FUNCTIONS.select_army.id
_NOT_QUEUED = [0]

class Action_Space:

    # define the units and their actions
    valid_units = {126: ("Move_screen", "Effect_InjectLarva_screen"), #queen
       104: ("Move_screen", "Harvest_Gather_screen", "Build_Hatchery_screen", "Build_SpawningPool_screen"), #drone
       151: ("Train_Drone_quick", "Train_Overlord_quick"), #larva
       86: ("Train_Queen_quick")}  # hatchery
    busy_units = {}
    
    def __init__(self):
        return
    # Action space functions
    def inject_Larva(queen_id):
        actions.FunctionCall(select_unit, [sc_ui.ActionMultiPanel.SingleSelect, 86])
        point = [0, 0]
        actions.FunctionCall(select_unit, [sc_ui.ActionMultiPanel.SelectAllOfType, 126])
        actions.FunctionCall(Effect_InjectLarva_screen, [_NOT_QUEUED, point])
        return
    def harvest_Minerals(drone_id):
        actions.FunctionCall(select_unit, [sc_ui.ActionMultiPanel.SelectAllOfType, 104])
        point = [0, 0]
        actions.FunctionCall(Harvest_Gather_screen, [_NOT_QUEUED, point])
        return
    def harvest_Gas(drone_id):
        actions.FunctionCall(select_unit, [sc_ui.ActionMultiPanel.SelectAllOfType, 104])
        point = [0, 0]
        actions.FunctionCall(Harvest_Gather_screen, [_NOT_QUEUED, point])
        return
    def build_Hatchery(drone_id):
        actions.FunctionCall(select_unit, [sc_ui.ActionMultiPanel.SelectAllOfType, 104])
        point = [0, 0]
        actions.FunctionCall(Build_Hatchery_screen, [_NOT_QUEUED, point])
        return
    def build_Gas_Gyser(drone_id):
        actions.FunctionCall(select_unit, [sc_ui.ActionMultiPanel.SelectAllOfType, 104])
        point = [0, 0]
        actions.FunctionCall(Build_Refinery_screen, [_NOT_QUEUED, point])
        return
    def train_Drone():
        actions.FunctionCall(select_larva, [])
        actions.FunctionCall(Train_Drone_quick, [_NOT_QUEUED])
        return
    def train_Queen():
        actions.FunctionCall(select_unit, [sc_ui.ActionMultiPanel.SelectAllOfType, 86])
        actions.FunctionCall(Train_Queen_quick, [_NOT_QUEUED])
        return
    def train_Overlord():
        actions.FunctionCall(select_larva, [])
        actions.FunctionCall(Train_Overlord_quick, [])
        return
    def build_Spawning_Pool(drone_id):
        actions.FunctionCall(select_unit, [sc_ui.ActionMultiPanel.SelectAllOfType, 104])
        point = [0, 0]
        actions.FunctionCall(Build_SpawningPool_screen, [_NOT_QUEUED, point])
        return

    # compare the provided ID number to the ID of the units allowed
    def get_actions(self, unit_id):
        # return the valid actions for the given unit 
        if unit_id in self.valid_units:
            return self.valid_units[unit_id]
        return "Unit not defined in action space"
    #function for checking if drones are doing a non-interuptable task
    def drone_busy(drone_id):
        if drone_id in busy_units:
            return True
        return False
  
class Mineral_agent(base_agent.BaseAgent):
  """An agent for building a base and populating it with drones."""

  def step(self, obs):
    act = Action_Space
    act.train_Drone()


# testing and debuging
def main():
    t1 = Action_Space
    print("getting drone actions")
    print (t1.get_actions(t1, 151))
    print("test for a unit not in the action space (112-zerg_Corruptor)")
    print (t1.get_actions(t1, 112))

    agent = Mineral_agent
    map_name = FLAGS.map_name
    print('Initializing Testing Enviroment')
    act_spec = sc2_env.SC2Env(map_name=map_name).action_spec()
    env = sc2_env.SC2Env(map_name=map_name, agent_race='Z')



if __name__ == '__main__':
    flags.DEFINE_string("map_name", "AbyssalReef", "Name of the map/minigame")
    FLAGS(sys.argv)
    main()

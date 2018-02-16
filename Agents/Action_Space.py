'''
This contains a class designed to limit the action space for training purposes,
as well as the functions needed to exicute the actions allowed in this space.
'''
import os
import sys
from collections import deque
from absl import flags
from absl.flags import FLAGS

from pysc2.env import sc2_env
from pysc2.agents import base_agent
from pysc2.lib import actions
from pysc2.maps import ladder
from pysc2.lib import features
from pysc2.lib import point

#units
_DRONE = 104
_HATCHERY = 86
_LARVA = 151
_QUEEN = 126

#Actions
_BUILD_POOL = actions.FUNCTIONS.Build_SpawningPool_screen.id
_BUILD_HATCHERY = actions.FUNCTIONS.Build_Hatchery_screen.id
_BUILD_GAS = actions.FUNCTIONS.Build_Extractor_screen.id
_GATHER_RESOURCES = actions.FUNCTIONS.Harvest_Gather_Drone_screen.id
_INJECT_LARVA = actions.FUNCTIONS.Effect_InjectLarva_screen.id
_SELECT_ARMY = actions.FUNCTIONS.select_army.id
_SELECT_POINT = actions.FUNCTIONS.select_point.id
_SELECT_LARVA = actions.FUNCTIONS.select_larva.id
_TRAIN_DRONE = actions.FUNCTIONS.Train_Drone_quick.id
_TRAIN_QUEEN = actions.FUNCTIONS.Train_Queen_quick.id
_TRAIN_OVERLORD = actions.FUNCTIONS.Train_Overlord_quick.id

#feature info
_PLAYER_RELATIVE = features.SCREEN_FEATURES.player_relative.index
_UNIT_TYPE = features.SCREEN_FEATURES.unit_type.index

#action arguments
_NOT_QUEUED = [0]
_QUEUED = [1]
_PLAYER_SELF = 1


class Action_Space:
    # define the units and their actions
    valid_units = {126: ("Move_screen", "Effect_InjectLarva_screen"), #queen
       104: ("Move_screen", "Harvest_Gather_screen", "Build_Hatchery_screen", "Build_SpawningPool_screen", "Build_Extractor_screen"), #drone
       151: ("Train_Drone_quick", "Train_Overlord_quick"), #larva
       86: ("Train_Queen_quick")}  # hatchery
    pool_flag = False


    def __init__(self):
        self.busy_units = {}
        self.actionq = deque([])
        self.pointq = deque([])
        return

    def action_step(self):
        if self.actionq:
            action = self.actionq.popleft()
        else:
            action = "No_Op"

        if ((action == "Select_Point_screen")
           | (action == "Effect_InjectLarva_screen")
           | (action == "Harvest_Gather_screen")
           | (action == "Build_Hatchery_screen")
           | (action == "Build_Extractor_screen")
           | (action == "Build_SpawningPool_screen")):
            target = self.pointq.popleft()
        else:
            target = [0,0]

        return {
            "Build_Extractor_screen" : actions.FunctionCall(_BUILD_GAS, [_NOT_QUEUED, target]),
            "Build_Hatchery_screen" : actions.FunctionCall(_BUILD_HATCHERY, [_NOT_QUEUED, target]),
            "Build_SpawningPool_screen" : actions.FunctionCall(_BUILD_POOL, [_NOT_QUEUED, point]),
            "Effect_InjectLarva_screen" : actions.FunctionCall(_INJECT_LARVA, [_NOT_QUEUED, target]),
            "Harvest_Gather_screen" : actions.FunctionCall(_GATHER_RESOURCES, [_NOT_QUEUED, target]),
            "Train_Drone_quick" : actions.FunctionCall(_TRAIN_DRONE, [_NOT_QUEUED]),
            "Train_Overlord_quick" : actions.FunctionCall(_TRAIN_OVERLORD, [_NOT_QUEUED]),
            "Train_Queen_quick" : actions.FunctionCall(_TRAIN_QUEEN, [_NOT_QUEUED]),     
            "Select_Point_screen" : actions.FunctionCall(_SELECT_POINT, [_NOT_QUEUED, target]),
            "No_Op" : actions.FunctionCall(actions.FUNCTIONS.no_op.id, [])
            }[action]

    # Action space functions
    def build_Hatchery(self, obs, drone_id):
        #first select a drone
        units = obs.observation["screen"][_UNIT_TYPE]
        unit_y, unit_x = (units == _DRONE).nonzero()
        target = [unit_x[0], unit_y[0]]
        self.pointq.append(target)
        self.actionq.append("Select_Point_screen")
        #get the coords for the next base and build there
        target = get_base_coord()
        self.pointq.append(target)
        self.actionq.append("Build_Hatchery_screen")

    def build_Gas_Gyser(self, obs, drone_id):
        #select a drone
        units = obs.observation["screen"][_UNIT_TYPE]
        unit_y, unit_x = (units == _DRONE).nonzero()
        target = [unit_x[0], unit_y[0]]
        self.pointq.append(target)
        self.actionq.append("Select_Point_screen")

        #find an unused geyser and build on it
        unit_y, unit_x = (units == 342).nonzero()
        half = len(unit_x)/2
        #only works for spawning in the bottom, need to figure out how to average location for placement
        target = [unit_x[:int(half)].mean(), unit_y[:int(half)].mean()]
        self.pointq.append(target)
        self.actionq.append("Build_Extractor_screen")

    def build_Spawning_Pool(self, obs, drone_id):
        #step on is selecting a dron to build with
        units = obs.observation["screen"][_UNIT_TYPE]
        unit_y, unit_x = (units == _DRONE).nonzero()
        #grab the first drone for now
        target = [unit_x[0], unit_y[0]]
        self.pointq.append(target)
        self.actionq.append("Select_Point_screen")

        #then build the pool
        units = obs.observation["screen"][_UNIT_TYPE]
        unit_y, unit_x = (units == _HATCHERY).nonzero()
        #location is just left of the nearest hatchery
        target = [unit_x.mean()-4, unit_y.mean()]
        self.pointq.append(target)
        self.actionq.append("Build_SpawningPool_screen")
        self.pool_flag = True
        
    def harvest_Minerals(self, obs, drone_id):
        #select a drone
        units = obs.observation["screen"][_UNIT_TYPE]
        unit_y, unit_x = (units == _DRONE).nonzero()
        target = [unit_x[0], unit_y[0]]
        self.pointq.append(target)
        self.actionq.append("Select_Point_screen")

        #find a mineral patch and que clicking it
        units = obs.observation["screen"][_UNIT_TYPE]
        unit_y, unit_x = (units == 341).nonzero()
        target = [unit_x[0], unit_y[0]]
        self.pointq.append(target)
        self.actionq.append("Harvest_Gather_screen")

    def harvest_Gas(self, obs, drone_id):
        #select a drone
        units = obs.observation["screen"][_UNIT_TYPE]
        unit_y, unit_x = (units == _DRONE).nonzero()
        target = [unit_x[0], unit_y[0]]
        self.pointq.append(target)
        self.actionq.append("Select_Point_screen")

        #find an extractor and que clicking it
        units = obs.observation["screen"][_UNIT_TYPE]
        unit_y, unit_x = (units == 88).nonzero()
        target = [unit_x.mean(), unit.mean()]
        self.pointq.append(target)
        self.actionq.append("Harvest_Gather_screen")

    def inject_Larva(self, obs, queen_id):
        #select a queen
        units = obs.observation["screen"][_UNIT_TYPE]
        unit_y, unit_x = (units == _QUEEN).nonzero()
        target = [unit_x[0], unit_y[0]]
        self.pointq.append(target)
        self.actionq.append("Select_Point_screen")

        #find a hatchery and inject it
        units = obs.observation["screen"][_UNIT_TYPE]
        unit_y, unit_x = (units == _HATCHERY).nonzero()
        target = [unit_x.mean(), unit_y.mean()]
        self.pointq.append(target)
        self.actionq.append("Effect_InjectLarva_screen")
        
    def train_Drone(self, obs):
        #find larva position
        units = obs.observation["screen"][_UNIT_TYPE]
        unit_y, unit_x = (units == _LARVA).nonzero()
        target = [unit_x[0], unit_y[0]]

        #que clicking a larva and morphing it to a drone
        self.pointq.append(target)
        self.actionq.append("Select_Point_screen")
        self.actionq.append("Train_Drone_quick")
                
    def train_Overlord(self, obs):
        #find larva position
        units = obs.observation["screen"][_UNIT_TYPE]
        unit_y, unit_x = (units == _LARVA).nonzero()
        target = [unit_x[0], unit_y[0]]

        #que clicking a larva and morphing it to a overlord
        self.pointq.append(target)
        self.actionq.append("Select_Point_screen")
        self.actionq.append("Train_Overlord_quick")

    def train_Queen(self, obs):
        #if no pool is built redirect to building it instead
        if self.pool_flag == False:
            self.build_Spawning_Pool(0, obs)
            return

        #select a hatchery
        units = obs.observation["screen"][_UNIT_TYPE]
        unit_y, unit_x = (units == _HATCHERY).nonzero()
        target = [unit_x.mean(), unit_y.mean()]
        self.pointq.append(target)
        self.actionq.append("Select_Point_screen")
        #que a queen
        self.actionq.append("Train_Queen_quick")
        
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
    #function for finding valid expos
    def get_base_coord():
        #need to find a method for getting base expansion coordinates.
        return [0,0]


def main():
    return

if __name__ == '__main__':
    main()

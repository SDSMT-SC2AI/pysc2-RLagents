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
       104: ("Move_screen", "Harvest_Gather_screen", "Build_Hatchery_screen", "Build_SpawningPool_screen"), #drone
       151: ("Train_Drone_quick", "Train_Overlord_quick"), #larva
       86: ("Train_Queen_quick")}  # hatchery
    pool_flag = False
    busy_units = {}
    actionq = {}
    
    def __init__(self):
        return

    # Action space functions
    def inject_Larva(step, obs, queen_id):
        if step == 0:
            #select a queen
            units = obs.observation["screen"][_UNIT_TYPE]
            unit_y, unit_x = (units == _QUEEN).nonzero()
            target = [unit_x[0], unit_y[0]]
            return actions.FunctionCall(_SELECT_POINT, [_NOT_QUEUED, target])
        elif step == 1:
            #find a hatchery and inject it
            units = obs.observation["screen"][_UNIT_TYPE]
            unit_y, unit_x = (units == _HATCHERY).nonzero()
            point = [unit_x[0], unit_y[0]]
            return actions.FunctionCall(_INJECT_LARVA, [_NOT_QUEUED, point])
        else:
            return actions.FunctionCall(actions.FUNCTIONS.no_op.id, [])
        
    def harvest_Minerals(step, obs, drone_id, mineral_id):
        if(step == 0):
            #select a drone
            units = obs.observation["screen"][_UNIT_TYPE]
            unit_y, unit_x = (units == _DRONE).nonzero()
            target = [unit_x[0], unit_y[0]]
            return actions.FunctionCall(_SELECT_POINT, [_NOT_QUEUED, target])
        elif(step == 1):
            #find a mineral patch and send the drone to mine it
            units = obs.observation["screen"][_UNIT_TYPE]
            unit_y, unit_x = (units == 341).nonzero()
            point = [unit_x[0], unit_y[0]]
            return actions.FunctionCall(_GATHER_RESOURCES, [_NOT_QUEUED, point])
        else:
            return actions.FunctionCall(actions.FUNCTIONS.no_op.id, [])

    def harvest_Gas(step, obs, drone_id, gas_id):
        if(step == 0):
            #select a drone
            units = obs.observation["screen"][_UNIT_TYPE]
            unit_y, unit_x = (units == _DRONE).nonzero()
            target = [unit_x[0], unit_y[0]]
            return actions.FunctionCall(_SELECT_POINT, [_NOT_QUEUED, target])
        elif(step == 1):
            #send it to an on screen extractor
            units = obs.observation["screen"][_UNIT_TYPE]
            unit_y, unit_x = (units == 88).nonzero()
            point = [unit_x[1], unit_y[1]]
            return actions.FunctionCall(_GATHER_RESOURCES, [_NOT_QUEUED, point])
        else:
            return actions.FunctionCall(actions.FUNCTIONS.no_op.id, [])

    def build_Hatchery(step, obs, drone_id):
        if(step == 0):
            #first select a drone
            units = obs.observation["screen"][_UNIT_TYPE]
            unit_y, unit_x = (units == _DRONE).nonzero()
            target = [unit_x[0], unit_y[0]]
            return actions.FunctionCall(_SELECT_POINT, [_NOT_QUEUED, target])
        elif(step == 1):
            #get the coords for the next base and build there
            point = get_base_coord()
            return actions.FunctionCall(_BUILD_POOL, [_NOT_QUEUED, point])
        else:
            return actions.FunctionCall(actions.FUNCTIONS.no_op.id, [])
        
        return

    def build_Gas_Gyser(step, drone_id, obs):
        if(step == 0):
            #select a drone
            units = obs.observation["screen"][_UNIT_TYPE]
            unit_y, unit_x = (units == _DRONE).nonzero()
            target = [unit_x[0], unit_y[0]]
            return actions.FunctionCall(_SELECT_POINT, [_NOT_QUEUED, target])
        elif(step == 1):
            #find an unused geyser and build on it
            units = obs.observation["screen"][_UNIT_TYPE]
            unit_y, unit_x = (units == 342).nonzero()
            #only works for spawning in the bottom, need to figure out how to average location for placement
            point = [unit_x[1], unit_y[1]]
            return actions.FunctionCall(_BUILD_GAS, [_NOT_QUEUED, point])
        else:
            return actions.FunctionCall(actions.FUNCTIONS.no_op.id, [])
        
    def train_Drone(step, obs):
        if step == 0:
            #select a larva
            units = obs.observation["screen"][_UNIT_TYPE]
            unit_y, unit_x = (units == _LARVA).nonzero()
            target = [unit_x[0], unit_y[0]]
            return actions.FunctionCall(_SELECT_POINT, [_NOT_QUEUED, target])
        elif step == 1:
            #morph to a drone
            return actions.FunctionCall(_TRAIN_DRONE, [_NOT_QUEUED])
        else:
            return actions.FunctionCall(actions.FUNCTIONS.no_op.id, [])
        
    def train_Queen(step, obs):
        if self.pool_flag == False:
            #if no pool is built redirect to building it instead
            self.build_Spawning_Pool(step, 0, obs)
        if step == 0:
            #select a hatchery
            units = obs.observation["screen"][_UNIT_TYPE]
            unit_y, unit_x = (units == _HATCHERY).nonzero()
            target = [unit_x[0], unit_y[0]]
            return actions.FunctionCall(_SELECT_POINT, [_NOT_QUEUED, target])
        elif step == 1:
            #build a queen
            return actions.FunctionCall(_TRAIN_QUEEN, [_NOT_QUEUED])
        else:
            return actions.FunctionCall(actions.FUNCTIONS.no_op.id, [])
        
    def train_Overlord(step, obs):
        if step == 0:
            #select a larva for the first step
            units = obs.observation["screen"][_UNIT_TYPE]
            unit_y, unit_x = (units == _LARVA).nonzero()
            target = [unit_x[0], unit_y[0]]
            return actions.FunctionCall(_SELECT_POINT, [_NOT_QUEUED, target])
        elif step == 1:
            #second step is train the overlord
            return actions.FunctionCall(_TRAIN_OVERLORD, [_NOT_QUEUED])
        else:
            return actions.FunctionCall(actions.FUNCTIONS.no_op.id, [])

    def build_Spawning_Pool(step, drone_id, obs):
        if(step == 0):
            #step on is selecting a dron to build with
            units = obs.observation["screen"][_UNIT_TYPE]
            unit_y, unit_x = (units == _DRONE).nonzero()
            #grab the first drone for now
            target = [unit_x[0], unit_y[0]]
            return actions.FunctionCall(_SELECT_POINT, [_NOT_QUEUED, target])
        elif(step == 1):
            #then build the pool
            units = obs.observation["screen"][_UNIT_TYPE]
            unit_y, unit_x = (units == _HATCHERY).nonzero()
            #location is just left of the nearest hatchery
            point = [unit_x[0]-3, unit_y[0]]
            self.pool_flag = True
            return actions.FunctionCall(_BUILD_POOL, [_NOT_QUEUED, point])
        else:
            return actions.FunctionCall(actions.FUNCTIONS.no_op.id, [])
        


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
        return [0,0]

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

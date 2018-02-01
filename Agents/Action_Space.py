'''
This contains a class designed to limit the action space for training purposes,
as well as the functions needed to exicute the actions allowed in this space.
'''
class Action_Space:

    # define the units and their actions
    valid_units = {126: ("Move_screen", "Effect_InjectLarva_screen"), #queen
       104: ("Move_screen", "Harvest_Gather_screen", "Build_Hatchery_screen", "Build_SpawningPool_screen"), #drone
       151: ("Train_Drone_quick", "Train_Overlord_quick"), #larva
       86: ("Train_Queen_quick")}  # hatchery
    
    def __init__(self):
        return

    # compare the provided ID number to the ID of the units allowed
    def get_actions(self, unit_id):
        # return the valid actions for the given unit 
        if unit_id in self.valid_units:
            return self.valid_units[unit_id]
        return "Unit not defined in action space"


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
def train_Drone(larva_id):
    return
def train_Queen(hatch_id):
    return
# I was thinking thats since you only need overlords when supply capped this function might be better as part of train_drone
# the same as the train queen tests for the spawning pool
def train_Overlord(larva_id):
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

if __name__ == '__main__':
	main()

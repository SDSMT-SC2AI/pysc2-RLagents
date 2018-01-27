
class Action_Space:
    def __init__(self):
        return

    #compare the provided ID number to the ID of the units allowed
    def get_actions(self, unit_id):
        id = unit_id
        #define the units and their actions
        valid_units = [(126, ("Move_screen", "Effect_InjectLarva_screen")), #queen
               (104, ("Move_screen", "Harvest_Gather_screen", "Build_Hatchery_screen", "Build_SpawningPool_screen")), #drone
               (151, ("Train_Drone_quick", "Train_Overlord_quick")), #larva
               (86), ("Train_Queen_quick")]  # hatchery
        num_units = len(valid_units)
        #compare the ID provided with the allowed IDS
        for x in range(num_units):
            if(id == valid_units[x][0]):
                #If an ID is mathced return the corrasponding action vector
                return valid_units[x][1]
           
# testing and debug function
def main():
    t1 = Action_Space
    print (t1.get_actions(t1, 151))

if __name__ == '__main__':
	main()

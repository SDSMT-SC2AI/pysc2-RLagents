
class Action_Space:

    #the unit ID
    id;


    def __init__(self):
        return
    def get_actions(self, unit_id):
        id = unit_id
        valid_units = [(126, ("move", "inject_larva")), #queen
               (104, ("move", "build_hatchery", "build_spawning_pool")), #drone
               (151, ("morph_drone", "morph_overlord")), #larva
               (86), ("build_queen")]  # hatchery
        #compare the ID provided with the allowed IDS
        for x in range(4):
            if(id == valid_units[x][0]):
                #If an ID is mathced return the corrasponding action vector
                return valid_units[x][1]
           
# testing and debug function
def main():
    t1 = Action_Space
    print (t1.get_actions(t1, 151))

if __name__ == '__main__':
	main()

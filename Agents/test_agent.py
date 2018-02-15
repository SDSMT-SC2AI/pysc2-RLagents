'''
An agent for testing the action space class 
Example usage:
python -m pysc2.bin.agent --map AbyssalReef --agent test_agent.TestAgent --agent_race Z 
'''
import Action_Space
from pysc2.agents import base_agent
from pysc2.lib import actions


_SELECT_ARMY = actions.FUNCTIONS.select_army.id
_NOT_QUEUED = [0]


class TestAgent(base_agent.BaseAgent):
    build_step = -1
    drone = True
    t1 = Action_Space.Action_Space()
    
    def step(self, obs):
        super(TestAgent, self).step(obs)

        if self.drone == True:
            self.t1.train_Drone(obs)
            self.drone = False

        return self.t1.action_step()



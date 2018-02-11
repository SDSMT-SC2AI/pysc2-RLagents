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
    def step(self, obs):
        super(TestAgent, self).step(obs)
        t1 = Action_Space.Action_Space
        
        self.build_step += 1
        if(self.drone & self.build_step < 2):
            return t1.build_Gas_Gyser(self.build_step, 0, obs)
        time.sleep(5)
        if(self.drone):
            self.build_step = 1
            self.drone = False
        return t1.train_Drone(self.build_step, obs)



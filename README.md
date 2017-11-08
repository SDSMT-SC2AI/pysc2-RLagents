# pysc2-RLagents
Notes and scripts for SC2LE released by DeepMind and Blizzard, more details [here](https://github.com/deepmind/pysc2).

## Important Links

[Original SC2LE Paper](https://deepmind.com/documents/110/sc2le.pdf)

[DeepMind blog post](https://deepmind.com/blog/deepmind-and-blizzard-open-starcraft-ii-ai-research-environment/)

[Blizzard blog post](http://us.battle.net/sc2/en/blog/20944009)

[PySC2 repo](https://github.com/deepmind/pysc2)

[Blizzard's SC2 API](https://github.com/Blizzard/s2client-api)

[Blizzard's SC2 API Protocol](https://github.com/Blizzard/s2client-proto)

[Python library for SC2 API Protocol](https://pypi.python.org/pypi/s2clientprotocol/)

## Work by others

Chris' blog post and repo

<http://chris-chris.ai/2017/08/30/pysc2-tutorial1/>

<https://github.com/chris-chris/pysc2-examples>

Siraj's Youtube tutorial and accompanying code

<https://www.youtube.com/watch?v=URWXG5jRB-A&feature=youtu.be>

<https://github.com/llSourcell/A-Guide-to-DeepMinds-StarCraft-AI-Environment>

Steven's Medium articles for a simple hardcoded agent and one based on Q-tables

<https://chatbotslife.com/building-a-basic-pysc2-agent-b109cde1477c>

<https://chatbotslife.com/building-a-smart-pysc2-agent-cdc269cb095d>

pekaalto's work on adapting OpenAI's gym environment to SC2LE and an implementation of the FullyConv algorithm plus results on three minigames

<https://github.com/pekaalto/sc2atari>

Arthur Juliani's posts and repo for RL agents

Not SC2LE but mentioned here because my agent script was built on Juliani's A3C implementation.

<https://medium.com/emergent-future/simple-reinforcement-learning-with-tensorflow-part-8-asynchronous-actor-critic-agents-a3c-c88f72a5e9f2>
<https://github.com/awjuliani/DeepRL-Agents>

Let me know if anyone else is also working on this and I'll add a link here!

## Notes

Contains general notes on working with SC2LE.

### Total Action Space

The entire unfiltered action space for an SC2LE agent.

It contains 524 base actions / functions with 101938719 possible actions given a minimap_resolution of (64, 64) and screen_resolution of (84, 84).

### List of Action Argument Types

The entire list of action argument types for use in the actions / functions.

It contains 13 argument types with descriptions.

### Running an Agent

Notes on running an agent in the pysc2.env.sc2_env.SC2Env environment. In particular, showing details and brief descriptions of the TimeStep object (observation) fed to the step function of an agent or returned from calling the step function of an environment.

## ResearchLog

Contains notes on developing RL agents for SC2LE.

## Agents

Contains a script that trains an A3C agent for the DefeatRoaches minigame.
 
"""Define the mini game map configs. These are maps made by Deepmind."""

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

from pysc2.maps import lib

class ExampleMaps(lib.Map):
  directory = "mini_games"
  players = 1
  score_index = 0
  game_steps_per_episode = 0
  step_mul = 8

maps = [
  "SpreadCreep",  # 120s
]

for name in maps:
  globals()[name] = type(name, (ExampleMaps,), dict(filename=name))

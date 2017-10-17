"""Scripted agents."""

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import numpy

from pysc2.agents import base_agent
from pysc2.lib import actions
from pysc2.lib import features

import random


_VISIBILITY_MAP = features.MINIMAP_FEATURES.visibility_map.index
_PLAYER_RELATIVE = features.MINIMAP_FEATURES.player_relative.index
_PLAYER_FRIENDLY = 1
_PLAYER_NEUTRAL = 3  # beacon/minerals
_PLAYER_HOSTILE = 4
_SELECTED = features.SCREEN_FEATURES.selected.index

_NO_OP = actions.FUNCTIONS.no_op.id
_MOVE_SCREEN = actions.FUNCTIONS.Move_screen.id
_ATTACK_SCREEN = actions.FUNCTIONS.Attack_screen.id
_ATTACK_MINIMAP = actions.FUNCTIONS.Attack_minimap.id
_SELECT_ARMY = actions.FUNCTIONS.select_army.id
_SELECT_POINT = actions.FUNCTIONS.select_point.id

_CONTROL_GROUP_SET = 1
_CONTROL_GROUP_RECALL = 0

_SELECT_CONTROL_GROUP = actions.FUNCTIONS.select_control_group.id

_NOT_QUEUED = [0]
_SELECT_ALL = [0]

class FindAndDefeatZerglings(base_agent.BaseAgent):
  """An agent specifically for solving the CollectMineralShards map."""

  offset_x = 20
  offset_y = 15
  
  def step(self, obs):
    super(FindAndDefeatZerglings, self).step(obs)
    if _ATTACK_MINIMAP in obs.observation["available_actions"]:
      player_relative = obs.observation["minimap"][_PLAYER_RELATIVE]
      enemy_y, enemy_x = (player_relative == _PLAYER_HOSTILE).nonzero()
      if not enemy_y.any():
        visibility_map = obs.observation["minimap"][_VISIBILITY_MAP][self.offset_x:-self.offset_x, self.offset_y:-self.offset_y]
        visibility_y, visibility_x = (visibility_map == 0).nonzero()
        if not visibility_y.any():
          return actions.FunctionCall(_NO_OP, [])
        index = [0]
        target = [visibility_x[index] + self.offset_x, visibility_y[index] + self.offset_y]
      else:
        index = numpy.argmax(enemy_y)
        target = [enemy_x[index], enemy_y[index]]
      return actions.FunctionCall(_ATTACK_MINIMAP, [_NOT_QUEUED, target])
    elif _SELECT_ARMY in obs.observation["available_actions"]:
      return actions.FunctionCall(_SELECT_ARMY, [_SELECT_ALL])
    else:
      return actions.FunctionCall(_NO_OP, [])

    return actions.FunctionCall(_NO_OP, [])

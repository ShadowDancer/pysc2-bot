"""Scripted agents."""

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import numpy

from pysc2.agents import base_agent
from pysc2.lib import actions
from pysc2.lib import features

import random


_VISIBILITY_MAP = features.SCREEN_FEATURES.visibility_map.index
_PLAYER_RELATIVE = features.SCREEN_FEATURES.player_relative.index
_CREEP = features.SCREEN_FEATURES.creep.index
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

_BUILD_CREEP_TUMOR = actions.FUNCTIONS.Build_CreepTumor_screen.id

_NOT_QUEUED = [0]
_QUEUED = [1]
_SELECT_ALL = [0]

from random import randint


class SpreadCreep(base_agent.BaseAgent):
  """An agent specifically for solving the SpreadCreep map."""

  offset_x = 20
  offset_y = 15
  
  def step(self, obs):
    super(SpreadCreep, self).step(obs)
    if _BUILD_CREEP_TUMOR in obs.observation["available_actions"]:
      print(obs.observation["single_select"])
      creep_raw = obs.observation["screen"][_CREEP]

      creep = numpy.empty(creep_raw.shape)
      sizeX, sizeY = creep_raw.shape
      for x in range(sizeX):
        for y in range(sizeY):
          creep[y][x] = creep_raw[y][x].sum()
      
      creep_y, creep_x = (creep != 0).nonzero()
      if not creep_y.any():
        return actions.FunctionCall(_NO_OP, [])
      else:
        index = randint(0, len(creep_y)-1)
        target = [creep_x[index], creep_y[index]]
      return actions.FunctionCall(_BUILD_CREEP_TUMOR, [_QUEUED, target])
    elif _SELECT_ARMY in obs.observation["available_actions"]:
      return actions.FunctionCall(_SELECT_ARMY, [_SELECT_ALL])
    else:
      return actions.FunctionCall(_NO_OP, [])

    return actions.FunctionCall(_NO_OP, [])

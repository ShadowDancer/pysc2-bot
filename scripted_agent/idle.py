"""Scripted agents."""

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import numpy

from pysc2.agents import base_agent
from pysc2.lib import actions
from pysc2.lib import features

_NO_OP = actions.FUNCTIONS.no_op.id
class Idle(base_agent.BaseAgent):
  """An agent that does nothing."""

  def step(self, obs):
    super(Idle, self).step(obs)
    return actions.FunctionCall(_NO_OP, [])

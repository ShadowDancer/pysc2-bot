import sys

from pysc2.env import sc2_env
from pysc2.lib import actions
from pysc2.env import run_loop


from maps.my_maps import ExampleMaps

step_mul = 1
steps = 200000

from absl import flags
FLAGS = flags.FLAGS
flags.DEFINE_string('map', None, 'Map to play on.')

flags.DEFINE_string('agent', None, 'Name of agent.')

import re
def convert(name):
    s1 = re.sub('(.)([A-Z][a-z]+)', r'\1_\2', name)
    return re.sub('([a-z0-9])([A-Z])', r'\1_\2', s1).lower()

def main():
  if FLAGS.map == None:
    print('Specify map with --map switch.')
    exit()

  if FLAGS.agent == None:
    FLAGS.agent = FLAGS.map

  agent_module = __import__('scripted_agent.' + convert(FLAGS.agent), fromlist=[FLAGS.agent])
  agent_factory = getattr(agent_module, FLAGS.agent)
  agent = agent_factory()

  with sc2_env.SC2Env(
      map_name=FLAGS.map,
      step_mul=step_mul,
      visualize=True,
      game_steps_per_episode=steps * step_mul) as env:

    run_loop.run_loop([agent], env, steps)
	

if __name__ == '__main__':
  import sys
  FLAGS(sys.argv)
  main()

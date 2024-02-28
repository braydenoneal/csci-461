# main.py
# Main program for GOAP exploration.

import config
import planner
import worldmodel


def goap_main():
    model = worldmodel.WorldModel(config.world_state, config.goal_list, config.action_list)
    goap_planner = planner.Planner(model)
    goap_planner.run()


# Run if this script is the top level script
if __name__ == '__main__':
    goap_main()
    print('Simulation complete')

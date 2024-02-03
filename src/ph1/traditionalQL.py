import argparse
import os
import sys
from rlDocs.environment.environment import SumoEnvironment
from rlDocs.agents.eGreedy import EpsilonGreedy
from rlDocs.agents.qlAlgo import QLAgent

if "SUMO_HOME" in os.environ:
    tools = os.path.join(os.environ["SUMO_HOME"], "tools")
    sys.path.append(tools)
else:
    sys.exit("Please declare the environment variable 'SUMO_HOME'")

if __name__ == "__main__":

    prs = argparse.ArgumentParser(
        formatter_class=argparse.ArgumentDefaultsHelpFormatter, description="""Phase One Traditional Intersection Q-Learning"""
    )

    prs.add_argument(
        "-route",
        dest="route",
        type=str,
        default="C:/Users/gavin/PycharmProjects/applyingRLtoUTM/sumoDocs/ph1SUMO/routeFile.rou.xml",
        help="Route definition xml file.\n",
    )

    # Alpha is the learning rate for the Q - learning algorithm. It controls how much the Q-values are updated based on new information.
    # A higher learning rate means that the agent will be more sensitive to new information, but it may also result in more volatility
    # in the agent's behavior.
    prs.add_argument("-a", dest="alpha", type=float, default=0.1, required=False, help="Alpha learning rate.\n")

    # Gamma is the discount factor used in the Q - learning algorithm to balance the importance of immediate and future rewards.
    # A high gamma value means that the agent will give more importance to future rewards, while a low gamma value means that it will focus
    # more on immediate rewards.
    prs.add_argument("-g", dest="gamma", type=float, default=0.99, required=False, help="Gamma discount rate.\n")

    # Epsilon is the probability of choosing a random action instead of the action with the highest Q-value.It is used to balance exploration
    # and exploitation in the agent's behavior. A high epsilon value means that the agent will explore more, while a low epsilon value means that it will exploit more.
    prs.add_argument("-e", dest="epsilon", type=float, default=1.0, required=False, help="Epsilon.\n")

    # Min_epsilon is the minimum value that epsilon can take during the training process.It is used to ensure that the agent continues to explore even after it has
    # converged to a good policy.
    prs.add_argument("-me", dest="min_epsilon", type=float, default=0.0, required=False, help="Minimum epsilon.\n")

    # Decay is the decay rate for epsilon.It controls how quickly epsilon decreases over time.A high decay rate means that epsilon will decrease more slowly,
    # while a low decay rate means that it will decrease more quickly.
    prs.add_argument("-d", dest="decay", type=float, default=0.99, required=False, help="Epsilon decay.\n")

    # Min_green is the minimum duration for green lights in the traffic signal.
    prs.add_argument("-mingreen", dest="min_green", type=int, default=10, required=False, help="Minimum green time.\n")

    # Max_green is the maximum duration for green lights in the traffic signal.
    prs.add_argument("-maxgreen", dest="max_green", type=int, default=30, required=False, help="Maximum green time.\n")

    # GUI is a Boolean flag that indicates whether the application should run with a visualization on SUMO, a traffic simulator.
    prs.add_argument("-gui", action="store_true", default=False, help="Run with visualization on SUMO.\n")

    # Fixed is a Boolean flag that indicates whether the application should run with fixed timing traffic signals or adaptive timing traffic signals.
    prs.add_argument("-fixed", action="store_true", default=False, help="Run with fixed timing traffic signals.\n")

    # Seconds is the number of simulation seconds that the application should run for.
    prs.add_argument("-s", dest="seconds", type=int, default=1800, required=False,  help="Number of simulation seconds.\n")

    # Reward specifies the reward function to use during training.
    prs.add_argument("-r", dest="reward", type=str,  default="wait", required=False, help="Reward function: [-r queue] for average queue reward or [-r wait] for waiting time reward.\n",)

    # Runs specifies the number of training runs to perform.
    prs.add_argument("-runs", dest="runs", type=int, default=25, help="Number of runs.\n")
    args = prs.parse_args()
    out_xlsx = f"runs/QL25"

    env = SumoEnvironment(
        net_file="C:/Users/gavin/PycharmProjects/MScPhaseOne/sumoDocs/intro/networkFile.net.xml",
        route_file=args.route,
        out_xlsx_name=out_xlsx,
        use_gui=args.gui,
        num_seconds=args.seconds,
        min_green=args.min_green,
        max_green=args.max_green,
        sumo_warnings=False,

    )

    for run in range(1, args.runs + 1):
        initial_states = env.reset()
        ql_agents = {
            ts: QLAgent(
                starting_state=env.encode(initial_states[ts], ts),
                state_space=env.observation_space,
                action_space=env.action_space,
                alpha=args.alpha,
                gamma=args.gamma,
                exploration_strategy=EpsilonGreedy(
                    initial_epsilon=args.epsilon, min_epsilon=args.min_epsilon, decay=args.decay
                ),
            )
            for ts in env.ts_ids

        }

        done = {"__all__": False}
        infos = []

        if args.fixed:
            while not done["__all__"]:
                _, _, done, _ = env.step({})

        else:
            while not done["__all__"]:
                actions = {ts: ql_agents[ts].act() for ts in ql_agents.keys()}
                s, r, done, _ = env.step(action=actions)

                for agent_id in ql_agents.keys():
                    ql_agents[agent_id].learn(next_state=env.encode(s[agent_id], agent_id), reward=r[agent_id])

        env.save_xlsx(out_xlsx, run)
        env.close()


# Step #0.00: This indicates the current simulation step or time, which is 0.00 in this case.
# (0ms ?*RT. ?UPS, TraCI: 5ms, vehicles TOT 0 ACT 0 BUF 0): This part of the message provides additional information about the simulation. Here's what each part of it means:
# 0ms: The amount of time it took to complete the current simulation step in milliseconds.
# ?*RT: The real-time factor (RTF) of the simulation. This is the ratio of the simulated time to real time. If the RTF is 1.0, then the simulation is running in real time. If the RTF is greater than 1.0, then the simulation is running faster than real time. If the RTF is less than 1.0, then the simulation is running slower than real time. The ? in this case indicates that the RTF is unknown or not applicable.
# ?UPS: The number of simulation steps per second (UPS). The ? in this case indicates that the UPS is unknown or not applicable.
# TraCI: 5ms: The amount of time it took TraCI to process the current simulation step in milliseconds.
# vehicles TOT 0 ACT 0 BUF 0: Information about the number of vehicles in the simulation. In this case, there are 0 total vehicles, 0 active vehicles, and 0 buffered vehicles.
# Overall, this log entry provides information about the current state of the TraCI simulation, including the simulation time, simulation speed, and number of vehicles.

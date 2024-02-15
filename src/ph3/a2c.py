import argparse
import os
import sys

from rlDocs.environment.environment import SumoEnvironment
from stable_baselines3 import A2C
from stable_baselines3.common.vec_env import SubprocVecEnv, VecNormalize

if "SUMO_HOME" in os.environ:
    tools = os.path.join(os.environ["SUMO_HOME"], "tools")
    sys.path.append(tools)
else:
    sys.exit("Please declare the environment variable 'SUMO_HOME'")


def makeEnv(ranking):
    def _init():
        env = SumoEnvironment(
            net_file="C:/Users/gavin/PycharmProjects/SingleIntersectionAlgos/sumoDocs/networkFile.net.xml",
            route_file="C:/Users/gavin/PycharmProjects/applyingRLtoUTM/sumoDocs/ph2SUMO/staticWaves.rou.xml",
            out_xlsx_name="biasa2cresults/a2cSingle{}".format(ranking),
            use_gui=False,
            num_seconds=18000,
            # min_green=args.min_green,
            # max_green=args.max_green,
            sumo_warnings=False,
            single_agent=True,
            max_depart_delay=0)
        return env

    return _init


if __name__ == "__main__":
    prs = argparse.ArgumentParser(formatter_class=argparse.ArgumentDefaultsHelpFormatter, description="""Rush Hour A2C Intersection""")
    prs.add_argument("-method", dest="method", type=str, default="a2c", required=False, help="Method to run.\n")
    prs.add_argument("-a", dest="alpha", type=float, default=0.1, required=False, help="Alpha learning rate.\n")
    prs.add_argument("-g", dest="gamma", type=float, default=0.99, required=False, help="Gamma discount rate.\n")
    prs.add_argument("-e", dest="epsilon", type=float, default=1.0, required=False, help="Epsilon.\n")
    prs.add_argument("-me", dest="min_epsilon", type=float, default=0.0, required=False, help="Minimum epsilon.\n")
    prs.add_argument("-d", dest="decay", type=float, default=0.99, required=False, help="Epsilon decay.\n")
    prs.add_argument("-batch", dest="batch_size", type=int, default=128, required=False, help="Batch size.\n")
    prs.add_argument("-maxgrad", dest="max_grad_norm", type=float, default=0.5, required=False, help="Max Gradient Norm.\n")
    prs.add_argument("-vfc", dest="vfc_coef", type=float, default=0.5, required=False, help="VFC Coefficient.\n")
    prs.add_argument("-efc", dest="efc_coef", type=float, default=0.0, required=False, help="EFC Coefficient.\n")
    prs.add_argument("-cr", dest="clip_range", type=float, default=0.2, required=False, help="Clip range.\n")
    runs = 10  # Number of processes to use

    env = SubprocVecEnv([makeEnv(i) for i in range(runs)])
    env = VecNormalize(env, norm_obs=True, norm_reward=True)
    model = A2C(
        "MlpPolicy",
        env,
        gamma=0.99,
        learning_rate=0.0005,
        n_steps=5,
        verbose=0
    )

    model.learn(total_timesteps=1000000)
    # prs.add_argument("-mingreen", dest="min_green", type=int, default=10, required=False, help="Minimum green time.\n")
    # prs.add_argument("-maxgreen", dest="max_green", type=int, default=30, required=False, help="Maximum green time.\n")
    # prs.add_argument("-gui", action="store_true", default=True, help="Run with visualization on SUMO.\n")
    # prs.add_argument("-fixed", action="store_true", default=False, help="Run with fixed timing traffic signals.\n")
    # Simulation will run for a period of 5 hours
    # prs.add_argument("-s", dest="seconds", type=int, default=18000, required=False,
    #                  help="Number of simulation seconds.\n")
    # prs.add_argument(
    #     "-r",
    #     dest="reward",
    #     type=str,
    #     default="wait",
    #     required=False,
    #     help="Reward function: [-r queue] for average queue reward or [-r wait] for waiting time reward.\n",
    # )
    # prs.add_argument("-runs", dest="runs", type=int, default=50, help="Number of runs.\n")
    # args = prs.parse_args()
    # out_xlsx = f"dqnresults/gridTestQL"

    #
    # env = SumoEnvironment(
    #     net_file="C:/Users/gavin/PycharmProjects/SingleIntersectionAlgos/sumoDocs/networkFile.net.xml",
    #     route_file=args.route,
    #     out_xlsx_name=out_xlsx,
    #     use_gui=args.gui,
    #     num_seconds=args.seconds,
    #     min_green=args.min_green,
    #     max_green=args.max_green,
    #     sumo_warnings=False,
    #
    # )

    # for run in range(1, args.runs + 1):
    #     initial_states = env.reset()
    #     ql_agents = {
    #         ts: QLAgent(
    #             starting_state=env.encode(initial_states[ts], ts),
    #             state_space=env.observation_space,
    #             action_space=env.action_space,
    #             alpha=args.alpha,
    #             gamma=args.gamma,
    #             exploration_strategy=EpsilonGreedy(
    #                 initial_epsilon=args.epsilon, min_epsilon=args.min_epsilon, decay=args.decay
    #             ),
    #         )
    #         for ts in env.ts_ids
    #
    #     }
    #
    #     done = {"__all__": False}
    #     infos = []
    #
    #     if args.fixed:
    #         while not done["__all__"]:
    #             _, _, done, _ = env.step({})
    #
    #     else:
    #         while not done["__all__"]:
    #             actions = {ts: ql_agents[ts].act() for ts in ql_agents.keys()}
    #             s, r, done, _ = env.step(action=actions)
    #
    #             for agent_id in ql_agents.keys():
    #                 ql_agents[agent_id].learn(next_state=env.encode(s[agent_id], agent_id), reward=r[agent_id])
    #
    #     env.save_xlsx(out_xlsx, run)
    #     env.close()

# Step #0.00: This indicates the current simulation step or time, which is 0.00 in this case.
# (0ms ?*RT. ?UPS, TraCI: 5ms, vehicles TOT 0 ACT 0 BUF 0): This part of the message provides additional information about the simulation. Here's what each part of it means:
# 0ms: The amount of time it took to complete the current simulation step in milliseconds.
# ?*RT: The real-time factor (RTF) of the simulation. This is the ratio of the simulated time to real time. If the RTF is 1.0, then the simulation is running in real time. If the RTF is greater than 1.0, then the simulation is running faster than real time. If the RTF is less than 1.0, then the simulation is running slower than real time. The ? in this case indicates that the RTF is unknown or not applicable.
# ?UPS: The number of simulation steps per second (UPS). The ? in this case indicates that the UPS is unknown or not applicable.
# TraCI: 5ms: The amount of time it took TraCI to process the current simulation step in milliseconds.
# vehicles TOT 0 ACT 0 BUF 0: Information about the number of vehicles in the simulation. In this case, there are 0 total vehicles, 0 active vehicles, and 0 buffered vehicles.
# Overall, this log entry provides information about the current state of the TraCI simulation, including the simulation time, simulation speed, and number of vehicles.

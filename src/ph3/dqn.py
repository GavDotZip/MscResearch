import argparse
import os
import sys

from rlDocs.environment.environment import SumoEnvironment
from stable_baselines3 import DQN
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
            out_xlsx_name="taudqnresults/dqnSingle{}".format(ranking),
            use_gui=False,
            num_seconds=18000,
            sumo_warnings=False,
            single_agent=True,
            max_depart_delay=0)
        return env

    return _init


if __name__ == "__main__":
    prs = argparse.ArgumentParser(formatter_class=argparse.ArgumentDefaultsHelpFormatter, description="""Rush Hour DQN Intersection""")
    prs.add_argument("-method", dest="method", type=str, default="dqn", required=False, help="Method to run.\n")
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
    model = DQN(
        "MlpPolicy",
        env,
        gamma=0.99,
        learning_rate=0.0005,
        verbose=0
    )

    model.learn(total_timesteps=1000000)

# Step #0.00: This indicates the current simulation step or time, which is 0.00 in this case.
# (0ms ?*RT. ?UPS, TraCI: 5ms, vehicles TOT 0 ACT 0 BUF 0): This part of the message provides additional information about the simulation. Here's what each part of it means:
# 0ms: The amount of time it took to complete the current simulation step in milliseconds.
# ?*RT: The real-time factor (RTF) of the simulation. This is the ratio of the simulated time to real time. If the RTF is 1.0, then the simulation is running in real time. If the RTF is greater than 1.0, then the simulation is running faster than real time. If the RTF is less than 1.0, then the simulation is running slower than real time. The ? in this case indicates that the RTF is unknown or not applicable.
# ?UPS: The number of simulation steps per second (UPS). The ? in this case indicates that the UPS is unknown or not applicable.
# TraCI: 5ms: The amount of time it took TraCI to process the current simulation step in milliseconds.
# vehicles TOT 0 ACT 0 BUF 0: Information about the number of vehicles in the simulation. In this case, there are 0 total vehicles, 0 active vehicles, and 0 buffered vehicles.
# Overall, this log entry provides information about the current state of the TraCI simulation, including the simulation time, simulation speed, and number of vehicles.

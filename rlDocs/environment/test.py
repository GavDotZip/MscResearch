import argparse

import numpy as np
import traci


def _get_system_info(self):
    vehicles = self.sumo.vehicle.getIDList()
    speeds = [self.sumo.vehicle.getSpeed(vehicle) for vehicle in vehicles]
    co = [self.sumo.vehicle.getCOEmission(vehicle) for vehicle in vehicles]
    pmx = [traci.vehicle.getPMxEmission(vehicle) for vehicle in vehicles]
    nox = [traci.vehicle.getNOxEmission(vehicle) for vehicle in vehicles]
    fuel = [self.sumo.vehicle.getFuelConsumption(vehicle) for vehicle in vehicles]
    noise = [self.sumo.vehicle.getNoiseEmission(vehicle) for vehicle in vehicles]
    waiting_times = [self.sumo.vehicle.getWaitingTime(vehicle) for vehicle in vehicles]

    return {
        # In SUMO, a vehicle is considered halting if its speed is below 0.1 m/s
        "Waiting_Times": sum(waiting_times),
        "Total_Air_Pollution": sum(co) + sum(pmx) + sum(nox),
        "Fuel_Consumption": sum(fuel),
        "Noise_Pollution": sum(noise),
        "Mean_Speed": 0.0 if len(vehicles) == 0 else np.mean(speeds),
    }


if __name__ == "__main__":
    prs = argparse.ArgumentParser(formatter_class=argparse.ArgumentDefaultsHelpFormatter,
                                  description="""Rush Hour DQN Intersection""")
    prs.add_argument("-method", dest="method", type=str, default="dqn", required=False, help="Method to run.\n")
    prs.add_argument("-a", dest="alpha", type=float, default=0.1, required=False, help="Alpha learning rate.\n")
    prs.add_argument("-g", dest="gamma", type=float, default=0.99, required=False, help="Gamma discount rate.\n")
    prs.add_argument("-e", dest="epsilon", type=float, default=1.0, required=False, help="Epsilon.\n")
    prs.add_argument("-me", dest="min_epsilon", type=float, default=0.0, required=False, help="Minimum epsilon.\n")
    prs.add_argument("-d", dest="decay", type=float, default=0.99, required=False, help="Epsilon decay.\n")
    prs.add_argument("-batch", dest="batch_size", type=int, default=128, required=False, help="Batch size.\n")
    prs.add_argument("-maxgrad", dest="max_grad_norm", type=float, default=0.5, required=False,
                     help="Max Gradient Norm.\n")
    prs.add_argument("-cr", dest="clip_range", type=float, default=0.2, required=False, help="Clip range.\n")

    prs.add_argument("-vfc", dest="vfc_coef", type=float, default=0.5, required=False, help="VFC Coefficient.\n")
    prs.add_argument("-efc", dest="efc_coef", type=float, default=0.0, required=False, help="EFC Coefficient.\n")


if __name__ == "__main__":
    prs = argparse.ArgumentParser(formatter_class=argparse.ArgumentDefaultsHelpFormatter, description="""Rush Hour PPO Intersection""")
    prs.add_argument("-method", dest="method", type=str, default="ppo", required=False, help="Method to run.\n")
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
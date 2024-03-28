import logging
from multiprocessing import Process

from oprl.algos.sac import SAC
from oprl.configs.utils import create_logdir, parse_args
from oprl.env import make_env as _make_env
from oprl.utils.logger import FileLogger, Logger
from oprl.utils.run_training import run_training

logging.basicConfig(level=logging.INFO)

args = parse_args()


def make_env(seed: int):
    return _make_env(args.env, seed=seed)


env = make_env(seed=0)
STATE_DIM: int = env.observation_space.shape[0]
ACTION_DIM: int = env.action_space.shape[0]


# --------  Config params -----------

config = {
    "state_dim": STATE_DIM,
    "action_dim": ACTION_DIM,
    "num_steps": int(1_000_000),
    "eval_every": 2500,
    "device": args.device,
    "save_buffer": False,
    "visualise_every": 0,
    "estimate_q_every": 5000,
    "log_every": 1000,
}

# -----------------------------------


def make_algo(logger, seed):
    return SAC(
        state_dim=STATE_DIM,
        action_dim=ACTION_DIM,
        device=args.device,
        seed=seed,
        logger=logger,
    )


def make_logger(seed: int):
    log_dir = create_logdir(logdir="logs", algo="SAC", env=args.env, seed=seed)
    # TODO: add config here instead {}
    return FileLogger(log_dir, {})


if __name__ == "__main__":
    args = parse_args()

    if args.seeds == 1:
        run_training(make_algo, make_env, make_logger, config, 0)
    else:
        processes = []
        for seed in range(args.start_seed, args.start_seed + args.seeds):
            processes.append(
                Process(
                    target=run_training,
                    args=(make_algo, make_env, make_logger, config, seed),
                )
            )

        for i, p in enumerate(processes):
            p.start()
            print(f"Starting process {i}...")

        for p in processes:
            p.join()

    print("OK.")

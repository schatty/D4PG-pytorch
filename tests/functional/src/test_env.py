import pytest

from oprl.env import DMControlEnv

dm_control_envs = [
    "acrobot-swingup",
    "ball_in_cup-catch",
    "cartpole-balance",
    "cartpole-swingup",
    "cheetah-run",
    "finger-spin",
    "finger-turn_easy",
    "finger-turn_hard",
    "fish-upright",
    "fish-swim",
    "hopper-stand",
    "hopper-hop",
    "humanoid-stand",
    "humanoid-walk",
    "humanoid-run",
    "pendulum-swingup",
    "point_mass-easy",
    "reacher-easy",
    "reacher-hard",
    "swimmer-swimmer6",
    "swimmer-swimmer15",
    "walker-stand",
    "walker-walk",
    "walker-run",
]


@pytest.mark.parametrize("env_name", dm_control_envs)
def test_dm_control_envs(env_name: str):
    env = DMControlEnv(env_name, seed=0)
    obs, info = env.reset()
    assert obs.shape[0] == env.observation_space.shape[0]
    assert isinstance(info, dict), "Info is expected to be a dict"

    rand_action = env.sample_action()
    assert rand_action.ndim == 1

    next_obs, reward, terminated, truncated, info = env.step(rand_action)
    assert next_obs.ndim == 1, "Expected 1-dimensional array as observation"
    assert isinstance(reward, float), "Reward is epxected to be a single float value"
    assert isinstance(
        terminated, bool
    ), "Terminated is expected to be a single bool value"
    assert isinstance(
        truncated, bool
    ), "Truncated is expected to be a single bool value"
    assert isinstance(info, dict), "Info is expected to be a dict"

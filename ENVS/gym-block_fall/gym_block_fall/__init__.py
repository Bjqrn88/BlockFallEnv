from gym.envs.registration import register

register(
    id='block_fall-v0',
    entry_point='gym_block_fall.envs:block_fallEnv',
)

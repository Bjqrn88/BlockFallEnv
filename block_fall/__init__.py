from gym.envs.registration import register

register(
    id='block_fall-v0',
    entry_point='block_fall.envs:BlockFallEnv',
)
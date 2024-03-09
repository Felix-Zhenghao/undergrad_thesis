from __future__ import annotations

"""Temporary import to debug"""
from dataclasses import MISSING
from terrains.rough_env_cfg import ROUGH_TERRAINS_CFG

"""import the base class for configuring an environment"""
from omni.isaac.orbit.envs import RLTaskEnvCfg

"""import the classes needed to configure the scene, including articulations/terrains/lights/sensors"""
from omni.isaac.orbit.scene import InteractiveSceneCfg # CFG to serve as the base class for the whole scene containing various assets
from omni.isaac.orbit.assets import AssetBaseCfg # CFG to serve as the base class for every asset
from articulations.unitree_go1_cfg import UNITREE_GO1_CFG # CFG defining the robot - Unitree Go1
from omni.isaac.orbit.sensors import ContactSensorCfg, RayCasterCfg, patterns # CFG to enable the sensors in the scene
from omni.isaac.orbit.terrains import TerrainImporterCfg # CFG to import terrain in the scene
import omni.isaac.orbit.sim as sim_utils

"""import classes needed to configure the mdp"""
import mdp # import the task-specific mdp
from omni.isaac.orbit.managers import ObservationTermCfg as ObsTerm # CFG to define the observation terms for agents
from omni.isaac.orbit.managers import ObservationGroupCfg as ObsGroup # CFG to define groups of observation terms
from omni.isaac.orbit.managers import RandomizationTermCfg as RandTerm # CFG to define the randomization done to the env for Sim-to-real gap
from omni.isaac.orbit.utils.noise import AdditiveUniformNoiseCfg as Unoise # CFG to support noise sampling for randomizaiton
from omni.isaac.orbit.managers import RewardTermCfg as RewTerm # CFG to define the reward functions
from omni.isaac.orbit.managers import SceneEntityCfg # CFG to get access to the assets in the env
from omni.isaac.orbit.managers import TerminationTermCfg as DoneTerm # CFG to define whether the task is completed
from omni.isaac.orbit.managers import CurriculumTermCfg as CurrTerm # CFG to define the curriculum for the agent learing

"""Import the decorator"""
from omni.isaac.orbit.utils import configclass

class MySceneCfg(InteractiveSceneCfg):

    # Terrain
    terrain = TerrainImporterCfg(
        # If terrain type is generator, then you can define a terrian cfg using TerrainGeneratorCfg
        prim_path="/World/ground",
        terrain_type = "plane",
    )
    # terrain = TerrainImporterCfg(
    #     # If terrain type is generator, then you can define a terrian cfg using TerrainGeneratorCfg
    #     prim_path="/World/ground",
    #     terrain_type = "generator",
    #     # TO LEARN: How to define a TerrainGeneratorCfg
    #     terrain_generator = ROUGH_TERRAINS_CFG, # The defined TerrainGeneratorCfg
    #     max_init_terrain_level = 5, # TO LEARN
    #     collision_group = -1, # TO LEARN
    #     physics_material=sim_utils.RigidBodyMaterialCfg( 
    #         # TO LEARN 
    #         friction_combine_mode="multiply",
    #         restitution_combine_mode="multiply",
    #         static_friction=1.0,
    #         dynamic_friction=1.0,
    #     ),
    #     visual_material=sim_utils.MdlFileCfg(
    #         # TO LEARN
    #         mdl_path="{NVIDIA_NUCLEUS_DIR}/Materials/Base/Architecture/Shingles_01.mdl",
    #         project_uvw=True,
    #     ),
    #     debug_vis=False,
    # )


    # Articualtion
    # cfg_attacker,cfg_defender = UNITREE_GO1_CFG()
    # cfg_attacker.func("{ENV_REGEX_NS}/Robot_Attacker",cfg_attacker)
    # cfg_defender.func("{ENV_REGEX_NS}/Robot_Defender",cfg_defender,translation=(distance,0.0,0.0),orientation=(0.0,0.0,1.0,0.0))

    robot: ArticulationCfg = UNITREE_GO1_CFG.replace(prim_path = "{ENV_REGEX_NS}/Robot")

    # Light
    light = AssetBaseCfg(
        prim_path="/World/light",
        spawn=sim_utils.DistantLightCfg(color=(0.75, 0.75, 0.75), intensity=3000.0),
    )
    sky_light = AssetBaseCfg(
        prim_path="/World/skyLight",
        spawn=sim_utils.DomeLightCfg(color=(0.13, 0.13, 0.13), intensity=1000.0),
    )

    
    # Sensor
    contact_forces = ContactSensorCfg(prim_path="{ENV_REGEX_NS}/Robot/.*", history_length=3, track_air_time=True)

    height_scanner = RayCasterCfg(
        prim_path = "{ENV_REGEX_NS}/Robot/trunk",
        offset = RayCasterCfg.OffsetCfg(pos=(0.0,0.0,20.0)),
        attach_yaw_only = True, # useful for ray-casting height map
        pattern_cfg = patterns.GridPatternCfg(resolution=0.1, size=[1.6,1.0]), # pattern is a sub-module for ray-casting patterns used by the ray-caster
        debug_vis = True,
        mesh_prim_paths=["/World/ground"],
    )


class ObservationsCfg:
    pass

class ActionCfg:
    joint_pos = mdp.JointPositionActionCfg(asset_name="robot", joint_names=[".*"], scale=0.5, use_default_offset=True)

class CommandsCfg:
    pass

class RewardsCfg:
    pass

class TerminationsCfg:
    pass

class RandomizationCfg:
    pass

class CurriculumCfg:
    pass

@configclass
class TomAndJerryEnvCfg(RLTaskEnvCfg):

    # scene
    scene: MySceneCfg = MySceneCfg(num_envs=4096,env_spacing=3.0)  
    
    """MDP Settings"""
    #actions
    actions: ActionCfg = ActionCfg()

    # reward
    rewards: RewardsCfg = RewardsCfg()

    # randomizaiton
    randomization: RandomizationCfg = RandomizationCfg()

    # curriculum
    curriculum: CurriculumCfg = CurriculumCfg()

    # command
    commands: CommandsCfg = CommandsCfg()

    # observations
    observations: ObservationsCfg = ObservationsCfg()

    # terminations
    terminations: TerminationsCfg = TerminationsCfg()

    # __post_init__ customization for this env
    def __post_init__(self):
        """Post initialization."""
        # self.scene.robot = UNITREE_GO1_CFG.replace("{ENV_REGEX_NS}/Robot")
        # general settings
        self.decimation = 4
        self.episode_length_s = 20.0
        # simulation settings
        self.sim.dt = 0.005 


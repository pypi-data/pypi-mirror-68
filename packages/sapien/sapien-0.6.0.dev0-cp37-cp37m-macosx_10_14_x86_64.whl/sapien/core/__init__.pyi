import sapien.core
from typing import *
from typing import Iterable as iterable
from typing import Iterator as iterator
from numpy import float64
_Shape = Tuple[int, ...]
import numpy
import sapien.core.pysapien
__all__  = [
"ActorBase",
"ActorDynamicBase",
"ActorBuilder",
"Actor",
"ActorStatic",
"ActorType",
"ArticulationBase",
"ArticulationDrivable",
"ArticulationBuilder",
"Articulation",
"ArticulationJointType",
"ArticulationType",
"CollisionGeometry",
"CameraSpec",
"CapsuleGeometry",
"BoxGeometry",
"CollisionShape",
"Contact",
"ConvexMeshGeometry",
"Drive",
"Engine",
"ISensor",
"IPxrRenderer",
"IPxrScene",
"ICamera",
"Input",
"JointBase",
"Joint",
"JointRecord",
"KinematicArticulation",
"KinematicJoint",
"KinematicJointFixed",
"KinematicJointSingleDof",
"KinematicJointRevolute",
"KinematicJointPrismatic",
"LinkBase",
"Link",
"KinematicLink",
"LinkBuilder",
"OptifuserCamera",
"OptifuserConfig",
"OptifuserController",
"OptifuserRenderer",
"PlaneGeometry",
"Pose",
"PxMaterial",
"PxrMaterial",
"Scene",
"SceneConfig",
"ShapeRecord",
"SolverType",
"SphereGeometry",
"URDFLoader",
"VisualRecord",
"__enable_gl",
"__enable_ptx",
"enable_default_gl3",
"enable_default_gl4",
"pysapien",
"DYNAMIC",
"FIX",
"GL_SHADER_ROOT",
"KINEMATIC",
"KINEMATIC_LINK",
"LINK",
"PGS",
"PRISMATIC",
"PTX_ROOT",
"REVOLUTE",
"SPHERICAL",
"STATIC",
"TGS",
"UNDEFINED",
"__GL_VERSION_DICT"
]
class ActorBase():
    def __repr__(self) -> str: ...
    def get_collision_shapes(self) -> List[CollisionShape]: ...
    def get_id(self) -> int: ...
    def get_name(self) -> str: ...
    def get_pose(self) -> Pose: ...
    def get_scene(self) -> Scene: ...
    def set_name(self, name: str) -> None: ...
    @property
    def col1(self) -> int:
        """
        :type: int
        """
    @property
    def col2(self) -> int:
        """
        :type: int
        """
    @property
    def col3(self) -> int:
        """
        :type: int
        """
    @property
    def id(self) -> int:
        """
        :type: int
        """
    @property
    def name(self) -> str:
        """
        :type: str
        """
    @name.setter
    def name(self, arg1: str) -> None:
        pass
    @property
    def pose(self) -> Pose:
        """
        :type: Pose
        """
    @property
    def type(self) -> ActorType:
        """
        :type: ActorType
        """
    pass
class ActorDynamicBase(ActorBase):
    def __repr__(self) -> str: ...
    def add_force_at_point(self, force: numpy.ndarray[float32], point: numpy.ndarray[float32]) -> None: ...
    def add_force_torque(self, force: numpy.ndarray[float32], torque: numpy.ndarray[float32]) -> None: ...
    def get_angular_velocity(self) -> numpy.ndarray[float32]: ...
    def get_cmass_local_pose(self) -> Pose: ...
    def get_collision_shapes(self) -> List[CollisionShape]: ...
    def get_id(self) -> int: ...
    def get_inertia(self) -> numpy.ndarray[float32]: ...
    def get_mass(self) -> float: ...
    def get_name(self) -> str: ...
    def get_pose(self) -> Pose: ...
    def get_scene(self) -> Scene: ...
    def get_velocity(self) -> numpy.ndarray[float32]: ...
    def set_damping(self, linear: float, angular: float) -> None: ...
    def set_name(self, name: str) -> None: ...
    @property
    def angular_velocity(self) -> numpy.ndarray[float32]:
        """
        :type: numpy.ndarray[float32]
        """
    @property
    def cmass_local_pose(self) -> Pose:
        """
        :type: Pose
        """
    @property
    def col1(self) -> int:
        """
        :type: int
        """
    @property
    def col2(self) -> int:
        """
        :type: int
        """
    @property
    def col3(self) -> int:
        """
        :type: int
        """
    @property
    def id(self) -> int:
        """
        :type: int
        """
    @property
    def inertia(self) -> numpy.ndarray[float32]:
        """
        :type: numpy.ndarray[float32]
        """
    @property
    def mass(self) -> float:
        """
        :type: float
        """
    @property
    def name(self) -> str:
        """
        :type: str
        """
    @name.setter
    def name(self, arg1: str) -> None:
        pass
    @property
    def pose(self) -> Pose:
        """
        :type: Pose
        """
    @property
    def type(self) -> ActorType:
        """
        :type: ActorType
        """
    @property
    def velocity(self) -> numpy.ndarray[float32]:
        """
        :type: numpy.ndarray[float32]
        """
    pass
class ActorBuilder():
    def add_box_shape(self, pose: Pose = Pose([0, 0, 0], [1, 0, 0, 0]), size: numpy.ndarray[float32] = array([1., 1., 1.], dtype=float32), material: PxMaterial = None, density: float = 1000) -> None: 
        """
        add_box_shape(self: sapien.core.pysapien.ActorBuilder, pose: sapien.core.pysapien.Pose = Pose([0, 0, 0], [1, 0, 0, 0]), size: numpy.ndarray[float32] = array([1., 1., 1.], dtype=float32), material: sapien.core.pysapien.PxMaterial = None, density: float = 1000) -> None
        """
    def add_box_visual(self, pose: Pose = Pose([0, 0, 0], [1, 0, 0, 0]), size: numpy.ndarray[float32] = array([1., 1., 1.], dtype=float32), color: numpy.ndarray[float32] = array([1., 1., 1.], dtype=float32), name: str = '') -> None: 
        """
        add_box_visual(self: sapien.core.pysapien.ActorBuilder, pose: sapien.core.pysapien.Pose = Pose([0, 0, 0], [1, 0, 0, 0]), size: numpy.ndarray[float32] = array([1., 1., 1.], dtype=float32), color: numpy.ndarray[float32] = array([1., 1., 1.], dtype=float32), name: str = '') -> None
        """
    def add_box_visual_complex(self, pose: Pose = Pose([0, 0, 0], [1, 0, 0, 0]), size: numpy.ndarray[float32] = array([1., 1., 1.], dtype=float32), material: PxrMaterial = PxrMaterial(), name: str = '') -> None: 
        """
        add_box_visual_complex(self: sapien.core.pysapien.ActorBuilder, pose: sapien.core.pysapien.Pose = Pose([0, 0, 0], [1, 0, 0, 0]), size: numpy.ndarray[float32] = array([1., 1., 1.], dtype=float32), material: sapien.core.pysapien.PxrMaterial = PxrMaterial(), name: str = '') -> None
        """
    def add_capsule_shape(self, pose: Pose = Pose([0, 0, 0], [1, 0, 0, 0]), radius: float = 1, half_length: float = 1, material: PxMaterial = None, density: float = 1000) -> None: 
        """
        add_capsule_shape(self: sapien.core.pysapien.ActorBuilder, pose: sapien.core.pysapien.Pose = Pose([0, 0, 0], [1, 0, 0, 0]), radius: float = 1, half_length: float = 1, material: sapien.core.pysapien.PxMaterial = None, density: float = 1000) -> None
        """
    def add_capsule_visual(self, pose: Pose = Pose([0, 0, 0], [1, 0, 0, 0]), radius: float = 1, half_length: float = 1, color: numpy.ndarray[float32] = array([1., 1., 1.], dtype=float32), name: str = '') -> None: 
        """
        add_capsule_visual(self: sapien.core.pysapien.ActorBuilder, pose: sapien.core.pysapien.Pose = Pose([0, 0, 0], [1, 0, 0, 0]), radius: float = 1, half_length: float = 1, color: numpy.ndarray[float32] = array([1., 1., 1.], dtype=float32), name: str = '') -> None
        """
    def add_capsule_visual_complex(self, pose: Pose = Pose([0, 0, 0], [1, 0, 0, 0]), radius: float = 1, half_length: float = 1, material: PxrMaterial = PxrMaterial(), name: str = '') -> None: 
        """
        add_capsule_visual_complex(self: sapien.core.pysapien.ActorBuilder, pose: sapien.core.pysapien.Pose = Pose([0, 0, 0], [1, 0, 0, 0]), radius: float = 1, half_length: float = 1, material: sapien.core.pysapien.PxrMaterial = PxrMaterial(), name: str = '') -> None
        """
    def add_collision_group(self, arg0: int, arg1: int, arg2: int) -> None: ...
    def add_convex_shape_from_file(self, filename: str, pose: Pose = Pose([0, 0, 0], [1, 0, 0, 0]), scale: numpy.ndarray[float32] = array([1., 1., 1.], dtype=float32), material: PxMaterial = None, density: float = 1000) -> None: 
        """
        add_convex_shape_from_file(self: sapien.core.pysapien.ActorBuilder, filename: str, pose: sapien.core.pysapien.Pose = Pose([0, 0, 0], [1, 0, 0, 0]), scale: numpy.ndarray[float32] = array([1., 1., 1.], dtype=float32), material: sapien.core.pysapien.PxMaterial = None, density: float = 1000) -> None
        """
    def add_multiple_convex_shapes_from_file(self, filename: str, pose: Pose = Pose([0, 0, 0], [1, 0, 0, 0]), scale: numpy.ndarray[float32] = array([1., 1., 1.], dtype=float32), material: PxMaterial = None, density: float = 1000) -> None: 
        """
        add_multiple_convex_shapes_from_file(self: sapien.core.pysapien.ActorBuilder, filename: str, pose: sapien.core.pysapien.Pose = Pose([0, 0, 0], [1, 0, 0, 0]), scale: numpy.ndarray[float32] = array([1., 1., 1.], dtype=float32), material: sapien.core.pysapien.PxMaterial = None, density: float = 1000) -> None
        """
    def add_sphere_shape(self, pose: Pose = Pose([0, 0, 0], [1, 0, 0, 0]), radius: float = 1, material: PxMaterial = None, density: float = 1000) -> None: 
        """
        add_sphere_shape(self: sapien.core.pysapien.ActorBuilder, pose: sapien.core.pysapien.Pose = Pose([0, 0, 0], [1, 0, 0, 0]), radius: float = 1, material: sapien.core.pysapien.PxMaterial = None, density: float = 1000) -> None
        """
    def add_sphere_visual(self, pose: Pose = Pose([0, 0, 0], [1, 0, 0, 0]), radius: float = 1, color: numpy.ndarray[float32] = array([1., 1., 1.], dtype=float32), name: str = '') -> None: 
        """
        add_sphere_visual(self: sapien.core.pysapien.ActorBuilder, pose: sapien.core.pysapien.Pose = Pose([0, 0, 0], [1, 0, 0, 0]), radius: float = 1, color: numpy.ndarray[float32] = array([1., 1., 1.], dtype=float32), name: str = '') -> None
        """
    def add_sphere_visual_complex(self, pose: Pose = Pose([0, 0, 0], [1, 0, 0, 0]), radius: float = 1, material: PxrMaterial = PxrMaterial(), name: str = '') -> None: 
        """
        add_sphere_visual_complex(self: sapien.core.pysapien.ActorBuilder, pose: sapien.core.pysapien.Pose = Pose([0, 0, 0], [1, 0, 0, 0]), radius: float = 1, material: sapien.core.pysapien.PxrMaterial = PxrMaterial(), name: str = '') -> None
        """
    def add_visual_from_file(self, filename: str, pose: Pose = Pose([0, 0, 0], [1, 0, 0, 0]), scale: numpy.ndarray[float32] = array([1., 1., 1.], dtype=float32), name: str = '') -> None: 
        """
        add_visual_from_file(self: sapien.core.pysapien.ActorBuilder, filename: str, pose: sapien.core.pysapien.Pose = Pose([0, 0, 0], [1, 0, 0, 0]), scale: numpy.ndarray[float32] = array([1., 1., 1.], dtype=float32), name: str = '') -> None
        """
    def build(self, is_kinematic: bool = False, name: str = '') -> Actor: ...
    def build_static(self, name: str = '') -> ActorStatic: ...
    def get_shapes(self) -> List[ShapeRecord]: ...
    def get_visuals(self) -> List[VisualRecord]: ...
    def remove_all_shapes(self) -> None: ...
    def remove_all_visuals(self) -> None: ...
    def remove_shape_at(self, index: int) -> None: ...
    def remove_visual_at(self, index: int) -> None: ...
    def reset_collision_group(self) -> None: ...
    def set_collision_group(self, arg0: int, arg1: int, arg2: int) -> None: ...
    def set_mass_and_inertia(self, arg0: float, arg1: Pose, arg2: numpy.ndarray[float32]) -> None: ...
    def set_scene(self, arg0: Scene) -> None: ...
    pass
class Actor(ActorDynamicBase, ActorBase):
    def __repr__(self) -> str: ...
    def add_force_at_point(self, force: numpy.ndarray[float32], point: numpy.ndarray[float32]) -> None: ...
    def add_force_torque(self, force: numpy.ndarray[float32], torque: numpy.ndarray[float32]) -> None: ...
    def get_angular_velocity(self) -> numpy.ndarray[float32]: ...
    def get_cmass_local_pose(self) -> Pose: ...
    def get_collision_shapes(self) -> List[CollisionShape]: ...
    def get_id(self) -> int: ...
    def get_inertia(self) -> numpy.ndarray[float32]: ...
    def get_mass(self) -> float: ...
    def get_name(self) -> str: ...
    def get_pose(self) -> Pose: ...
    def get_scene(self) -> Scene: ...
    def get_velocity(self) -> numpy.ndarray[float32]: ...
    def lock_motion(self, x: bool = True, y: bool = True, z: bool = True, rx: bool = True, ry: bool = True, rz: bool = True) -> None: ...
    def pack(self) -> List[float]: ...
    def set_angular_velocity(self, arg0: numpy.ndarray[float32]) -> None: ...
    def set_damping(self, linear: float, angular: float) -> None: ...
    def set_name(self, name: str) -> None: ...
    def set_pose(self, pose: Pose) -> None: ...
    def set_solver_iterations(self, position: int, velocity: int = 1) -> None: ...
    def set_velocity(self, arg0: numpy.ndarray[float32]) -> None: ...
    def unpack(self, arg0: numpy.ndarray[float32]) -> None: ...
    @property
    def angular_velocity(self) -> numpy.ndarray[float32]:
        """
        :type: numpy.ndarray[float32]
        """
    @property
    def cmass_local_pose(self) -> Pose:
        """
        :type: Pose
        """
    @property
    def col1(self) -> int:
        """
        :type: int
        """
    @property
    def col2(self) -> int:
        """
        :type: int
        """
    @property
    def col3(self) -> int:
        """
        :type: int
        """
    @property
    def id(self) -> int:
        """
        :type: int
        """
    @property
    def inertia(self) -> numpy.ndarray[float32]:
        """
        :type: numpy.ndarray[float32]
        """
    @property
    def mass(self) -> float:
        """
        :type: float
        """
    @property
    def name(self) -> str:
        """
        :type: str
        """
    @name.setter
    def name(self, arg1: str) -> None:
        pass
    @property
    def pose(self) -> Pose:
        """
        :type: Pose
        """
    @property
    def type(self) -> ActorType:
        """
        :type: ActorType
        """
    @property
    def velocity(self) -> numpy.ndarray[float32]:
        """
        :type: numpy.ndarray[float32]
        """
    pass
class ActorStatic(ActorBase):
    def __repr__(self) -> str: ...
    def get_collision_shapes(self) -> List[CollisionShape]: ...
    def get_id(self) -> int: ...
    def get_name(self) -> str: ...
    def get_pose(self) -> Pose: ...
    def get_scene(self) -> Scene: ...
    def pack(self) -> List[float]: ...
    def set_name(self, name: str) -> None: ...
    def set_pose(self, pose: Pose) -> None: ...
    def unpack(self, arg0: numpy.ndarray[float32]) -> None: ...
    @property
    def col1(self) -> int:
        """
        :type: int
        """
    @property
    def col2(self) -> int:
        """
        :type: int
        """
    @property
    def col3(self) -> int:
        """
        :type: int
        """
    @property
    def id(self) -> int:
        """
        :type: int
        """
    @property
    def name(self) -> str:
        """
        :type: str
        """
    @name.setter
    def name(self, arg1: str) -> None:
        pass
    @property
    def pose(self) -> Pose:
        """
        :type: Pose
        """
    @property
    def type(self) -> ActorType:
        """
        :type: ActorType
        """
    pass
class ActorType():
    """
    Members:

      STATIC

      KINEMATIC

      DYNAMIC

      LINK

      KINEMATIC_LINK
    """
    def __init__(self, arg0: int) -> None: ...
    def __int__(self) -> int: ...
    @property
    def name(self) -> str:
        """
        (self: handle) -> str

        :type: str
        """
    DYNAMIC: sapien.core.pysapien.ActorType # value = ActorType.DYNAMIC
    KINEMATIC: sapien.core.pysapien.ActorType # value = ActorType.KINEMATIC
    KINEMATIC_LINK: sapien.core.pysapien.ActorType # value = ActorType.KINEMATIC_LINK
    LINK: sapien.core.pysapien.ActorType # value = ActorType.LINK
    STATIC: sapien.core.pysapien.ActorType # value = ActorType.STATIC
    __entries: dict # value = {'STATIC': (ActorType.STATIC, None), 'KINEMATIC': (ActorType.KINEMATIC, None), 'DYNAMIC': (ActorType.DYNAMIC, None), 'LINK': (ActorType.LINK, None), 'KINEMATIC_LINK': (ActorType.KINEMATIC_LINK, None)}
    __members__: dict # value = {'STATIC': ActorType.STATIC, 'KINEMATIC': ActorType.KINEMATIC, 'DYNAMIC': ActorType.DYNAMIC, 'LINK': ActorType.LINK, 'KINEMATIC_LINK': ActorType.KINEMATIC_LINK}
    pass
class ArticulationBase():
    def get_base_joints(self) -> List[JointBase]: ...
    def get_base_links(self) -> List[LinkBase]: ...
    def get_name(self) -> str: ...
    def get_pose(self) -> Pose: 
        """
        same as get_root_pose
        """
    def get_qacc(self) -> numpy.ndarray[float32]: ...
    def get_qf(self) -> numpy.ndarray[float32]: ...
    def get_qlimits(self) -> numpy.ndarray[float32]: ...
    def get_qpos(self) -> numpy.ndarray[float32]: ...
    def get_qvel(self) -> numpy.ndarray[float32]: ...
    def get_root_pose(self) -> Pose: ...
    def set_name(self, name: str) -> None: ...
    def set_pose(self, pose: Pose) -> None: 
        """
        same as set_root_pose
        """
    def set_qacc(self, qacc: numpy.ndarray[float32]) -> None: ...
    def set_qf(self, qf: numpy.ndarray[float32]) -> None: ...
    def set_qlimits(self, qlimits: numpy.ndarray[float32]) -> None: ...
    def set_qpos(self, qpos: numpy.ndarray[float32]) -> None: ...
    def set_qvel(self, qvel: numpy.ndarray[float32]) -> None: ...
    def set_root_pose(self, pose: Pose) -> None: ...
    @property
    def dof(self) -> int:
        """
        :type: int
        """
    @property
    def name(self) -> str:
        """
        :type: str
        """
    @name.setter
    def name(self, arg1: str) -> None:
        pass
    @property
    def pose(self) -> Pose:
        """
        same as get_root_pose()

        :type: Pose
        """
    @property
    def type(self) -> ArticulationType:
        """
        :type: ArticulationType
        """
    pass
class ArticulationDrivable(ArticulationBase):
    def get_base_joints(self) -> List[JointBase]: ...
    def get_base_links(self) -> List[LinkBase]: ...
    def get_drive_target(self) -> numpy.ndarray[float32]: ...
    def get_name(self) -> str: ...
    def get_pose(self) -> Pose: 
        """
        same as get_root_pose
        """
    def get_qacc(self) -> numpy.ndarray[float32]: ...
    def get_qf(self) -> numpy.ndarray[float32]: ...
    def get_qlimits(self) -> numpy.ndarray[float32]: ...
    def get_qpos(self) -> numpy.ndarray[float32]: ...
    def get_qvel(self) -> numpy.ndarray[float32]: ...
    def get_root_pose(self) -> Pose: ...
    def set_drive_target(self, drive_target: numpy.ndarray[float32]) -> None: ...
    def set_name(self, name: str) -> None: ...
    def set_pose(self, pose: Pose) -> None: 
        """
        same as set_root_pose
        """
    def set_qacc(self, qacc: numpy.ndarray[float32]) -> None: ...
    def set_qf(self, qf: numpy.ndarray[float32]) -> None: ...
    def set_qlimits(self, qlimits: numpy.ndarray[float32]) -> None: ...
    def set_qpos(self, qpos: numpy.ndarray[float32]) -> None: ...
    def set_qvel(self, qvel: numpy.ndarray[float32]) -> None: ...
    def set_root_pose(self, pose: Pose) -> None: ...
    @property
    def dof(self) -> int:
        """
        :type: int
        """
    @property
    def name(self) -> str:
        """
        :type: str
        """
    @name.setter
    def name(self, arg1: str) -> None:
        pass
    @property
    def pose(self) -> Pose:
        """
        same as get_root_pose()

        :type: Pose
        """
    @property
    def type(self) -> ArticulationType:
        """
        :type: ArticulationType
        """
    pass
class ArticulationBuilder():
    def build(self, fix_base: bool = False) -> Articulation: ...
    def build_kinematic(self) -> KinematicArticulation: ...
    def create_link_builder(self, parent: LinkBuilder = None) -> LinkBuilder: ...
    def get_link_builders(self) -> List[LinkBuilder]: ...
    def get_scene(self) -> Scene: ...
    def set_scene(self, scene: Scene) -> None: ...
    pass
class Articulation(ArticulationDrivable, ArticulationBase):
    def compute_adjoint_matrix(self, source_link_ik: int, target_link_id: int) -> numpy.ndarray[float32, _Shape[6, 6]]: ...
    def compute_cartesian_diff_ik(self, world_velocity: numpy.ndarray[float32, _Shape[6, 1]], commanded_link_id: int, active_joint_ids: List[int] = []) -> numpy.ndarray[float32, _Shape[m, 1]]: ...
    def compute_forward_dynamics(self, arg0: numpy.ndarray[float32]) -> numpy.ndarray[float32]: ...
    def compute_inverse_dynamics(self, arg0: numpy.ndarray[float32]) -> numpy.ndarray[float32]: ...
    def compute_jacobian(self) -> numpy.ndarray[float32, _Shape[m, n]]: ...
    def compute_manipulator_inertia_matrix(self) -> numpy.ndarray[float32, _Shape[m, n]]: ...
    def compute_passive_force(self, gravity: bool = True, coriolis_and_centrifugal: bool = True, external: bool = True) -> numpy.ndarray[float32]: ...
    def compute_spatial_twist_jacobian(self) -> numpy.ndarray[float32, _Shape[m, n]]: ...
    def compute_transformation_matrix(self, source_link_id: int, target_link_id: int) -> numpy.ndarray[float32, _Shape[4, 4]]: ...
    def compute_twist_diff_ik(self, spatial_twist: numpy.ndarray[float32, _Shape[6, 1]], commanded_link_id: int, active_joint_ids: List[int] = []) -> numpy.ndarray[float32, _Shape[m, 1]]: ...
    def compute_world_cartesian_jacobian(self) -> numpy.ndarray[float32, _Shape[m, n]]: ...
    def get_active_joints(self) -> List[Joint]: ...
    def get_base_joints(self) -> List[JointBase]: ...
    def get_base_links(self) -> List[LinkBase]: ...
    def get_drive_target(self) -> numpy.ndarray[float32]: ...
    def get_joints(self) -> List[Joint]: ...
    def get_links(self) -> List[Link]: ...
    def get_name(self) -> str: ...
    def get_pose(self) -> Pose: 
        """
        same as get_root_pose
        """
    def get_qacc(self) -> numpy.ndarray[float32]: ...
    def get_qf(self) -> numpy.ndarray[float32]: ...
    def get_qlimits(self) -> numpy.ndarray[float32]: ...
    def get_qpos(self) -> numpy.ndarray[float32]: ...
    def get_qvel(self) -> numpy.ndarray[float32]: ...
    def get_root_pose(self) -> Pose: ...
    def pack(self) -> List[float]: ...
    def set_drive_target(self, drive_target: numpy.ndarray[float32]) -> None: ...
    def set_name(self, name: str) -> None: ...
    def set_pose(self, pose: Pose) -> None: 
        """
        same as set_root_pose
        """
    def set_qacc(self, qacc: numpy.ndarray[float32]) -> None: ...
    def set_qf(self, qf: numpy.ndarray[float32]) -> None: ...
    def set_qlimits(self, qlimits: numpy.ndarray[float32]) -> None: ...
    def set_qpos(self, qpos: numpy.ndarray[float32]) -> None: ...
    def set_qvel(self, qvel: numpy.ndarray[float32]) -> None: ...
    def set_root_angular_velocity(self, vel: numpy.ndarray[float32]) -> None: ...
    def set_root_pose(self, pose: Pose) -> None: ...
    def set_root_velocity(self, vel: numpy.ndarray[float32]) -> None: ...
    def unpack(self, arg0: numpy.ndarray[float32]) -> None: ...
    @property
    def dof(self) -> int:
        """
        :type: int
        """
    @property
    def name(self) -> str:
        """
        :type: str
        """
    @name.setter
    def name(self, arg1: str) -> None:
        pass
    @property
    def pose(self) -> Pose:
        """
        same as get_root_pose()

        :type: Pose
        """
    @property
    def type(self) -> ArticulationType:
        """
        :type: ArticulationType
        """
    pass
class ArticulationJointType():
    """
    Members:

      PRISMATIC

      REVOLUTE

      SPHERICAL

      FIX

      UNDEFINED
    """
    def __init__(self, arg0: int) -> None: ...
    def __int__(self) -> int: ...
    @property
    def name(self) -> str:
        """
        (self: handle) -> str

        :type: str
        """
    FIX: sapien.core.pysapien.ArticulationJointType # value = ArticulationJointType.FIX
    PRISMATIC: sapien.core.pysapien.ArticulationJointType # value = ArticulationJointType.PRISMATIC
    REVOLUTE: sapien.core.pysapien.ArticulationJointType # value = ArticulationJointType.REVOLUTE
    SPHERICAL: sapien.core.pysapien.ArticulationJointType # value = ArticulationJointType.SPHERICAL
    UNDEFINED: sapien.core.pysapien.ArticulationJointType # value = ArticulationJointType.UNDEFINED
    __entries: dict # value = {'PRISMATIC': (ArticulationJointType.PRISMATIC, None), 'REVOLUTE': (ArticulationJointType.REVOLUTE, None), 'SPHERICAL': (ArticulationJointType.SPHERICAL, None), 'FIX': (ArticulationJointType.FIX, None), 'UNDEFINED': (ArticulationJointType.UNDEFINED, None)}
    __members__: dict # value = {'PRISMATIC': ArticulationJointType.PRISMATIC, 'REVOLUTE': ArticulationJointType.REVOLUTE, 'SPHERICAL': ArticulationJointType.SPHERICAL, 'FIX': ArticulationJointType.FIX, 'UNDEFINED': ArticulationJointType.UNDEFINED}
    pass
class ArticulationType():
    """
    Members:

      DYNAMIC

      KINEMATIC
    """
    def __init__(self, arg0: int) -> None: ...
    def __int__(self) -> int: ...
    @property
    def name(self) -> str:
        """
        (self: handle) -> str

        :type: str
        """
    DYNAMIC: sapien.core.pysapien.ArticulationType # value = ArticulationType.DYNAMIC
    KINEMATIC: sapien.core.pysapien.ArticulationType # value = ArticulationType.KINEMATIC
    __entries: dict # value = {'DYNAMIC': (ArticulationType.DYNAMIC, None), 'KINEMATIC': (ArticulationType.KINEMATIC, None)}
    __members__: dict # value = {'DYNAMIC': ArticulationType.DYNAMIC, 'KINEMATIC': ArticulationType.KINEMATIC}
    pass
class CollisionGeometry():
    pass
class CameraSpec():
    def get_model_matrix(self) -> numpy.ndarray[float32]: ...
    def get_projection_matrix(self) -> numpy.ndarray[float32]: ...
    def lookAt(self, direction: numpy.ndarray[float32], up: numpy.ndarray[float32]) -> None: ...
    def set_position(self, position: numpy.ndarray[float32]) -> None: ...
    def set_rotation(self, rotation: numpy.ndarray[float32]) -> None: ...
    @property
    def aspect(self) -> float:
        """
        :type: float
        """
    @aspect.setter
    def aspect(self, arg0: float) -> None:
        pass
    @property
    def far(self) -> float:
        """
        :type: float
        """
    @far.setter
    def far(self, arg0: float) -> None:
        pass
    @property
    def name(self) -> str:
        """
        :type: str
        """
    @name.setter
    def name(self, arg0: str) -> None:
        pass
    @property
    def near(self) -> float:
        """
        :type: float
        """
    @near.setter
    def near(self, arg0: float) -> None:
        pass
    @property
    def position(self) -> numpy.ndarray[float32]:
        """
        :type: numpy.ndarray[float32]
        """
    @property
    def rotation(self) -> numpy.ndarray[float32]:
        """
        :type: numpy.ndarray[float32]
        """
    pass
class CapsuleGeometry(CollisionGeometry):
    @property
    def half_length(self) -> float:
        """
        :type: float
        """
    @property
    def radius(self) -> float:
        """
        :type: float
        """
    pass
class BoxGeometry(CollisionGeometry):
    @property
    def half_lengths(self) -> numpy.ndarray[float32]:
        """
        :type: numpy.ndarray[float32]
        """
    pass
class CollisionShape():
    @property
    def box_geometry(self) -> BoxGeometry:
        """
        :type: BoxGeometry
        """
    @property
    def capsule_geometry(self) -> CapsuleGeometry:
        """
        :type: CapsuleGeometry
        """
    @property
    def convex_mesh_geometry(self) -> ConvexMeshGeometry:
        """
        :type: ConvexMeshGeometry
        """
    @property
    def plane_geometry(self) -> PlaneGeometry:
        """
        :type: PlaneGeometry
        """
    @property
    def pose(self) -> Pose:
        """
        :type: Pose
        """
    @property
    def sphere_geometry(self) -> SphereGeometry:
        """
        :type: SphereGeometry
        """
    @property
    def type(self) -> str:
        """
        :type: str
        """
    pass
class Contact():
    def __repr__(self) -> str: ...
    @property
    def actor1(self) -> ActorBase:
        """
        :type: ActorBase
        """
    @property
    def actor2(self) -> ActorBase:
        """
        :type: ActorBase
        """
    @property
    def ends(self) -> bool:
        """
        :type: bool
        """
    @property
    def impulse(self) -> numpy.ndarray[float32]:
        """
        :type: numpy.ndarray[float32]
        """
    @property
    def normal(self) -> numpy.ndarray[float32]:
        """
        :type: numpy.ndarray[float32]
        """
    @property
    def persists(self) -> bool:
        """
        :type: bool
        """
    @property
    def point(self) -> numpy.ndarray[float32]:
        """
        :type: numpy.ndarray[float32]
        """
    @property
    def separation(self) -> float:
        """
        :type: float
        """
    @property
    def starts(self) -> bool:
        """
        :type: bool
        """
    pass
class ConvexMeshGeometry(CollisionGeometry):
    @property
    def indices(self) -> numpy.ndarray[uint32]:
        """
        :type: numpy.ndarray[uint32]
        """
    @property
    def rotation(self) -> numpy.ndarray[float32]:
        """
        :type: numpy.ndarray[float32]
        """
    @property
    def scale(self) -> numpy.ndarray[float32]:
        """
        :type: numpy.ndarray[float32]
        """
    @property
    def vertices(self) -> numpy.ndarray[float32]:
        """
        :type: numpy.ndarray[float32]
        """
    pass
class Drive():
    def destroy(self) -> None: ...
    def set_properties(self, stiffness: float, damping: float, force_limit: float = 3.4028234663852886e+38, is_acceleration: bool = True) -> None: ...
    def set_target(self, pose: Pose) -> None: ...
    def set_target_velocity(self, linear: numpy.ndarray[float32], angular: numpy.ndarray[float32]) -> None: ...
    pass
class Engine():
    def __init__(self, n_thread: int = 0, tolerance_length: float = 0.10000000149011612, tolerance_speed: float = 0.20000000298023224) -> None: ...
    def create_physical_material(self, static_friction: float, dynamic_friction: float, restitution: float) -> PxMaterial: ...
    def create_scene(self, gravity: numpy.ndarray[float32] = array([ 0. ,  0. , -9.8], dtype=float32), solver_type: SolverType = SolverType.PGS, enable_ccd: bool = False, enable_pcm: bool = True, config: SceneConfig = None) -> Scene: 
        """
        create_scene(self: sapien.core.pysapien.Engine, gravity: numpy.ndarray[float32] = array([ 0. ,  0. , -9.8], dtype=float32), solver_type: sapien.core.pysapien.SolverType = SolverType.PGS, enable_ccd: bool = False, enable_pcm: bool = True, config: sapien.core.pysapien.SceneConfig = None) -> sapien.core.pysapien.Scene
        """
    def get_renderer(self) -> IPxrRenderer: ...
    def set_log_level(self, level: str) -> None: ...
    def set_renderer(self, renderer: IPxrRenderer) -> None: ...
    pass
class ISensor():
    def get_pose(self) -> Pose: ...
    def set_initial_pose(self, pose: Pose) -> None: ...
    def set_pose(self, pose: Pose) -> None: ...
    pass
class IPxrRenderer():
    pass
class IPxrScene():
    pass
class ICamera(ISensor):
    def get_albedo_rgba(self) -> numpy.ndarray[float32]: ...
    def get_color_rgba(self) -> numpy.ndarray[float32]: ...
    def get_depth(self) -> numpy.ndarray[float32]: ...
    def get_far(self) -> float: ...
    def get_fovy(self) -> float: ...
    def get_height(self) -> int: ...
    def get_name(self) -> str: ...
    def get_near(self) -> float: ...
    def get_normal_rgba(self) -> numpy.ndarray[float32]: ...
    def get_obj_segmentation(self) -> numpy.ndarray[int32]: ...
    def get_pose(self) -> Pose: ...
    def get_segmentation(self) -> numpy.ndarray[int32]: ...
    def get_width(self) -> int: ...
    def set_initial_pose(self, pose: Pose) -> None: ...
    def set_pose(self, pose: Pose) -> None: ...
    def take_picture(self) -> None: ...
    pass
class Input():
    def get_key_down(self, arg0: int) -> int: ...
    def get_key_mods(self, arg0: int) -> int: ...
    def get_key_state(self, arg0: int) -> int: ...
    pass
class JointBase():
    def __repr__ (self) -> str: ...
    def get_child_link(self) -> LinkBase: ...
    def get_dof(self) -> int: ...
    def get_limits(self) -> numpy.ndarray[float32]: ...
    def get_name(self) -> str: ...
    def get_parent_link(self) -> LinkBase: ...
    def get_pose_in_child_frame(self) -> Pose: ...
    def get_pose_in_parent_frame(self) -> Pose: ...
    def set_limits(self, limits: numpy.ndarray[float32]) -> None: ...
    def set_name(self, name: str) -> None: ...
    @property
    def name(self) -> str:
        """
        :type: str
        """
    @name.setter
    def name(self, arg1: str) -> None:
        pass
    @property
    def type(self) -> ArticulationJointType:
        """
        :type: ArticulationJointType
        """
    pass
class Joint(JointBase):
    def __repr__ (self) -> str: ...
    def get_child_link(self) -> LinkBase: ...
    def get_dof(self) -> int: ...
    def get_global_pose(self) -> Pose: ...
    def get_limits(self) -> numpy.ndarray[float32]: ...
    def get_name(self) -> str: ...
    def get_parent_link(self) -> LinkBase: ...
    def get_pose_in_child_frame(self) -> Pose: ...
    def get_pose_in_parent_frame(self) -> Pose: ...
    def set_drive_property(self, stiffness: float, damping: float, force_limit: float = 3.4028234663852886e+38) -> None: ...
    def set_drive_target(self, target: float) -> None: ...
    def set_drive_velocity_target(self, velocity: float) -> None: ...
    def set_friction(self, friction: float) -> None: ...
    def set_limits(self, limits: numpy.ndarray[float32]) -> None: ...
    def set_name(self, name: str) -> None: ...
    @property
    def damping(self) -> float:
        """
        :type: float
        """
    @property
    def force_limit(self) -> float:
        """
        :type: float
        """
    @property
    def friction(self) -> float:
        """
        :type: float
        """
    @property
    def name(self) -> str:
        """
        :type: str
        """
    @name.setter
    def name(self, arg1: str) -> None:
        pass
    @property
    def stiffness(self) -> float:
        """
        :type: float
        """
    @property
    def type(self) -> ArticulationJointType:
        """
        :type: ArticulationJointType
        """
    pass
class JointRecord():
    @property
    def child_pose(self) -> Pose:
        """
        :type: Pose
        """
    @property
    def damping(self) -> float:
        """
        :type: float
        """
    @property
    def friction(self) -> float:
        """
        :type: float
        """
    @property
    def joint_type(self) -> str:
        """
        :type: str
        """
    @property
    def limits(self) -> numpy.ndarray[float32]:
        """
        :type: numpy.ndarray[float32]
        """
    @property
    def name(self) -> str:
        """
        :type: str
        """
    @property
    def parent_pose(self) -> Pose:
        """
        :type: Pose
        """
    pass
class KinematicArticulation(ArticulationDrivable, ArticulationBase):
    def get_base_joints(self) -> List[JointBase]: ...
    def get_base_links(self) -> List[LinkBase]: ...
    def get_drive_target(self) -> numpy.ndarray[float32]: ...
    def get_name(self) -> str: ...
    def get_pose(self) -> Pose: 
        """
        same as get_root_pose
        """
    def get_qacc(self) -> numpy.ndarray[float32]: ...
    def get_qf(self) -> numpy.ndarray[float32]: ...
    def get_qlimits(self) -> numpy.ndarray[float32]: ...
    def get_qpos(self) -> numpy.ndarray[float32]: ...
    def get_qvel(self) -> numpy.ndarray[float32]: ...
    def get_root_pose(self) -> Pose: ...
    def set_drive_target(self, drive_target: numpy.ndarray[float32]) -> None: ...
    def set_name(self, name: str) -> None: ...
    def set_pose(self, pose: Pose) -> None: 
        """
        same as set_root_pose
        """
    def set_qacc(self, qacc: numpy.ndarray[float32]) -> None: ...
    def set_qf(self, qf: numpy.ndarray[float32]) -> None: ...
    def set_qlimits(self, qlimits: numpy.ndarray[float32]) -> None: ...
    def set_qpos(self, qpos: numpy.ndarray[float32]) -> None: ...
    def set_qvel(self, qvel: numpy.ndarray[float32]) -> None: ...
    def set_root_pose(self, pose: Pose) -> None: ...
    @property
    def dof(self) -> int:
        """
        :type: int
        """
    @property
    def name(self) -> str:
        """
        :type: str
        """
    @name.setter
    def name(self, arg1: str) -> None:
        pass
    @property
    def pose(self) -> Pose:
        """
        same as get_root_pose()

        :type: Pose
        """
    @property
    def type(self) -> ArticulationType:
        """
        :type: ArticulationType
        """
    pass
class KinematicJoint(JointBase):
    def __repr__ (self) -> str: ...
    def get_child_link(self) -> LinkBase: ...
    def get_dof(self) -> int: ...
    def get_limits(self) -> numpy.ndarray[float32]: ...
    def get_name(self) -> str: ...
    def get_parent_link(self) -> LinkBase: ...
    def get_pose_in_child_frame(self) -> Pose: ...
    def get_pose_in_parent_frame(self) -> Pose: ...
    def set_limits(self, limits: numpy.ndarray[float32]) -> None: ...
    def set_name(self, name: str) -> None: ...
    @property
    def name(self) -> str:
        """
        :type: str
        """
    @name.setter
    def name(self, arg1: str) -> None:
        pass
    @property
    def type(self) -> ArticulationJointType:
        """
        :type: ArticulationJointType
        """
    pass
class KinematicJointFixed(KinematicJoint, JointBase):
    def __repr__ (self) -> str: ...
    def get_child_link(self) -> LinkBase: ...
    def get_dof(self) -> int: ...
    def get_limits(self) -> numpy.ndarray[float32]: ...
    def get_name(self) -> str: ...
    def get_parent_link(self) -> LinkBase: ...
    def get_pose_in_child_frame(self) -> Pose: ...
    def get_pose_in_parent_frame(self) -> Pose: ...
    def set_limits(self, limits: numpy.ndarray[float32]) -> None: ...
    def set_name(self, name: str) -> None: ...
    @property
    def name(self) -> str:
        """
        :type: str
        """
    @name.setter
    def name(self, arg1: str) -> None:
        pass
    @property
    def type(self) -> ArticulationJointType:
        """
        :type: ArticulationJointType
        """
    pass
class KinematicJointSingleDof(KinematicJoint, JointBase):
    def __repr__ (self) -> str: ...
    def get_child_link(self) -> LinkBase: ...
    def get_dof(self) -> int: ...
    def get_limits(self) -> numpy.ndarray[float32]: ...
    def get_name(self) -> str: ...
    def get_parent_link(self) -> LinkBase: ...
    def get_pose_in_child_frame(self) -> Pose: ...
    def get_pose_in_parent_frame(self) -> Pose: ...
    def set_limits(self, limits: numpy.ndarray[float32]) -> None: ...
    def set_name(self, name: str) -> None: ...
    @property
    def name(self) -> str:
        """
        :type: str
        """
    @name.setter
    def name(self, arg1: str) -> None:
        pass
    @property
    def type(self) -> ArticulationJointType:
        """
        :type: ArticulationJointType
        """
    pass
class KinematicJointRevolute(KinematicJointSingleDof, KinematicJoint, JointBase):
    def __repr__ (self) -> str: ...
    def get_child_link(self) -> LinkBase: ...
    def get_dof(self) -> int: ...
    def get_limits(self) -> numpy.ndarray[float32]: ...
    def get_name(self) -> str: ...
    def get_parent_link(self) -> LinkBase: ...
    def get_pose_in_child_frame(self) -> Pose: ...
    def get_pose_in_parent_frame(self) -> Pose: ...
    def set_limits(self, limits: numpy.ndarray[float32]) -> None: ...
    def set_name(self, name: str) -> None: ...
    @property
    def name(self) -> str:
        """
        :type: str
        """
    @name.setter
    def name(self, arg1: str) -> None:
        pass
    @property
    def type(self) -> ArticulationJointType:
        """
        :type: ArticulationJointType
        """
    pass
class KinematicJointPrismatic(KinematicJointSingleDof, KinematicJoint, JointBase):
    def __repr__ (self) -> str: ...
    def get_child_link(self) -> LinkBase: ...
    def get_dof(self) -> int: ...
    def get_limits(self) -> numpy.ndarray[float32]: ...
    def get_name(self) -> str: ...
    def get_parent_link(self) -> LinkBase: ...
    def get_pose_in_child_frame(self) -> Pose: ...
    def get_pose_in_parent_frame(self) -> Pose: ...
    def set_limits(self, limits: numpy.ndarray[float32]) -> None: ...
    def set_name(self, name: str) -> None: ...
    @property
    def name(self) -> str:
        """
        :type: str
        """
    @name.setter
    def name(self, arg1: str) -> None:
        pass
    @property
    def type(self) -> ArticulationJointType:
        """
        :type: ArticulationJointType
        """
    pass
class LinkBase(ActorDynamicBase, ActorBase):
    def __repr__(self) -> str: ...
    def add_force_at_point(self, force: numpy.ndarray[float32], point: numpy.ndarray[float32]) -> None: ...
    def add_force_torque(self, force: numpy.ndarray[float32], torque: numpy.ndarray[float32]) -> None: ...
    def get_angular_velocity(self) -> numpy.ndarray[float32]: ...
    def get_articulation(self) -> ArticulationBase: ...
    def get_cmass_local_pose(self) -> Pose: ...
    def get_collision_shapes(self) -> List[CollisionShape]: ...
    def get_id(self) -> int: ...
    def get_index(self) -> int: ...
    def get_inertia(self) -> numpy.ndarray[float32]: ...
    def get_mass(self) -> float: ...
    def get_name(self) -> str: ...
    def get_pose(self) -> Pose: ...
    def get_scene(self) -> Scene: ...
    def get_velocity(self) -> numpy.ndarray[float32]: ...
    def set_damping(self, linear: float, angular: float) -> None: ...
    def set_name(self, name: str) -> None: ...
    @property
    def angular_velocity(self) -> numpy.ndarray[float32]:
        """
        :type: numpy.ndarray[float32]
        """
    @property
    def cmass_local_pose(self) -> Pose:
        """
        :type: Pose
        """
    @property
    def col1(self) -> int:
        """
        :type: int
        """
    @property
    def col2(self) -> int:
        """
        :type: int
        """
    @property
    def col3(self) -> int:
        """
        :type: int
        """
    @property
    def id(self) -> int:
        """
        :type: int
        """
    @property
    def inertia(self) -> numpy.ndarray[float32]:
        """
        :type: numpy.ndarray[float32]
        """
    @property
    def mass(self) -> float:
        """
        :type: float
        """
    @property
    def name(self) -> str:
        """
        :type: str
        """
    @name.setter
    def name(self, arg1: str) -> None:
        pass
    @property
    def pose(self) -> Pose:
        """
        :type: Pose
        """
    @property
    def type(self) -> ActorType:
        """
        :type: ActorType
        """
    @property
    def velocity(self) -> numpy.ndarray[float32]:
        """
        :type: numpy.ndarray[float32]
        """
    pass
class Link(LinkBase, ActorDynamicBase, ActorBase):
    def __repr__(self) -> str: ...
    def add_force_at_point(self, force: numpy.ndarray[float32], point: numpy.ndarray[float32]) -> None: ...
    def add_force_torque(self, force: numpy.ndarray[float32], torque: numpy.ndarray[float32]) -> None: ...
    def get_angular_velocity(self) -> numpy.ndarray[float32]: ...
    def get_articulation(self) -> Articulation: ...
    def get_cmass_local_pose(self) -> Pose: ...
    def get_collision_shapes(self) -> List[CollisionShape]: ...
    def get_id(self) -> int: ...
    def get_index(self) -> int: ...
    def get_inertia(self) -> numpy.ndarray[float32]: ...
    def get_mass(self) -> float: ...
    def get_name(self) -> str: ...
    def get_pose(self) -> Pose: ...
    def get_scene(self) -> Scene: ...
    def get_velocity(self) -> numpy.ndarray[float32]: ...
    def set_damping(self, linear: float, angular: float) -> None: ...
    def set_name(self, name: str) -> None: ...
    @property
    def angular_velocity(self) -> numpy.ndarray[float32]:
        """
        :type: numpy.ndarray[float32]
        """
    @property
    def cmass_local_pose(self) -> Pose:
        """
        :type: Pose
        """
    @property
    def col1(self) -> int:
        """
        :type: int
        """
    @property
    def col2(self) -> int:
        """
        :type: int
        """
    @property
    def col3(self) -> int:
        """
        :type: int
        """
    @property
    def id(self) -> int:
        """
        :type: int
        """
    @property
    def inertia(self) -> numpy.ndarray[float32]:
        """
        :type: numpy.ndarray[float32]
        """
    @property
    def mass(self) -> float:
        """
        :type: float
        """
    @property
    def name(self) -> str:
        """
        :type: str
        """
    @name.setter
    def name(self, arg1: str) -> None:
        pass
    @property
    def pose(self) -> Pose:
        """
        :type: Pose
        """
    @property
    def type(self) -> ActorType:
        """
        :type: ActorType
        """
    @property
    def velocity(self) -> numpy.ndarray[float32]:
        """
        :type: numpy.ndarray[float32]
        """
    pass
class KinematicLink(LinkBase, ActorDynamicBase, ActorBase):
    def __repr__(self) -> str: ...
    def add_force_at_point(self, force: numpy.ndarray[float32], point: numpy.ndarray[float32]) -> None: ...
    def add_force_torque(self, force: numpy.ndarray[float32], torque: numpy.ndarray[float32]) -> None: ...
    def get_angular_velocity(self) -> numpy.ndarray[float32]: ...
    def get_articulation(self) -> KinematicArticulation: ...
    def get_cmass_local_pose(self) -> Pose: ...
    def get_collision_shapes(self) -> List[CollisionShape]: ...
    def get_id(self) -> int: ...
    def get_index(self) -> int: ...
    def get_inertia(self) -> numpy.ndarray[float32]: ...
    def get_mass(self) -> float: ...
    def get_name(self) -> str: ...
    def get_pose(self) -> Pose: ...
    def get_scene(self) -> Scene: ...
    def get_velocity(self) -> numpy.ndarray[float32]: ...
    def set_damping(self, linear: float, angular: float) -> None: ...
    def set_name(self, name: str) -> None: ...
    @property
    def angular_velocity(self) -> numpy.ndarray[float32]:
        """
        :type: numpy.ndarray[float32]
        """
    @property
    def cmass_local_pose(self) -> Pose:
        """
        :type: Pose
        """
    @property
    def col1(self) -> int:
        """
        :type: int
        """
    @property
    def col2(self) -> int:
        """
        :type: int
        """
    @property
    def col3(self) -> int:
        """
        :type: int
        """
    @property
    def id(self) -> int:
        """
        :type: int
        """
    @property
    def inertia(self) -> numpy.ndarray[float32]:
        """
        :type: numpy.ndarray[float32]
        """
    @property
    def mass(self) -> float:
        """
        :type: float
        """
    @property
    def name(self) -> str:
        """
        :type: str
        """
    @name.setter
    def name(self, arg1: str) -> None:
        pass
    @property
    def pose(self) -> Pose:
        """
        :type: Pose
        """
    @property
    def type(self) -> ActorType:
        """
        :type: ActorType
        """
    @property
    def velocity(self) -> numpy.ndarray[float32]:
        """
        :type: numpy.ndarray[float32]
        """
    pass
class LinkBuilder(ActorBuilder):
    def add_box_shape(self, pose: Pose = Pose([0, 0, 0], [1, 0, 0, 0]), size: numpy.ndarray[float32] = array([1., 1., 1.], dtype=float32), material: PxMaterial = None, density: float = 1000) -> None: 
        """
        add_box_shape(self: sapien.core.pysapien.ActorBuilder, pose: sapien.core.pysapien.Pose = Pose([0, 0, 0], [1, 0, 0, 0]), size: numpy.ndarray[float32] = array([1., 1., 1.], dtype=float32), material: sapien.core.pysapien.PxMaterial = None, density: float = 1000) -> None
        """
    def add_box_visual(self, pose: Pose = Pose([0, 0, 0], [1, 0, 0, 0]), size: numpy.ndarray[float32] = array([1., 1., 1.], dtype=float32), color: numpy.ndarray[float32] = array([1., 1., 1.], dtype=float32), name: str = '') -> None: 
        """
        add_box_visual(self: sapien.core.pysapien.ActorBuilder, pose: sapien.core.pysapien.Pose = Pose([0, 0, 0], [1, 0, 0, 0]), size: numpy.ndarray[float32] = array([1., 1., 1.], dtype=float32), color: numpy.ndarray[float32] = array([1., 1., 1.], dtype=float32), name: str = '') -> None
        """
    def add_box_visual_complex(self, pose: Pose = Pose([0, 0, 0], [1, 0, 0, 0]), size: numpy.ndarray[float32] = array([1., 1., 1.], dtype=float32), material: PxrMaterial = PxrMaterial(), name: str = '') -> None: 
        """
        add_box_visual_complex(self: sapien.core.pysapien.ActorBuilder, pose: sapien.core.pysapien.Pose = Pose([0, 0, 0], [1, 0, 0, 0]), size: numpy.ndarray[float32] = array([1., 1., 1.], dtype=float32), material: sapien.core.pysapien.PxrMaterial = PxrMaterial(), name: str = '') -> None
        """
    def add_capsule_shape(self, pose: Pose = Pose([0, 0, 0], [1, 0, 0, 0]), radius: float = 1, half_length: float = 1, material: PxMaterial = None, density: float = 1000) -> None: 
        """
        add_capsule_shape(self: sapien.core.pysapien.ActorBuilder, pose: sapien.core.pysapien.Pose = Pose([0, 0, 0], [1, 0, 0, 0]), radius: float = 1, half_length: float = 1, material: sapien.core.pysapien.PxMaterial = None, density: float = 1000) -> None
        """
    def add_capsule_visual(self, pose: Pose = Pose([0, 0, 0], [1, 0, 0, 0]), radius: float = 1, half_length: float = 1, color: numpy.ndarray[float32] = array([1., 1., 1.], dtype=float32), name: str = '') -> None: 
        """
        add_capsule_visual(self: sapien.core.pysapien.ActorBuilder, pose: sapien.core.pysapien.Pose = Pose([0, 0, 0], [1, 0, 0, 0]), radius: float = 1, half_length: float = 1, color: numpy.ndarray[float32] = array([1., 1., 1.], dtype=float32), name: str = '') -> None
        """
    def add_capsule_visual_complex(self, pose: Pose = Pose([0, 0, 0], [1, 0, 0, 0]), radius: float = 1, half_length: float = 1, material: PxrMaterial = PxrMaterial(), name: str = '') -> None: 
        """
        add_capsule_visual_complex(self: sapien.core.pysapien.ActorBuilder, pose: sapien.core.pysapien.Pose = Pose([0, 0, 0], [1, 0, 0, 0]), radius: float = 1, half_length: float = 1, material: sapien.core.pysapien.PxrMaterial = PxrMaterial(), name: str = '') -> None
        """
    def add_collision_group(self, arg0: int, arg1: int, arg2: int) -> None: ...
    def add_convex_shape_from_file(self, filename: str, pose: Pose = Pose([0, 0, 0], [1, 0, 0, 0]), scale: numpy.ndarray[float32] = array([1., 1., 1.], dtype=float32), material: PxMaterial = None, density: float = 1000) -> None: 
        """
        add_convex_shape_from_file(self: sapien.core.pysapien.ActorBuilder, filename: str, pose: sapien.core.pysapien.Pose = Pose([0, 0, 0], [1, 0, 0, 0]), scale: numpy.ndarray[float32] = array([1., 1., 1.], dtype=float32), material: sapien.core.pysapien.PxMaterial = None, density: float = 1000) -> None
        """
    def add_multiple_convex_shapes_from_file(self, filename: str, pose: Pose = Pose([0, 0, 0], [1, 0, 0, 0]), scale: numpy.ndarray[float32] = array([1., 1., 1.], dtype=float32), material: PxMaterial = None, density: float = 1000) -> None: 
        """
        add_multiple_convex_shapes_from_file(self: sapien.core.pysapien.ActorBuilder, filename: str, pose: sapien.core.pysapien.Pose = Pose([0, 0, 0], [1, 0, 0, 0]), scale: numpy.ndarray[float32] = array([1., 1., 1.], dtype=float32), material: sapien.core.pysapien.PxMaterial = None, density: float = 1000) -> None
        """
    def add_sphere_shape(self, pose: Pose = Pose([0, 0, 0], [1, 0, 0, 0]), radius: float = 1, material: PxMaterial = None, density: float = 1000) -> None: 
        """
        add_sphere_shape(self: sapien.core.pysapien.ActorBuilder, pose: sapien.core.pysapien.Pose = Pose([0, 0, 0], [1, 0, 0, 0]), radius: float = 1, material: sapien.core.pysapien.PxMaterial = None, density: float = 1000) -> None
        """
    def add_sphere_visual(self, pose: Pose = Pose([0, 0, 0], [1, 0, 0, 0]), radius: float = 1, color: numpy.ndarray[float32] = array([1., 1., 1.], dtype=float32), name: str = '') -> None: 
        """
        add_sphere_visual(self: sapien.core.pysapien.ActorBuilder, pose: sapien.core.pysapien.Pose = Pose([0, 0, 0], [1, 0, 0, 0]), radius: float = 1, color: numpy.ndarray[float32] = array([1., 1., 1.], dtype=float32), name: str = '') -> None
        """
    def add_sphere_visual_complex(self, pose: Pose = Pose([0, 0, 0], [1, 0, 0, 0]), radius: float = 1, material: PxrMaterial = PxrMaterial(), name: str = '') -> None: 
        """
        add_sphere_visual_complex(self: sapien.core.pysapien.ActorBuilder, pose: sapien.core.pysapien.Pose = Pose([0, 0, 0], [1, 0, 0, 0]), radius: float = 1, material: sapien.core.pysapien.PxrMaterial = PxrMaterial(), name: str = '') -> None
        """
    def add_visual_from_file(self, filename: str, pose: Pose = Pose([0, 0, 0], [1, 0, 0, 0]), scale: numpy.ndarray[float32] = array([1., 1., 1.], dtype=float32), name: str = '') -> None: 
        """
        add_visual_from_file(self: sapien.core.pysapien.ActorBuilder, filename: str, pose: sapien.core.pysapien.Pose = Pose([0, 0, 0], [1, 0, 0, 0]), scale: numpy.ndarray[float32] = array([1., 1., 1.], dtype=float32), name: str = '') -> None
        """
    def build(self, is_kinematic: bool = False, name: str = '') -> Actor: ...
    def build_static(self, name: str = '') -> ActorStatic: ...
    def get_index(self) -> int: ...
    def get_joints(self) -> JointRecord: ...
    def get_shapes(self) -> List[ShapeRecord]: ...
    def get_visuals(self) -> List[VisualRecord]: ...
    def remove_all_shapes(self) -> None: ...
    def remove_all_visuals(self) -> None: ...
    def remove_shape_at(self, index: int) -> None: ...
    def remove_visual_at(self, index: int) -> None: ...
    def reset_collision_group(self) -> None: ...
    def set_collision_group(self, arg0: int, arg1: int, arg2: int) -> None: ...
    def set_joint_name(self, arg0: str) -> None: ...
    def set_joint_properties(self, joint_type: ArticulationJointType, limits: numpy.ndarray[float32], parent_pose: Pose = Pose([0, 0, 0], [1, 0, 0, 0]), child_pose: Pose = Pose([0, 0, 0], [1, 0, 0, 0]), friction: float = 0, damping: float = 0) -> None: 
        """
        set_joint_properties(self: sapien.core.pysapien.LinkBuilder, joint_type: sapien.core.pysapien.ArticulationJointType, limits: numpy.ndarray[float32], parent_pose: sapien.core.pysapien.Pose = Pose([0, 0, 0], [1, 0, 0, 0]), child_pose: sapien.core.pysapien.Pose = Pose([0, 0, 0], [1, 0, 0, 0]), friction: float = 0, damping: float = 0) -> None
        """
    def set_mass_and_inertia(self, arg0: float, arg1: Pose, arg2: numpy.ndarray[float32]) -> None: ...
    def set_name(self, arg0: str) -> None: ...
    def set_parent(self, arg0: int) -> None: ...
    def set_scene(self, arg0: Scene) -> None: ...
    pass
class OptifuserCamera(ICamera, ISensor):
    def get_albedo_rgba(self) -> numpy.ndarray[float32]: ...
    def get_camera_matrix(self) -> numpy.ndarray[float32]: ...
    def get_color_rgba(self) -> numpy.ndarray[float32]: ...
    def get_custom_rgba(self) -> numpy.ndarray[float32]: ...
    def get_depth(self) -> numpy.ndarray[float32]: ...
    def get_far(self) -> float: ...
    def get_fovy(self) -> float: ...
    def get_height(self) -> int: ...
    def get_model_matrix(self) -> numpy.ndarray[float32]: ...
    def get_name(self) -> str: ...
    def get_near(self) -> float: ...
    def get_normal_rgba(self) -> numpy.ndarray[float32]: ...
    def get_obj_segmentation(self) -> numpy.ndarray[int32]: ...
    def get_pose(self) -> Pose: ...
    def get_projection_matrix(self) -> numpy.ndarray[float32]: ...
    def get_segmentation(self) -> numpy.ndarray[int32]: ...
    def get_width(self) -> int: ...
    def set_initial_pose(self, pose: Pose) -> None: ...
    def set_mode_orthographic(self, scaling: float = 1.0) -> None: ...
    def set_mode_perspective(self, fovy: float = 0.6108652353286743) -> None: ...
    def set_pose(self, pose: Pose) -> None: ...
    def take_picture(self) -> None: ...
    def take_raytraced_picture(self, samples_per_pixel: int = 128, reflection_count: int = 4, use_denoiser: bool = True) -> numpy.ndarray[float32]: ...
    pass
class OptifuserConfig():
    def __init__(self) -> None: ...
    @property
    def shadow_frustum_size(self) -> float:
        """
        :type: float
        """
    @shadow_frustum_size.setter
    def shadow_frustum_size(self, arg0: float) -> None:
        pass
    @property
    def shadow_map_size(self) -> int:
        """
        :type: int
        """
    @shadow_map_size.setter
    def shadow_map_size(self, arg0: int) -> None:
        pass
    @property
    def use_ao(self) -> bool:
        """
        :type: bool
        """
    @use_ao.setter
    def use_ao(self, arg0: bool) -> None:
        pass
    @property
    def use_shadow(self) -> bool:
        """
        :type: bool
        """
    @use_shadow.setter
    def use_shadow(self, arg0: bool) -> None:
        pass
    pass
class OptifuserController():
    def __init__(self, renderer: OptifuserRenderer) -> None: ...
    def focus(self, actor: ActorBase) -> None: ...
    def get_camera_pose(self) -> Pose: ...
    def get_selected_actor(self) -> ActorBase: ...
    def hide_window(self) -> None: ...
    def render(self) -> None: ...
    def set_camera_position(self, x: float, y: float, z: float) -> None: ...
    def set_camera_rotation(self, yaw: float, pitch: float) -> None: ...
    def set_current_scene(self, scene: Scene) -> None: ...
    def show_window(self) -> None: ...
    @property
    def input(self) -> Input:
        """
        :type: Input
        """
    @property
    def should_quit(self) -> bool:
        """
        :type: bool
        """
    pass
class OptifuserRenderer(IPxrRenderer):
    def __init__(self, glsl_dir: str = '', glsl_version: str = '', config: OptifuserConfig = OptifuserConfig()) -> None: ...
    def enable_global_axes(self, enable: bool = True) -> None: ...
    @staticmethod
    def set_default_shader_config(glsl_dir: str, glsl_version: str) -> None: ...
    def set_log_level(self, level: str) -> None: ...
    @staticmethod
    def set_optix_config(ptx_dir: str) -> None: ...
    pass
class PlaneGeometry(CollisionGeometry):
    pass
class Pose():
    def __init__(self, p: numpy.ndarray[float32] = array([0., 0., 0.], dtype=float32), q: numpy.ndarray[float32] = array([1., 0., 0., 0.], dtype=float32)) -> None: 
        """
        __init__(self: sapien.core.pysapien.Pose, p: numpy.ndarray[float32] = array([0., 0., 0.], dtype=float32), q: numpy.ndarray[float32] = array([1., 0., 0., 0.], dtype=float32)) -> None
        """
    def __mul__(self, arg0: Pose) -> Pose: ...
    def __repr__(self) -> str: ...
    @staticmethod
    def from_transformation_matrix(mat44: numpy.ndarray[float32]) -> Pose: ...
    def inv(self) -> Pose: ...
    def set_p(self, p: numpy.ndarray[float32]) -> None: ...
    def set_q(self, q: numpy.ndarray[float32]) -> None: ...
    def set_rotation(self, arg0: numpy.ndarray[float32]) -> None: ...
    def to_transformation_matrix(self) -> numpy.ndarray[float32, _Shape[4, 4]]: ...
    def transform(self, arg0: Pose) -> Pose: ...
    @property
    def p(self) -> numpy.ndarray[float32, _Shape[3, 1]]:
        """
        :type: numpy.ndarray[float32, _Shape[3, 1]]
        """
    @property
    def q(self) -> numpy.ndarray[float32, _Shape[4, 1]]:
        """
        :type: numpy.ndarray[float32, _Shape[4, 1]]
        """
    pass
class PxMaterial():
    def get_dynamic_friction(self) -> float: ...
    def get_restitution(self) -> float: ...
    def get_static_friction(self) -> float: ...
    def set_dynamic_friction(self, coef: float) -> None: ...
    def set_restitution(self, coef: float) -> None: ...
    def set_static_friction(self, coef: float) -> None: ...
    pass
class PxrMaterial():
    def __init__(self) -> None: ...
    def __repr__(self) -> str: ...
    def set_base_color(self, rgba: numpy.ndarray[float32]) -> None: ...
    @property
    def base_color(self) -> numpy.ndarray[float32]:
        """
        :type: numpy.ndarray[float32]
        """
    @property
    def metallic(self) -> float:
        """
        :type: float
        """
    @metallic.setter
    def metallic(self, arg0: float) -> None:
        pass
    @property
    def roughness(self) -> float:
        """
        :type: float
        """
    @roughness.setter
    def roughness(self, arg0: float) -> None:
        pass
    @property
    def specular(self) -> float:
        """
        :type: float
        """
    @specular.setter
    def specular(self, arg0: float) -> None:
        pass
    pass
class Scene():
    def add_directional_light(self, direction: numpy.ndarray[float32], color: numpy.ndarray[float32]) -> None: ...
    def add_ground(self, altitude: float, render: bool = True, material: PxMaterial = None, render_material: PxrMaterial = PxrMaterial()) -> None: 
        """
        add_ground(self: sapien.core.pysapien.Scene, altitude: float, render: bool = True, material: sapien.core.pysapien.PxMaterial = None, render_material: sapien.core.pysapien.PxrMaterial = PxrMaterial()) -> None
        """
    def add_mounted_camera(self, name: str, actor: ActorBase, pose: Pose, width: int, height: int, fovx: float, fovy: float, near: float, far: float) -> ICamera: ...
    def add_point_light(self, position: numpy.ndarray[float32], color: numpy.ndarray[float32]) -> None: ...
    def create_actor_builder(self) -> ActorBuilder: ...
    def create_articulation_builder(self) -> ArticulationBuilder: ...
    def create_drive(self, actor1: ActorBase, pose1: Pose, actor2: ActorBase, pose2: Pose) -> Drive: ...
    def create_urdf_loader(self) -> URDFLoader: ...
    def find_actor_by_id(self, id: int) -> ActorBase: ...
    def find_articulation_link_by_link_id(self, id: int) -> LinkBase: ...
    def find_mounted_camera(self, name: str, actor: ActorBase = None) -> ICamera: ...
    def get_all_actors(self) -> List[ActorBase]: ...
    def get_all_articulations(self) -> List[ArticulationBase]: ...
    def get_contacts(self) -> List[Contact]: ...
    def get_mounted_actors(self) -> List[ActorBase]: ...
    def get_mounted_cameras(self) -> List[ICamera]: ...
    def get_renderer_scene(self) -> IPxrScene: ...
    def get_timestep(self) -> float: ...
    def remove_actor(self, actor: ActorBase) -> None: ...
    def remove_articulation(self, articulation: Articulation) -> None: ...
    def remove_kinematic_articulation(self, kinematic_articulation: KinematicArticulation) -> None: ...
    def remove_mounted_camera(self, camera: ICamera) -> None: ...
    def set_ambient_light(self, clor: numpy.ndarray[float32]) -> None: ...
    def set_shadow_light(self, direction: numpy.ndarray[float32], color: numpy.ndarray[float32]) -> None: ...
    def set_timestep(self, second: float) -> None: ...
    def step(self) -> None: ...
    def update_render(self) -> None: ...
    @property
    def name(self) -> str:
        """
        :type: str
        """
    @property
    def timestep(self) -> float:
        """
        :type: float
        """
    @timestep.setter
    def timestep(self, arg1: float) -> None:
        pass
    pass
class SceneConfig():
    def __init__(self) -> None: ...
    @property
    def bounce_threshold(self) -> float:
        """
        :type: float
        """
    @bounce_threshold.setter
    def bounce_threshold(self, arg0: float) -> None:
        pass
    @property
    def contact_offset(self) -> float:
        """
        :type: float
        """
    @contact_offset.setter
    def contact_offset(self, arg0: float) -> None:
        pass
    @property
    def default_dynamic_friction(self) -> float:
        """
        :type: float
        """
    @default_dynamic_friction.setter
    def default_dynamic_friction(self, arg0: float) -> None:
        pass
    @property
    def default_restitution(self) -> float:
        """
        :type: float
        """
    @default_restitution.setter
    def default_restitution(self, arg0: float) -> None:
        pass
    @property
    def default_static_friction(self) -> float:
        """
        :type: float
        """
    @default_static_friction.setter
    def default_static_friction(self, arg0: float) -> None:
        pass
    @property
    def enable_adaptive_force(self) -> bool:
        """
        :type: bool
        """
    @enable_adaptive_force.setter
    def enable_adaptive_force(self, arg0: bool) -> None:
        pass
    @property
    def enable_ccd(self) -> bool:
        """
        :type: bool
        """
    @enable_ccd.setter
    def enable_ccd(self, arg0: bool) -> None:
        pass
    @property
    def enable_enhanced_determinism(self) -> bool:
        """
        :type: bool
        """
    @enable_enhanced_determinism.setter
    def enable_enhanced_determinism(self, arg0: bool) -> None:
        pass
    @property
    def enable_friction_every_iteration(self) -> bool:
        """
        :type: bool
        """
    @enable_friction_every_iteration.setter
    def enable_friction_every_iteration(self, arg0: bool) -> None:
        pass
    @property
    def enable_pcm(self) -> bool:
        """
        :type: bool
        """
    @enable_pcm.setter
    def enable_pcm(self, arg0: bool) -> None:
        pass
    @property
    def enable_tgs(self) -> bool:
        """
        :type: bool
        """
    @enable_tgs.setter
    def enable_tgs(self, arg0: bool) -> None:
        pass
    @property
    def gravity(self) -> numpy.ndarray[float32, _Shape[3, 1]]:
        """
        :type: numpy.ndarray[float32, _Shape[3, 1]]
        """
    @gravity.setter
    def gravity(self, arg0: numpy.ndarray[float32, _Shape[3, 1]]) -> None:
        pass
    @property
    def sleep_threshold(self) -> float:
        """
        :type: float
        """
    @sleep_threshold.setter
    def sleep_threshold(self, arg0: float) -> None:
        pass
    @property
    def solver_iterations(self) -> int:
        """
        :type: int
        """
    @solver_iterations.setter
    def solver_iterations(self, arg0: int) -> None:
        pass
    @property
    def solver_velocity_iterations(self) -> int:
        """
        :type: int
        """
    @solver_velocity_iterations.setter
    def solver_velocity_iterations(self, arg0: int) -> None:
        pass
    pass
class ShapeRecord():
    @property
    def density(self) -> float:
        """
        :type: float
        """
    @property
    def filename(self) -> str:
        """
        :type: str
        """
    @property
    def material(self) -> PxMaterial:
        """
        :type: PxMaterial
        """
    @property
    def pose(self) -> Pose:
        """
        :type: Pose
        """
    @property
    def radius(self) -> float:
        """
        :type: float
        """
    @property
    def scale(self) -> numpy.ndarray[float32]:
        """
        :type: numpy.ndarray[float32]
        """
    pass
class SolverType():
    """
    Members:

      PGS

      TGS
    """
    def __init__(self, arg0: int) -> None: ...
    def __int__(self) -> int: ...
    @property
    def name(self) -> str:
        """
        (self: handle) -> str

        :type: str
        """
    PGS: sapien.core.pysapien.SolverType # value = SolverType.PGS
    TGS: sapien.core.pysapien.SolverType # value = SolverType.TGS
    __entries: dict # value = {'PGS': (SolverType.PGS, None), 'TGS': (SolverType.TGS, None)}
    __members__: dict # value = {'PGS': SolverType.PGS, 'TGS': SolverType.TGS}
    pass
class SphereGeometry(CollisionGeometry):
    @property
    def radius(self) -> float:
        """
        :type: float
        """
    pass
class URDFLoader():
    def __init__(self, scene: Scene) -> None: ...
    def load(self, filename: str, material: PxMaterial = None) -> Articulation: ...
    def load_file_as_articulation_builder(self, filename: str, material: PxMaterial = None) -> ArticulationBuilder: ...
    def load_from_string(self, urdf_string: str, srdf_string: str, material: PxMaterial = None) -> Articulation: ...
    def load_kinematic(self, filename: str, material: PxMaterial = None) -> KinematicArticulation: ...
    @property
    def collision_is_visual(self) -> bool:
        """
        :type: bool
        """
    @collision_is_visual.setter
    def collision_is_visual(self, arg0: bool) -> None:
        pass
    @property
    def default_density(self) -> float:
        """
        :type: float
        """
    @default_density.setter
    def default_density(self, arg0: float) -> None:
        pass
    @property
    def fix_root_link(self) -> bool:
        """
        :type: bool
        """
    @fix_root_link.setter
    def fix_root_link(self, arg0: bool) -> None:
        pass
    @property
    def scale(self) -> float:
        """
        :type: float
        """
    @scale.setter
    def scale(self, arg0: float) -> None:
        pass
    pass
class VisualRecord():
    @property
    def density(self) -> str:
        """
        :type: str
        """
    @property
    def filename(self) -> str:
        """
        :type: str
        """
    @property
    def length(self) -> float:
        """
        :type: float
        """
    @property
    def material(self) -> PxrMaterial:
        """
        :type: PxrMaterial
        """
    @property
    def pose(self) -> Pose:
        """
        :type: Pose
        """
    @property
    def radius(self) -> float:
        """
        :type: float
        """
    @property
    def scale(self) -> numpy.ndarray[float32]:
        """
        :type: numpy.ndarray[float32]
        """
    pass
DYNAMIC: sapien.core.pysapien.ArticulationType # value = ArticulationType.DYNAMIC
FIX: sapien.core.pysapien.ArticulationJointType # value = ArticulationJointType.FIX
GL_SHADER_ROOT = ''
KINEMATIC: sapien.core.pysapien.ArticulationType # value = ArticulationType.KINEMATIC
KINEMATIC_LINK: sapien.core.pysapien.ActorType # value = ActorType.KINEMATIC_LINK
LINK: sapien.core.pysapien.ActorType # value = ActorType.LINK
PGS: sapien.core.pysapien.SolverType # value = SolverType.PGS
PRISMATIC: sapien.core.pysapien.ArticulationJointType # value = ArticulationJointType.PRISMATIC
PTX_ROOT = ''
REVOLUTE: sapien.core.pysapien.ArticulationJointType # value = ArticulationJointType.REVOLUTE
SPHERICAL: sapien.core.pysapien.ArticulationJointType # value = ArticulationJointType.SPHERICAL
STATIC: sapien.core.pysapien.ActorType # value = ActorType.STATIC
TGS: sapien.core.pysapien.SolverType # value = SolverType.TGS
UNDEFINED: sapien.core.pysapien.ArticulationJointType # value = ArticulationJointType.UNDEFINED
__GL_VERSION_DICT = {3: '130', 4: '410'}

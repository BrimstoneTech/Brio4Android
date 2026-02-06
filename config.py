from dataclasses import dataclass
from enum import Enum, auto

class LifeStage(Enum):
    CHILD = auto()
    YOUNG_ADULT = auto()
    ELDER = auto()

@dataclass
class PhysicsProfile:
    gravity: float
    friction: float
    bounce: float
    mass: float
    max_velocity: float
    rotation_speed: float

@dataclass
class AnimationProfile:
    idle_breath_speed: float
    blink_interval: tuple  # (min, max) seconds
    sway_amplitude: float
    step_height: float

@dataclass
class BehaviorProfile:
    curiosity_radius: int
    attention_span: float
    rest_frequency: float
    social_affinity: float

# Stage-specific configurations
PHYSICS_CONFIGS = {
    LifeStage.CHILD: PhysicsProfile(
        gravity=0.4,
        friction=0.92,
        bounce=0.7,
        mass=0.3,
        max_velocity=15.0,
        rotation_speed=8.0
    ),
    LifeStage.YOUNG_ADULT: PhysicsProfile(
        gravity=0.6,
        friction=0.88,
        bounce=0.4,
        mass=0.6,
        max_velocity=10.0,
        rotation_speed=4.0
    ),
    LifeStage.ELDER: PhysicsProfile(
        gravity=0.8,
        friction=0.95,
        bounce=0.2,
        mass=1.0,
        max_velocity=4.0,
        rotation_speed=1.5
    )
}

ANIMATION_CONFIGS = {
    LifeStage.CHILD: AnimationProfile(
        idle_breath_speed=0.15,
        blink_interval=(2.0, 5.0),
        sway_amplitude=15.0,
        step_height=25.0
    ),
    LifeStage.YOUNG_ADULT: AnimationProfile(
        idle_breath_speed=0.08,
        blink_interval=(3.0, 7.0),
        sway_amplitude=5.0,
        step_height=12.0
    ),
    LifeStage.ELDER: AnimationProfile(
        idle_breath_speed=0.04,
        blink_interval=(4.0, 10.0),
        sway_amplitude=2.0,
        step_height=5.0
    )
}

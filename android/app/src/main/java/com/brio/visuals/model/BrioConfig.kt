package com.brio.visuals.model

data class PhysicsProfile(
    val gravity: Float,
    val friction: Float,
    val bounce: Float,
    val mass: Float,
    val maxVelocity: Float,
    val rotationSpeed: Float
)

data class AnimationProfile(
    val idleBreathSpeed: Float,
    val blinkIntervalMin: Float,
    val blinkIntervalMax: Float,
    val swayAmplitude: Float,
    val stepHeight: Float
)

enum class LifeStage {
    CHILD, YOUNG_ADULT, ELDER
}

object BrioConfig {
    val PHYSICS_CONFIGS = mapOf(
        LifeStage.CHILD to PhysicsProfile(0.4f, 0.92f, 0.7f, 0.3f, 15.0f, 8.0f),
        LifeStage.YOUNG_ADULT to PhysicsProfile(0.6f, 0.88f, 0.4f, 0.6f, 10.0f, 4.0f),
        LifeStage.ELDER to PhysicsProfile(0.8f, 0.95f, 0.2f, 1.0f, 4.0f, 1.5f)
    )

    val ANIMATION_CONFIGS = mapOf(
        LifeStage.CHILD to AnimationProfile(0.15f, 2.0f, 5.0f, 15.0f, 25.0f),
        LifeStage.YOUNG_ADULT to AnimationProfile(0.08f, 3.0f, 7.0f, 5.0f, 12.0f),
        LifeStage.ELDER to AnimationProfile(0.04f, 4.0f, 10.0f, 2.0f, 5.0f)
    )
}

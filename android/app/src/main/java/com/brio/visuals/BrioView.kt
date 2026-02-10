package com.brio.visuals

import android.content.Context
import android.graphics.Bitmap
import android.graphics.BitmapFactory
import android.graphics.Canvas
import android.graphics.Paint
import android.view.View
import android.view.Choreographer
import com.brio.visuals.model.BrioConfig
import com.brio.visuals.model.LifeStage
import kotlin.math.sin

class BrioView(context: Context) : View(context) {

    private val paint = Paint(Paint.ANTI_ALIAS_FLAG)
    private var brioBitmap: Bitmap? = null
    
    // State
    private var positionX = 500f
    private var positionY = 500f
    private var velocityY = 0f
    private val stage = LifeStage.YOUNG_ADULT
    private val physics = BrioConfig.PHYSICS_CONFIGS[stage]!!
    private val animation = BrioConfig.ANIMATION_CONFIGS[stage]!!

    // Animation State
    private var breathTime = 0f
    private var lastTime = 0L

    // Game Loop
    private val choreographerCallback = object : Choreographer.FrameCallback {
        override fun doFrame(frameTimeNanos: Long) {
            val dt = if (lastTime == 0L) 0.016f else (frameTimeNanos - lastTime) / 1_000_000_000f
            lastTime = frameTimeNanos
            
            update(dt)
            invalidate() // Request redraw
            Choreographer.getInstance().postFrameCallback(this)
        }
    }

    init {
        // Load asset based on stage (simplified logic for now)
        // In real app, resource ID should be resolved dynamically
        // Note: resources.getIdentifier is slow, better to use R.drawable directly if possible or map it
        try {
            val resId = resources.getIdentifier("youth_removebg_preview", "drawable", context.packageName)
            if (resId != 0) {
                brioBitmap = BitmapFactory.decodeResource(resources, resId)
            }
        } catch (e: Exception) {
            e.printStackTrace()
        }
        
        // Start loop
        Choreographer.getInstance().postFrameCallback(choreographerCallback)
    }

    private fun update(dt: Float) {
        // Simple Physics: Gravity and Floor Collision
        velocityY += physics.gravity * 50f * dt // Scale gravity for pixel coordinates
        positionY += velocityY

        // Floor collision (hardcoded floor for now)
        val floorY = height - 400f
        if (positionY > floorY) {
            positionY = floorY
            velocityY *= -physics.bounce
            if (kotlin.math.abs(velocityY) < 1f) velocityY = 0f
        }

        // Animation: Breathing (Scaling)
        breathTime += dt * animation.idleBreathSpeed * 10f
    }

    override fun onDraw(canvas: Canvas) {
        super.onDraw(canvas)
        
        brioBitmap?.let { bitmap ->
            // Apply breathing scale
            val scale = 1.0f + 0.05f * sin(breathTime)
            
            val drawWidth = bitmap.width * scale
            val drawHeight = bitmap.height * scale
            
            // Draw centered at position
            val drawX = positionX - drawWidth / 2
            val drawY = positionY - drawHeight
            
            // Save/Restore for transformations if needed
            canvas.save()
            canvas.translate(drawX, drawY)
            canvas.scale(scale, scale)
            canvas.drawBitmap(bitmap, 0f, 0f, paint)
            canvas.restore()
        }
    }
}

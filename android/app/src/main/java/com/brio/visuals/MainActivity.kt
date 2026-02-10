package com.brio.visuals

import android.app.Activity
import android.os.Bundle

class MainActivity : Activity() {
    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        
        // Set full screen, hide status bar content
        // In a real app, use WindowInsetsController for proper fullscreen
        
        val brioView = BrioView(this)
        setContentView(brioView)
    }
}

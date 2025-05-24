#!/usr/bin/env python3
"""
SBTM Tool - Session-Based Test Management Tool
Main entry point for the application
"""

import os
from nicegui import ui, app
from database.models import init_db
from views.main_layout import create_main_layout

async def startup():
    """Initialize the application"""
    await init_db()

@ui.page('/health')
def health_check():
    """Health check endpoint for load balancers"""
    return {'status': 'healthy', 'service': 'sbtm-tool'}

if __name__ in {"__main__", "__mp_main__"}:
    app.on_startup(startup)
    
    @ui.page('/')
    def index():
        create_main_layout()
    
    # Production configuration
    port = int(os.getenv('PORT', 8080))
    host = os.getenv('HOST', '0.0.0.0')
    environment = os.getenv('ENVIRONMENT', 'development')
    
    ui.run(
        title="SBTM Tool", 
        port=port,
        host=host,
        reload=(environment == 'development'),
        show=False
    )
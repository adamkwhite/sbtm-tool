"""
Main layout and navigation for SBTM Tool
"""

from nicegui import ui
from .session_view import create_session_view
from .session_list_view import create_session_list_view
from .charter_view import create_charter_view
from .tester_view import create_tester_view
from .product_view import create_product_view
from .tag_view import create_tag_view
from .statistics_view import create_statistics_view

def create_main_layout():
    """Create the main application layout with navigation"""
    
    ui.page_title("SBTM Tool - Session-Based Test Management")
    
    with ui.header().classes('bg-blue-600'):
        ui.label('SBTM Tool').classes('text-h6 text-white')
        
        # Navigation menu
        with ui.row().classes('w-full justify-center'):
            ui.button('Sessions', on_click=lambda: switch_view('sessions')).classes('text-white')
            ui.button('Session List', on_click=lambda: switch_view('session_list')).classes('text-white')
            ui.button('Charters', on_click=lambda: switch_view('charters')).classes('text-white')
            ui.button('Testers', on_click=lambda: switch_view('testers')).classes('text-white')
            ui.button('Products', on_click=lambda: switch_view('products')).classes('text-white')
            ui.button('Tags', on_click=lambda: switch_view('tags')).classes('text-white')
            ui.button('Statistics', on_click=lambda: switch_view('statistics')).classes('text-white')
    
    # Main content area
    content_area = ui.column().classes('w-full p-4')
    
    def switch_view(view_name):
        """Switch between different views"""
        content_area.clear()
        
        with content_area:
            if view_name == 'sessions':
                create_session_view()
            elif view_name == 'session_list':
                create_session_list_view()
            elif view_name == 'charters':
                create_charter_view()
            elif view_name == 'testers':
                create_tester_view()
            elif view_name == 'products':
                create_product_view()
            elif view_name == 'tags':
                create_tag_view()
            elif view_name == 'statistics':
                create_statistics_view()
    
    # Default view
    switch_view('sessions')
"""
Charter view for managing test charters and charter templates
"""

from nicegui import ui

def create_charter_view():
    """Create the charter management view"""
    
    ui.label('Charter Management').classes('text-h4 mb-4')
    
    with ui.row().classes('w-full gap-4'):
        # Left column - Charter list and search
        with ui.column().classes('w-1/2'):
            ui.label('Charter Library').classes('text-h6 mb-2')
            
            # Search and filter controls
            with ui.row().classes('w-full gap-2 mb-4'):
                search_input = ui.input(
                    label='Search charters',
                    placeholder='Search charter statements...'
                ).classes('flex-1')
                
                ui.button('Search', on_click=search_charters).props('color=primary')
            
            with ui.row().classes('w-full gap-2 mb-4'):
                filter_tags = ui.select(
                    [],  # Will be populated with available tags
                    label='Filter by Tags',
                    multiple=True
                ).classes('flex-1')
                
                sort_by = ui.select(
                    ['Created Date', 'Charter Statement', 'Usage Count'],
                    label='Sort by',
                    value='Created Date'
                ).classes('w-48')
            
            # Charter list
            with ui.card().classes('w-full'):
                ui.label('Charter Templates').classes('font-bold p-4')
                
                # Sample charter list (will be replaced with database data)
                charter_list = ui.list().classes('w-full')
                
                with charter_list:
                    with ui.item(on_click=lambda: select_charter(1)):
                        with ui.item_section():
                            ui.item_label('Test login functionality with various user types')
                            ui.item_label('Created: 2024-01-10 | Used: 5 times').props('caption')
                    
                    with ui.item(on_click=lambda: select_charter(2)):
                        with ui.item_section():
                            ui.item_label('Explore payment workflow edge cases')
                            ui.item_label('Created: 2024-01-08 | Used: 3 times').props('caption')
                    
                    with ui.item(on_click=lambda: select_charter(3)):
                        with ui.item_section():
                            ui.item_label('Investigate data validation across forms')
                            ui.item_label('Created: 2024-01-05 | Used: 8 times').props('caption')
        
        # Right column - Charter editor
        with ui.column().classes('w-1/2'):
            ui.label('Charter Editor').classes('text-h6 mb-2')
            
            with ui.card().classes('w-full p-4'):
                # Charter form
                charter_statement = ui.textarea(
                    label='Charter Statement',
                    placeholder='Enter the charter statement (mission for test sessions)...'
                ).classes('w-full mb-4').style('min-height: 200px')
                
                # Associated tags
                charter_tags = ui.select(
                    [],  # Will be populated with available tags
                    label='Associated Tags',
                    multiple=True
                ).classes('w-full mb-4')
                
                # Associated documents
                ui.label('Associated Documents').classes('font-bold mb-2')
                with ui.row().classes('w-full gap-2 mb-4'):
                    document_select = ui.select(
                        [],  # Will be populated with available documents
                        label='Select Documents',
                        multiple=True
                    ).classes('flex-1')
                    
                    ui.button('Upload New', on_click=upload_document).props('outlined')
                
                # Charter groups/hierarchy
                ui.label('Charter Groups').classes('font-bold mb-2')
                charter_groups = ui.select(
                    [],  # Will be populated with charter groups
                    label='Assign to Groups',
                    multiple=True
                ).classes('w-full mb-4')
                
                # Action buttons
                with ui.row().classes('w-full gap-2 mt-4'):
                    ui.button('Save Charter', on_click=save_charter).props('color=primary')
                    ui.button('Save as Template', on_click=save_as_template).props('outlined')
                    ui.button('Create from Template', on_click=create_from_template).props('outlined')
                    ui.button('Clear', on_click=clear_form).props('outlined')
    
    # Action buttons for list operations
    with ui.row().classes('w-full gap-2 mt-4'):
        ui.button('Export to JSON', on_click=export_json).props('outlined')
        ui.button('Print Charters', on_click=print_charters).props('outlined')
        ui.button('Organize Groups', on_click=organize_groups).props('outlined')

def search_charters():
    """Search charters based on input"""
    ui.notify('Searching charters...', type='info')

def select_charter(charter_id):
    """Select a charter from the list for editing"""
    ui.notify(f'Selected charter {charter_id}', type='info')

def upload_document():
    """Upload a new document"""
    ui.notify('Document upload dialog...', type='info')

def save_charter():
    """Save the current charter"""
    ui.notify('Charter saved successfully!', type='positive')

def save_as_template():
    """Save current charter as a template"""
    ui.notify('Charter template saved!', type='positive')

def create_from_template():
    """Create a new charter from a template"""
    ui.notify('Creating charter from template...', type='info')

def clear_form():
    """Clear the charter form"""
    ui.notify('Form cleared', type='info')

def export_json():
    """Export charters to JSON format"""
    ui.notify('Exporting charters to JSON...', type='info')

def print_charters():
    """Print charter list"""
    ui.notify('Printing charters...', type='info')

def organize_groups():
    """Open charter group organization dialog"""
    ui.notify('Opening group organization...', type='info')
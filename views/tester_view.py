"""
Tester view for managing tester repository
"""

from nicegui import ui

def create_tester_view():
    """Create the tester management view"""
    
    ui.label('Tester Management').classes('text-h4 mb-4')
    
    with ui.row().classes('w-full gap-4'):
        # Left column - Tester list
        with ui.column().classes('w-1/2'):
            ui.label('Tester Repository').classes('text-h6 mb-2')
            
            # Search and filter controls
            with ui.row().classes('w-full gap-2 mb-4'):
                search_input = ui.input(
                    label='Search testers',
                    placeholder='Search by name...'
                ).classes('flex-1')
                
                ui.button('Search', on_click=search_testers).props('color=primary')
            
            with ui.row().classes('w-full gap-2 mb-4'):
                filter_tags = ui.select(
                    [],  # Will be populated with available tags
                    label='Filter by Tags',
                    multiple=True
                ).classes('flex-1')
                
                sort_by = ui.select(
                    ['Name', 'Sessions Count', 'Created Date'],
                    label='Sort by',
                    value='Name'
                ).classes('w-48')
            
            # Tester list
            with ui.card().classes('w-full'):
                ui.label('Testers').classes('font-bold p-4')
                
                # Sample tester list (will be replaced with database data)
                tester_list = ui.list().classes('w-full')
                
                with tester_list:
                    with ui.item(on_click=lambda: select_tester(1)):
                        with ui.item_section():
                            ui.item_label('John Doe')
                            ui.item_label('Sessions: 15 | Last active: 2024-01-15').props('caption')
                    
                    with ui.item(on_click=lambda: select_tester(2)):
                        with ui.item_section():
                            ui.item_label('Jane Smith')
                            ui.item_label('Sessions: 8 | Last active: 2024-01-14').props('caption')
                    
                    with ui.item(on_click=lambda: select_tester(3)):
                        with ui.item_section():
                            ui.item_label('Bob Johnson')
                            ui.item_label('Sessions: 22 | Last active: 2024-01-13').props('caption')
        
        # Right column - Tester editor
        with ui.column().classes('w-1/2'):
            ui.label('Tester Details').classes('text-h6 mb-2')
            
            with ui.card().classes('w-full p-4'):
                # Tester form
                tester_name = ui.input(
                    label='Tester Name',
                    placeholder='Enter tester name...'
                ).classes('w-full mb-4')
                
                ui.label('Note: Testers do not need accounts on this system').classes('text-caption text-grey mb-4')
                
                # Associated tags
                tester_tags = ui.select(
                    [],  # Will be populated with available tags
                    label='Associated Tags',
                    multiple=True
                ).classes('w-full mb-4')
                
                # Statistics section
                ui.separator().classes('my-4')
                ui.label('Tester Statistics').classes('font-bold mb-2')
                
                with ui.row().classes('w-full gap-4'):
                    with ui.column():
                        ui.label('Total Sessions: 0').classes('text-lg')
                        ui.label('Completed Sessions: 0').classes('text-lg')
                    
                    with ui.column():
                        ui.label('Average T Metric: 0%').classes('text-lg')
                        ui.label('Total Testing Hours: 0').classes('text-lg')
                
                # Associated sessions (read-only)
                ui.separator().classes('my-4')
                ui.label('Recent Sessions').classes('font-bold mb-2')
                
                # Sessions table for this tester
                session_columns = [
                    {'name': 'id', 'label': 'ID', 'field': 'id'},
                    {'name': 'charter', 'label': 'Charter', 'field': 'charter'},
                    {'name': 'date', 'label': 'Date', 'field': 'date'},
                    {'name': 'status', 'label': 'Status', 'field': 'status'},
                ]
                
                session_rows = [
                    {'id': 1, 'charter': 'Test login functionality', 'date': '2024-01-15', 'status': 'Completed'},
                    {'id': 2, 'charter': 'Explore payment workflow', 'date': '2024-01-14', 'status': 'In Progress'},
                ]
                
                ui.table(columns=session_columns, rows=session_rows, row_key='id').classes('w-full')
                
                # Action buttons
                with ui.row().classes('w-full gap-2 mt-4'):
                    ui.button('Save Tester', on_click=save_tester).props('color=primary')
                    ui.button('Delete Tester', on_click=delete_tester).props('color=negative outlined')
                    ui.button('Clear', on_click=clear_form).props('outlined')
    
    # Action buttons for list operations
    with ui.row().classes('w-full gap-2 mt-4'):
        ui.button('Add New Tester', on_click=add_new_tester).props('color=primary')
        ui.button('Export to JSON', on_click=export_json).props('outlined')
        ui.button('Export to XML', on_click=export_xml).props('outlined')
        ui.button('Group by Tags', on_click=group_by_tags).props('outlined')

def search_testers():
    """Search testers based on input"""
    ui.notify('Searching testers...', type='info')

def select_tester(tester_id):
    """Select a tester from the list for editing"""
    ui.notify(f'Selected tester {tester_id}', type='info')

def save_tester():
    """Save the current tester"""
    ui.notify('Tester saved successfully!', type='positive')

def delete_tester():
    """Delete the current tester"""
    ui.notify('Tester deleted', type='warning')

def clear_form():
    """Clear the tester form"""
    ui.notify('Form cleared', type='info')

def add_new_tester():
    """Add a new tester"""
    ui.notify('Adding new tester...', type='info')

def export_json():
    """Export testers to JSON format"""
    ui.notify('Exporting testers to JSON...', type='info')

def export_xml():
    """Export testers to XML format"""
    ui.notify('Exporting testers to XML...', type='info')

def group_by_tags():
    """Group testers by tags"""
    ui.notify('Grouping testers by tags...', type='info')
"""
Tag view for managing hierarchical tag system
"""

from nicegui import ui

def create_tag_view():
    """Create the tag management view"""
    
    ui.label('Tag Management').classes('text-h4 mb-4')
    
    with ui.row().classes('w-full gap-4'):
        # Left column - Tag hierarchy
        with ui.column().classes('w-1/2'):
            ui.label('Tag Hierarchy').classes('text-h6 mb-2')
            
            # Search and filter controls
            with ui.row().classes('w-full gap-2 mb-4'):
                search_input = ui.input(
                    label='Search tags',
                    placeholder='Search by name or description...'
                ).classes('flex-1')
                
                ui.button('Search', on_click=search_tags).props('color=primary')
            
            with ui.row().classes('w-full gap-2 mb-4'):
                view_mode = ui.select(
                    ['Tree View', 'Flat List', 'Mind Map'],
                    label='View Mode',
                    value='Tree View'
                ).classes('w-48')
                
                sort_by = ui.select(
                    ['Name', 'Usage Count', 'Created Date'],
                    label='Sort by',
                    value='Name'
                ).classes('w-48')
            
            # Tag hierarchy tree
            with ui.card().classes('w-full'):
                ui.label('Tag Tree').classes('font-bold p-4')
                
                # Sample tag hierarchy (will be replaced with database data)
                with ui.tree([
                    {
                        'id': 'testing-types',
                        'label': 'Testing Types',
                        'children': [
                            {'id': 'functional', 'label': 'Functional Testing'},
                            {'id': 'performance', 'label': 'Performance Testing'},
                            {'id': 'security', 'label': 'Security Testing'},
                        ]
                    },
                    {
                        'id': 'features',
                        'label': 'Features',
                        'children': [
                            {'id': 'login', 'label': 'Login System'},
                            {'id': 'payment', 'label': 'Payment Processing'},
                            {'id': 'user-mgmt', 'label': 'User Management'},
                        ]
                    },
                    {
                        'id': 'platforms',
                        'label': 'Platforms',
                        'children': [
                            {'id': 'web', 'label': 'Web Browser'},
                            {'id': 'mobile', 'label': 'Mobile App'},
                            {'id': 'api', 'label': 'API Testing'},
                        ]
                    }
                ], node_key='id', label_key='label', on_select=select_tag) as tree:
                    tree.classes('w-full')
        
        # Right column - Tag editor
        with ui.column().classes('w-1/2'):
            ui.label('Tag Details').classes('text-h6 mb-2')
            
            with ui.card().classes('w-full p-4'):
                # Tag form
                tag_name = ui.input(
                    label='Tag Name',
                    placeholder='Enter tag name...'
                ).classes('w-full mb-4')
                
                tag_description = ui.textarea(
                    label='Tag Description',
                    placeholder='Enter description for this tag...'
                ).classes('w-full mb-4').style('min-height: 100px')
                
                # Parent tag selection
                parent_tag = ui.select(
                    [],  # Will be populated with available parent tags
                    label='Parent Tag (Optional)',
                    clearable=True
                ).classes('w-full mb-4')
                
                # Tag groups
                tag_groups = ui.select(
                    [],  # Will be populated with available groups
                    label='Assign to Groups',
                    multiple=True
                ).classes('w-full mb-4')
                
                # Usage statistics
                ui.separator().classes('my-4')
                ui.label('Tag Usage Statistics').classes('font-bold mb-2')
                
                with ui.row().classes('w-full gap-4'):
                    with ui.column():
                        ui.label('Used in Sessions: 0').classes('text-lg')
                        ui.label('Used in Charters: 0').classes('text-lg')
                    
                    with ui.column():
                        ui.label('Used in Testers: 0').classes('text-lg')
                        ui.label('Used in Products: 0').classes('text-lg')
                
                # Associated items preview
                ui.separator().classes('my-4')
                ui.label('Associated Items').classes('font-bold mb-2')
                
                with ui.expansion('Sessions using this tag', icon='assignment'):
                    ui.label('Session 1: Test login functionality')
                    ui.label('Session 2: Explore payment workflow')
                
                with ui.expansion('Charters using this tag', icon='description'):
                    ui.label('Charter 1: Login system testing')
                    ui.label('Charter 2: Payment integration tests')
                
                # Action buttons
                with ui.row().classes('w-full gap-2 mt-4'):
                    ui.button('Save Tag', on_click=save_tag).props('color=primary')
                    ui.button('Delete Tag', on_click=delete_tag).props('color=negative outlined')
                    ui.button('Clear', on_click=clear_form).props('outlined')
    
    # Action buttons for tag operations
    with ui.row().classes('w-full gap-2 mt-4'):
        ui.button('Add New Tag', on_click=add_new_tag).props('color=primary')
        ui.button('Re-map Tags', on_click=remap_tags).props('outlined')
        ui.button('Export to JSON', on_click=export_json).props('outlined')
        ui.button('Export to XML', on_click=export_xml).props('outlined')
        ui.button('Export Mind Map', on_click=export_mindmap).props('outlined')
        ui.button('Import Tags', on_click=import_tags).props('outlined')

def search_tags():
    """Search tags based on input"""
    ui.notify('Searching tags...', type='info')

def select_tag(e):
    """Select a tag from the tree for editing"""
    selected_tag = e.value
    ui.notify(f'Selected tag: {selected_tag}', type='info')

def save_tag():
    """Save the current tag"""
    ui.notify('Tag saved successfully!', type='positive')

def delete_tag():
    """Delete the current tag"""
    ui.notify('Tag deleted', type='warning')

def clear_form():
    """Clear the tag form"""
    ui.notify('Form cleared', type='info')

def add_new_tag():
    """Add a new tag"""
    ui.notify('Adding new tag...', type='info')

def remap_tags():
    """Open tag remapping dialog"""
    with ui.dialog() as dialog, ui.card().classes('w-[600px]'):
        ui.label('Re-map Tags').classes('text-h6 mb-4')
        
        with ui.column().classes('w-full gap-4'):
            ui.label('Search and replace tags with other tags')
            
            source_tag = ui.select(
                [],  # Will be populated with available tags
                label='Source Tag (to replace)'
            ).classes('w-full')
            
            target_tag = ui.select(
                [],  # Will be populated with available tags
                label='Target Tag (replacement)'
            ).classes('w-full')
            
            ui.label('This will update all associations using the source tag')
            
            with ui.row().classes('w-full justify-end gap-2'):
                ui.button('Cancel', on_click=dialog.close).props('outlined')
                ui.button('Re-map Tags', on_click=lambda: perform_remap(dialog)).props('color=primary')
    
    dialog.open()

def perform_remap(dialog):
    """Perform the tag remapping operation"""
    ui.notify('Tags remapped successfully!', type='positive')
    dialog.close()

def export_json():
    """Export tags to JSON format"""
    ui.notify('Exporting tags to JSON...', type='info')

def export_xml():
    """Export tags to XML format"""
    ui.notify('Exporting tags to XML...', type='info')

def export_mindmap():
    """Export tags to mind map format"""
    ui.notify('Exporting tags to mind map...', type='info')

def import_tags():
    """Import tags from file"""
    ui.notify('Opening import dialog...', type='info')
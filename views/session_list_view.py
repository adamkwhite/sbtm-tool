"""
Session list view for browsing and managing session reports
"""

from nicegui import ui

def create_session_list_view():
    """Create the session list view"""
    
    ui.label('Session List').classes('text-h4 mb-4')
    
    # Search and filter controls
    with ui.row().classes('w-full gap-4 mb-4'):
        search_input = ui.input(
            label='Search sessions',
            placeholder='Search by charter, notes, tester...'
        ).classes('flex-1')
        
        filter_status = ui.select(
            ['All', 'Not Started', 'In Progress', 'Completed', 'Accepted'],
            label='Filter by Status',
            value='All'
        ).classes('w-48')
        
        sort_by = ui.select(
            ['Start Time', 'Duration', 'T Metric', 'B Metric', 'S Metric', 'Status'],
            label='Sort by',
            value='Start Time'
        ).classes('w-48')
    
    # Action buttons
    with ui.row().classes('w-full gap-2 mb-4'):
        ui.button('New Session', on_click=lambda: ui.notify('Navigate to session view')).props('color=primary')
        ui.button('Export to JSON', on_click=export_json).props('outlined')
        ui.button('Export to Mind Map', on_click=export_mindmap).props('outlined')
        ui.button('Group by Tags', on_click=group_by_tags).props('outlined')
    
    # Session statistics summary
    with ui.card().classes('w-full p-4 mb-4'):
        ui.label('Session Statistics').classes('text-h6 mb-2')
        
        with ui.row().classes('w-full gap-8'):
            with ui.column():
                ui.label('Total Sessions: 0').classes('text-lg')
                ui.label('Completed: 0').classes('text-lg')
            
            with ui.column():
                ui.label('Avg T Metric: 0%').classes('text-lg')
                ui.label('Avg B Metric: 0%').classes('text-lg')
            
            with ui.column():
                ui.label('Avg S Metric: 0%').classes('text-lg')
                ui.label('Total Hours: 0').classes('text-lg')
    
    # Sessions table
    columns = [
        {'name': 'id', 'label': 'ID', 'field': 'id', 'required': True, 'align': 'left'},
        {'name': 'charter', 'label': 'Charter', 'field': 'charter', 'align': 'left'},
        {'name': 'tester', 'label': 'Tester(s)', 'field': 'tester', 'align': 'left'},
        {'name': 'start_time', 'label': 'Start Time', 'field': 'start_time', 'align': 'left'},
        {'name': 'duration', 'label': 'Duration', 'field': 'duration', 'align': 'center'},
        {'name': 't_metric', 'label': 'T%', 'field': 't_metric', 'align': 'center'},
        {'name': 'b_metric', 'label': 'B%', 'field': 'b_metric', 'align': 'center'},
        {'name': 's_metric', 'label': 'S%', 'field': 's_metric', 'align': 'center'},
        {'name': 'status', 'label': 'Status', 'field': 'status', 'align': 'center'},
        {'name': 'actions', 'label': 'Actions', 'field': 'actions', 'align': 'center'},
    ]
    
    # Sample data (will be replaced with database data)
    rows = [
        {
            'id': 1,
            'charter': 'Test login functionality',
            'tester': 'John Doe',
            'start_time': '2024-01-15 09:00',
            'duration': '60 min',
            't_metric': 70,
            'b_metric': 20,
            's_metric': 10,
            'status': 'Completed',
            'actions': 'Edit | View | Delete'
        },
        {
            'id': 2,
            'charter': 'Explore payment workflow',
            'tester': 'Jane Smith',
            'start_time': '2024-01-15 14:00',
            'duration': '90 min',
            't_metric': 60,
            'b_metric': 30,
            's_metric': 10,
            'status': 'In Progress',
            'actions': 'Edit | View | Delete'
        }
    ]
    
    table = ui.table(columns=columns, rows=rows, row_key='id').classes('w-full')
    table.add_slot('body-cell-actions', '''
        <q-td :props="props">
            <q-btn flat dense color="primary" label="Edit" />
            <q-btn flat dense color="secondary" label="View" />
            <q-btn flat dense color="negative" label="Delete" />
        </q-td>
    ''')

def export_json():
    """Export sessions to JSON format"""
    ui.notify('Exporting sessions to JSON...', type='info')

def export_mindmap():
    """Export sessions to mind map format"""
    ui.notify('Exporting sessions to mind map...', type='info')

def group_by_tags():
    """Group sessions by tags"""
    ui.notify('Grouping sessions by tags...', type='info')
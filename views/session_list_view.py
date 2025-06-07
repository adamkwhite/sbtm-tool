"""
Session list view for browsing and managing session reports
"""

from nicegui import ui
from database.models import get_db, Session

def create_session_list_view():
    """Create the session list view"""
    
    ui.label('Session List').classes('text-h4 mb-4')
    
    # Create containers that can be updated
    stats_container = ui.column()
    table_container = ui.column()
    
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
    
    # Define data loading functions first
    def load_sessions():
        try:
            db = next(get_db())
            sessions = db.query(Session).all()
            rows = []
            
            for session in sessions:
                rows.append({
                    'id': session.id,
                    'charter': session.local_charter[:50] + '...' if session.local_charter and len(session.local_charter) > 50 else session.local_charter or 'No charter',
                    'tester': 'TBD',  # Will need to join with testers
                    'start_time': session.start_time.strftime('%Y-%m-%d %H:%M') if session.start_time else 'Not set',
                    'duration': f'{session.duration} min' if session.duration else 'Not set',
                    't_metric': session.t_metric,
                    'b_metric': session.b_metric,
                    's_metric': session.s_metric,
                    'status': session.status,
                    'actions': 'Edit | View | Delete'
                })
            
            return rows
        except Exception as e:
            ui.notify(f'Error loading sessions: {str(e)}', type='negative')
            return []
        finally:
            db.close()

    def calculate_stats(sessions_data):
        if not sessions_data:
            return {
                'total': 0, 'completed': 0, 'avg_t': 0, 'avg_b': 0, 'avg_s': 0, 'total_hours': 0
            }
        
        total = len(sessions_data)
        completed = len([s for s in sessions_data if s['status'] == 'Completed'])
        avg_t = sum(s['t_metric'] for s in sessions_data) / total if total > 0 else 0
        avg_b = sum(s['b_metric'] for s in sessions_data) / total if total > 0 else 0
        avg_s = sum(s['s_metric'] for s in sessions_data) / total if total > 0 else 0
        
        # Calculate total hours from duration strings
        total_minutes = 0
        for s in sessions_data:
            duration_str = s['duration']
            if duration_str != 'Not set' and 'min' in duration_str:
                total_minutes += int(duration_str.replace(' min', ''))
        total_hours = total_minutes / 60
        
        return {
            'total': total, 'completed': completed, 'avg_t': avg_t, 'avg_b': avg_b, 
            'avg_s': avg_s, 'total_hours': total_hours
        }

    # Define table columns
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

    # Define refresh function
    def refresh_data():
        """Refresh session data without reloading page"""
        # Clear containers
        stats_container.clear()
        table_container.clear()
        
        # Reload data
        rows = load_sessions()
        stats = calculate_stats(rows)
        
        # Rebuild stats
        with stats_container:
            with ui.card().classes('w-full p-4 mb-4'):
                ui.label('Session Statistics').classes('text-h6 mb-2')
                
                with ui.row().classes('w-full gap-8'):
                    with ui.column():
                        ui.label(f'Total Sessions: {stats["total"]}').classes('text-lg')
                        ui.label(f'Completed: {stats["completed"]}').classes('text-lg')
                    
                    with ui.column():
                        ui.label(f'Avg T Metric: {stats["avg_t"]:.1f}%').classes('text-lg')
                        ui.label(f'Avg B Metric: {stats["avg_b"]:.1f}%').classes('text-lg')
                    
                    with ui.column():
                        ui.label(f'Avg S Metric: {stats["avg_s"]:.1f}%').classes('text-lg')
                        ui.label(f'Total Hours: {stats["total_hours"]:.1f}').classes('text-lg')
        
        # Rebuild table
        with table_container:
            table = ui.table(columns=columns, rows=rows, row_key='id').classes('w-full')
            table.add_slot('body-cell-actions', '''
                <q-td :props="props">
                    <q-btn flat dense color="primary" label="Edit" />
                    <q-btn flat dense color="secondary" label="View" />
                    <q-btn flat dense color="negative" label="Delete" />
                </q-td>
            ''')
        
        ui.notify('Session list refreshed', type='positive')

    # Action buttons
    with ui.row().classes('w-full gap-2 mb-4'):
        ui.button('New Session', on_click=lambda: ui.notify('Navigate to session view')).props('color=primary')
        ui.button('Refresh', on_click=refresh_data).props('outlined')
        ui.button('Export to JSON', on_click=export_json).props('outlined')
        ui.button('Export to Mind Map', on_click=export_mindmap).props('outlined')
        ui.button('Group by Tags', on_click=group_by_tags).props('outlined')
    
    # Initial load of data
    refresh_data()

def export_json():
    """Export sessions to JSON format"""
    ui.notify('Exporting sessions to JSON...', type='info')

def export_mindmap():
    """Export sessions to mind map format"""
    ui.notify('Exporting sessions to mind map...', type='info')

def group_by_tags():
    """Group sessions by tags"""
    ui.notify('Grouping sessions by tags...', type='info')
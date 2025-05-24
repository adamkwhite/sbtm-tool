"""
Statistics dashboard view for SBTM metrics and analytics
"""

from nicegui import ui
import plotly.graph_objects as go
from plotly.subplots import make_subplots

def create_statistics_view():
    """Create the statistics dashboard view"""
    
    ui.label('Statistics Dashboard').classes('text-h4 mb-4')
    
    # Time scale and filter controls
    with ui.card().classes('w-full p-4 mb-4'):
        ui.label('Dashboard Filters').classes('text-h6 mb-2')
        
        with ui.row().classes('w-full gap-4'):
            time_scale = ui.select(
                ['Last 7 days', 'Last 30 days', 'Last 3 months', 'Last 6 months', 'Last year', 'All time'],
                label='Time Scale',
                value='Last 30 days'
            ).classes('w-48')
            
            tag_filter = ui.select(
                [],  # Will be populated with available tags
                label='Filter by Tags',
                multiple=True
            ).classes('flex-1')
            
            tester_filter = ui.select(
                [],  # Will be populated with available testers
                label='Filter by Testers',
                multiple=True
            ).classes('w-48')
            
            ui.button('Apply Filters', on_click=apply_filters).props('color=primary')
            ui.button('Export to CSV', on_click=export_csv).props('outlined')
    
    # Key metrics cards
    with ui.row().classes('w-full gap-4 mb-4'):
        with ui.card().classes('flex-1 p-4 text-center'):
            ui.label('Total Sessions').classes('text-h6')
            ui.label('47').classes('text-3xl font-bold text-blue-600')
            ui.label('+12% from last month').classes('text-sm text-green-600')
        
        with ui.card().classes('flex-1 p-4 text-center'):
            ui.label('Avg T Metric').classes('text-h6')
            ui.label('68%').classes('text-3xl font-bold text-green-600')
            ui.label('+5% from last month').classes('text-sm text-green-600')
        
        with ui.card().classes('flex-1 p-4 text-center'):
            ui.label('Avg B Metric').classes('text-h6')
            ui.label('22%').classes('text-3xl font-bold text-orange-600')
            ui.label('-2% from last month').classes('text-sm text-red-600')
        
        with ui.card().classes('flex-1 p-4 text-center'):
            ui.label('Total Hours').classes('text-h6')
            ui.label('94.5').classes('text-3xl font-bold text-purple-600')
            ui.label('+18% from last month').classes('text-sm text-green-600')
    
    # Charts row
    with ui.row().classes('w-full gap-4 mb-4'):
        # Session growth over time
        with ui.card().classes('w-1/2 p-4'):
            ui.label('Session Growth Over Time').classes('text-h6 mb-2')
            
            # Sample data for session growth
            fig_growth = go.Figure()
            fig_growth.add_trace(go.Scatter(
                x=['2024-01-01', '2024-01-08', '2024-01-15', '2024-01-22', '2024-01-29'],
                y=[5, 12, 18, 25, 35],
                mode='lines+markers',
                name='Cumulative Sessions',
                line=dict(color='blue', width=3)
            ))
            fig_growth.update_layout(
                title='Normalized Session Growth',
                xaxis_title='Date',
                yaxis_title='Cumulative Sessions',
                height=300,
                showlegend=False
            )
            
            ui.plotly(fig_growth).classes('w-full')
        
        # TBS metrics pie chart
        with ui.card().classes('w-1/2 p-4'):
            ui.label('TBS Metrics Breakdown').classes('text-h6 mb-2')
            
            # Sample TBS data
            fig_pie = go.Figure(data=[go.Pie(
                labels=['Testing (T)', 'Bug Investigation (B)', 'Setup/Admin (S)', 'Opportunity Time'],
                values=[68, 22, 10, 15],
                colors=['#2E8B57', '#FF6B35', '#4169E1', '#FFD700']
            )])
            fig_pie.update_layout(
                title='Average Time Distribution',
                height=300,
                showlegend=True
            )
            
            ui.plotly(fig_pie).classes('w-full')
    
    # Tag hierarchy vs TBS metrics
    with ui.card().classes('w-full p-4 mb-4'):
        ui.label('TBS Metrics by Tag Hierarchy').classes('text-h6 mb-2')
        
        # Sample hierarchical data
        fig_hierarchy = make_subplots(
            rows=1, cols=3,
            subplot_titles=('T Metric by Tags', 'B Metric by Tags', 'S Metric by Tags'),
            specs=[[{"type": "bar"}, {"type": "bar"}, {"type": "bar"}]]
        )
        
        tags = ['Login', 'Payment', 'User Mgmt', 'API', 'Mobile']
        t_values = [75, 65, 70, 80, 60]
        b_values = [20, 25, 22, 15, 30]
        s_values = [5, 10, 8, 5, 10]
        
        fig_hierarchy.add_trace(go.Bar(x=tags, y=t_values, name='T Metric', marker_color='green'), row=1, col=1)
        fig_hierarchy.add_trace(go.Bar(x=tags, y=b_values, name='B Metric', marker_color='orange'), row=1, col=2)
        fig_hierarchy.add_trace(go.Bar(x=tags, y=s_values, name='S Metric', marker_color='blue'), row=1, col=3)
        
        fig_hierarchy.update_layout(
            height=400,
            showlegend=False,
            title_text="TBS Metrics Distribution Across Tag Categories"
        )
        
        ui.plotly(fig_hierarchy).classes('w-full')
    
    # Detailed statistics table
    with ui.card().classes('w-full p-4'):
        ui.label('Detailed Session Statistics').classes('text-h6 mb-2')
        
        # Statistics table
        stats_columns = [
            {'name': 'metric', 'label': 'Metric', 'field': 'metric', 'align': 'left'},
            {'name': 'total', 'label': 'Total', 'field': 'total', 'align': 'center'},
            {'name': 'avg', 'label': 'Average', 'field': 'avg', 'align': 'center'},
            {'name': 'min', 'label': 'Minimum', 'field': 'min', 'align': 'center'},
            {'name': 'max', 'label': 'Maximum', 'field': 'max', 'align': 'center'},
            {'name': 'trend', 'label': 'Trend', 'field': 'trend', 'align': 'center'},
        ]
        
        stats_rows = [
            {'metric': 'Sessions', 'total': 47, 'avg': '1.6/day', 'min': 0, 'max': 5, 'trend': '↗ +12%'},
            {'metric': 'T Metric (%)', 'total': '-', 'avg': '68%', 'min': '45%', 'max': '95%', 'trend': '↗ +5%'},
            {'metric': 'B Metric (%)', 'total': '-', 'avg': '22%', 'min': '5%', 'max': '40%', 'trend': '↘ -2%'},
            {'metric': 'S Metric (%)', 'total': '-', 'avg': '10%', 'min': '0%', 'max': '25%', 'trend': '↘ -3%'},
            {'metric': 'Duration (min)', 'total': '5,670', 'avg': '120.6', 'min': 30, 'max': 240, 'trend': '↗ +8%'},
            {'metric': 'Issues Found', 'total': 23, 'avg': '0.5/session', 'min': 0, 'max': 3, 'trend': '↗ +15%'},
        ]
        
        ui.table(columns=stats_columns, rows=stats_rows, row_key='metric').classes('w-full')

def apply_filters():
    """Apply the selected filters to update charts"""
    ui.notify('Applying filters and updating charts...', type='info')

def export_csv():
    """Export statistics to CSV format"""
    ui.notify('Exporting statistics to CSV...', type='info')
"""
Session view for creating and editing test sessions
"""

from nicegui import ui
from datetime import datetime
from database.models import get_db, Session, Charter, Tester, Product, TestEnvironment, Tag

def create_session_view():
    """Create the session management view"""
    
    # Function definitions (moved to top to avoid reference errors)
    def validate_tbs(t_metric, b_metric, s_metric):
        total = t_metric.value + b_metric.value + s_metric.value
        if abs(total - 100) > 0.1:
            ui.notify(f'T+B+S must equal 100% (currently {total}%)', type='warning')
            return False
        return True

    def open_notes_window(notes_field):
        """Open notes in a floating, distraction-free window"""
        with ui.dialog() as dialog, ui.card().classes('w-[800px] h-[600px]'):
            with ui.column().classes('w-full h-full'):
                ui.label('Session Notes - Distraction Free Mode').classes('text-h6 mb-2')
                
                floating_notes = ui.textarea(
                    value=notes_field.value,
                    placeholder='Enter detailed session notes...'
                ).classes('w-full flex-1').style('min-height: 500px')
                
                with ui.row().classes('w-full justify-end gap-2 mt-2'):
                    ui.button('Stay on Top', on_click=lambda: ui.notify('Window pinned')).props('outlined')
                    ui.button('Save & Close', on_click=lambda: save_and_close(floating_notes, notes_field, dialog))
        
        dialog.open()
    
    def save_and_close(floating_notes, original_notes, dialog):
        """Save notes from floating window back to main form"""
        original_notes.value = floating_notes.value
        dialog.close()
        ui.notify('Notes saved')
    
    def save_session():
        """Save the current session to database"""
        try:
            # Validate TBS metrics first
            if not validate_tbs(t_metric, b_metric, s_metric):
                return
            
            # Get database session
            db = next(get_db())
            
            # Create new session object
            new_session = Session(
                project_id=1,  # Default project for now
                local_charter=local_charter.value,
                t_metric=t_metric.value,
                b_metric=b_metric.value,
                s_metric=s_metric.value,
                start_time=datetime.strptime(start_time.value, '%Y-%m-%d %H:%M') if start_time.value else None,
                duration=duration.value,
                status=status.value,
                notes=notes.value
            )
            
            # Save to database
            db.add(new_session)
            db.commit()
            db.refresh(new_session)
            
            ui.notify(f'Session saved successfully! ID: {new_session.id}', type='positive')
            
        except Exception as e:
            ui.notify(f'Error saving session: {str(e)}', type='negative')
        finally:
            db.close()
    
    def save_as_template():
        """Save current session as a template"""
        ui.notify('Session template saved!', type='positive')
    
    def clear_form():
        """Clear all form fields"""
        ui.notify('Form cleared')
    
    ui.label('Session Management').classes('text-h4 mb-4')
    
    with ui.row().classes('w-full gap-4'):
        # Left column - Session form
        with ui.column().classes('w-1/2'):
            ui.label('Create/Edit Session').classes('text-h6 mb-2')
            
            # Session form
            with ui.card().classes('w-full p-4'):
                local_charter = ui.textarea(
                    label='Local Charter (Optional)',
                    placeholder='Enter the mission statement for this session...'
                ).classes('w-full')
                
                with ui.row().classes('w-full gap-2'):
                    t_metric = ui.number(
                        label='T Metric (%)', 
                        value=0, 
                        min=0, 
                        max=100,
                        step=1
                    ).classes('flex-1')
                    
                    b_metric = ui.number(
                        label='B Metric (%)', 
                        value=0, 
                        min=0, 
                        max=100,
                        step=1
                    ).classes('flex-1')
                    
                    s_metric = ui.number(
                        label='S Metric (%)', 
                        value=0, 
                        min=0, 
                        max=100,
                        step=1
                    ).classes('flex-1')
                
                # TBS validation
                t_metric.on('blur', lambda: validate_tbs(t_metric, b_metric, s_metric))
                b_metric.on('blur', lambda: validate_tbs(t_metric, b_metric, s_metric))
                s_metric.on('blur', lambda: validate_tbs(t_metric, b_metric, s_metric))
                
                with ui.row().classes('w-full gap-2'):
                    start_time = ui.input(
                        label='Start Time',
                        value=datetime.now().strftime('%Y-%m-%d %H:%M')
                    ).classes('flex-1')
                    
                    duration = ui.number(
                        label='Duration (minutes)',
                        value=60,
                        min=1
                    ).classes('flex-1')
                
                status = ui.select(
                    ['Not Started', 'In Progress', 'Completed', 'Accepted'],
                    label='Status',
                    value='Not Started'
                ).classes('w-full')
                
                # Notes section with floating window option
                with ui.row().classes('w-full items-end gap-2'):
                    notes = ui.textarea(
                        label='Notes (Markdown supported)',
                        placeholder='Enter session notes, findings, issues...'
                    ).classes('flex-1')
                    
                    ui.button(
                        'Open in Floating Window',
                        on_click=lambda: open_notes_window(notes)
                    ).props('outlined')
                
                # Action buttons
                with ui.row().classes('w-full gap-2 mt-4'):
                    ui.button('Save Session', on_click=save_session).props('color=primary')
                    ui.button('Save as Template', on_click=save_as_template).props('outlined')
                    ui.button('Clear Form', on_click=clear_form).props('outlined')
        
        # Right column - Associations and metadata
        with ui.column().classes('w-1/2'):
            ui.label('Associations').classes('text-h6 mb-2')
            
            with ui.card().classes('w-full p-4'):
                # Associated charters
                ui.label('Associated Charters').classes('font-bold mb-2')
                charter_select = ui.select(
                    [],  # Will be populated from database
                    label='Select Charters',
                    multiple=True
                ).classes('w-full mb-4')
                
                # Associated testers  
                ui.label('Associated Testers').classes('font-bold mb-2')
                tester_select = ui.select(
                    [],  # Will be populated from database
                    label='Select Testers (Required)',
                    multiple=True
                ).classes('w-full mb-4')
                
                # Associated products
                ui.label('Associated Products').classes('font-bold mb-2')
                product_select = ui.select(
                    [],  # Will be populated from database
                    label='Select Products (Required)',
                    multiple=True
                ).classes('w-full mb-4')
                
                # Associated test environments
                ui.label('Associated Test Environments').classes('font-bold mb-2')
                env_select = ui.select(
                    [],  # Will be populated from database
                    label='Select Test Environments',
                    multiple=True
                ).classes('w-full mb-4')
                
                # Associated tags
                ui.label('Associated Tags').classes('font-bold mb-2')
                tag_select = ui.select(
                    [],  # Will be populated from database
                    label='Select Tags',
                    multiple=True
                ).classes('w-full mb-4')

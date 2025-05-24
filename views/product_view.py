"""
Product view for managing product repository
"""

from nicegui import ui

def create_product_view():
    """Create the product management view"""
    
    ui.label('Product Management').classes('text-h4 mb-4')
    
    with ui.row().classes('w-full gap-4'):
        # Left column - Product list
        with ui.column().classes('w-1/2'):
            ui.label('Product Repository').classes('text-h6 mb-2')
            
            # Search and filter controls
            with ui.row().classes('w-full gap-2 mb-4'):
                search_input = ui.input(
                    label='Search products',
                    placeholder='Search by name or description...'
                ).classes('flex-1')
                
                ui.button('Search', on_click=search_products).props('color=primary')
            
            with ui.row().classes('w-full gap-2 mb-4'):
                filter_tags = ui.select(
                    [],  # Will be populated with available tags
                    label='Filter by Tags',
                    multiple=True
                ).classes('flex-1')
                
                sort_by = ui.select(
                    ['Name', 'Version', 'Created Date', 'Sessions Count'],
                    label='Sort by',
                    value='Name'
                ).classes('w-48')
            
            # Product list
            with ui.card().classes('w-full'):
                ui.label('Products').classes('font-bold p-4')
                
                # Sample product list (will be replaced with database data)
                product_list = ui.list().classes('w-full')
                
                with product_list:
                    with ui.item(on_click=lambda: select_product(1)):
                        with ui.item_section():
                            ui.item_label('E-commerce Web App')
                            ui.item_label('Version: 2.1.0 | Sessions: 25').props('caption')
                    
                    with ui.item(on_click=lambda: select_product(2)):
                        with ui.item_section():
                            ui.item_label('Mobile Shopping App')
                            ui.item_label('Version: 1.5.2 | Sessions: 18').props('caption')
                    
                    with ui.item(on_click=lambda: select_product(3)):
                        with ui.item_section():
                            ui.item_label('Payment Gateway API')
                            ui.item_label('Version: 3.0.1 | Sessions: 12').props('caption')
        
        # Right column - Product editor
        with ui.column().classes('w-1/2'):
            ui.label('Product Details').classes('text-h6 mb-2')
            
            with ui.card().classes('w-full p-4'):
                # Product form
                product_name = ui.input(
                    label='Product Name',
                    placeholder='Enter product name...'
                ).classes('w-full mb-4')
                
                product_version = ui.input(
                    label='Version',
                    placeholder='e.g., 1.0.0, v2.1, beta-3...'
                ).classes('w-full mb-4')
                
                product_description = ui.textarea(
                    label='Product Description',
                    placeholder='Enter detailed description of the product...'
                ).classes('w-full mb-4').style('min-height: 150px')
                
                # Associated tags
                product_tags = ui.select(
                    [],  # Will be populated with available tags
                    label='Associated Tags',
                    multiple=True
                ).classes('w-full mb-4')
                
                # Statistics section
                ui.separator().classes('my-4')
                ui.label('Product Statistics').classes('font-bold mb-2')
                
                with ui.row().classes('w-full gap-4'):
                    with ui.column():
                        ui.label('Total Sessions: 0').classes('text-lg')
                        ui.label('Active Sessions: 0').classes('text-lg')
                    
                    with ui.column():
                        ui.label('Issues Found: 0').classes('text-lg')
                        ui.label('Total Testing Hours: 0').classes('text-lg')
                
                # Associated sessions (read-only)
                ui.separator().classes('my-4')
                ui.label('Recent Sessions').classes('font-bold mb-2')
                
                # Sessions table for this product
                session_columns = [
                    {'name': 'id', 'label': 'ID', 'field': 'id'},
                    {'name': 'charter', 'label': 'Charter', 'field': 'charter'},
                    {'name': 'tester', 'label': 'Tester', 'field': 'tester'},
                    {'name': 'date', 'label': 'Date', 'field': 'date'},
                    {'name': 'status', 'label': 'Status', 'field': 'status'},
                ]
                
                session_rows = [
                    {'id': 1, 'charter': 'Test checkout flow', 'tester': 'John Doe', 'date': '2024-01-15', 'status': 'Completed'},
                    {'id': 2, 'charter': 'Explore user registration', 'tester': 'Jane Smith', 'date': '2024-01-14', 'status': 'In Progress'},
                ]
                
                ui.table(columns=session_columns, rows=session_rows, row_key='id').classes('w-full')
                
                # Action buttons
                with ui.row().classes('w-full gap-2 mt-4'):
                    ui.button('Save Product', on_click=save_product).props('color=primary')
                    ui.button('Delete Product', on_click=delete_product).props('color=negative outlined')
                    ui.button('Clear', on_click=clear_form).props('outlined')
    
    # Action buttons for list operations
    with ui.row().classes('w-full gap-2 mt-4'):
        ui.button('Add New Product', on_click=add_new_product).props('color=primary')
        ui.button('Export to JSON', on_click=export_json).props('outlined')
        ui.button('Export to XML', on_click=export_xml).props('outlined')
        ui.button('Group by Tags', on_click=group_by_tags).props('outlined')

def search_products():
    """Search products based on input"""
    ui.notify('Searching products...', type='info')

def select_product(product_id):
    """Select a product from the list for editing"""
    ui.notify(f'Selected product {product_id}', type='info')

def save_product():
    """Save the current product"""
    ui.notify('Product saved successfully!', type='positive')

def delete_product():
    """Delete the current product"""
    ui.notify('Product deleted', type='warning')

def clear_form():
    """Clear the product form"""
    ui.notify('Form cleared', type='info')

def add_new_product():
    """Add a new product"""
    ui.notify('Adding new product...', type='info')

def export_json():
    """Export products to JSON format"""
    ui.notify('Exporting products to JSON...', type='info')

def export_xml():
    """Export products to XML format"""
    ui.notify('Exporting products to XML...', type='info')

def group_by_tags():
    """Group products by tags"""
    ui.notify('Grouping products by tags...', type='info')
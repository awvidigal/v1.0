import dash
import dash_bootstrap_components as dbc
from dash import html, dcc, callback, Input, Output

dash.register_page(
    __name__,
    name='Clientes',
    path='/clientes'
)

def layout():
    layout = dbc.Container(
        children=[
            dbc.Row(
                children=
                    dbc.Input(
                        id='search-input', 
                        placeholder='Busca...', 
                        type='text',
                        size='md',
                        class_name='text-field-search',
                        debounce=False,
                        html_size='100',
                        # list='lista com os nomes dos clientes no db'
                    ),
            ),
            # dbc.Row(
            #     children=['tabela do db com os clientes
            #     ]
            # ),

            # dbc.Row(
            #     children=[
            #         'pagina do db com até 10 resultados'
            #     ]
            # )

            dbc.Button(
                    children=html.I(className='fa-solid fa-user-plus'),
                    id='btn-add-client',
                    class_name='btn-client'
                )
            
        ]
    )
    return layout
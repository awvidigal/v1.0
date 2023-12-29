import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
import dash_bootstrap_components as dbc
import dash

from dash import Dash, dcc, html, Input, Output
from navbar import createNavBar

NAVBAR = createNavBar()
FA621 = "https://use.fontawesome.com/releases/v6.2.1/css/all.css"

app = Dash(
    __name__,
    use_pages=True,
    suppress_callback_exceptions=True,
    external_stylesheets=[
        dbc.themes.LUX,
        FA621
    ]
)



# app.layout = html.Div(
#     children = [
#         # html.Img(src='/assets/logo_negativo.png', id='siteLogo'),
#         html.Div(
#             children=[                
#                 html.A(children='Home', href='/', className='menuLink'),
#                 html.A(children='Clientes', href='pages\clientes.py', className='menuLink'),
#                 html.A(children='UCs', href='/', className='menuLink'),
#                 html.A(children='Orçamentos', href='/', className='menuLink'),
#                 html.A(children='Monitoramento', href='/', className='menuLink')
#             ],
#             className='generalDiv',
#             id='menuBar'
#         )
#     ]
# )

# navbar = dbc.NavbarSimple(
#     children=[
#         html.Img(src='/assets/logo_negativo.png', id='siteLogo'),
#         dbc.NavItem(
#             children=[
#                 dbc.NavLink('Home', href='#', class_name='menuLink'),
#                 dbc.NavLink('Clientes', href='#', class_name='menuLink'),
#                 dbc.NavLink('UCs', href='#', class_name='menuLink'),
#                 dbc.NavLink('Orçamentos', href='#', class_name='menuLink'),
#                 dbc.NavLink('Monitoramento', href='#', class_name='menuLink')
#             ],
#             class_name='navbar'
#         ),
#         dbc.DropdownMenu(
#             children=[
#                 dbc.DropdownMenuItem('Perfil', header=True),
#                 dbc.DropdownMenuItem('Configurações', href='#')
#             ],
#             nav=True,
#             in_navbar=True,
#             label='Menu'
#         ),
#     ],
#     id='menuBar',
#     color='primary',
#     dark=True,
#     fluid=True
# )

app.layout = dcc.Loading(
    id='loading_page_content',
    children=[
        html.Div(
            [
                NAVBAR,
                dash.page_container
            ],
        ), 
        # dbc.Modal(
        #     children=[
        #         dbc.ModalHeader(dbc.ModalTitle('Novo Cliente')),
        #         dbc.ModalBody('Formulario de cadastro do cliente'),
        #         dbc.ModalFooter(dbc.Button(children='Inserir Cliente', id='btn-insert', n_clicks=0))
        #     ],
        #     id='new-client-modal',
        #     is_open=False                
        # )
    ],
    color='primary',
    fullscreen=True
)

# @app.callback(
#     Output(component_id='new-client-modal', component_property='is_open'),
#     Input(component_id='btn-add-cliente', component_property='n_clicks'),
# )
# def showModal(inputValue):
#     return 'is_open'

if __name__ == '__main__':
    app.run(debug=True)
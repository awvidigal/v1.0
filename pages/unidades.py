import sqlite3 as sql
import pandas as pd
import numpy as np
import datetime
import dash
import dash_bootstrap_components as dbc
from dash import html, callback, Input, Output, State

dash.register_page(
    __name__,
    name='UCs',
    path='/unidades'
)

conn = sql.connect('c:/Users/vidig/OneDrive/Python/agv/v1.0/agv.db')
cursor = conn.cursor()
cursor.execute(
    '''
        SELECT nome  
        FROM concessionarias;
    '''
)

utilities = cursor.fetchall()

cursor.execute(
    '''
        SELECT
            IFNULL(nome, 'NaN') as nome,
            IFNULL(razao_social, 'NaN') as razao_social
        FROM clientes;
    '''
)
clients = cursor.fetchall()
conn.close()

utilities = [item[0] for item in utilities]

clientsColumns = ['Nome', 'Razão Social']
clients = pd.DataFrame(data=clients, columns=clientsColumns)
clients.replace('NaN', np.nan, inplace=True)  
clients['Nome'] = clients['Nome'].astype('string')  
clients['Razão Social'] = clients['Razão Social'].astype('string')
clients = pd.Series(clients[clientsColumns].sum(1))
clients = [item for item in clients]

def layout():
    layout = dbc.Container(
        # html.H1('pagina de UCs')
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
                    justify='center',
                    
            ),

            dbc.Button(
                children=html.I(className='fa-solid fa-user-plus'),
                id='btn-add-client',
                n_clicks=0
            ),

            dbc.Modal(
                children=[
                    dbc.ModalHeader(dbc.ModalTitle('Nova UC')),
                    dbc.ModalBody(
                        children=[
                            dbc.Row(
                                children=[
                                    dbc.Col(
                                        children=[
                                            dbc.Select(
                                                class_name='input-field-modal',
                                                id='select-cliente',
                                                placeholder='Cliente',
                                                options=[{'label':client, 'value':client} for client in clients]
                                            ),
                                        ]
                                    ), 

                                    dbc.Col(
                                        children=[
                                            dbc.Select(
                                                class_name='input-field-modal',
                                                id='select-concessionaria',
                                                placeholder='Concessionária',
                                                options=[{'label':utility, 'value':utility} for utility in utilities]
                                            )
                                        ]
                                    ),

                                    dbc.Col(
                                        children=[
                                            dbc.Input(
                                                class_name='input-field-modal',
                                                id='input-uc',
                                                placeholder='Número da UC'
                                            )

                                        ]
                                    ),
                                    

                                     
                                ]
                            )
                            
                        ],
                        
                    )
                ],
                is_open=True,
                id='modal-cadastro-ucs'
            )
        ]
    )

    return layout
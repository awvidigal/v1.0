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

cursor.execute(
    '''
        SELECT subgrupo
        FROM subgrupos;
    '''
)
subgroups = cursor.fetchall()

cursor.execute(
    '''
        SELECT modalidade
        FROM modalidades;
    '''
)
mod = cursor.fetchall()
conn.close()

utilities = [item[0] for item in utilities]
subgroups = [item[0] for item in subgroups]
mod = [item[0] for item in mod]

clientsColumns = ['Nome', 'Razão Social']
clients = pd.DataFrame(data=clients, columns=clientsColumns)
clients.replace('NaN', np.nan, inplace=True)  
clients['Nome'] = clients['Nome'].astype('string')  
clients['Razão Social'] = clients['Razão Social'].astype('string')
clients = pd.Series(clients[clientsColumns].sum(1))
clients = [item for item in clients]

# abre o modal de cadastro de uc
@callback(
    [
        Output(component_id='modal-cadastro-ucs', component_property='is_open'),
        # inserir os valores dos inputs como outputs de forma a limpar os campos quando o modal for aberto ou fechado
    ],
    [
        Input(component_id='btn-add-client', component_property='n_clicks'),
        Input(component_id='btn-close', component_property='n_clicks')
    ],
    [
        State(component_id='modal-cadastro-ucs', component_property='is_open')
    ],
    prevent_initial_call=True
)
def showModal(n1, n2, is_open):
    if n1 or n2:
        return [not is_open]
    return [is_open]

# altera os status dos inputs de demanda
@callback(
    [
        Output(component_id='input-demanda', component_property='disabled'),
        Output(component_id='input-demanda-fponta', component_property='disabled'),
    ],
    [
        Input(component_id='select-subgrupo', component_property='value'),
        Input(component_id='select-modalidade', component_property='value')
    ],
    prevent_initial_call=True
)
def disabledInputs(selectSubgrupo, selectModalidade):
    baixaTensão=[
        'B1',
        'B2',
        'B3'
    ]

    allOutputs = [True, True]

    for grupo in baixaTensão:
        if selectSubgrupo == grupo:
            for pos in allOutputs:
                allOutputs[pos] = True
            break
        else:
            allOutputs[0] = False

    if selectModalidade == 'Azul':
        allOutputs[1] = False
    
    return allOutputs

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
                    dbc.ModalHeader(dbc.ModalTitle('Cadastro de UC')),
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
                                        ],
                                        width={'size':8, 'offset':0}
                                    ), 

                                    dbc.Col(
                                        children=[
                                            dbc.Select(
                                                class_name='input-field-modal',
                                                id='select-concessionaria',
                                                placeholder='Concessionária',
                                                options=[{'label':utility, 'value':utility} for utility in utilities]
                                            )
                                        ],
                                        width={'size':4, 'offset':0}
                                    ),                                       
                                ]
                            ),

                            html.Br(),

                            dbc.Row(
                                children=[
                                    dbc.Col(
                                        children=[
                                            dbc.Input(
                                                class_name='input-field-modal',
                                                id='input-uc',
                                                placeholder='Número da UC'
                                            )
                                        ],
                                        width={'size':5, 'offset':0}
                                    ),

                                    dbc.Col(
                                        children=[
                                            dbc.Select(
                                                class_name='input-field-modal',
                                                id='select-subgrupo',
                                                placeholder='Subgrupo',
                                                options=[{'label':subgroup, 'value':subgroup} for subgroup in subgroups]
                                            )
                                        ],
                                        width={'size':3, 'offset':0}
                                    ),

                                    dbc.Col(
                                        children=[
                                            dbc.Select(
                                                class_name='input-field-modal',
                                                id='select-modalidade',
                                                placeholder='Modalidade',
                                                options=[{'label':modalidade, 'value':modalidade} for modalidade in mod]
                                            )
                                        ],
                                        width={'size':4, 'offset':0}
                                    ) 
                                ]
                            ),
                            html.Br(),

                            dbc.Row(
                                children=[
                                    dbc.Col(
                                        dbc.Input(
                                            class_name='input-field-modal',
                                            id='input-demanda',
                                            # placeholder deve ser alterado no callback
                                            placeholder='Demanda contratada (kW)',
                                            type='number'
                                        )
                                    ),

                                    dbc.Col(
                                        dbc.Input(
                                            class_name='input-field-modal',
                                            id='input-demanda-fponta',
                                            placeholder='Demanda contratada fora ponta(kW)',
                                            type='number',
                                            # disabled deve ser alterado no callback
                                            disabled=False
                                        )
                                    )
                                ]
                            ),
                            html.Br(),
                            
                            dbc.ModalFooter(
                                children=[
                                    dbc.Button(children='Fechar', id='btn-close', n_clicks=0),
                                    dbc.Button(children='Inserir', id='btn-insert', n_clicks=0)
                                ]
                            )    
                        ],
                    )
                ],
                is_open=False,
                id='modal-cadastro-ucs',
                size='lg'
            )
        ]
    )

    return layout
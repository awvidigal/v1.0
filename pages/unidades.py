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
        Output(component_id='input-demanda',            component_property='placeholder'),
        Output(component_id='input-demanda',            component_property='disabled'),
        Output(component_id='input-demanda-ponta',      component_property='disabled'),
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

    allOutputs = [
        'Demanda Contratada (kW)',  # 0 - input-demanda             | placeholder
        True,                       # 1 - input-demanda             | disabled
        True,                       # 2 - input-demanda-ponta       | disabled
    ]

    for grupo in baixaTensão:
        if selectSubgrupo == grupo:
            for pos in range(1,len(allOutputs)):
                allOutputs[pos] = True            
            break
        else:
            allOutputs[1] = False

    if selectModalidade == 'Azul':
        allOutputs[2] = False
        allOutputs[0] = 'Demanda Fora Ponta (kW)'
    elif selectModalidade == 'Verde':
        allOutputs[0] = 'Demanda (kW)'
        allOutputs[2] = True
    
    return allOutputs

@callback(
    [
        Output(component_id='modal-aviso',              component_property='is_open'),
        Output(component_id='modal-err-field',          component_property='is_open'),
        Output(component_id='modal-err-uc',             component_property='is_open'),
        Output(component_id='select-cliente',           component_property='class_name'),
        Output(component_id='select-concessionaria',    component_property='class_name'),
        Output(component_id='input-uc',                 component_property='class_name'),
        Output(component_id='select-subgrupo',          component_property='class_name'),
        Output(component_id='select-modalidade',        component_property='class_name'),
        Output(component_id='input-demanda',            component_property='class_name'),
        Output(component_id='input-demanda-ponta',      component_property='class_name'),
    ],
    [
        Input(component_id='btn-insert',            component_property='n_clicks'),
        Input(component_id='btn-close-aviso',       component_property='n_clicks'),
        Input(component_id='btn-close-err-field',   component_property='n_clicks'),
        Input(component_id='btn-close-err-uc',      component_property='n_clicks'),
    ],
    [
        State(component_id='modal-aviso',           component_property='is_open'),
        State(component_id='modal-err-field',       component_property='is_open'),
        State(component_id='modal-err-uc',          component_property='is_open'),
        State(component_id='select-cliente',        component_property='value'),
        State(component_id='select-concessionaria', component_property='value'),
        State(component_id='input-uc',              component_property='value'),
        State(component_id='select-subgrupo',       component_property='value'),
        State(component_id='select-modalidade',     component_property='value'),
        State(component_id='input-demanda',         component_property='value'),
        State(component_id='input-demanda-ponta',   component_property='value'),
        State(component_id='input-demanda',         component_property='disabled'),
        State(component_id='input-demanda-ponta',   component_property='disabled'),
    ],
    prevent_initial_call=True
)
def cadastrarUc(btnInsertUc, btnCloseAviso, btnCloseErrField, btnCloseErrUC, 
                stateModalAviso, stateModalErrField, stateModalErrUC, stateClient, 
                stateUtilities, stateUC, stateGroup, stateModality, stateDemand, 
                statepDemand, stateDemandDisabled, statepDemandDisabled):
    '''
        As saídas estão organizadas em uma lista que é retornada ao final de cada execução. Estão numeradas da seguinte forma dentro dessa lista:
            modal-aviso             | is_open       -> 0
            modal-err-field         | is_open       -> 1
            modal-err-uc            | is_open       -> 2
            select-cliente          | class_name    -> 3
            select-concessionaria   | class_name    -> 4
            input-uc                | class_name    -> 5
            select-grupo            | class_name    -> 6
            select-modalidade       | class_name    -> 7
            input-demanda           | class_name    -> 8
            input-demanda-ponta     | class_name    -> 9
    '''

    allOutputs = [
        False,                  # 0 - modal-aviso               | is_open
        False,                  # 1 - modal-err-field           | is_open
        False,                  # 2 - modal-err-uc              | is_open
        'input-field-modal',    # 3 - select-cliente            | class_name
        'input-field-modal',    # 4 - select-concessionaria     | class_name
        'input-field-modal',    # 5 - input-uc                  | class_name
        'input-field-modal',    # 6 - select-grupo              | class_name
        'input-field-modal',    # 7 - select-modalidade         | class_name
        'input-field-modal',    # 8 - input-demanda             | class_name
        'input-field-modal',    # 9 - input-demanda-ponta       | class_name
    ]

    emptyFieldIndicator = False
    existsUC = None
    today = datetime.datetime.now()
    demand = None
    pDemand = None
    fpDemand = None

    if btnInsertUc is not None and btnInsertUc > 0:

        if not stateClient:
            allOutputs[3] = 'input-field-modal-error'
            emptyFieldIndicator = True
        else:
            allOutputs[3] = 'input-field-modal'
        
        if not stateUtilities:
            allOutputs[4] = 'input-field-modal-error'
            emptyFieldIndicator = True
        else:
            allOutputs[4] = 'input-field-modal'

        if not stateUC:
            allOutputs[5] = 'input-field-modal-error'
            emptyFieldIndicator = True
        else:
            allOutputs[5] = 'input-field-modal'

        if not stateGroup:
            emptyFieldIndicator = True
            allOutputs[6] = 'input-field-modal-error'
        else:
            allOutputs[6] = 'input-field-modal'

        if not stateModality:
            emptyFieldIndicator = True
            allOutputs[7] = 'input-field-modal-error'
        else:
            allOutputs[7] = 'input-field-modal'

        if not stateDemand and not stateDemandDisabled:
            emptyFieldIndicator = True
            allOutputs[8] = 'input-field-modal-error'
        else:
            allOutputs[8] = 'input-field-modal'

        if not statepDemand and not statepDemandDisabled:
            emptyFieldIndicator = True
            allOutputs[9] = 'input-field-modal-error'
        else:
            allOutputs[9] = 'input-field-modal'
        
        if emptyFieldIndicator:
            allOutputs[1] = not stateModalErrField
        elif btnCloseAviso is not None and btnCloseAviso > 0:
            allOutputs[0] = not stateModalAviso
        elif btnCloseErrField is not None and btnCloseErrField > 0:
            allOutputs[1] = not stateModalErrField
        elif btnCloseErrUC is not None and btnCloseErrUC > 0:
            allOutputs[2] = not stateModalErrUC
        else:
            if statepDemandDisabled:
                demand = stateDemand
            else:
                pDemand = statepDemand
                fpDemand = stateDemand
            # cadastra no db
            conn = sql.connect('c:/Users/vidig/OneDrive/Python/agv/v1.0/agv.db')
            cursor = conn.cursor()

            # verifica se a uc já existe
            existsUC = cursor.execute(
                f'''
                SELECT *
                FROM ucs
                WHERE uc = ?;
                ''', (stateUC,)
            ).fetchone()

            if existsUC is not None:
                allOutputs[2] = not stateModalErrUC
                conn.close()

            else:
                try:
                    cursor.execute(
                        '''
                            SELECT id
                            FROM clientes
                            WHERE nome = ?
                        ''', (stateClient,)
                    )
                    clientID = cursor.fetchone()
                    print(clientID)
                    
                except Exception as e:
                    print(f'Erro ao executar SELECT: {e}')

                try:
                    cursor.execute(
                        '''
                            INSERT INTO ucs (concessionaria, cliente_id, uc, subgrupo, modalidade, demanda_contratada, demanda_contratada_ponta, demanda_contratada_fora_ponta, created_at)
                            VALUES (?,?,?,?,?,?,?,?,?)
                        ''',(stateUtilities, clientID[0], stateUC, stateGroup, stateModality, demand, pDemand, fpDemand, today)
                    )
                    allOutputs[0] = not stateModalAviso
                    
                except Exception as e:
                    print(f'Erro ao executar INSERT: {e}')
                
                # try:
                #     cursor.execute(
                #         '''
                #             INERT INTO consumos_baixa_tens
                #         '''
                #     )

                # except Exception as e:
                #     pass
                
                conn.commit()
                conn.close()
        

    print (emptyFieldIndicator)
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
                           'DADOS DA UC',
                           html.Br(),
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
                                            placeholder='Demanda Contratada (kW)',
                                            type='number',
                                            disabled=True
                                        )
                                    ),

                                    dbc.Col(
                                        dbc.Input(
                                            class_name='input-field-modal',
                                            id='input-demanda-ponta',
                                            placeholder='Demanda Contratada Ponta (kW)',
                                            type='number',
                                            # disabled deve ser alterado no callback
                                            disabled=True
                                        )
                                    )
                                ]
                            ),
                            html.Hr(),
                        ],
                    ),

                    dbc.ModalFooter(
                        children=[
                            dbc.Button(children='Fechar', id='btn-close', n_clicks=0),
                            dbc.Button(children='Inserir', id='btn-insert', n_clicks=0)
                        ]
                    )
                ],
                is_open=False,
                id='modal-cadastro-ucs',
                size='lg',
                scrollable=True
            ),

            # modalç de sucesso
            dbc.Modal(
                children=[
                    dbc.ModalHeader(
                        children=[
                            html.I(className='fa-solid fa-check'),
                            'Sucesso'
                        ]
                    ),

                    dbc.ModalBody('UC cadastrada com sucesso!'),

                    dbc.ModalFooter(
                        dbc.Button(children='Fechar', id='btn-close-aviso', n_clicks=0),
                    )
                    
                ],
                is_open=False,
                id='modal-aviso',
                size='md',
                centered=True
            ),

            # modal de erro de preenchimento
            dbc.Modal(
                children=[
                    dbc.ModalHeader(
                        children=[
                            html.I(className='fa-solid fa-xmark'),
                            'Erro'
                        ]
                    ),

                    dbc.ModalBody('Prencha os campos obrigatórios em vermelho'),

                    dbc.ModalFooter(
                        dbc.Button(children='Fechar', id='btn-close-err-field', n_clicks=0),
                    )
                    
                ],
                is_open=False,
                id='modal-err-field',
                size='md',
                centered=True
            ),
            
            # modal de erro de uc ja existente
            dbc.Modal(
                children=[
                    dbc.ModalHeader(
                        children=[
                            html.I(className='fa-solid fa-xmark'),
                            'Erro'
                        ]
                    ),

                    dbc.ModalBody('UC já existente'),

                    dbc.ModalFooter(
                        dbc.Button(children='Fechar', id='btn-close-err-uc', n_clicks=0),
                    )
                    
                ],
                is_open=False,
                id='modal-err-uc',
                size='md',
                centered=True
            ),

        ]
    )

    return layout
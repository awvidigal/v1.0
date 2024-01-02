import sqlite3 as sql
import pandas as pd
import numpy as np
import datetime
import dash
import dash_bootstrap_components as dbc
from dash import html, callback, Input, Output, State


dash.register_page(
    __name__,
    name='Clientes',
    path='/clientes'
)

estados=['AC', 'AL', 'AP', 'AM', 'BA', 'CE', 'DF', 'ES', 'GO', 'MA', 'MT', 'MS', 'MG', 'PA', 'PB', 'PR', 'PE', 'PI', 'RJ', 'RN', 'RS', 'RO', 'RR', 'SC', 'SP', 'SE', 'TO']

# abre o modal de cadastro de clientes
@callback(
    [
        Output(component_id='new-client-modal', component_property='is_open'),
        # inserir os valores dos inputs como outputs de forma a limpar os campos quando o modal for aberto ou fechado
    ],
    [
        Input(component_id='btn-add-client', component_property='n_clicks'),
        Input(component_id='btn-close', component_property='n_clicks')
    ],
    [
        State(component_id='new-client-modal', component_property='is_open')
    ],
    prevent_initial_call=True
)
def showModal(n1, n2, is_open):
    if n1 or n2:
        return not is_open
    return is_open

# controle os placeholders dos campos de acordo com a escolha de PF ou PJ
@callback(
   [
       Output(component_id='input-nome-razao-social', component_property='placeholder'),
       Output(component_id='input-cpf-cnpj', component_property='placeholder')
   ],

   Input(component_id='radio-itens-pf-pj', component_property='value'),
   prevent_initial_call=True 
)
def personType(radioValue):
    nameOutput = 'Nome'
    documentOutput = 'CPF'

    if radioValue == 2:
        nameOutput = 'Razão Social'
        documentOutput = 'CNPJ'

    return nameOutput, documentOutput

# insere o novo registro no db
@callback(
    [
        Output(component_id='modal-client-error', component_property='children'),
        Output(component_id='modal-client-error', component_property='is_open'),  
        Output(component_id='input-cpf-cnpj', component_property='class_name'),
        Output(component_id='input-endereco', component_property='class_name'),
        Output(component_id='input-cidade', component_property='class_name'),
        Output(component_id='select-estado', component_property='class_name')
        # Output(component_id='modal_client-success', component_property='is_open'),
        
    ],
    [
        Input(component_id='btn-insert', component_property='n_clicks'),
        Input(component_id='btn-close', component_property='n_clicks'),         
        # Input(component_id='btn-close-success', component_property='n_clicks'),    
    ],
    [
        State(component_id='input-cpf-cnpj', component_property='value'),
        State(component_id='input-endereco', component_property='value'),
        State(component_id='input-cidade', component_property='value'),
        State(component_id='select-estado', component_property='value'),
        State(component_id='modal-client-error', component_property='is_open'),
        State(component_id='radio-itens-pf-pj', component_property='value'),
        State(component_id='input-nome-razao-social', component_property='value'),
        State(component_id='input-numero', component_property='value'),
        State(component_id='input-email', component_property='value'),
        State(component_id='input-telefone', component_property='value')        
    ],
    prevent_initial_call=True
)
def newRegister(btnInsert, btnCloseError, inputDocs, inputAddress, inputCity, selectState, stateModal, stateRadio, inputName, inputNumber, inputEmail, inputPhone):
    '''
        As saídas estão organizadas em uma lista que é retornada ao final de cada execução. Estão numeradas da seguinte forma dentro dessa lista:
            modal-client-error  | children   -> 0
            modal-client-error  | os_open    -> 1
            input-cpf-cnpj      | class_name -> 2
            input-endereco      | class_name -> 3
            input-cidade        | class_name -> 4
            select-estado       | class_name -> 5
    '''
    
    print("começoooouuu")
    existsIndicator = ''
    created_at = datetime.datetime.now()
    document = 'cpf'
    person = 'pf'
    completeAddress = inputAddress + ', ' + inputNumber

    if stateRadio == 2:
        document = 'cnpj'
        person = 'pj'

    emptyFieldIndicator = False
    
    childrenErrClient = [
        dbc.ModalHeader(
            children=[
                html.I(className='fa-solid fa-xmark'),
                'Cliente já cadastrado'
            ]
        ),
        dbc.ModalBody('O cliente que você está tentando cadastrar já existe'),
        dbc.ModalFooter(
            children=[
                dbc.Button(children='Fechar', id='btn-close', n_clicks=0)
            ]
        )
    ]

    childrenErrField = [
        dbc.ModalHeader(
            children=[
                html.I(className='fa-solid fa-xmark'),
                'Campos obrigatórios'
            ]
        ),
        dbc.ModalBody('Os campos marcados em vermelho são obrigatórios'),
        dbc.ModalFooter(
            children=[
                dbc.Button(children='Fechar', id='btn-close', n_clicks=0)
            ]
        )
    ]

    childrenSuccess = [
        dbc.ModalHeader(
            children=[
                html.I(className='fa-solid fa-check'),
                            'Sucesso'
                    ]
                ),
        dbc.ModalBody('Cliente cadastrado com sucesso'),
        dbc.ModalFooter(
            children=[
                dbc.Button(children='Fechar', id='btn-close', n_clicks=0)
            ]
        )
    ]

    allOutputs = [
        childrenErrField,
        False,
        'input-field-modal',
        'input-field-modal',
        'input-field-modal',
        'input-field-modal'
    ]

    # inserir validação do campo de cpf/cnpj

    if btnInsert is not None and btnInsert > 0:

        # VERIFICAR SE OS CAMPOS ESTAO PREENCHIDOS
        if not inputDocs:
            allOutputs[2] = 'input-field-modal-error'
            emptyFieldIndicator = True
        else: 
            allOutputs[2] = 'input-field-modal'
            emptyFieldIndicator = False

        if not inputAddress:
            allOutputs[3] = 'input-field-modal-error'
            emptyFieldIndicator = True
        else:
            allOutputs[3] = 'input-field-modal'
            emptyFieldIndicator = False

        if not inputCity:
            allOutputs[4] = 'input-field-modal-error'
            emptyFieldIndicator = True
        else:
            allOutputs[4] = 'input-field-modal'
            emptyFieldIndicator = False

        if not selectState:
            allOutputs[5] = 'input-field-modal-error'
            emptyFieldIndicator = True
        else:
            allOutputs[5] = 'input-field-modal'
            emptyFieldIndicator = False


        if emptyFieldIndicator:
            allOutputs[1] = not stateModal
        
        elif btnCloseError is not None and btnCloseError > 0:
            allOutputs[1] = not stateModal

        else:
            # cadastro no banco de dados
            conn = sql.connect('agv.db')
            cursor = conn.cursor()

            # verificar se o cpf/cnpj ja existem
            existsIndicator = cursor.execute(
                f'''
                SELECT *
                FROM clientes
                WHERE {document} = ?;
                ''', (inputDocs,)
            ).fetchone()

            if existsIndicator == None:
                # se nao existir, cadastro do cliente no db
                if person == 'pf':                    
                    try:
                        cursor.execute(
                            '''
                            INSERT INTO clientes (pessoa, cpf, nome, endereco, cidade, estado, email, telefone, created_at)
                            VALUES (?,?,?,?,?,?,?,?,?)
                            ''', (person, inputDocs, inputName, completeAddress, inputCity, selectState, inputEmail, inputPhone, created_at)
                        )
                        conn.commit()

                        allOutputs[0] = childrenSuccess
                        allOutputs[1] = not stateModal

                    except Exception as e:
                        print(f'Erro ao executar INSERT: {e}')
                        print(f"Consulta SQL:", {'''
                            INSERT INTO clientes (pessoa, cpf, nome, endereco, cidade, estado, email, telefone, created_at)
                            VALUES (?,?,?,?,?,?,?,?,?)
                        '''})

                elif person == 'pj':
                    try:
                        cursor.execute(
                            '''
                            INSERT INTO clientes (pessoa, cnpj, razao_social, endereco, cidade, estado, email, telefone, created_at)
                            VALUES (?,?,?,?,?,?,?,?,?)
                            ''', (person, inputDocs, inputName, completeAddress, inputCity, selectState, inputEmail, inputPhone, created_at)
                        )
                        conn.commit()

                        

                    except Exception as e:
                        print(f'Erro ao executar INSERT: {e}')
                        print(f"Consulta SQL:", {'''
                            INSERT INTO clientes (pessoa, cpf, nome, endereco, cidade, estado, email, telefone, created_at)
                            VALUES (?,?,?,?,?,?,?,?,?)
                        '''})

                conn.close()
            
            else:
                print('#deuruim')
                allOutputs[0] = childrenErrClient
                allOutputs[1] = not stateModal
                # limpar os campos do modal principal?        
        return allOutputs


# Cria dataframe com a tabela de clientes inteira
conn = sql.connect('c:/Users/vidig/OneDrive/Python/agv/v1.0/agv.db')
query = '''SELECT 
            IFNULL(pessoa, 'NaN') as pessoa,
            IFNULL(cpf, 'NaN') as cpf,
            IFNULL(cnpj, 'NaN') as cnpj,
            IFNULL(nome, 'NaN') as nome,
            IFNULL(razao_social, 'NaN') as razao_social,
            IFNULL(cidade, 'NaN') as cidade,
            IFNULL(estado, 'NaN') as estado,
            IFNULL(telefone, 'NaN') as telefone,
            IFNULL(email, 'NaN') as email
        FROM clientes;'''

clientsTable = pd.read_sql_query(
    sql=query,
    con=conn
)

conn.close()

clientsTable.replace('NaN', np.nan, inplace=True)

docsColumns = ['cpf', 'cnpj']
namesColumns = ['nome', 'razao_social']

clientsTable[docsColumns] = clientsTable[docsColumns].astype('string')
clientsTable[namesColumns] = clientsTable[namesColumns].astype('string')

showTable = pd.DataFrame(columns=['Nome/Razão Social', 'CPF/CNPJ', 'Telefone', 'Email'])
showTable['Nome/Razão Social'] = clientsTable[namesColumns].sum(1)
showTable['CPF/CNPJ'] = clientsTable[docsColumns].sum(1)
showTable['Telefone'] = clientsTable['telefone']
showTable['Email'] = clientsTable['email']

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
                    justify='center',
                    
            ),
            
            # dbc.Row(
            #     children=['tabela do db com os clientes
            #     ]
            # )
            
            html.Div(
                children = dbc.Table.from_dataframe(
                    showTable, 
                    striped=False,
                    bordered=False,
                    hover=True,
                    class_name='table-clients',
                    color='dark',
                    size='lg'
                ),
                className='div-table'
            ),



            # dbc.Row(
            #     children=[
            #         'pagina do db com até 10 resultados'
            #     ]
            # )

            dbc.Button(
                children=html.I(className='fa-solid fa-user-plus'),
                id='btn-add-client',
                n_clicks=0
            ),

            dbc.Modal(
                children=[
                    dbc.ModalHeader(dbc.ModalTitle('Novo Cliente')),
                    dbc.ModalBody(
                        children=[
                            html.H5('Formulário de cadastro do cliente', className='h5-modal-body-title'),
                            html.Br(),
                            # dbc.Label("PF/PJ"),
                            dbc.RadioItems(
                                options=[
                                    {'label':'Pessoa Física', 'value':1},
                                    {'label':'Pessoa Jurídica', 'value':2},
                                ],
                                inline=True,
                                id='radio-itens-pf-pj',
                                value=1                            
                            ),
                            html.Br(),
                            # dbc.Label('Nome', id='lbl-nome', hidden=False),
                            # dbc.Label('Razão Social', id='lbl-razao-social', hidden=True),
                            dbc.Input(
                                class_name='input-field-modal',
                                id='input-nome-razao-social',
                                placeholder='Nome',
                                type='text'
                            ),
                            
                            html.Br(),
                            dbc.Input(
                                class_name='input-field-modal',
                                id='input-cpf-cnpj',
                                placeholder='CPF',
                                type='text',
                                value='',
                            ),

                            html.Br(),
                            dbc.Row(
                                children=[
                                    dbc.Col(
                                        dbc.Input(
                                            class_name='input-field-modal',
                                            id='input-endereco',
                                            placeholder='Endereço'
                                        ),
                                        width={'size':10, 'offset':0}
                                    ),

                                    dbc.Col(
                                        dbc.Input(
                                            class_name='input-field-modal',
                                            id='input-numero',
                                            placeholder='Nº'
                                        ),
                                        width={'size':2, 'offset':0}
                                    )
                                ]
                            ),
                            html.Br(),
                            dbc.Row(
                                children=[
                                    dbc.Col(
                                        dbc.Input(
                                            class_name='input-field-modal',
                                            placeholder='Bairro',
                                            id='input-bairro'
                                        ),
                                        width={'size':4, 'offset':0}
                                    ),
                                    dbc.Col(
                                        dbc.Input(
                                            class_name='input-field-modal',
                                            placeholder='Cidade',
                                            id='input-cidade'
                                        ),
                                        width={'size':5, 'offset':0}
                                    ),

                                    dbc.Col(
                                        dbc.Select(
                                            class_name='input-field-modal',
                                            placeholder='UF',
                                            id='select-estado',
                                            options=[{'label':estado, 'value':estado} for estado in estados]
                                        ),
                                        width={'size':3, 'offset':0}
                                    )
                                ]
                                
                            ),
                            html.Br(),

                            dbc.Row(
                                children=[
                                    dbc.Col(
                                        dbc.Input(
                                            class_name='input-field-modal',
                                            placeholder='Email',
                                            id='input-email'
                                        ),
                                        width={'size':8, 'offset':0}
                                    ),
                                    dbc.Col(
                                        dbc.Input(
                                            class_name='input-field-modal',
                                            placeholder='Telefone',
                                            id='input-telefone'
                                        ),
                                        width={'size':4}
                                    )
                                ]
                            )

                        ]
                    ),
                    dbc.ModalFooter(
                        children=[
                            dbc.Button(children='Fechar', id='btn-close', n_clicks=0),
                            dbc.Button(children='Inserir', id='btn-insert', n_clicks=0)
                        ]
                    )
                ],
                id='new-client-modal',
                is_open=False,
                size='lg',
                scrollable=True,
                backdrop=False,               
            ),

            dbc.Modal(
                children=[
                    dbc.ModalHeader(
                        children=[
                            html.I(className='fa-solid fa-xmark'),
                            'Cliente já cadastrado'
                        ]
                    ),
                    dbc.ModalBody('O cliente que você está tentando cadastrar já existe'),
                    dbc.ModalFooter(
                        children=[
                            dbc.Button(children='Fechar', id='btn-close-error', n_clicks=0)
                        ]
                    )
                ],
                is_open=False,
                id='modal-client-error',
                centered=True
            ),

            dbc.Modal(
                children=[
                    dbc.ModalHeader(
                        children=[
                            html.I(className='fa-solid fa-check'),
                            'Sucesso'
                        ]
                    ),
                    dbc.ModalBody('Cliente cadastrado com sucesso'),
                    dbc.ModalFooter(
                        children=[
                            dbc.Button(children='Fechar', id='btn-close-success', n_clicks=0)
                        ]
                    )
                ],
                is_open=False,
                id='modal-client-success',
                centered=True
            )
                    
        ],
        fluid=True
    )


    return layout



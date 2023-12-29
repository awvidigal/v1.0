import dash
import dash_bootstrap_components as dbc
from dash import html, dcc, callback, Input, Output, State


dash.register_page(
    __name__,
    name='Clientes',
    path='/clientes'
)

@callback(
    Output(component_id='new-client-modal', component_property='is_open'),
    [
        Input(component_id='btn-add-client', component_property='n_clicks'),
        Input(component_id='btn-close', component_property='n_clicks')
    ],
    [
        State(component_id='new-client-modal', component_property='is_open')
    ]
)
def showModal(n1, n2, is_open):
    if n1 or n2:
        return not is_open
    return is_open

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
                n_clicks=0
            ),

            dbc.Modal(
                children=[
                    dbc.ModalHeader(dbc.ModalTitle('Novo Cliente')),
                    dbc.ModalBody(
                        children=[
                           'Formulario de cadastro do cliente',
                            html.Br(),
                            html.Br(),
                            # dbc.Label("PF/PJ"),
                            dbc.RadioItems(
                                options=[
                                    {'label':'Pessoa Física', 'value':1},
                                    {'label':'Pessoa Jurídica', 'value':2},
                                ],
                                inline=True                                
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
                                type='number'
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
                                        width={'size':5, 'offset':0}
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
                                        dbc.Input(
                                            class_name='input-field-modal',
                                            placeholder='UF',
                                            id='input-estado'
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
                scrollable=True                
            )        
        ]
    )


    return layout



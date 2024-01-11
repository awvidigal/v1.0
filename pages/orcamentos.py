import dash
from dash import html, dcc, callback, Input, Output
import sqlite3 as sql
import pandas as pd
import numpy as np
import datetime
import dash
import dash_bootstrap_components as dbc
from dash import html, callback, Input, Output, State

dash.register_page(
    __name__,
    name='Orçamentos',
    path='/orcamentos'
)

conn = sql.connect('c:/Users/vidig/OneDrive/Python/agv/v1.0/agv.db')
cursor = conn.cursor()

cursor.execute(
    '''
        SELECT uc
        FROM ucs
    '''
)
ucs = cursor.fetchall()
conn.close()

ucs = [uc[0] for uc in ucs]


def layout():
    layout = dbc.Container(
        children=[
            dbc.Row(
                children=dbc.Input(
                    id='search-input', 
                    placeholder='Busca...', 
                    type='text',
                    size='md',
                    class_name='text-field-search',
                    debounce=False,
                    html_size='100',
                    # list='lista com os nomes dos clientes no db'
                ),
                justify='center'
            ),

            dbc.Button(                
                children='Novo Orçamento',
                id='btn-new-proposal'                
            ),

            dbc.Modal(
                children=[
                    dbc.ModalHeader(dbc.ModalTitle('NOVO ORÇAMENTO')),
                    dbc.ModalBody(
                        children=[
                            dbc.Row(
                                dbc.Col(
                                    children=dbc.Select(
                                        class_name='input-field-modal',
                                        options=ucs,
                                        id='select-uc',
                                        placeholder='Número da UC'
                                    )
                                )
                            ),
                            html.Br(),

                            dbc.Accordion(
                                children=[
                                    dbc.AccordionItem(
                                        children=[
                                            dbc.Row(
                                                dbc.Col(
                                                    children=[
                                                        dbc.InputGroup(
                                                            children=[
                                                                dbc.InputGroupText('Jan'),
                                                                dbc.Input(placeholder='Consumo', id='input-consumo-jan'),
                                                                dbc.InputGroupText('kWh'),
                                                                dbc.Input(placeholder='Consumo Ponta', id='input-consumo-ponta-jan', disabled=True),
                                                                dbc.InputGroupText('kWh')  
                                                            ],
                                                            className='mb-3',
                                                        )
                                                    ]
                                                )
                                            ),

                                            dbc.Row(
                                                dbc.Col(
                                                    children=[
                                                        dbc.InputGroup(
                                                            children=[
                                                                dbc.InputGroupText('Fev'),
                                                                dbc.Input(placeholder='Consumo', id='input-consumo-fev'),
                                                                dbc.InputGroupText('kWh'),
                                                                dbc.Input(placeholder='Consumo Ponta', id='input-consumo-ponta-fev', disabled=True),
                                                                dbc.InputGroupText('kWh')                                                
                                                            ],
                                                            className='mb-3'
                                                        )
                                                    ]
                                                )
                                            ),

                                            dbc.Row(
                                                dbc.Col(
                                                    children=[
                                                        dbc.InputGroup(
                                                            children=[
                                                                dbc.InputGroupText('Mar'),
                                                                dbc.Input(placeholder='Consumo', id='input-consumo-mar'),
                                                                dbc.InputGroupText('kWh'),
                                                                dbc.Input(placeholder='Consumo Ponta', id='input-consumo-ponta-mar', disabled=True),
                                                                dbc.InputGroupText('kWh')                                                
                                                            ],
                                                            className='mb-3'
                                                        )
                                                    ]
                                                )
                                            ),

                                            dbc.Row(
                                                dbc.Col(
                                                    children=[
                                                        dbc.InputGroup(
                                                            children=[
                                                                dbc.InputGroupText('Abr'),
                                                                dbc.Input(placeholder='Consumo', id='input-consumo-abr'),
                                                                dbc.InputGroupText('kWh'),
                                                                dbc.Input(placeholder='Consumo Ponta', id='input-consumo-ponta-abr', disabled=True),
                                                                dbc.InputGroupText('kWh')                                              
                                                            ],
                                                            className='mb-3'
                                                        )
                                                    ]
                                                )
                                            ),

                                            dbc.Row(
                                                dbc.Col(
                                                    children=[
                                                        dbc.InputGroup(
                                                            children=[
                                                                dbc.InputGroupText('Mai'),
                                                                dbc.Input(placeholder='Consumo', id='input-consumo-mai'),
                                                                dbc.InputGroupText('kWh'),
                                                                dbc.Input(placeholder='Consumo Ponta', id='input-consumo-ponta-mai', disabled=True),
                                                                dbc.InputGroupText('kWh')                                               
                                                            ],
                                                            className='mb-3'
                                                        )
                                                    ]
                                                )
                                            ),

                                            dbc.Row(
                                                dbc.Col(
                                                    children=[
                                                        dbc.InputGroup(
                                                            children=[
                                                                dbc.InputGroupText('Jun'),
                                                                dbc.Input(placeholder='Consumo', id='input-consumo-jun'),
                                                                dbc.InputGroupText('kWh'),
                                                                dbc.Input(placeholder='Consumo Ponta', id='input-consumo-ponta-jun', disabled=True),
                                                                dbc.InputGroupText('kWh')
                                                            ],
                                                            className='mb-3'
                                                        )
                                                    ]
                                                )
                                            ),

                                            dbc.Row(
                                                dbc.Col(
                                                    children=[
                                                        dbc.InputGroup(
                                                            children=[
                                                                dbc.InputGroupText('Jul'),
                                                                dbc.Input(placeholder='Consumo', id='input-consumo-jul'),
                                                                dbc.InputGroupText('kWh'),
                                                                dbc.Input(placeholder='Consumo Ponta', id='input-consumo-ponta-jul', disabled=True),
                                                                dbc.InputGroupText('kWh')                                                
                                                            ],
                                                            className='mb-3'
                                                        )
                                                    ]
                                                )
                                            ), 

                                            dbc.Row(
                                                dbc.Col(
                                                    children=[
                                                        dbc.InputGroup(
                                                            children=[
                                                                dbc.InputGroupText('Ago'),
                                                                dbc.Input(placeholder='Consumo', id='input-consumo-ago'),
                                                                dbc.InputGroupText('kWh'),
                                                                dbc.Input(placeholder='Consumo Ponta', id='input-consumo-ponta-ago', disabled=True),
                                                                dbc.InputGroupText('kWh')                                                 
                                                            ],
                                                            className='mb-3'
                                                        )
                                                    ]
                                                )
                                            ),

                                            dbc.Row(
                                                dbc.Col(
                                                    children=[
                                                        dbc.InputGroup(
                                                            children=[
                                                                dbc.InputGroupText('Set'),
                                                                dbc.Input(placeholder='Consumo', id='input-consumo-set'),
                                                                dbc.InputGroupText('kWh'),
                                                                dbc.Input(placeholder='Consumo Ponta', id='input-consumo-ponta-set', disabled=True),
                                                                dbc.InputGroupText('kWh')                                                 
                                                            ],
                                                            className='mb-3'
                                                        )
                                                    ]
                                                )
                                            ),

                                            dbc.Row(
                                                dbc.Col(
                                                    children=[
                                                        dbc.InputGroup(
                                                            children=[
                                                                dbc.InputGroupText('Out'),
                                                                dbc.Input(placeholder='Consumo', id='input-consumo-out'),
                                                                dbc.InputGroupText('kWh'),
                                                                dbc.Input(placeholder='Consumo Ponta', id='input-consumo-ponta-out', disabled=True),
                                                                dbc.InputGroupText('kWh')                                                 
                                                            ],
                                                            className='mb-3'
                                                        )
                                                    ]
                                                )
                                            ),

                                            dbc.Row(
                                                dbc.Col(
                                                    children=[
                                                        dbc.InputGroup(
                                                            children=[
                                                                dbc.InputGroupText('Nov'),
                                                                dbc.Input(placeholder='Consumo', id='input-consumo-nov'),
                                                                dbc.InputGroupText('kWh'),
                                                                dbc.Input(placeholder='Consumo Ponta', id='input-consumo-ponta-nov', disabled=True),
                                                                dbc.InputGroupText('kWh')                                                
                                                            ],
                                                            className='mb-3'
                                                        )
                                                    ]
                                                )
                                            ),

                                            dbc.Row(
                                                dbc.Col(
                                                    children=[
                                                        dbc.InputGroup(
                                                            children=[
                                                                dbc.InputGroupText('Dez'),
                                                                dbc.Input(placeholder='Consumo', id='input-consumo-dez'),
                                                                dbc.InputGroupText('kWh'),
                                                                dbc.Input(placeholder='Consumo Ponta', id='input-consumo-ponta-dez', disabled=True),
                                                                dbc.InputGroupText('kWh')                                                 
                                                            ],
                                                            className='mb-3'
                                                        )
                                                    ]
                                                )
                                            ),    
                                        ],
                                        title='DADOS DE CONSUMO'
                                    ),
                                    dbc.AccordionItem(
                                        children=[
                                            dbc.Row(
                                                dbc.Col(
                                                    children=[
                                                        dbc.InputGroup(
                                                            children=[
                                                                dbc.InputGroupText('Jan'),
                                                                dbc.Input(placeholder='Demanda', id='input-demanda-jan'),
                                                                dbc.InputGroupText('kW'),
                                                                dbc.Input(placeholder='Demanda Ponta', id='input-demanda-ponta-jan', disabled=True),
                                                                dbc.InputGroupText('kW')  
                                                            ],
                                                            className='mb-3',
                                                        )
                                                    ]
                                                )
                                            ),

                                            dbc.Row(
                                                dbc.Col(
                                                    children=[
                                                        dbc.InputGroup(
                                                            children=[
                                                                dbc.InputGroupText('Fev'),
                                                                dbc.Input(placeholder='Demanda', id='input-demanda-fev'),
                                                                dbc.InputGroupText('kW'),
                                                                dbc.Input(placeholder='Demanda Ponta', id='input-demanda-ponta-fev', disabled=True),
                                                                dbc.InputGroupText('kW')                                                
                                                            ],
                                                            className='mb-3'
                                                        )
                                                    ]
                                                )
                                            ),

                                            dbc.Row(
                                                dbc.Col(
                                                    children=[
                                                        dbc.InputGroup(
                                                            children=[
                                                                dbc.InputGroupText('Mar'),
                                                                dbc.Input(placeholder='Demanda', id='input-demanda-mar'),
                                                                dbc.InputGroupText('kW'),
                                                                dbc.Input(placeholder='Demanda Ponta', id='input-demanda-ponta-mar', disabled=True),
                                                                dbc.InputGroupText('kW')                                                
                                                            ],
                                                            className='mb-3'
                                                        )
                                                    ]
                                                )
                                            ),

                                            dbc.Row(
                                                dbc.Col(
                                                    children=[
                                                        dbc.InputGroup(
                                                            children=[
                                                                dbc.InputGroupText('Abr'),
                                                                dbc.Input(placeholder='Demanda', id='input-demanda-abr'),
                                                                dbc.InputGroupText('kW'),
                                                                dbc.Input(placeholder='Demanda Ponta', id='input-demanda-ponta-abr', disabled=True),
                                                                dbc.InputGroupText('kW')                                              
                                                            ],
                                                            className='mb-3'
                                                        )
                                                    ]
                                                )
                                            ),

                                            dbc.Row(
                                                dbc.Col(
                                                    children=[
                                                        dbc.InputGroup(
                                                            children=[
                                                                dbc.InputGroupText('Mai'),
                                                                dbc.Input(placeholder='Demanda', id='input-demanda-mai'),
                                                                dbc.InputGroupText('kW'),
                                                                dbc.Input(placeholder='Demanda Ponta', id='input-demanda-ponta-mai', disabled=True),
                                                                dbc.InputGroupText('kW')                                               
                                                            ],
                                                            className='mb-3'
                                                        )
                                                    ]
                                                )
                                            ),

                                            dbc.Row(
                                                dbc.Col(
                                                    children=[
                                                        dbc.InputGroup(
                                                            children=[
                                                                dbc.InputGroupText('Jun'),
                                                                dbc.Input(placeholder='Demanda', id='input-demanda-jun'),
                                                                dbc.InputGroupText('kW'),
                                                                dbc.Input(placeholder='Demanda Ponta', id='input-demanda-ponta-jun', disabled=True),
                                                                dbc.InputGroupText('kW')
                                                            ],
                                                            className='mb-3'
                                                        )
                                                    ]
                                                )
                                            ),

                                            dbc.Row(
                                                dbc.Col(
                                                    children=[
                                                        dbc.InputGroup(
                                                            children=[
                                                                dbc.InputGroupText('Jul'),
                                                                dbc.Input(placeholder='Demanda', id='input-demanda-jul'),
                                                                dbc.InputGroupText('kW'),
                                                                dbc.Input(placeholder='Demanda Ponta', id='input-demanda-ponta-jul', disabled=True),
                                                                dbc.InputGroupText('kW')                                                
                                                            ],
                                                            className='mb-3'
                                                        )
                                                    ]
                                                )
                                            ), 

                                            dbc.Row(
                                                dbc.Col(
                                                    children=[
                                                        dbc.InputGroup(
                                                            children=[
                                                                dbc.InputGroupText('Ago'),
                                                                dbc.Input(placeholder='Demanda', id='input-demanda-ago'),
                                                                dbc.InputGroupText('kW'),
                                                                dbc.Input(placeholder='Demanda Ponta', id='input-demanda-ponta-ago', disabled=True),
                                                                dbc.InputGroupText('kW')                                                 
                                                            ],
                                                            className='mb-3'
                                                        )
                                                    ]
                                                )
                                            ),

                                            dbc.Row(
                                                dbc.Col(
                                                    children=[
                                                        dbc.InputGroup(
                                                            children=[
                                                                dbc.InputGroupText('Set'),
                                                                dbc.Input(placeholder='Demanda', id='input-demanda-set'),
                                                                dbc.InputGroupText('kW'),
                                                                dbc.Input(placeholder='Demanda Ponta', id='input-demanda-ponta-set', disabled=True),
                                                                dbc.InputGroupText('kW')                                                 
                                                            ],
                                                            className='mb-3'
                                                        )
                                                    ]
                                                )
                                            ),

                                            dbc.Row(
                                                dbc.Col(
                                                    children=[
                                                        dbc.InputGroup(
                                                            children=[
                                                                dbc.InputGroupText('Out'),
                                                                dbc.Input(placeholder='Demanda', id='input-demanda-out'),
                                                                dbc.InputGroupText('kW'),
                                                                dbc.Input(placeholder='Demanda Ponta', id='input-demanda-ponta-out', disabled=True),
                                                                dbc.InputGroupText('kW')                                                 
                                                            ],
                                                            className='mb-3'
                                                        )
                                                    ]
                                                )
                                            ),

                                            dbc.Row(
                                                dbc.Col(
                                                    children=[
                                                        dbc.InputGroup(
                                                            children=[
                                                                dbc.InputGroupText('Nov'),
                                                                dbc.Input(placeholder='Demanda', id='input-demanda-nov'),
                                                                dbc.InputGroupText('kW'),
                                                                dbc.Input(placeholder='Demanda Ponta', id='input-demanda-ponta-nov', disabled=True),
                                                                dbc.InputGroupText('kW')                                                
                                                            ],
                                                            className='mb-3'
                                                        )
                                                    ]
                                                )
                                            ),

                                            dbc.Row(
                                                dbc.Col(
                                                    children=[
                                                        dbc.InputGroup(
                                                            children=[
                                                                dbc.InputGroupText('Dez'),
                                                                dbc.Input(placeholder='Demanda', id='input-demanda-dez'),
                                                                dbc.InputGroupText('kW'),
                                                                dbc.Input(placeholder='Demanda Ponta', id='input-demanda-ponta-dez', disabled=True),
                                                                dbc.InputGroupText('kW')                                                 
                                                            ],
                                                            className='mb-3'
                                                        )
                                                    ]
                                                )
                                            )
                                        ],
                                        title='DADOS DE DEMANDA'
                                    )
                                ],
                                start_collapsed=True,
                                
                            ),
                        ]
                    )
                ],
                is_open=True,
                fullscreen=True
            )
        ]
    )

    return layout
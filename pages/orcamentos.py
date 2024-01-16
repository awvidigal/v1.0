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

year=datetime.datetime.now()
year=year.year

conn = sql.connect('c:/Users/vidig/OneDrive/Python/agv/v1.0/agv.db')
cursor = conn.cursor()

cursor.execute(
    '''
        SELECT uc
        FROM ucs
    '''
)
ucs = cursor.fetchall()

cursor.execute(
    '''
        SELECT subgrupo
        FROM subgrupos
    '''
)
subgroups = cursor.fetchall()

cursor.execute(
    '''
        SELECT modalidade
        FROM modalidades
    '''
)
modalities = cursor.fetchall()

conn.close()

ucs = [uc[0] for uc in ucs]
subgroups = [subgroup[0] for subgroup in subgroups]
modalities = [modality[0] for modality in modalities]


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
                                    ),
                                    dbc.AccordionItem(
                                        children=[
                                            dbc.Row(
                                                children=[
                                                    dbc.Col(
                                                        children=[
                                                            dbc.RadioItems(
                                                                options=[
                                                                    {'label':'Ajuste de subgrupo', 'value':1}
                                                                ],
                                                                id='switch-subgrupo',
                                                                switch=True
                                                            )
                                                        ],
                                                        width={'size':3, 'offset':0}
                                                    ),

                                                    dbc.Col(
                                                        children=[
                                                            dbc.Select(
                                                                class_name='input-field-modal',
                                                                options=subgroups,
                                                                id='select-subgrupo-ajustado',
                                                                placeholder='Subgrupo ajustado...',
                                                                size='md'
                                                            )
                                                        ],
                                                        width={'size':3, 'offset':0}
                                                    )
                                                ],
                                                align='center'
                                            ),

                                            dbc.Row(
                                                children=[
                                                    dbc.Col(
                                                        children=[
                                                            dbc.RadioItems(
                                                                options=[
                                                                    {'label':'Ajuste de modalidade', 'value':2}
                                                                ],
                                                                id='switch-modality',
                                                                switch=True
                                                            )
                                                        ],
                                                        width={'size':3, 'offset':0}
                                                    ),

                                                    dbc.Col(
                                                        children=[
                                                            dbc.Select(
                                                                class_name='input-field-modal',
                                                                options=modalities,
                                                                id='adjust-modality',
                                                                placeholder='Modalidade ajustada...',
                                                                size='md'
                                                            )
                                                        ],
                                                        width={'size':3, 'offset':0}
                                                    )
                                                ],
                                                align='center'
                                            ),

                                            dbc.Row(
                                                children=[
                                                    dbc.Col(
                                                        children=[
                                                            dbc.RadioItems(
                                                                options=[
                                                                    {'label':'Ajuste de demanda', 'value':3}
                                                                ],
                                                                id='switch-demand',
                                                                switch=True,
                                                                value=[1]
                                                            )
                                                        ],
                                                        width={'size':3, 'offset':0}
                                                    ),

                                                    dbc.Col(
                                                        children=[
                                                            dbc.Input(
                                                                class_name='input-field-modal',
                                                                id='adjust-demand',
                                                                placeholder='Demanda ajustada...',
                                                                type='number',
                                                                size='md'
                                                            )
                                                        ],
                                                        width={'size':3, 'offset':0}
                                                    )
                                                ],
                                                align='center'
                                            ),
                                        ],
                                        title='DADOS DE AJUSTE'
                                    ),
                                    dbc.AccordionItem(
                                        children=[
                                            dbc.Row(
                                                children=[
                                                    dbc.RadioItems(
                                                        options=[
                                                            {'label':'GD', 'value':1},
                                                            {'label':'ACL', 'value':2}
                                                        ],
                                                        value=1,
                                                        id='radio-choose-mode',
                                                        inline=True
                                                    )
                                                ]
                                            ),
                                            html.Br(),
                                            dbc.Row(
                                                children=[
                                                    dbc.InputGroup(
                                                        children=[
                                                            dbc.Input(
                                                                id='input-gddiscount-acltime',
                                                                type='number',
                                                                placeholder='Desconto na fatura',
                                                                class_name='inputgroup-left-field-modal'
                                                            ),
                                                            dbc.InputGroupText(
                                                                children='%',
                                                                id='input-percentage-years',
                                                                class_name='inputgroup-right-field-modal'
                                                            )
                                                        ],
                                                    )
                                                ] 
                                            ),
                                            html.Br(),

                                            dbc.Fade(
                                                dbc.Row(
                                                    children=[
                                                        dbc.Col(
                                                            children=[
                                                                dbc.Row(
                                                                    children=[
                                                                        dbc.InputGroup(
                                                                            children=[
                                                                                dbc.InputGroupText(year, class_name='inputgroup-left-field-modal'),
                                                                                dbc.Input(
                                                                                    id='input-price-year-0',
                                                                                    placeholder='Preço (R$/MWh)',
                                                                                    class_name='inputgroup-right-field-modal'
                                                                                )
                                                                            ]
                                                                        )
                                                                    ]
                                                                ),

                                                                dbc.Row(
                                                                    children=[
                                                                        dbc.InputGroup(
                                                                            children=[
                                                                                dbc.InputGroupText(year+1, class_name='inputgroup-left-field-modal'),
                                                                                dbc.Input(
                                                                                    id='input-price-year-1',
                                                                                    placeholder='Preço (R$/MWh)',
                                                                                    class_name='inputgroup-right-field-modal'
                                                                                )
                                                                            ]
                                                                        )
                                                                    ]
                                                                ),

                                                                dbc.Row(
                                                                    children=[
                                                                        dbc.InputGroup(
                                                                            children=[
                                                                                dbc.InputGroupText(year+2, class_name='inputgroup-left-field-modal'),
                                                                                dbc.Input(
                                                                                    id='input-price-year-2',
                                                                                    placeholder='Preço (R$/MWh)',
                                                                                    class_name='inputgroup-right-field-modal'
                                                                                )
                                                                            ]
                                                                        )
                                                                    ]
                                                                ),

                                                                dbc.Row(
                                                                    children=[
                                                                        dbc.InputGroup(
                                                                            children=[
                                                                                dbc.InputGroupText(year+3, class_name='inputgroup-left-field-modal'),
                                                                                dbc.Input(
                                                                                    id='input-price-year-3',
                                                                                    placeholder='Preço (R$/MWh)',
                                                                                    class_name='inputgroup-right-field-modal'
                                                                                )
                                                                            ]
                                                                        )
                                                                    ]
                                                                ),

                                                                dbc.Row(
                                                                    children=[
                                                                        dbc.InputGroup(
                                                                            children=[
                                                                                dbc.InputGroupText(year+4, class_name='inputgroup-left-field-modal'),
                                                                                dbc.Input(
                                                                                    id='input-price-year-4',
                                                                                    placeholder='Preço (R$/MWh)',
                                                                                    class_name='inputgroup-right-field-modal'
                                                                                )
                                                                            ]
                                                                        )
                                                                    ]
                                                                )
                                                            ],
                                                            width={'size':4, 'offset':0}
                                                        ),

                                                        dbc.Col(
                                                            children=[
                                                                dbc.Row(
                                                                    children=[
                                                                        dbc.InputGroup(
                                                                            children=[
                                                                                dbc.InputGroupText(
                                                                                    children='Reajuste Anual:',
                                                                                    class_name='inputgroup-left-field-modal'
                                                                                ),
                                                                                dbc.Input(
                                                                                    id='input-annual-adjustment',
                                                                                    class_name='inputgroup-middle-field-modal',
                                                                                    type='number',
                                                                                    value=3.91                                                                                    
                                                                                ),
                                                                                dbc.InputGroupText(
                                                                                    children='%',
                                                                                    class_name='inputgroup-right-field-modal'
                                                                                )
                                                                            ]
                                                                        )
                                                                    ]
                                                                ),
                                                                dbc.Row(
                                                                    children=[
                                                                        dbc.InputGroup(
                                                                            children=[
                                                                                dbc.InputGroupText(
                                                                                    children='Desconto TUSD:',
                                                                                    class_name='inputgroup-left-field-modal'
                                                                                ),
                                                                                dbc.Input(
                                                                                    id='input-tusd-discount',
                                                                                    class_name='inputgroup-middle-field-modal',
                                                                                    type='number',
                                                                                ),
                                                                                dbc.InputGroupText(
                                                                                    children='%',
                                                                                    class_name='inputgroup-right-field-modal'
                                                                                )
                                                                            ]
                                                                        )
                                                                    ]
                                                                )
                                                            ],
                                                            width={'size':4, 'offset':4}
                                                        )
                                                    ]
                                                ),
                                                is_in=True
                                            )
                                        ],
                                        title='DADOS DE FORNECIMENTO'
                                    )
                                ],
                                start_collapsed=True,
                                
                            ),
                            html.Br(),
                        ]
                    ),
                    
                    dbc.ModalFooter(
                        children=[
                            dbc.Button(
                                children='Gerar Proposta',
                                n_clicks=0,
                                color='success',
                                id='btn-gerar-proposta'
                            )
                        ]
                    )
                    
                            
                ],
                is_open=True,
                fullscreen=True
            )
        ]
    )

    return layout
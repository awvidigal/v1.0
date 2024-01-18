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

# Abre o modal de nova proposta
@callback(
    [
        Output(component_id='modal-novo-orcamento', component_property='is_open')
    ],
    [
        Input(component_id='btn-new-proposal',      component_property='n_clicks'),
        Input(component_id='btn-gerar-proposta',    component_property='n_clicks')
    ],
    [
        State(component_id='modal-novo-orcamento', component_property='is_open')
    ],
    prevent_initial_call=True
)
def openModalOrcamento(btnNewProposal, btnGenerateProposal, stateIsOpen):
    if btnNewProposal > 0 or btnGenerateProposal > 0:
        return [not stateIsOpen]
    return [stateIsOpen]

# Função para habilitar campos de demanda e consumo em função da modalidade e subgrupo e alteração de placeholders
@callback(
    [
        # inputs de consumo ponta
        Output(component_id='input-consumo-ponta-jan', component_property='disabled'),
        Output(component_id='input-consumo-ponta-fev', component_property='disabled'),
        Output(component_id='input-consumo-ponta-mar', component_property='disabled'),
        Output(component_id='input-consumo-ponta-abr', component_property='disabled'),
        Output(component_id='input-consumo-ponta-mai', component_property='disabled'),
        Output(component_id='input-consumo-ponta-jun', component_property='disabled'),
        Output(component_id='input-consumo-ponta-jul', component_property='disabled'),
        Output(component_id='input-consumo-ponta-ago', component_property='disabled'),
        Output(component_id='input-consumo-ponta-set', component_property='disabled'),
        Output(component_id='input-consumo-ponta-out', component_property='disabled'),
        Output(component_id='input-consumo-ponta-nov', component_property='disabled'),
        Output(component_id='input-consumo-ponta-dez', component_property='disabled'),

        # inputs de demanda - disabled
        Output(component_id='input-demanda-jan', component_property='disabled'),
        Output(component_id='input-demanda-fev', component_property='disabled'),
        Output(component_id='input-demanda-mar', component_property='disabled'),
        Output(component_id='input-demanda-abr', component_property='disabled'),
        Output(component_id='input-demanda-mai', component_property='disabled'),
        Output(component_id='input-demanda-jun', component_property='disabled'),
        Output(component_id='input-demanda-jul', component_property='disabled'),
        Output(component_id='input-demanda-ago', component_property='disabled'),
        Output(component_id='input-demanda-set', component_property='disabled'),
        Output(component_id='input-demanda-out', component_property='disabled'),
        Output(component_id='input-demanda-nov', component_property='disabled'),
        Output(component_id='input-demanda-dez', component_property='disabled'),

        # inputs de demanda ponta
        Output(component_id='input-demanda-ponta-jan', component_property='disabled'),
        Output(component_id='input-demanda-ponta-fev', component_property='disabled'),
        Output(component_id='input-demanda-ponta-mar', component_property='disabled'),
        Output(component_id='input-demanda-ponta-abr', component_property='disabled'),
        Output(component_id='input-demanda-ponta-mai', component_property='disabled'),
        Output(component_id='input-demanda-ponta-jun', component_property='disabled'),
        Output(component_id='input-demanda-ponta-jul', component_property='disabled'),
        Output(component_id='input-demanda-ponta-ago', component_property='disabled'),
        Output(component_id='input-demanda-ponta-set', component_property='disabled'),
        Output(component_id='input-demanda-ponta-out', component_property='disabled'),
        Output(component_id='input-demanda-ponta-nov', component_property='disabled'),
        Output(component_id='input-demanda-ponta-dez', component_property='disabled'),

        # inputs de demanda - placeholder
        Output(component_id='input-demanda-jan', component_property='placeholder'),
        Output(component_id='input-demanda-fev', component_property='placeholder'),
        Output(component_id='input-demanda-mar', component_property='placeholder'),
        Output(component_id='input-demanda-abr', component_property='placeholder'),
        Output(component_id='input-demanda-mai', component_property='placeholder'),
        Output(component_id='input-demanda-jun', component_property='placeholder'),
        Output(component_id='input-demanda-jul', component_property='placeholder'),
        Output(component_id='input-demanda-ago', component_property='placeholder'),
        Output(component_id='input-demanda-set', component_property='placeholder'),
        Output(component_id='input-demanda-out', component_property='placeholder'),
        Output(component_id='input-demanda-nov', component_property='placeholder'),
        Output(component_id='input-demanda-dez', component_property='placeholder'),

        # inputs de ajuste
        Output(component_id='select-subgrupo-ajustado',     component_property='disabled'),
        Output(component_id='select-modalidade-ajustada',   component_property='disabled'),
        Output(component_id='input-demanda-ajustada',      component_property='disabled'),

        # fade
        Output(component_id='fade-mode', component_property='is_in'),

        # input de desconto gd | tempo de contrato
        Output(component_id='input-gddiscount-acltime', component_property='placeholder'),
        Output(component_id='input-percentage-years',   component_property='children'),

        # inputs de preço no ano
        Output(component_id='input-price-year-0', component_property='disabled'),
        Output(component_id='input-price-year-1', component_property='disabled'),
        Output(component_id='input-price-year-2', component_property='disabled'),
        Output(component_id='input-price-year-3', component_property='disabled'),
        Output(component_id='input-price-year-4', component_property='disabled'),
    ],
    [
        Input(component_id='select-uc',                 component_property='value'),
        Input(component_id='switch-subgrupo',           component_property='value'),
        Input(component_id='switch-modalidade',         component_property='value'),
        Input(component_id='switch-demanda',            component_property='value'),
        Input(component_id='radio-choose-mode',         component_property='value'),
        Input(component_id='input-gddiscount-acltime',  component_property='value')
    ],
    [
        State(component_id='radio-choose-mode',   component_property='value'),
    ],
    prevent_initial_call=True        
)
def fieldsEnable(inputUC, swSubGroup, swModality, swDemand, rdModeInput, inputYears, rdModeState):
    print('executando funcao')
    allOutputs = [
        True,   # 0 -> input-consumo-ponta-jan
        True,   # 1 -> input-consumo-ponta-fev
        True,   # 2 -> input-consumo-ponta-mar
        True,   # 3 -> input-consumo-ponta-abr
        True,   # 4 -> input-consumo-ponta-mai
        True,   # 5 -> input-consumo-ponta-jun
        True,   # 6 -> input-consumo-ponta-jul
        True,   # 7 -> input-consumo-ponta-ago
        True,   # 8 -> input-consumo-ponta-set
        True,   # 9 -> input-consumo-ponta-out
        True,   # 10 -> input-consumo-ponta-nov
        True,   # 11 -> input-consumo-ponta-dez
        True,   # 12 -> input-demanda-jan | disabled
        True,   # 13 -> input-demanda-fev | disabled
        True,   # 14 -> input-demanda-mar | disabled
        True,   # 15 -> input-demanda-abr | disabled
        True,   # 16 -> input-demanda-mai | disabled
        True,   # 17 -> input-demanda-jun | disabled
        True,   # 18 -> input-demanda-jul | disabled
        True,   # 19 -> input-demanda-ago | disabled
        True,   # 20 -> input-demanda-set | disabled
        True,   # 21 -> input-demanda-out | disabled
        True,   # 22 -> input-demanda-nov | disabled
        True,   # 23 -> input-demanda-dez | disabled
        True,   # 24 -> input-demanda-ponta-jan
        True,   # 25 -> input-demanda-ponta-fev
        True,   # 26 -> input-demanda-ponta-mar
        True,   # 27 -> input-demanda-ponta-abr
        True,   # 28 -> input-demanda-ponta-mai
        True,   # 29 -> input-demanda-ponta-jun
        True,   # 30 -> input-demanda-ponta-jul
        True,   # 31 -> input-demanda-ponta-ago
        True,   # 32 -> input-demanda-ponta-set
        True,   # 33 -> input-demanda-ponta-out
        True,   # 34 -> input-demanda-ponta-nov
        True,   # 35 -> input-demanda-ponta-dez
        'Demanda',  # 36 -> input-demanda-jan | placeholder
        'Demanda',  # 37 -> input-demanda-fev | placeholder
        'Demanda',  # 38 -> input-demanda-mar | placeholder
        'Demanda',  # 39 -> input-demanda-abr | placeholder
        'Demanda',  # 40 -> input-demanda-mai | placeholder
        'Demanda',  # 41 -> input-demanda-jun | placeholder
        'Demanda',  # 42 -> input-demanda-jul | placeholder
        'Demanda',  # 43 -> input-demanda-ago | placeholder
        'Demanda',  # 44 -> input-demanda-set | placeholder
        'Demanda',  # 45 -> input-demanda-out | placeholder
        'Demanda',  # 46 -> input-demanda-nov | placeholder
        'Demanda',  # 47 -> input-demanda-dez | placeholder
        True,   # 48 -> select-subgrupo-ajustado    | disabled 
        True,   # 49 -> select-modalidade-ajustada  | disabled 
        True,   # 50 -> input-demanda-ajustada      | disabled
        False,  # 51 -> fade-mode                   | is_in
        'Desconto na fatura',   # 52 -> input-gddiscount-acltime    | placeholder   
        '%',                    # 53 -> input-percentage-years      | children  
        True,   # 54 -> input-price-year-0  | disabled
        True,   # 55 -> input-price-year-1  | disabled
        True,   # 56 -> input-price-year-2  | disabled
        True,   # 57 -> input-price-year-3  | disabled
        True,   # 58 -> input-price-year-4  | disabled
    ]

    boolBT = False

    conn = sql.connect('c:/Users/vidig/OneDrive/Python/agv/v1.0/agv.db')
    cursor = conn.cursor()

    try:
        cursor.execute(
            f'''
                SELECT modalidade
                FROM ucs
                WHERE uc = {inputUC}
            '''
        )

    except Exception as e:
        print(e)

    modalidade = cursor.fetchone()
    modalidade = modalidade[0]


    try:
        cursor.execute(
            f'''
                SELECT subgrupo
                FROM ucs
                WHERE uc = {inputUC}
            '''
        )
    except Exception as e:
        print(e)
    subgrupo = cursor.fetchone()
    subgrupo = subgrupo[0]


    conn.close()

    print(f'Modalidade: {modalidade}\nSubgrupo:{subgrupo}')
    if subgrupo == ('B1' or 'B2' or 'B3'):
        print('entrou no if')
        boolBT = True

    print(boolBT)
    if boolBT == True:
        for output in range(36):
            allOutputs[output] = True
    else:
        for i in range(24):
            allOutputs[i] = False

    if modalidade == 'Azul':
        for i in range(24,36):
            allOutputs[i] = False
        for i in range(36,48):
            allOutputs[i] = 'Demanda Fora Ponta'
    else:
        for i in range(24,36):
            allOutputs[i] = True
        for i in range(36,48):
            allOutputs[i] = 'Demanda'
   
    allOutputs[48] = not swSubGroup
    allOutputs[49] = not swModality
    allOutputs[50] = not swDemand

    if rdModeInput == 1:
        allOutputs[51] = False
        allOutputs[52] = 'Desconto na fatura'
        allOutputs[53] = '%'
    elif rdModeInput == 2:
        allOutputs[51] = True
        allOutputs[52] = 'Tempo de contrato'
        allOutputs[53] = 'anos'

    if rdModeState == 2:
        if not inputYears or inputYears > 5:
            for output in range(54,59):
                allOutputs[output] = True
        elif inputYears < 6:
            for output in range(54,54 + inputYears):
                allOutputs[output] = False
        

    print(allOutputs)
    return allOutputs



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
                                                            dbc.Switch(
                                                                label='Ajuste de subgrupo',
                                                                id='switch-subgrupo',
                                                                value=False,
                                                                input_class_name='switch'
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
                                                                size='md',
                                                                disabled=True
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
                                                           dbc.Switch(
                                                                label='Ajuste de modalidade',
                                                                id='switch-modalidade',
                                                                value=False,
                                                                input_class_name='switch'
                                                            )
                                                        ],
                                                        width={'size':3, 'offset':0}
                                                    ),

                                                    dbc.Col(
                                                        children=[
                                                            dbc.Select(
                                                                class_name='input-field-modal',
                                                                options=modalities,
                                                                id='select-modalidade-ajustada',
                                                                placeholder='Modalidade ajustada...',
                                                                size='md',
                                                                disabled=True
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
                                                            dbc.Switch(
                                                                label='Ajuste de demanda',
                                                                id='switch-demanda',
                                                                value=False,
                                                                input_class_name='switch'
                                                            )
                                                        ],
                                                        width={'size':3, 'offset':0}
                                                    ),

                                                    dbc.Col(
                                                        children=[
                                                            dbc.Input(
                                                                class_name='input-field-modal',
                                                                id='input-demanda-ajustada',
                                                                placeholder='Demanda ajustada...',
                                                                type='number',
                                                                size='md',
                                                                disabled=True
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
                                                                                    class_name='inputgroup-right-field-modal',
                                                                                    disabled=True
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
                                                                                    class_name='inputgroup-right-field-modal',
                                                                                    disabled=True
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
                                                                                    class_name='inputgroup-right-field-modal',
                                                                                    disabled=True
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
                                                                                    class_name='inputgroup-right-field-modal',
                                                                                    disabled=True
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
                                                                                    class_name='inputgroup-right-field-modal',
                                                                                    disabled=True
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
                                                is_in=False,
                                                id='fade-mode'
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
                is_open=False,
                fullscreen=True,
                id='modal-novo-orcamento'
            )
        ]
    )

    return layout
import dash_bootstrap_components as dbc
from dash import html

def createNavBar():
    # navBar = dbc.NavbarSimple(
    #     children=[
    #         dbc.NavItem(
    #             children=[
    #                 html.Img(src='/assets/logo_negativo.png', id='siteLogo'),
    #                 dbc.NavLink('Home', href='pages\home.py', class_name='menuLink'),
    #                 dbc.NavLink('Clientes', href='pages\clientes.py', class_name='menuLink'),
    #                 dbc.NavLink('Orçamentos', href='pages\orcamentos.py', class_name='menuLink'),
    #                 dbc.NavLink('Monitoramento', href='pages\monitoramento.py', class_name='menuLink')
    #             ],
    #             class_name='navitem'
    #         ),
            
            
    #     ],
    #     links_left=False,
    #     id='navigation',
    #     color='dark',
    #     dark=True,
    #     fluid=True,
    #     expand='xl'
    # 
    # )
    menu = dbc.Row(
        [
            dbc.Col(html.A('Home', href='pages\home.py', className='menuLink'), width='auto'),
            dbc.Col(html.A('Clientes', href='pages\clientes.py', className='menuLink'), width='auto'),
            # dbc.Col(dbc.NavLink('UCs', href='pages\unidades.py', class_name='menuLink'), width=True),
            dbc.Col(html.A('Orçamentos', href='pages\orcamentos.py', className='menuLink'), width='auto'),
            dbc.Col(html.A('Monitoramento', href='pages\monitormento.py', className='menuLink'), width='auto'),            
        ],
        align='center',
        justify='end'
    )

    navBar = dbc.Navbar(
        dbc.Container(
                dbc.Row(
                    [
                        dbc.Col(html.Img(src='/assets/logo_negativo.png', id='siteLogo'), width={'size':2, 'offset':0}),
                        dbc.Col(menu, width={'size':6, 'offset':4})
                    ],
                    align='center',
                    # justify='end',
                    class_name='nav-menu-row'
                ),
                fluid=True,
                class_name='nav-container'
        ),
        color='#000000',
        light=False,
        dark=True,
        class_name='navbar',
    )
    return navBar

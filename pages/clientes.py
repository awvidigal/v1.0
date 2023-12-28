import dash
from dash import html, dcc, callback, Input, Output

dash.register_page(
    __name__,
    name='Clientes',
    path='/clientes'
)

def layout():
    layout = html.Div(
        html.H1('pagina de clientes')
    )

    return layout
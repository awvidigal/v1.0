import dash
from dash import html, dcc, callback, Input, Output

dash.register_page(
    __name__,
    name='Monitoramento',
    path='/monitoramento'
)

def layout():
    layout = html.Div(
        html.H1('pagina de monitoramento')
    )

    return layout
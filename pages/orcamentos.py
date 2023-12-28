import dash
from dash import html, dcc, callback, Input, Output

dash.register_page(
    __name__,
    name='Orçamentos',
    path='/orcamentos'
)

def layout():
    layout = html.Div(
        html.H1('pagina de orcamentos')
    )

    return layout
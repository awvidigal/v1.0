from dash import html, register_page, callback

register_page(
    __name__,
    name='Home',
    path='/'    
)

def layout():
    layout = html.Div(
        html.H1('Homepage')
    )

    return layout
import dash_html_components as html
from dash.dependencies import Output, Input


def page_load_anchor_issue(app, trigger_id=None, output_id=None):
    # Setup dummy elements.
    trigger_id = "trigger" if trigger_id is None else trigger_id
    output_id = "output" if output_id is None else output_id
    app.layout += [html.Div(id=trigger_id, style={"display": "none"}),
                   html.Div(id=output_id, style={"display": "none"})]
    # Add client side callback that scrolls to anchor location after load.
    app.clientside_callback(
        """
        function(value) {
            const match = document.getElementById(window.location.hash.substring(1))
            if(match){
                match.scrollIntoView();
            }
        }
        """,
        Output('dummy', 'children'),
        [Input('trigger', 'children')],
        prevent_initial_call=False)

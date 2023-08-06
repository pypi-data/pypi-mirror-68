import uuid
import dash_core_components as dcc
import dash_html_components as html

from dash.dependencies import Output, Input


def fix_page_load_anchor_issue(app, delay=None):
    """
    Fixes the issue that the pages is not scrolled to the anchor position on initial load.
    :param app: the Dash app object
    :param delay: in some cases, an additional delay might be needed for the page to load, specify in ms
    :return: dummy elements, which must be added to the layout for the fix to work
    """
    # Create dummy components.
    input_id, output_id = str(uuid.uuid4()), str(uuid.uuid4())
    dummy_input = html.Div(id=input_id, style={"display": "hidden"})
    dummy_output = html.Div(id=output_id, style={"display": "hidden"})
    # Setup the callback that does the magic.
    app.clientside_callback(
        """
        function(dummy_value) {{
            setTimeout(function(){{
                const match = document.getElementById(window.location.hash.substring(1))
                match.scrollIntoView();
            }}, {});
        }}
        """.format(delay),
        Output(output_id, "children"), [Input(input_id, "children")], prevent_initial_call=False)
    return [dummy_input, dummy_output]


def download_store(app, id, dummy_output=None, **kwargs):
    elements = [dcc.Store(id=id, **kwargs)]
    # If no output is provided, create one and return it. The user MUST add this element to the app layout.
    if dummy_output is None:
        output_id = str(uuid.uuid4())
        dummy_output = Output(output_id, "data")
        elements.append(dcc.Store(id=output_id))
    # Setup the callback.
    app.clientside_callback(
        """
        function(args) {
            var blob = new Blob([args["data"]], { type: args["type"] });
            var filename = args["filename"];
            // Save file function, from https://stackoverflow.com/questions/19327749/javascript-blob-filename-without-link
            if (window.navigator.msSaveOrOpenBlob) {
                window.navigator.msSaveOrOpenBlob(blob, filename);
            } else {
                const a = document.createElement('a');
                document.body.appendChild(a);
                const url = window.URL.createObjectURL(blob);
                a.href = url;
                a.download = filename;
                a.click();
                setTimeout(() => {
                  window.URL.revokeObjectURL(url);
                  document.body.removeChild(a);
                  }, 0)
            }
            // Return nothing. 
            return "";
        }
        """,
        [dummy_output], [Input(id, "data")]
    )
    # Return elements that must be added to the layout.
    return elements

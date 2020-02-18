import dash
from dash.dependencies import Input, Output, State
from app import app
from app.models import Utilization
from sqlalchemy import Integer, func
from sqlalchemy.sql.expression import cast
from openpyxl import Workbook, load_workbook



# CITY DROPDOWN - ACCESS
# disabling/enabling dropdown (so that it's disabled when the value of the upstream dropdown changes but enabled when its own options finish updating and change).
# General Note: Note that all higher upstream dropdown values are used as inputs in these types of functions as all downstream dropdowns are to be disabled as quickly
# as possible vs. waiting in line for their turn.
@app.callback(
    Output('city_dropdown', 'disabled'),
    [
        Input('state_dropdown', 'value'),
        Input('city_dropdown', 'options')
    ]
)
def city_access(*args):
    context = dash.callback_context.triggered[0]['prop_id']
    if context != 'city_dropdown.options':
        return True
    else:
        return False



# CITY DROPDOWN - UPDATING OPTIONS & CLEARING VALUES
# update dropdown options.
# General Note: Note that only the next level upstream dropdown value is needed as an input in these types of functions, as changes to values in higher upstream dropdowns will trigger
# the next lower one to clear and its options to update (and so forth).  If all higher upstream dropdown values are used as inputs in these types of fuctions then the database
# could be queried multiple times to update the options of a downstream dropdown after only one [real] upstream dropdown value change.  So the intent is for applicable
# downstream dropdowns to wait their turn for their options to be updated and their values to be cleared.
@app.callback(
    [
        Output('city_dropdown', 'options'),
        Output('city_dropdown', 'value')
    ],
    [
        Input('state_dropdown', 'value'),
    ]
)
def city_update(state_value):
    filters = {}

    # if not blank, ensure values are in a list
    state_value = [state_value, ] if state_value and not isinstance(state_value, list) else state_value

    # if not blank, put values in dictionary
    if state_value: filters['state'] = state_value

    # build query
    query = Utilization.query.with_entities(Utilization.city).group_by(Utilization.city).order_by(Utilization.city)
    if filters:
        for col, value in filters.items():
            query = query.filter(getattr(Utilization, col).in_(value))

    return [{'label': result[0], 'value': result[0]} for result in query], ''



# ZIP_CODE DROPDOWN - ACCESS
@app.callback(
    Output('zip_code_dropdown', 'disabled'),
    [
        Input('state_dropdown', 'value'),
        Input('city_dropdown', 'value'),
        Input('zip_code_dropdown', 'options')
    ]
)
def zip_code_access(*args):
    context = dash.callback_context.triggered[0]['prop_id']
    if context != 'zip_code_dropdown.options':
        return True
    else:
        return False



# ZIP_CODE CODE DROPDOWN - UPDATING OPTIONS & CLEARING VALUES
@app.callback(
    [
        Output('zip_code_dropdown', 'options'),
        Output('zip_code_dropdown', 'value')
    ],
    [
        Input('city_dropdown', 'value')
    ],
    [
        State('state_dropdown', 'value')
    ]
)
def zip_code_update(city_value, state_value):
    filters = {}

    # if not blank, ensure values are in a list
    state_value = [state_value, ] if state_value and not isinstance(state_value, list) else state_value
    city_value = [city_value, ] if city_value and not isinstance(city_value, list) else city_value

    # if not blank, put values in dictionary
    if state_value: filters['state'] = state_value
    if city_value: filters['city'] = city_value

    # build query
    query = Utilization.query.with_entities(Utilization.zip_code).group_by(Utilization.zip_code).order_by(Utilization.zip_code)
    if filters:
        for col, value in filters.items():
            query = query.filter(getattr(Utilization, col).in_(value))

    return [{'label': result[0], 'value': result[0]} for result in query], ''


# PLACE_OF_SERVICE DROPDOWN - ACCESS
@app.callback(
    Output('place_of_service_dropdown', 'disabled'),
    [
        Input('state_dropdown', 'value'),
        Input('city_dropdown', 'value'),
        Input('zip_code_dropdown', 'value'),
        Input('place_of_service_dropdown', 'options')
    ]
)
def place_of_service_access(*args):
    context = dash.callback_context.triggered[0]['prop_id']
    if context != 'place_of_service_dropdown.options':
        return True
    else:
        return False


# PLACE_OF_SERVICE DROPDOWN - UPDATING OPTIONS & CLEARING VALUES
@app.callback(
    [
        Output('place_of_service_dropdown', 'options'),
        Output('place_of_service_dropdown', 'value')
    ],
    [
        Input('zip_code_dropdown', 'value')
    ],
    [
        State('state_dropdown', 'value'),
        State('city_dropdown', 'value')
    ]
)
def place_of_service_update(zip_code_value, state_value, city_value):
    filters = {}

    # if not blank, ensure values are in a list
    state_value = [state_value, ] if state_value and not isinstance(state_value, list) else state_value
    city_value = [city_value, ] if city_value and not isinstance(city_value, list) else city_value
    zip_code_value = [zip_code_value, ] if zip_code_value and not isinstance(zip_code_value, list) else zip_code_value

    # if not blank, put values in dictionary
    if state_value: filters['state'] = state_value
    if city_value: filters['city'] = city_value
    if zip_code_value: filters['zip_code'] = zip_code_value

    # build query
    query = Utilization.query.with_entities(Utilization.place_of_service).group_by(Utilization.place_of_service).order_by(Utilization.place_of_service)
    if filters:
        for col, value in filters.items():
            query = query.filter(getattr(Utilization, col).in_(value))

    return [{'label': result[0], 'value': result[0]} for result in query], ''



# PROVIDER TYPE DROPDOWN - ACCESS
@app.callback(
    Output('provider_type_dropdown', 'disabled'),
    [
        Input('state_dropdown', 'value'),
        Input('city_dropdown', 'value'),
        Input('zip_code_dropdown', 'value'),
        Input('place_of_service_dropdown', 'value'),
        Input('provider_type_dropdown', 'options')
    ]
)
def provider_type_access(*args):
    context = dash.callback_context.triggered[0]['prop_id']
    if context != 'provider_type_dropdown.options':
        return True
    else:
        return False



# PROVIDER TYPE DROPDOWN - UPDATING OPTIONS & CLEARING VALUES
@app.callback(
    [
        Output('provider_type_dropdown', 'options'),
        Output('provider_type_dropdown', 'value')
    ],
    [
        Input('place_of_service_dropdown', 'value')
    ],
    [
        State('state_dropdown', 'value'),
        State('city_dropdown', 'value'),
        State('zip_code_dropdown', 'value')
    ]
)
def provider_type_update(place_of_service_value, state_value, city_value, zip_code_value):
    filters = {}

    # if not blank, ensure values are in a list
    state_value = [state_value, ] if state_value and not isinstance(state_value, list) else state_value
    city_value = [city_value, ] if city_value and not isinstance(city_value, list) else city_value
    zip_code_value = [zip_code_value, ] if zip_code_value and not isinstance(zip_code_value, list) else zip_code_value
    place_of_service_value = [place_of_service_value, ] if place_of_service_value and not isinstance(place_of_service_value, list) else place_of_service_value

    # if not blank, put values in dictionary
    if state_value: filters['state'] = state_value
    if city_value: filters['city'] = city_value
    if zip_code_value: filters['zip_code'] = zip_code_value
    if place_of_service_value: filters['place_of_service'] = place_of_service_value

    # build query
    query = Utilization.query.with_entities(Utilization.provider_type).group_by(Utilization.provider_type).order_by(Utilization.provider_type)
    if filters:
        for col, value in filters.items():
            query = query.filter(getattr(Utilization, col).in_(value))

    return [{'label': result[0], 'value': result[0]} for result in query], ''



# CREDENTIAL DROPDOWN - ACCESS
@app.callback(
    Output('credential_dropdown', 'disabled'),
    [
        Input('state_dropdown', 'value'),
        Input('city_dropdown', 'value'),
        Input('zip_code_dropdown', 'value'),
        Input('place_of_service_dropdown', 'value'),
        Input('provider_type_dropdown', 'value'),
        Input('credential_dropdown', 'options')
    ]
)
def credential_access(*args):
    context = dash.callback_context.triggered[0]['prop_id']
    if context != 'credential_dropdown.options':
        return True
    else:
        return False



# CREDENTIAL DROPDOWN - UPDATING OPTIONS & CLEARING VALUES
@app.callback(
    [
        Output('credential_dropdown', 'options'),
        Output('credential_dropdown', 'value')
    ],
    [
        Input('provider_type_dropdown', 'value')
    ],
    [
        State('state_dropdown', 'value'),
        State('city_dropdown', 'value'),
        State('zip_code_dropdown', 'value'),
        State('place_of_service_dropdown', 'value')
    ]
)
def credential_update(provider_type_value, state_value, city_value, zip_code_value, place_of_service_value):
    filters = {}

    # if not blank, ensure values are in a list
    state_value = [state_value, ] if state_value and not isinstance(state_value, list) else state_value
    city_value = [city_value, ] if city_value and not isinstance(city_value, list) else city_value
    zip_code_value = [zip_code_value, ] if zip_code_value and not isinstance(zip_code_value, list) else zip_code_value
    place_of_service_value = [place_of_service_value, ] if place_of_service_value and not isinstance(place_of_service_value, list) else place_of_service_value
    provider_type_value = [provider_type_value, ] if provider_type_value and not isinstance(provider_type_value, list) else provider_type_value

    # if not blank, put values in dictionary
    if state_value: filters['state'] = state_value
    if city_value: filters['city'] = city_value
    if zip_code_value: filters['zip_code'] = zip_code_value
    if place_of_service_value: filters['place_of_service'] = place_of_service_value
    if provider_type_value: filters['provider_type'] = provider_type_value

    # build query
    query = Utilization.query.with_entities(Utilization.credential).group_by(Utilization.credential).order_by(Utilization.credential)
    if filters:
        for col, value in filters.items():
            query = query.filter(getattr(Utilization, col).in_(value))

    return [{'label': result[0], 'value': result[0]} for result in query], ''



# HCPCS CODE DROPDOWN - ACCESS
@app.callback(
    Output('hcpcs_code_dropdown', 'disabled'),
    [
        Input('state_dropdown', 'value'),
        Input('city_dropdown', 'value'),
        Input('zip_code_dropdown', 'value'),
        Input('place_of_service_dropdown', 'value'),
        Input('provider_type_dropdown', 'value'),
        Input('credential_dropdown', 'value'),
        Input('hcpcs_code_dropdown', 'options')
    ]
)
def hcpcs_code_access(*args):
    context = dash.callback_context.triggered[0]['prop_id']
    if context != 'hcpcs_code_dropdown.options':
        return True
    else:
        return False



# HCPCS CODE DROPDOWN - UPDATING OPTIONS & CLEARING VALUES
@app.callback(
    [
        Output('hcpcs_code_dropdown', 'options'),
        Output('hcpcs_code_dropdown', 'value')
    ],
    [
        Input('credential_dropdown', 'value')
    ],
    [
        State('state_dropdown', 'value'),
        State('city_dropdown', 'value'),
        State('zip_code_dropdown', 'value'),
        State('place_of_service_dropdown', 'value'),
        State('provider_type_dropdown', 'value')
    ]
)
def hcpcs_code_update(credential_value, state_value, city_value, zip_code_value, place_of_service_value, provider_type_value):
    filters = {}

    # if not blank, ensure values are in a list
    state_value = [state_value, ] if state_value and not isinstance(state_value, list) else state_value
    city_value = [city_value, ] if city_value and not isinstance(city_value, list) else city_value
    zip_code_value = [zip_code_value, ] if zip_code_value and not isinstance(zip_code_value, list) else zip_code_value
    place_of_service_value = [place_of_service_value, ] if place_of_service_value and not isinstance(place_of_service_value, list) else place_of_service_value
    provider_type_value = [provider_type_value, ] if provider_type_value and not isinstance(provider_type_value, list) else provider_type_value
    credential_value = [credential_value, ] if credential_value and not isinstance(credential_value, list) else credential_value

    # if not blank, put values in dictionary
    if state_value: filters['state'] = state_value
    if city_value: filters['city'] = city_value
    if zip_code_value: filters['zip_code'] = zip_code_value
    if place_of_service_value: filters['place_of_service'] = place_of_service_value
    if provider_type_value: filters['provider_type'] = provider_type_value
    if credential_value: filters['credential'] = credential_value

    # build query
    query = Utilization.query.with_entities(Utilization.hcpcs_code).group_by(Utilization.hcpcs_code).order_by(Utilization.hcpcs_code)
    if filters:
        for col, value in filters.items():
            query = query.filter(getattr(Utilization, col).in_(value))

    return [{'label': result[0], 'value': result[0]} for result in query], ''



# HCPCS DESCRIPTION TEXTBOX - VISIBILITY & VALUES
@app.callback(
    [
        Output('hcpcs_description_textbox', 'hidden'),
        Output('hcpcs_description_textbox', 'value')
    ],
    [
        Input('hcpcs_description_checkbox', 'value'),
        Input('hcpcs_code_dropdown', 'options')
    ],
    [
        State('state_dropdown', 'value'),
        State('city_dropdown', 'value'),
        State('zip_code_dropdown', 'value'),
        State('place_of_service_dropdown', 'value'),
        State('provider_type_dropdown', 'value'),
        State('credential_dropdown', 'value'),
        State('hcpcs_code_dropdown', 'value')
    ]
)
def hcpcs_description_update(hcpcs_description_checkbox_value, hcpcs_code_options, state_value, city_value, zip_code_value, place_of_service_value, provider_type_value, credential_value, hcpcs_code_value):
    if hcpcs_description_checkbox_value and hcpcs_description_checkbox_value[0] == 'yes':
        filters = {}
        text = '\n'

        # if not blank, ensure values are in a list
        state_value = [state_value, ] if state_value and not isinstance(state_value, list) else state_value
        city_value = [city_value, ] if city_value and not isinstance(city_value, list) else city_value
        zip_code_value = [zip_code_value, ] if zip_code_value and not isinstance(zip_code_value, list) else zip_code_value
        place_of_service_value = [place_of_service_value, ] if place_of_service_value and not isinstance(place_of_service_value, list) else place_of_service_value
        provider_type_value = [provider_type_value, ] if provider_type_value and not isinstance(provider_type_value, list) else provider_type_value
        credential_value = [credential_value, ] if credential_value and not isinstance(credential_value, list) else credential_value
        hcpcs_code_value = [hcpcs_code_value, ] if hcpcs_code_value and not isinstance(hcpcs_code_value, list) else hcpcs_code_value

        # if not blank, put values in dictionary
        if state_value: filters['state'] = state_value
        if city_value: filters['city'] = city_value
        if zip_code_value: filters['zip_code'] = zip_code_value
        if place_of_service_value: filters['place_of_service'] = place_of_service_value
        if provider_type_value: filters['provider_type'] = provider_type_value
        if credential_value: filters['credential'] = credential_value
        if hcpcs_code_value: filters['hcpcs_code'] = hcpcs_code_value

        # build query
        # (This query provides the desired result even though an aggregate function isn't specified for the hcpcs desc column [in order to decrease query run time].)
        query = Utilization.query.with_entities(Utilization.hcpcs_code, Utilization.hcpcs_desc).group_by(Utilization.hcpcs_code).order_by(Utilization.hcpcs_code)
        if filters:
            for col, value in filters.items():
                query = query.filter(getattr(Utilization, col).in_(value))

        # build text
        for result in query:
            text = text + f'{result.hcpcs_code}:\t{result.hcpcs_desc}\n'

        return False, text
    else:
        return True, ''
    
    
    
# SUBMIT BUTTON - ACCESS
# (Note that the purpose of disabling the submit button is to help safeguard a user from submitting a set of values that are stale; this could occur if the submit button was pressed
# while dropdowns were being updated and their values from previous selections had not yet been cleared.)
@app.callback(
    Output('submit_button', 'disabled'),
    [
        Input('state_dropdown', 'disabled'),
        Input('city_dropdown', 'disabled'),
        Input('zip_code_dropdown', 'disabled'),
        Input('place_of_service_dropdown', 'disabled'),
        Input('provider_type_dropdown', 'disabled'),
        Input('credential_dropdown', 'disabled'),
        Input('hcpcs_code_dropdown', 'disabled')
    ]
)
def submit_button_visible(*dropdown_disabled):
    # disable submit button if any of the applicable dropdowns are disabled, else enable
    if any(dropdown_disabled):
        return True
    else:
        return False



# EXPORT BUTTON - VISIBILITY
# (Note that the user is required to first press the Submit button before having the option to export; the data displayed on the screen should match what's exported.
# This is to help the user export what they intend- otherwise, they could make changes to the selection values, forget to press the Submit button to refresh the display,
# and then export what they think is displayed vs. their now updated selections.)
# (Fyi, CSS is used to hide/unhide this button since there is not a functioning 'hidden' attribute for this button.)
@app.callback(
    Output('export_button', 'style'),
    [
        Input('submit_button', 'n_clicks'),
        Input('state_dropdown', 'value'),
        Input('city_dropdown', 'value'),
        Input('zip_code_dropdown', 'value'),
        Input('place_of_service_dropdown', 'value'),
        Input('provider_type_dropdown', 'value'),
        Input('credential_dropdown', 'value'),
        Input('hcpcs_code_dropdown', 'value'),
        Input('rank_position_dropdown', 'value'),
        Input('rank_by_dropdown', 'value')
    ]
)
def export_button_visible(submit_button_clicks, *args):
    context = dash.callback_context.triggered[0]['prop_id']

    # if the submit button (n_clicks property) was not the trigger or it doesn't have a n_clicks value (i.e. the button wasn't actually pressed so n_clicks has a value of None) then hide export button, else [show]
    if context != 'submit_button.n_clicks' or not submit_button_clicks:
        return dict(display='none')
    else:
        return dict()



# EXPORT TO EXCEL
@app.callback(
    # callbacks must have an output (even if you don't require one) so chose the export button's language property
    Output('export_button', 'lang'),
    [
        Input('export_button', 'n_clicks')
    ]
)
def export_to_excel(export_button_clicks):
    wb = Workbook()



# REQUIRED INPUTS MESSAGE - VALUES & VISIBILITY
# (Note that the Rank Position and Rank By selections are required.  The app (elsewhere... not in this callback) assumes a Rank Position value of "Top" and a Rank By value of "Avg Charged" if the provided values
# from the user are not valid.  For example, the user could delete a selected value and leave the value of the dropdown as an empty string.  The callback below simply displays a message prompt
# to inform the user on what value will be assumed if a provided selection is invalid.  Whether the user selects "OK" or "Cancel" on the message prompt does not impact the app's behavior.)
@app.callback(
    [
        Output('required_inputs_message', 'displayed'),
        Output('required_inputs_message', 'message'),
    ],
    [
        Input('submit_button', 'n_clicks'),
    ],
    [
        State('rank_position_dropdown', 'value'),
        State('rank_by_dropdown', 'value')
    ]
)
def required_inputs_message_update(submit_button_clicks, rank_position_value, rank_by_value):
    mssg = []
    mssg += ['"Top" will be used for the Rank Position value'] if rank_position_value not in ['Top', 'Bottom'] else []
    mssg += ['"Avg Charged" will be used for the Rank By value'] if rank_by_value not in ['Avg Charged', 'Patient'] else []
    plural_ending = 's' if len(mssg) > 1 else ''
    mssg = ' and '.join(mssg)

    if mssg:
        mssg = f'Rank Position and Rank By selections are required.  Instead of the invalid value{plural_ending} provided, ' + mssg + '.'
        return True, mssg
    else:
        return False, mssg



# RESULTS (all tables/charts) - VISIBILITY & VALUES
# (Note that the purpose of having the graphs and tables in one callback is so they populate on screen all at once vs piece-meal since some queries/etc. take longer than others.)
@app.callback(
    [
        Output('results_container', 'style'),
        Output('ten_table', 'data'),
        Output('bar_chart', 'figure')
    ],
    [
        Input('submit_button', 'n_clicks'),
        Input('state_dropdown', 'value'),
        Input('city_dropdown', 'value'),
        Input('zip_code_dropdown', 'value'),
        Input('place_of_service_dropdown', 'value'),
        Input('provider_type_dropdown', 'value'),
        Input('credential_dropdown', 'value'),
        Input('hcpcs_code_dropdown', 'value'),
        Input('rank_position_dropdown', 'value'),
        Input('rank_by_dropdown', 'value')
    ]
)
def results_update(submit_button_clicks, state_value, city_value, zip_code_value, place_of_service_value, provider_type_value, credential_value, hcpcs_code_value, rank_position_value, rank_by_value):
    # the display value is set to none so that the results are hidden
    results_container_style = {'minHeight': '100%', 'maxHeight': '100%', 'minWidth': '75%', 'maxWidth': '75%', 'display':'none'}
    context = dash.callback_context.triggered[0]['prop_id']

    # if the submit button (n_clicks property) was not the trigger or it doesn't have a n_clicks value (i.e. the button wasn't actually pressed so n_clicks has a value of None) then return no data and hide results, else return data and [unhide] results
    if context != 'submit_button.n_clicks' or not submit_button_clicks:
        return results_container_style, '', ''
    else:
        filters = {}
        order_by_col = 'num_beneficiaries' if rank_by_value == 'Patient' else 'avg_charged'
        bar_chart_increment = 200
        bar_chart_num_groupings = 11
        bar_chart_x_values = []
        bar_chart_x_axis_values = []
        bar_chart_y_axis_values = []
        bar_chart_last_y_value = 0
        bar_chart_figure = {}

        # make the results visible (by setting the container's display attribute to it's default value)
        results_container_style['display'] = 'initial'

        # if not blank, ensure values are in a list
        state_value = [state_value, ] if state_value and not isinstance(state_value, list) else state_value
        city_value = [city_value, ] if city_value and not isinstance(city_value, list) else city_value
        zip_code_value = [zip_code_value, ] if zip_code_value and not isinstance(zip_code_value, list) else zip_code_value
        place_of_service_value = [place_of_service_value, ] if place_of_service_value and not isinstance(place_of_service_value, list) else place_of_service_value
        provider_type_value = [provider_type_value, ] if provider_type_value and not isinstance(provider_type_value, list) else provider_type_value
        credential_value = [credential_value, ] if credential_value and not isinstance(credential_value, list) else credential_value
        hcpcs_code_value = [hcpcs_code_value, ] if hcpcs_code_value and not isinstance(hcpcs_code_value, list) else hcpcs_code_value

        # if not blank, put values in dictionary
        if state_value: filters['state'] = state_value
        if city_value: filters['city'] = city_value
        if zip_code_value: filters['zip_code'] = zip_code_value
        if place_of_service_value: filters['place_of_service'] = place_of_service_value
        if provider_type_value: filters['provider_type'] = provider_type_value
        if credential_value: filters['credential'] = credential_value
        if hcpcs_code_value: filters['hcpcs_code'] = hcpcs_code_value

        # queries
        ten_table_query = Utilization.query.with_entities(Utilization.provider_id, Utilization.num_beneficiaries, Utilization.avg_charged, Utilization.avg_allowed, Utilization.avg_paid)
        # (find the avg charged groupings by [rounding to the nearest multiple of the increment] and grouping these up while summing up the number of patients)
        bar_chart_query = Utilization.query.with_entities(((cast(Utilization.avg_charged / bar_chart_increment, Integer) + 1) * bar_chart_increment).label('charged_group'), func.sum(Utilization.num_beneficiaries).label('patients')).group_by(((cast(Utilization.avg_charged / bar_chart_increment, Integer) + 1) * bar_chart_increment)).order_by(((cast(Utilization.avg_charged / bar_chart_increment, Integer) + 1) * bar_chart_increment))

        if filters:
            for col, value in filters.items():
                ten_table_query = ten_table_query.filter(getattr(Utilization, col).in_(value))
                bar_chart_query = bar_chart_query.filter(getattr(Utilization, col).in_(value))

        # finalize ten table query
        if rank_position_value == 'Bottom':
            ten_table_query = ten_table_query.order_by(getattr(Utilization, order_by_col))
        else:
            ten_table_query = ten_table_query.order_by(getattr(Utilization, order_by_col).desc())

        ten_table_query = ten_table_query.limit(10)

        # get ten table results
        # (also format numbers with commas but no decimals as a string; fyi, you can use the DataTable's format attribute in Dash instead of doing this)
        ten_table_data = [{'provider_id':f'{result.provider_id:,.0f}', 'patients':f'{result.num_beneficiaries:,.0f}', 'avg_charged':f'{result.avg_charged:,.0f}', 'avg_allowed':f'{result.avg_allowed:,.0f}', 'avg_paid':f'{result.avg_paid:,.0f}'} for result in ten_table_query]

        # ---get bar chart results---
        # build up the x values starting with the lowest one (i.e. the first one) in the query
        bar_chart_x_values.append(bar_chart_query[0].charged_group)

        # then increment a certain number of times based on the number of groupings, to end up with n-1 x values; afterwards, add the last x value by using the same value as in the n-1 position
        for i in range(bar_chart_num_groupings-2):
            bar_chart_x_values.append(bar_chart_x_values[i] + bar_chart_increment)
        else:
            bar_chart_x_values.append(bar_chart_x_values[-1])

        # build the x axis values
        bar_chart_x_axis_values = [None] * len(bar_chart_x_values)

        for i in range(bar_chart_num_groupings):
            if i != 0 and i != bar_chart_num_groupings-1:
                bar_chart_x_axis_values[i] = f'{bar_chart_x_values[i-1]:,} - {bar_chart_x_values[i]:,}'
            elif i == 0:
                bar_chart_x_axis_values[i] = f'0 - {bar_chart_x_values[i]:,}'
            else:
                bar_chart_x_axis_values[i] = f'{bar_chart_x_values[i]:,}+'

        # build y values
        bar_chart_y_axis_values = [None] * len(bar_chart_x_values)

        for result in bar_chart_query:
            if result.charged_group in bar_chart_x_values[:-1]:
                bar_chart_y_axis_values[bar_chart_x_values[:-1].index(result.charged_group)] = result.patients
            else:
                bar_chart_last_y_value += result.patients
        else:
            bar_chart_y_axis_values[-1] = bar_chart_last_y_value

    bar_chart_figure = {
        'data':
            [
            {'x': bar_chart_x_axis_values, 'y': bar_chart_y_axis_values, 'type': 'bar'}
            ],
        'layout':
            {
            'title': 'Patients by Average Charged Amount',
            'margin':
                {
                    't': '40',
                },
            'xaxis':
                {
                    'type': 'category',
                    'title':
                        {
                            'text': '<b>Avg Charged</b>'
                        }
                },
            'yaxis':
                {
                    'title':
                        {
                            'text': '<b>Patients</b>'
                        }
                }
            }
    }

    # make visible and return results
    return results_container_style, ten_table_data, bar_chart_figure



# SPINNER - VISIBILITY
@app.callback(
    Output('spinner_container', 'style'),
    [
        Input('submit_button', 'n_clicks'),
        Input('results_container', 'style')
    ]
)
def spinner_visible(submit_button_clicks, results_container_style):
    context = dash.callback_context.triggered[0]['prop_id']

    # show spinner if the submit button (n_clicks) was the trigger and it has a value (i.e. it was actually pressed and doesn't have a value of None) and the results aren't visible (so that pressing the submit button again after the results have already been populated doesn't show a spinner)... else hide spinner
    if context == 'submit_button.n_clicks' and submit_button_clicks and (results_container_style['display'] != 'initial' if 'display' in results_container_style else True):
        return {'minHeight': '100%', 'maxHeight': '100%', 'minWidth': '100%', 'maxWidth': '100%', 'display': 'initial'}
    else:
        return {'display': 'none'}
# importing Libraries

import pandas as pd
import numpy as np
import dash
import os
import shutil
import socket
from dash import dcc, html, Input, Output, State, Dash
import dash_bootstrap_components as dbc
from dash_bootstrap_components._components.Container import Container
import dash_daq as daq
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime
from datetime import timedelta
import datetime as dt
import calendar
from pandas.tseries.offsets import MonthEnd
from dateutil.relativedelta import relativedelta
from dash_iconify import DashIconify


# LOAD INPUTS ##################
colour1 = "#3D555E"  #BG Grey/Green
colour2 = "#E7EAEB"  #Off White
colour3 = "#93F205"  #Green
colour4 = "#1DC8F2"  #Blue
colour5 = "#F27D11"  #Orange

colors = {
    'background': colour1,
    'text': colour2,
    'green_text': colour3,
    'blue_text': colour4,
    'orange_text': colour5
}

load_start_date = "2021-09-30"
load_end_date = "2023-09-30"

class Portfolio:
    def __init__(self, portfolioCode):
        self.df_L1_w = pd.read_parquet('./ServerData/'+portfolioCode+'/df_L1_w.parquet')
        self.df_L1_w.index = pd.to_datetime(self.df_L1_w.index, format= '%Y-%m-%d')
        self.df_L2_w = pd.read_parquet('./ServerData/'+portfolioCode+'/df_L2_w.parquet')
        self.df_L2_w.index = pd.to_datetime(self.df_L2_w.index, format= '%Y-%m-%d')
        self.df_L3_w = pd.read_parquet('./ServerData/'+portfolioCode+'/df_L3_w.parquet')
        self.df_L3_w.index = pd.to_datetime(self.df_L3_w.index, format='%Y-%m-%d')
        self.df_L3_limits = pd.read_parquet('./ServerData/'+portfolioCode+'/df_L3_limits.parquet')
        self.df_L1_r = pd.read_parquet('./ServerData/'+portfolioCode+'/df_L1_r.parquet')
        self.df_L1_r.index = pd.to_datetime(self.df_L1_r.index, format='%Y-%m-%d')
        self.df_L1_contrib = pd.read_parquet('./ServerData/'+portfolioCode+'/df_L1_contrib.parquet')
        self.df_L1_contrib.index = pd.to_datetime(self.df_L1_contrib.index, format='%Y-%m-%d')
        self.df_L2_r = pd.read_parquet('./ServerData/'+portfolioCode+'/df_L2_r.parquet')
        self.df_L2_r.index = pd.to_datetime(self.df_L2_r.index, format= '%Y-%m-%d')
        self.df_L2_contrib = pd.read_parquet('./ServerData/'+portfolioCode+'/df_L2_contrib.parquet')
        self.df_L2_contrib.index = pd.to_datetime(self.df_L2_contrib.index, format='%Y-%m-%d')
        self.df_L3_r = pd.read_parquet('./ServerData/'+portfolioCode+'/df_L3_r.parquet')
        self.df_L3_r.index = pd.to_datetime(self.df_L3_r.index, format='%Y-%m-%d')
        self.df_L3_contrib = pd.read_parquet('./ServerData/'+portfolioCode+'/df_L3_contrib.parquet')
        self.df_L3_contrib.index = pd.to_datetime(self.df_L3_contrib.index, format='%Y-%m-%d')
        self.df_L2vsL1_relw = pd.read_parquet('./ServerData/'+portfolioCode+'/df_L2vsL1_relw.parquet')
        self.df_L2vsL1_relw.index = pd.to_datetime(self.df_L2vsL1_relw.index, format='%Y-%m-%d')
        self.df_L3vsL2_relw = pd.read_parquet('./ServerData/'+portfolioCode+'/df_L3vsL2_relw.parquet')
        self.df_L3vsL2_relw.index = pd.to_datetime(self.df_L3vsL2_relw.index, format='%Y-%m-%d')
        self.df_L3_2FAttrib = pd.read_parquet('./ServerData/'+portfolioCode+'/df_L3_2FAttrib.parquet')
        self.df_L3_2FAttrib.index = pd.to_datetime(self.df_L3_2FAttrib.index, format='%Y-%m-%d')
        self.df_L3_1FAttrib = pd.read_parquet('./ServerData/'+portfolioCode+'/df_L3_1FAttrib.parquet')
        self.df_L3_1FAttrib.index = pd.to_datetime(self.df_L3_1FAttrib.index, format='%Y-%m-%d')
        self.t_dates = pd.read_parquet('./ServerData/'+portfolioCode+'/t_dates.parquet')
        self.tME_dates = pd.read_parquet('./ServerData/'+portfolioCode+'/tME_dates.parquet')
        self.tQE_dates = pd.read_parquet('./ServerData/'+portfolioCode+'/tQE_dates.parquet')
        self.df_productList = pd.read_parquet('./ServerData/'+portfolioCode+'/df_productList.parquet')
        self.df_BM_G1 = pd.read_parquet('./ServerData/'+portfolioCode+'/df_BM_G1.parquet')
        self.summaryVariables = pd.read_parquet('./ServerData/'+portfolioCode+'/summaryVariables.parquet')
        # Recreate Category Group Labels for Charts
        self.portfolioName = self.summaryVariables['portfolioName'].iloc[0]
        self.t_StartDate = self.summaryVariables['t_StartDate'].iloc[0]
        self.t_EndDate = self.summaryVariables['t_EndDate'].iloc[0]
        self.groupName = self.df_BM_G1.columns[0]
        self.groupList = self.df_BM_G1[self.df_BM_G1.columns[0]].unique()


def f_get_subfolder_names(path):
    subfolder_names = []

    if os.path.exists(path) and os.path.isdir(path):
        for item in os.listdir(path):
            item_path = os.path.join(path, item)
            if os.path.isdir(item_path):
                subfolder_names.append(item)

    return subfolder_names

# IMPORT Datafiles stored on Kev's GitHUB Registry
# Must be linked to "./ServerData/"
availablePortfolios = f_get_subfolder_names('./ServerData/')

# Create Portfolio class objects (import all data)
All_Portfolios = []
for code in availablePortfolios:
    print(code)
    All_Portfolios.append(Portfolio(code))

# Initialise charts with 1st dataset

Selected_Portfolio = All_Portfolios[3]
Selected_Code = Selected_Portfolio.portfolioName

Alt1_Portfolio = All_Portfolios[1]
Alt1_Code = Alt1_Portfolio.portfolioName

Alt2_Portfolio = All_Portfolios[2]
Alt2_Code = Alt2_Portfolio.portfolioName

text_Start_Date = load_start_date
text_End_Date = load_end_date

Product_List = Selected_Portfolio.df_productList.index.tolist()

dt_start_date = pd.to_datetime(text_Start_Date)
dt_end_date = pd.to_datetime(text_End_Date)
groupName = Selected_Portfolio.groupName
groupList = Selected_Portfolio.groupList

# START APP %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP, dbc.themes.MATERIA, dbc.icons.FONT_AWESOME], suppress_callback_exceptions=True)
server = app.server
port_number = 8050

def get_local_ip(port_number):
    try:
        host_name = socket.gethostname()
        local_ip = socket.gethostbyname(host_name)
        return f'http://{local_ip}:{port_number}'
    except socket.error:
        return "Couldn't get local IP address"
dashLocation = get_local_ip(port_number)
print("**** Atchison Analytics Dash App Can Be Accessed Via Local Server Running On Kev's PC Here: ")
print(dashLocation)


# %%%%%%%%%%% CORE FUNCTIONS - Calculation Return and Volatility Results

# Calculation Performance Index
def f_CalcReturnValues(df_Input, startDate, endDate):
    # example use:  returnOutput = f_CalcReturnValues(df_L3_r, dates1.loc[1,'Date'], dates1.loc[0,'Date'])
    returnOutput = 0.0
    days = 0.0
    days = ((endDate - startDate).days)

    if days > 0:
        returnOutput = ((df_Input.loc[startDate + relativedelta(days=1):endDate] + 1).cumprod() - 1).iloc[-1]
    elif days == 0:
        returnOutput = df_Input.iloc[0]
    else:
        returnOutput = 0  # throw error here

    if days > 365: returnOutput = (((1 + returnOutput) ** (1 / (days / 365))) - 1)

    return returnOutput


def f_CalcReturnTable(df_Input, dateList):
    # example use:  f_CalcReturnTable(df_L3_r.loc[:,['IOZ','IVV']], tME_dates)
    df_Output = pd.DataFrame()

    for n in range(len(dateList)):
        if n > 0: df_Output[dateList.loc[n, 'Name']] = f_CalcReturnValues(df_Input, dateList.loc[n, 'Date'],
                                                                          dateList.loc[0, 'Date'])
    return df_Output


def f_CalcDrawdown(df_Input):
    # example use:  returnOutput = f_CalcReturnValues(df_L3_r.loc[:,['Data 1', 'Data 2']])
    # Calculate cumulative returns for each asset
    df_cumulative = (1 + df_Input).cumprod()
    # Calculate rolling maximum cumulative returns
    rolling_max = df_cumulative.expanding().max()
    # Calculate drawdowns as percentage decline from peaks
    drawdowns = (df_cumulative - rolling_max) / rolling_max * 100

    # Create the drawdown chart DataFrame
    drawdown_chart_data = pd.DataFrame()
    for col in df_Input.columns[:]:
        drawdown_chart_data[col + '_Drawdown'] = drawdowns[col]
    return drawdown_chart_data


def f_CalcRollingDailyVol(df_Input, window, trading_days_per_year):
    # Calculate percentage returns for each asset
    percentage_returns = df_Input.replace([np.inf, -np.inf], np.nan).dropna()
    # Calculate rolling volatility
    rolling_volatility = percentage_returns.rolling(window=window).std() * np.sqrt(trading_days_per_year)
    # Drop rows with NaN values (corresponding to the start of each series)
    rolling_volatility = rolling_volatility.dropna()
    return rolling_volatility

def f_CalcRollingMonthlyVol(df_Input, window, trading_months_per_year):
    # Calculate percentage returns for each asset
    percentage_returns = df_Input.replace([np.inf, -np.inf], np.nan).dropna()
    # Resample to monthly returns
    monthly_returns = (1 + percentage_returns).resample('M').prod() - 1
    # Calculate rolling volatility
    rolling_volatility = monthly_returns.rolling(window=window).std() * np.sqrt(trading_months_per_year)
    # Drop rows with NaN values (corresponding to the start of each series)
    rolling_volatility = rolling_volatility.dropna()
    return rolling_volatility

def f_CalcRollingMonthlySharpe(df_Input, window, trading_months_per_year, risk_free_rate):
    # Calculate percentage returns for each asset
    percentage_returns = df_Input.replace([np.inf, -np.inf], np.nan).dropna()
    # Resample to monthly returns
    monthly_returns = (1 + percentage_returns).resample('M').prod() - 1
    # Calculate rolling volatility
    rolling_volatility = monthly_returns.rolling(window=window).std() * np.sqrt(trading_months_per_year)
    #rolling_volatility = rolling_volatility.iloc[-1]
    days = window*365/12

    if days > 0: returnOutput = (monthly_returns.rolling(window=window).apply(lambda x: (x + 1).prod() - 1, raw=True))

    if days > 365: returnOutput = (((1 + returnOutput) ** (1 / (days / 365))) - 1)

    rolling_mean_excess_returns = returnOutput - risk_free_rate/12

    rolling_sharpe_ratio = rolling_mean_excess_returns / rolling_volatility
    # Drop rows with NaN values (corresponding to the start of each series)
    rolling_sharpe_ratio = rolling_sharpe_ratio.loc[dt_start_date:dt_end_date]
    #rolling_sharpe_ratio = rolling_sharpe_ratio.dropna()
    return rolling_sharpe_ratio

def count_positive_values(x):
    return np.sum(x > 0)

def f_CalcRollingMonthlyBattingAverage(df_Input, window):
    # Calculate percentage returns for each asset
    percentage_returns = df_Input.replace([np.inf, -np.inf], np.nan).dropna()
    # Resample to monthly returns
    monthly_returns = (1 + percentage_returns).resample('M').prod() - 1
    monthly_returns.replace(0.0000, np.nan, inplace=True)

    monthly_returns['Alpha to Benchmark'] = monthly_returns['P_TOTAL'] - monthly_returns['BM_G1_TOTAL']
    monthly_returns['Alpha to Peers'] = monthly_returns['P_TOTAL'] - monthly_returns['Peer_TOTAL']

    print(monthly_returns)

    monthly_returns = monthly_returns.dropna()

    valid_window = min(window, monthly_returns.shape[0])

    rolling_batting_average = monthly_returns[['Alpha to Benchmark', 'Alpha to Peers']].rolling(window=window).apply(count_positive_values) / valid_window
    rolling_batting_average = rolling_batting_average.loc[dt_start_date:dt_end_date]

    return rolling_batting_average


def f_AssetClassContrib(df_Input, Input_G1_Name):
    columns_to_include = df_Input.columns[(df_Input != 0).any()].tolist()
    indices_with_G1 = Selected_Portfolio.df_productList[Selected_Portfolio.df_productList['G1'] == Input_G1_Name].index

    set1 = set(columns_to_include)
    set2 = set(indices_with_G1)
    common_elements = set1.intersection(set2)
    common_elements_list = list(common_elements)

    # Ensure that indices_with_G1 are valid indices in df_Input
    if len(common_elements_list) == 0:
        print("No valid indices found.")
        return None

    return common_elements_list


# Create Sidebar %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

sidebar = html.Div(
    [
        html.Div(
            [
                html.H2("Atchison Analytics", style={"color": "#1DC8F2"}),
            ],
            className="sidebar-header",
        ),
        dcc.Store(id='stored-portfolio-code', data={'key': Selected_Code}),
        html.Div(id='display-portfolio-code', style={"color": "#1DC8F2", "margin-left": "5rem"}, className="sidebar-subheader"),
        html.Hr(),
        html.Hr(style={'border-color': "#1DC8F2", 'width': '80%', 'margin': '0 auto'}),
        dbc.Nav(
            [
                dbc.NavLink(
                    [
                        html.I(className="fa-solid fa-gear me-2"),
                        html.Span("Portfolio Settings")],
                    href="/",
                    active="exact",
                ),
                html.Hr(),
                html.Hr(style={'border-color': "#1DC8F2", 'width': '80%', 'margin': '0 auto'}),
                dbc.NavLink(
                    [
                        html.I(className="fas fa-home me-2"),
                        html.Span("Summary Dashboard"),
                    ],
                    href="/0-Summary",
                    active="exact",
                ),
                dbc.NavLink(
                    [
                        html.I(className="fa-solid fa-arrow-trend-up me-2"),
                        html.Span("Performance"),
                    ],
                    href="/1-Performance",
                    active="exact",
                ),
                dbc.NavLink(
                    [
                        html.I(className="fa-solid fa-face-surprise me-2"),
                        html.Span("Risk Analysis"),
                    ],
                    href="/2-Risk",
                    active="exact",
                ),
                dbc.NavLink(
                    [
                        html.I(className="fa-solid fa-chart-pie me-2"),
                        html.Span("Allocation / Exposure"),
                    ],
                    href="/3-Allocation",
                    active="exact",
                ),
                html.Hr(),
                html.Hr(style={'border-color': "#1DC8F2", 'width': '80%', 'margin': '0 auto'}),
                dbc.NavLink(
                    [
                        html.I(className="fa-solid fa-trophy me-2"),
                        html.Span("Brinson-Fachler Attribution"),
                    ],
                    href="/4-Attribution",
                    active="exact",
                ),
                dbc.NavLink(
                    [
                        html.I(className="fa-solid fa-scale-unbalanced me-2"),
                        html.Span("Contribution Analysis"),
                    ],
                    href="/5-Contribution",
                    active="exact",
                ),
                dbc.NavLink(
                    [
                        html.I(className="fa-solid fa-shapes me-2"),
                        html.Span("Portfolio Components"),
                    ],
                    href="/6-Component",
                    active="exact",
                ),
                html.Hr(),
                html.Hr(style={'border-color': "#1DC8F2", 'width': '80%', 'margin': '0 auto'}),
                dbc.NavLink(
                    [
                        html.I(className="fa-solid fa-tree me-2"),
                        html.Span("ESG / Controversy"),
                    ],
                    href="/10-ESG",
                    active="exact",
                ),
                dbc.NavLink(
                    [
                        html.I(className="fa-solid fa-sack-dollar me-2"),
                        html.Span("Fee Analysis"),
                    ],
                    href="/11-Fees",
                    active="exact",
                ),
                html.Hr(),
                html.Hr(style={'border-color': "#1DC8F2", 'width': '80%', 'margin': '0 auto'}),
                dbc.NavLink(
                    [
                        html.I(className="fa-solid fa-landmark me-2"),
                        html.Span("Market Valuation Analysis"),
                    ],
                    href="/20-Markets",
                    active="exact",
                ),
                dbc.NavLink(
                    [
                        html.I(className="fa-solid fa-file-lines me-2"),
                        html.Span("Report Generator"),
                    ],
                    href="/21-Reports",
                    active="exact",
                ),
                html.Hr(),
                html.Hr(style={'border-color': "#1DC8F2", 'width': '80%', 'margin': '0 auto'}),
                dbc.NavLink(
                    [
                        html.I(className="fa-solid fa-circle-info me-2"),
                        html.Span("Need Help?"),
                    ],
                    href="/30-Help",
                    active="exact",
                ),

            ],
            vertical=True,
            pills=True,
        ),
    ],
    className="sidebar",
)


content = html.Div(id="page-content", children=[])

## MAIN LAYOUT --------

app.layout = html.Div([
    dcc.Location(id="url"),
    sidebar,
    content
])

@app.callback(
    Output("page-content", "children"),
    [Input("url", "pathname")]
)
def render_page_content(pathname):
    if pathname == "/":
        return [
            html.Div(style={'height': '2rem'}),
            html.H2('Select Portfolio & Analysis Settings',
                    style={'textAlign':'center', 'color': "#3D555E"}),
            html.Hr(),
            html.Hr(style={'border-color': "#3D555E", 'width': '70%', 'margin': 'auto auto'}),
            html.Hr(),
            dbc.Row([
                dbc.Col(dbc.Card([dbc.CardHeader("Select Portfolio:", className="card-header-bold"),
                                  dbc.CardBody([

                                      html.H6('Primary Portfolio:'),
                                      dcc.Dropdown(id='portfolio-dropdown',
                                                   options=[{'label': portfolio, 'value': portfolio} for portfolio in
                                                            availablePortfolios],
                                                   value=Selected_Code),
                                      html.Hr(),
                                      html.H6('Alternative 1:'),
                                      dcc.Dropdown(id='portfolio-dropdown-alt1',
                                                   options=[{'label': portfolio, 'value': portfolio} for portfolio in
                                                            availablePortfolios],
                                                   value=Alt1_Code),
                                      html.Hr(),
                                      html.H6('Alternative 2:'),
                                      dcc.Dropdown(id='portfolio-dropdown-alt2',
                                                   options=[{'label': portfolio, 'value': portfolio} for portfolio in
                                                            availablePortfolios],
                                                   value=Alt2_Code)
                                  ]
                                  )], color="primary", outline=True, style={"height": "100%"}), width=4, align="stretch", className="mb-3"),
                dbc.Col(dbc.Card([dbc.CardHeader("Select Attribution Grouping:", className="card-header-bold"),
                                  dbc.CardBody([
                                      dbc.Row([
                                          dbc.Col(
                                              dcc.RadioItems(
                                                  options=[
                                                      {'label': ' G1 - Atchison Sleeve Categories', 'value': 'G1'},
                                                      {'label': ' G2 - CFS Edge Policy', 'value': 'G2'},
                                                      {'label': ' G3 - HUB24 Policy', 'value': 'G3'},
                                                      {'label': ' G4 - Sleeve Sub-Categories', 'value': 'G4'},
                                                      {'label': ' G5 - Geography', 'value': 'G5'},
                                                  ],
                                                  id="radio-001",
                                                  value='G1',
                                              ), align="start"),
                                      ], justify="evenly", align="start", className="mb-2"),
                                  ])], color="primary", outline=True, style={"height": "100%"}), width=2,
                        align="stretch", className="mb-3"),
                dbc.Col(dbc.Card(
                    [dbc.CardHeader("Select Analysis Timeframe:", className="card-header-bold"), dbc.CardBody([
                        dcc.DatePickerRange(display_format='DD-MMM-YYYY', start_date=load_start_date, day_size=35,
                                            end_date=load_end_date, id='date-picker', style={"font-size": "11px"})
                    ])], color="primary", outline=True, style={"height": "100%"}), width=2, align="start", className="mb-2"),

                ], justify="center", style={"display": "flex", "flex-wrap": "wrap"}, className="mb-3"),

            html.Hr(),
            dbc.Row([dbc.Col(
                dbc.Card([dbc.CardHeader("Some Other Stuff To Be Added....:", className="card-header-bold"),
                          dbc.CardBody([
                              dbc.Row([
                                  dbc.Col(daq.BooleanSwitch(id='switch-003', on=True, color="#93F205",
                                                            label="More Settings #3 tbc",
                                                            labelPosition="bottom",
                                                            style={"text-align": "center"}), align="start"),
                                  dbc.Col(daq.BooleanSwitch(id='switch-004', on=False, color="#93F205",
                                                            label="More Settings #4 tbc",
                                                            labelPosition="bottom"),
                                          style={"text-align": "center"}, align="start"),
                              ], justify="evenly", align="start", className="mb-2"),
                          ])], color="primary", outline=True, style={"height": "100%"}),
                width=8, align = "stretch", className = "mb-3"),
            ], justify="center", style={"display": "flex", "flex-wrap": "wrap"}, className="mb-3"),


        ]
    elif pathname == "/0-Summary":
        return [
            html.Div(style={'height': '2rem'}),
            html.H2('Summary Dashboard',
                    style={'textAlign': 'center', 'color': "#3D555E"}),
            html.Hr(),
            html.Hr(style={'border-color': "#3D555E", 'width': '70%', 'margin': 'auto auto'}),
            html.Hr(),

            dbc.Row([
                # Left Gutter
                dbc.Col(width=2, align="center", className="mb-3"),
                # Centre Work Area
                dbc.Col([

                    # End of Centre Work Area
                ], width=8, align="center", className="mb-3"),

                # Right Gutter
                dbc.Col("", width=2, align="center", className="mb-3"),

            ], align="center", className="mb-3")
        ]
    elif pathname == "/1-Performance":

        filtered_df_1_1 = pd.concat([Selected_Portfolio.df_L3_r.loc[dt_start_date:dt_end_date, ['P_' + groupName + '_' + n]] * 100 for n in groupList], axis=1)
        filtered_df_1_1.columns = groupList

        # Create figures for each output
        figure_1_1 = px.bar(
            filtered_df_1_1,
            x=filtered_df_1_1.index,
            y=[c for c in filtered_df_1_1.columns],
            labels={"x": "Date", "y": "Values"},
            template="plotly_white",
            barmode='relative',
        )
        figure_1_1.update_layout(
            yaxis_title="Return (%)",
            xaxis_title="",
            legend=dict(
                orientation="h",
                yanchor="top",
                y=-0.3,
                xanchor="center",
                x=0.5,
                title=None,
                font=dict(size=11)
            ),
            margin=dict(r=0),
        )

        filtered_df_1_2 = (((Selected_Portfolio.df_L3_r.loc[dt_start_date:dt_end_date,
                           ['P_TOTAL', 'BM_G1_TOTAL', 'Peer_TOTAL', 'Obj_TOTAL']] + 1).cumprod() - 1) * 100)
        filtered_df_1_2.columns = [Selected_Code, 'SAA Benchmark', 'Peer Manager', 'Objective']

        if Alt1_Code != 'Off':
            a1 = (((Alt1_Portfolio.df_L3_r.loc[dt_start_date:dt_end_date, ['P_TOTAL']] + 1).cumprod() - 1) * 100)
            a1.columns = ['Alt 1 ('+Alt1_Code+')']
            filtered_df_1_2 = pd.concat([filtered_df_1_2, a1], axis=1)

        if Alt2_Code != 'Off':
            a2 = (((Alt2_Portfolio.df_L3_r.loc[dt_start_date:dt_end_date, ['P_TOTAL']] + 1).cumprod() - 1) * 100)
            a2.columns = ['Alt 2 ('+Alt2_Code+')']
            filtered_df_1_2 = pd.concat([filtered_df_1_2, a2], axis=1)

        figure_1_2 = px.line(
            filtered_df_1_2,
            x=filtered_df_1_2.index,
            y=[c for c in filtered_df_1_2.columns],
            labels={"x": "Date", "y": "Values"},
            template="plotly_white",
        )
        figure_1_2.update_layout(
            yaxis_title="Cumulative Return (%)",
            xaxis_title="",
            legend=dict(
                orientation="h",
                yanchor="top",
                y=-0.3,
                xanchor="center",
                x=0.5,
                title=None,
                font=dict(size=11)
            ),
            margin=dict(r=0),
        )

        filtered_df_1_3 = (f_CalcReturnTable(
            Selected_Portfolio.df_L3_r.loc[:, ['P_TOTAL', 'BM_G1_TOTAL', 'Peer_TOTAL', 'Obj_TOTAL']],
            Selected_Portfolio.t_dates) * 100).T

        filtered_df_1_3.columns = [Selected_Code, 'SAA Benchmark', 'Peer Manager', 'Objective']

        if Alt1_Code != 'Off':
            a1 = (f_CalcReturnTable(Alt1_Portfolio.df_L3_r.loc[:, ['P_TOTAL']], Selected_Portfolio.t_dates) * 100).T
            a1.columns = ['Alt 1 ('+Alt1_Code+')']
            filtered_df_1_3 = pd.concat([filtered_df_1_3, a1], axis=1)

        if Alt2_Code != 'Off':
            a2 = (f_CalcReturnTable(Alt2_Portfolio.df_L3_r.loc[:, ['P_TOTAL']], Selected_Portfolio.t_dates) * 100).T
            a2.columns = ['Alt 2 ('+Alt2_Code+')']
            filtered_df_1_3 = pd.concat([filtered_df_1_3, a2], axis=1)

        figure_1_3 = px.bar(
            filtered_df_1_3,
            x=filtered_df_1_3.index,
            y=[c for c in filtered_df_1_3.columns],
            labels={"x": "Date", "y": "Values"},
            template="plotly_white",
            barmode='group'
        )
        figure_1_3.update_layout(
            yaxis_title="Return (%, %p.a.)",
            legend=dict(
                orientation="h",
                yanchor="top",
                y=-0.3,
                xanchor="center",
                x=0.5,
                title=None,
                font=dict(size=11)
            ),
            margin=dict(r=0),
        )

        filtered_df_1_4 = (f_CalcReturnTable(
            Selected_Portfolio.df_L3_r.loc[:, ['P_TOTAL', 'BM_G1_TOTAL', 'Peer_TOTAL', 'Obj_TOTAL']],
            Selected_Portfolio.tME_dates) * 100).T
        filtered_df_1_4.columns = [Selected_Code, 'SAA Benchmark', 'Peer Manager', 'Objective']

        if Alt1_Code != 'Off':
            a1 = (f_CalcReturnTable(Alt1_Portfolio.df_L3_r.loc[:, ['P_TOTAL']], Selected_Portfolio.tME_dates) * 100).T
            a1.columns = ['Alt 1 ('+Alt1_Code+')']
            filtered_df_1_4 = pd.concat([filtered_df_1_4, a1], axis=1)

        if Alt2_Code != 'Off':
            a2 = (f_CalcReturnTable(Alt2_Portfolio.df_L3_r.loc[:, ['P_TOTAL']], Selected_Portfolio.tME_dates) * 100).T
            a2.columns = ['Alt 2 ('+Alt2_Code+')']
            filtered_df_1_4 = pd.concat([filtered_df_1_4, a2], axis=1)

        figure_1_4 = px.bar(
            filtered_df_1_4,
            x=filtered_df_1_4.index,
            y=[c for c in filtered_df_1_4.columns],
            labels={"x": "Date", "y": "Values"},
            template="plotly_white",
            barmode='group'
        )
        figure_1_4.update_layout(
            yaxis_title="Return (%, %p.a.)",
            legend=dict(
                orientation="h",
                yanchor="top",
                y=-0.3,
                xanchor="center",
                x=0.5,
                title=None,
                font=dict(size=11)
            ),
            margin=dict(r=0),
        )

        filtered_df_1_5 = (f_CalcReturnTable(
            Selected_Portfolio.df_L3_r.loc[:, ['P_TOTAL', 'BM_G1_TOTAL', 'Peer_TOTAL', 'Obj_TOTAL']],
            Selected_Portfolio.tQE_dates) * 100).T

        filtered_df_1_5.columns = [Selected_Code, 'SAA Benchmark', 'Peer Manager', 'Objective']

        if Alt1_Code != 'Off':
            a1 = (f_CalcReturnTable(Alt1_Portfolio.df_L3_r.loc[:, ['P_TOTAL']], Selected_Portfolio.tQE_dates) * 100).T
            a1.columns = ['Alt 1 ('+Alt1_Code+')']
            filtered_df_1_5 = pd.concat([filtered_df_1_5, a1], axis=1)

        if Alt2_Code != 'Off':
            a2 = (f_CalcReturnTable(Alt2_Portfolio.df_L3_r.loc[:, ['P_TOTAL']], Selected_Portfolio.tQE_dates) * 100).T
            a2.columns = ['Alt 2 ('+Alt2_Code+')']
            filtered_df_1_5 = pd.concat([filtered_df_1_5, a2], axis=1)

        figure_1_5 = px.bar(
            filtered_df_1_5,
            x=filtered_df_1_5.index,
            y=[c for c in filtered_df_1_5.columns],
            labels={"x": "Date", "y": "Values"},
            template="plotly_white",
            barmode='group'
        )
        figure_1_5.update_layout(
            yaxis_title="Return (%, %p.a.)",
            legend=dict(
                orientation="h",
                yanchor="top",
                y=-0.3,
                xanchor="center",
                x=0.5,
                title=None,
                font=dict(size=11)
            ),
            margin=dict(r=0),
        )

        ## Populate Charts for Page 1-Performance
        return [
            html.Div(style={'height': '2rem'}),
            html.H2('Performance Benchmarking',
                    style={'textAlign': 'center', 'color': "#3D555E"}),
            html.Hr(),
            html.Hr(style={'border-color': "#3D555E", 'width': '70%', 'margin': 'auto auto'}),
            html.Hr(),

            dbc.Row([
                # Left Gutter
                dbc.Col("", width=2, align="center", className="mb-3"),
                # Centre Work Area
                dbc.Col([
                    # Tab 1 - Performance
                    dbc.Row([
                        dbc.Tabs([
                            dbc.Tab([
                                dbc.Card([
                                    dbc.CardHeader(
                                        "Chart 2: Total Portfolio Performance - as at Last Price " +
                                        Selected_Portfolio.tME_dates.loc[0, 'Date'].strftime("(%d %b %Y)")),
                                    dbc.CardBody([dcc.Graph(figure=figure_1_4),
                                                  html.Hr(),
                                                  dbc.Table.from_dataframe(filtered_df_1_4.T.round(2), index=True,
                                                                           striped=True, bordered=True, hover=True)
                                                  ]),
                                    dbc.CardFooter("Enter some dot point automated analysis here....")
                                ], color="primary", outline=True)], label="Month End Date",
                                active_label_style={"background-color": "#1DC8F2"},
                                label_style={"background-color": "#E7EAEB", "color": "#3D555E"}),
                            dbc.Tab([
                                dbc.Card([
                                    dbc.CardHeader(
                                        "Chart 3: Total Portfolio Performance - as at Last Price " +
                                        Selected_Portfolio.tQE_dates.loc[0, 'Date'].strftime("(%d %b %Y)")),
                                    dbc.CardBody([dcc.Graph(figure=figure_1_5),
                                                  html.Hr(),
                                                  dbc.Table.from_dataframe(filtered_df_1_5.T.round(2), index=True,
                                                                           striped=True, bordered=True, hover=True)
                                                  ]),
                                    dbc.CardFooter("Enter some dot point automated analysis here....")
                                ], color="primary", outline=True)], label="Quarter End Date",
                                active_label_style={"background-color": "#1DC8F2"},
                                label_style={"background-color": "#E7EAEB", "color": "#3D555E"}),
                            dbc.Tab([
                                dbc.Card([
                                    dbc.CardHeader(
                                        "Chart 1: Total Portfolio Performance - as at Last Price " +
                                        Selected_Portfolio.t_dates.loc[0, 'Date'].strftime("(%d %b %Y)")),
                                    dbc.CardBody([dcc.Graph(figure=figure_1_3),
                                                  html.Hr(),
                                                  dbc.Table.from_dataframe(filtered_df_1_3.T.round(2), index=True,
                                                                           striped=True, bordered=True, hover=True)
                                                  ]),
                                    dbc.CardFooter("Enter some dot point automated analysis here....")
                                ], color="primary", outline=True)], label="To Latest Daily",
                                active_label_style={"background-color": "#1DC8F2"},
                                label_style={"background-color": "#E7EAEB", "color": "#3D555E"}),

                        ], className="mb-3")
                    ], align="center", className="mb-3"),

                    dbc.Row([
                        dbc.Col(dbc.Card([
                            dbc.CardHeader(
                                "Chart 4: Example Portfolio Return Chart - Daily Asset Sleeve Returns"),
                            dbc.CardBody(dcc.Graph(figure=figure_1_1)),
                            dbc.CardFooter("Enter some dot point automated analysis here....")
                        ], color="primary", outline=True), align="center", className="mb-3"),
                    ], align="center", className="mb-3"),

                    dbc.Row([
                        dbc.Col(dbc.Card([
                            dbc.CardHeader("Chart 5: Portfolio Total Returns (L3)"),
                            dbc.CardBody(dcc.Graph(figure=figure_1_2)),
                            dbc.CardFooter("Enter some dot point automated analysis here....")
                        ], color="primary", outline=True), align="center", className="mb-3"),
                    ], align="center", className="mb-3"),

                    # End of Centre Work Area
                ], width=8, align="center", className="mb-3"),

                # Right Gutter
                dbc.Col("", width=2, align="center", className="mb-3"),

            ], align="center", className="mb-3")

        ]


    elif pathname == "/2-Risk":
        filtered_df_2_1 = f_CalcDrawdown(
            Selected_Portfolio.df_L3_r.loc[dt_start_date:dt_end_date, ['P_TOTAL', 'BM_G1_TOTAL', 'Peer_TOTAL']])

        filtered_df_2_1.columns = [Selected_Code, 'SAA Benchmark', 'Peer Manager']

        figure_2_1 = px.line(
            filtered_df_2_1,
            x=filtered_df_2_1.index,
            y=[c for c in filtered_df_2_1.columns],
            labels={"x": "Date", "y": "Values"},
            template="plotly_white",
        )
        figure_2_1.update_layout(
            yaxis_title="Drawdown Return (%)",
            xaxis_title="",
            legend=dict(
                orientation="h",
                yanchor="top",  # Change this to "top" to move the legend below the chart
                y=-0.3,  # Adjust the y value to position the legend below the chart
                xanchor="center",  # Center the legend horizontally
                x=0.5,  # Center the legend horizontally
                title=None,
                font=dict(size=11)
            ),
            margin=dict(r=0),  # Reduce right margin to maximize visible area
        )

        # Based on 30 day Window - Daily Data annualised (252 trading days)
        filtered_df_2_2 = f_CalcRollingDailyVol(
            Selected_Portfolio.df_L3_r.loc[(dt_start_date-timedelta(days=30)):dt_end_date,
            ['P_TOTAL', 'BM_G1_TOTAL', 'Peer_TOTAL']], 30, 252) *100

        filtered_df_2_2.columns = [Selected_Code, 'SAA Benchmark', 'Peer Manager']

        figure_2_2 = px.line(
            filtered_df_2_2,
            x=filtered_df_2_2.index,
            y=[c for c in filtered_df_2_2.columns],
            labels={"x": "Date", "y": "Values"},
            template="plotly_white",
        )
        figure_2_2.update_layout(
            yaxis_title="30 Day Rolling Volatility (% p.a.)",
            xaxis_title="",
            legend=dict(
                orientation="h",
                yanchor="top",  # Change this to "top" to move the legend below the chart
                y=-0.3,  # Adjust the y value to position the legend below the chart
                xanchor="center",  # Center the legend horizontally
                x=0.5,  # Center the legend horizontally
                title=None,
                font=dict(size=11)
            ),
            margin=dict(r=0),  # Reduce right margin to maximize visible area
        )

        # Based on 90 day Window - Daily Data annualised (252 trading days)
        filtered_df_2_3 = f_CalcRollingDailyVol(
            Selected_Portfolio.df_L3_r.loc[(dt_start_date-timedelta(days=90)):dt_end_date,
            ['P_TOTAL', 'BM_G1_TOTAL', 'Peer_TOTAL']], 90, 252) * 100

        filtered_df_2_3.columns = [Selected_Code, 'SAA Benchmark', 'Peer Manager']

        figure_2_3 = px.line(
            filtered_df_2_3,
            x=filtered_df_2_3.index,
            y=[c for c in filtered_df_2_3.columns],
            labels={"x": "Date", "y": "Values"},
            template="plotly_white",
        )
        figure_2_3.update_layout(
            yaxis_title="90 Day Rolling Volatility (% p.a.)",
            xaxis_title="",
            legend=dict(
                orientation="h",
                yanchor="top",  # Change this to "top" to move the legend below the chart
                y=-0.3,  # Adjust the y value to position the legend below the chart
                xanchor="center",  # Center the legend horizontally
                x=0.5,  # Center the legend horizontally
                title=None,
                font=dict(size=11)
            ),
            margin=dict(r=0),  # Reduce right margin to maximize visible area
        )

        # Based on 1 Year Monthly data Windows - Monthly Data annualised (12 months)
        filtered_df_2_4 = f_CalcRollingMonthlyVol(
            Selected_Portfolio.df_L3_r.loc[(dt_start_date - timedelta(days=364)):dt_end_date,
            ['P_TOTAL', 'BM_G1_TOTAL', 'Peer_TOTAL']], 12, 12) * 100

        filtered_df_2_4.columns = [Selected_Code, 'SAA Benchmark', 'Peer Manager']

        figure_2_4 = px.line(
            filtered_df_2_4,
            x=filtered_df_2_4.index,
            y=[c for c in filtered_df_2_4.columns],
            labels={"x": "Date", "y": "Values"},
            template="plotly_white",
        )
        figure_2_4.update_layout(
            yaxis_title="12 Month Rolling Volatility (% p.a.)",
            xaxis_title="",
            legend=dict(
                orientation="h",
                yanchor="top",  # Change this to "top" to move the legend below the chart
                y=-0.3,  # Adjust the y value to position the legend below the chart
                xanchor="center",  # Center the legend horizontally
                x=0.5,  # Center the legend horizontally
                title=None,
                font=dict(size=11)
            ),
            margin=dict(r=0),  # Reduce right margin to maximize visible area
        )

        filtered_df_2_5 = f_CalcRollingMonthlyVol(
            Selected_Portfolio.df_L3_r.loc[(dt_start_date - timedelta(days=(3*365-1))):dt_end_date,
            ['P_TOTAL', 'BM_G1_TOTAL', 'Peer_TOTAL']], 36, 12) * 100

        filtered_df_2_5.columns = [Selected_Code, 'SAA Benchmark', 'Peer Manager']

        figure_2_5 = px.line(
            filtered_df_2_5,
            x=filtered_df_2_5.index,
            y=[c for c in filtered_df_2_5.columns],
            labels={"x": "Date", "y": "Values"},
            template="plotly_white",
        )
        figure_2_5.update_layout(
            yaxis_title="36 Month Rolling Volatility (% p.a.)",
            xaxis_title="",
            legend=dict(
                orientation="h",
                yanchor="top",  # Change this to "top" to move the legend below the chart
                y=-0.3,  # Adjust the y value to position the legend below the chart
                xanchor="center",  # Center the legend horizontally
                x=0.5,  # Center the legend horizontally
                title=None,
                font=dict(size=11)
            ),
            margin=dict(r=0),  # Reduce right margin to maximize visible area
        )

        filtered_df_2_6 = f_CalcRollingMonthlySharpe(
            Selected_Portfolio.df_L3_r.loc[(dt_start_date - timedelta(days=(3*365-1))):dt_end_date,
            ['P_TOTAL', 'BM_G1_TOTAL', 'Peer_TOTAL']], 36, 12, 0)

        filtered_df_2_6.columns = [Selected_Code, 'SAA Benchmark', 'Peer Manager']

        figure_2_6 = px.line(
            filtered_df_2_6,
            x=filtered_df_2_6.index,
            y=[c for c in filtered_df_2_6.columns],
            labels={"x": "Date", "y": "Values"},
            template="plotly_white",
        )
        figure_2_6.update_layout(
            yaxis_title="Rolling 3 Year Sharpe Ratio",
            xaxis_title="",
            legend=dict(
                orientation="h",
                yanchor="top",  # Change this to "top" to move the legend below the chart
                y=-0.3,  # Adjust the y value to position the legend below the chart
                xanchor="center",  # Center the legend horizontally
                x=0.5,  # Center the legend horizontally
                title=None,
                font=dict(size=11)
            ),
            margin=dict(r=0),  # Reduce right margin to maximize visible area
        )

        filtered_df_2_7 = f_CalcRollingMonthlyBattingAverage(
            Selected_Portfolio.df_L3_r.loc[(dt_start_date - timedelta(days=(3 * 365 - 1))):dt_end_date,
            ['P_TOTAL', 'BM_G1_TOTAL', 'Peer_TOTAL']], 36) * 100

        filtered_df_2_7.columns = [Selected_Code+'vs SAA Benchmark', Selected_Code+'vs Peer Manager']

        figure_2_7 = px.line(
            filtered_df_2_7,
            x=filtered_df_2_7.index,
            y=[c for c in filtered_df_2_7.columns],
            labels={"x": "Date", "y": "Values"},
            template="plotly_white",
        )
        figure_2_7.update_layout(
            yaxis_title="Rolling 3 Year Batting Average (%)",
            xaxis_title="",
            legend=dict(
                orientation="h",
                yanchor="top",  # Change this to "top" to move the legend below the chart
                y=-0.3,  # Adjust the y value to position the legend below the chart
                xanchor="center",  # Center the legend horizontally
                x=0.5,  # Center the legend horizontally
                title=None,
                font=dict(size=11)
            ),
            margin=dict(r=0),  # Reduce right margin to maximize visible area
        )


        filtered_df_2_9 = (f_CalcReturnTable(
            Selected_Portfolio.df_L3_r.loc[:, ['P_TOTAL', 'BM_G1_TOTAL', 'Peer_TOTAL', 'Obj_TOTAL']],
            Selected_Portfolio.tME_dates) * 100).T

        filtered_df_2_9.columns = [Selected_Code, 'SAA Benchmark', 'Peer Manager', 'Objective']

        if Alt1_Code != 'Off':
            a1 = (f_CalcReturnTable(Alt1_Portfolio.df_L3_r.loc[:, ['P_TOTAL']], Selected_Portfolio.tME_dates) * 100).T
            a1.columns = ['Alt 1 (' + Alt1_Code + ')']
            filtered_df_2_9 = pd.concat([filtered_df_2_9, a1], axis=1)

        if Alt2_Code != 'Off':
            a2 = (f_CalcReturnTable(Alt2_Portfolio.df_L3_r.loc[:, ['P_TOTAL']], Selected_Portfolio.tME_dates) * 100).T
            a2.columns = ['Alt 2 (' + Alt2_Code + ')']
            filtered_df_2_9 = pd.concat([filtered_df_2_9, a2], axis=1)

        figure_2_9 = px.bar(
            filtered_df_2_9,
            x=filtered_df_2_9.index,
            y=[c for c in filtered_df_2_9.columns],
            labels={"x": "Date", "y": "Values"},
            template="plotly_white",
            barmode='group'
        )
        figure_2_9.update_layout(
            yaxis_title="Return (%, %p.a.)",
            legend=dict(
                orientation="h",
                yanchor="top",
                y=-0.3,
                xanchor="center",
                x=0.5,
                title=None,
                font=dict(size=11)
            ),
            margin=dict(r=0),
        )


        ## Populate Charts for Page 2-Risk
        return [
            html.Div(style={'height': '2rem'}),
            html.H2('Risk Analysis',
                    style={'textAlign': 'center', 'color': "#3D555E"}),
            html.Hr(),
            html.Hr(style={'border-color': "#3D555E", 'width': '70%', 'margin': 'auto auto'}),
            html.Hr(),

            dbc.Row([
                # Left Gutter
                dbc.Col("", width=2, align="center", className="mb-3"),
                # Centre Work Area
                dbc.Col([

                    # Tab 2 - Risk
                    dbc.Row([
                        dbc.Col(dbc.Card([
                            dbc.CardHeader("Chart 1: Portfolio 30 Day Rolling Volatility (%p.a.)"),
                            dbc.CardBody(dcc.Graph(figure=figure_2_2)),
                            dbc.CardFooter("Enter some dot point automated analysis here....")
                        ], color="primary", outline=True), align="center", className="mb-3"),
                        dbc.Col(dbc.Card([
                            dbc.CardHeader("Chart 2: Portfolio 90 Day Rolling Volatility (%p.a.)"),
                            dbc.CardBody(dcc.Graph(figure=figure_2_3)),
                            dbc.CardFooter("Enter some dot point automated analysis here....")
                        ], color="primary", outline=True), align="center", className="mb-3"),
                    ], align="center", className="mb-3"),
                    dbc.Row([
                        dbc.Col(dbc.Card([
                            dbc.CardHeader("Chart 3: Portfolio 12 Month Rolling Volatility (%p.a.)"),
                            dbc.CardBody(dcc.Graph(figure=figure_2_4)),
                            dbc.CardFooter("Enter some dot point automated analysis here....")
                        ], color="primary", outline=True), align="center", className="mb-3"),
                        dbc.Col(dbc.Card([
                            dbc.CardHeader("Chart 4: Portfolio 36 Month Rolling Volatility (%p.a.)"),
                            dbc.CardBody(dcc.Graph(figure=figure_2_5)),
                            dbc.CardFooter("Enter some dot point automated analysis here....")
                        ], color="primary", outline=True), align="center", className="mb-3"),
                    ], align="center", className="mb-3"),
                    dbc.Row([
                        dbc.Col(dbc.Card([
                            dbc.CardHeader("Chart 5: Portfolio Drawdown Analysis"),
                            dbc.CardBody(dcc.Graph(figure=figure_2_1)),
                            dbc.CardFooter("Enter some dot point automated analysis here....")
                        ], color="primary", outline=True), align="center", className="mb-3"),
                        dbc.Col(dbc.Card([
                            dbc.CardHeader("Chart 6: Portfolio 3 Year Rolling Sharpe Ratio"),
                            dbc.CardBody(dcc.Graph(figure=figure_2_6)),
                            dbc.CardFooter("Enter some dot point automated analysis here....")
                        ], color="primary", outline=True), align="center", className="mb-3"),
                    ], align="center", className="mb-3"),
                    dbc.Row([
                        dbc.Col(dbc.Card([
                            dbc.CardHeader("Chart 7: Portfolio 3 Year Rolling Batting Average"),
                            dbc.CardBody(dcc.Graph(figure=figure_2_7)),
                            dbc.CardFooter("Enter some dot point automated analysis here....")
                        ], color="primary", outline=True), align="center", className="mb-3"),
                        dbc.Col(dbc.Card([
                            dbc.CardHeader("Chart 8: Portfolio 3 Year Rolling Sharpe Ratio"),
                            dbc.CardBody(dcc.Graph(figure=figure_2_6)),
                            dbc.CardFooter("Enter some dot point automated analysis here....")
                        ], color="primary", outline=True), align="center", className="mb-3"),
                    ], align="center", className="mb-3"),
                    dbc.Row([
                        dbc.Col(dbc.Card([
                            dbc.CardHeader(
                                "Chart 3: Portfolio Risk Metrics Chart - Daily Asset Sleeve Returns"),
                            dbc.CardBody([dcc.Graph(figure=figure_2_9),
                                          html.Hr(),
                                          dbc.Table.from_dataframe(filtered_df_2_9.T.round(2), index=True,
                                                                   striped=True, bordered=True, hover=True)
                                          ]),
                            dbc.CardFooter("Enter some dot point automated analysis here....")
                        ], color="primary", outline=True), align="center", className="mb-3"),
                    ], align="center", className="mb-3"),

                        # End of Centre Work Area
                ], width=8, align="center", className="mb-3"),

                # Right Gutter
                dbc.Col("", width=2, align="center", className="mb-3"),

            ], align="center", className="mb-3")


        ]


    elif pathname == "/3-Allocation":

        filtered_df_3_2 = pd.concat([Selected_Portfolio.df_L3_w.loc[dt_end_date:dt_end_date, ['P_' + groupName + '_' + n]].T for n in groupList], axis=1)
        filtered_df_3_2.index = groupList
        filtered_df_3_2['Current'] = filtered_df_3_2.sum(axis=1)
        filtered_df_3_2 = filtered_df_3_2[['Current']]
        filtered_df_3_2.reset_index(inplace=True)
        filtered_df_3_2.columns = ['GroupValue', 'Current']

        figure_3_2 = px.pie(
            filtered_df_3_2,
            values='Current',
            names='GroupValue',
            template="plotly_white"
        )
        figure_3_2.update_layout(
            title={
                "text": f"As at {dt_end_date:%d-%b-%Y}",
                "font": {"size": 11}  # Adjust the font size as needed
            },

            legend=dict(
                orientation="h",
                yanchor="top",  # Change this to "top" to move the legend below the chart
                y=-0.3,  # Adjust the y value to position the legend below the chart
                xanchor="center",  # Center the legend horizontally
                x=0.5,  # Center the legend horizontally
                title=None,
                font=dict(size=11)
            ),
            # margin = dict(r=0, l=0),  # Reduce right margin to maximize visible area
        )

        # Below is dependent on 3.2
        row_values = []
        allrows_values = []
        group_df = Selected_Portfolio.df_L3_limits[Selected_Portfolio.df_L3_limits['Group'] == groupName]
        for n, element in enumerate(groupList):
            # Filter the DataFrame for the current group
            group_df2 = group_df[group_df['GroupValue'] == groupList[n]]
            row_values.append(groupList[n])
            row_values.append(filtered_df_3_2.loc[n, "Current"])
            # Check if there are any rows for the current group
            if not group_df2.empty:
                # Get the minimum value from the 'Min' column of the filtered DataFrame
                row_values.append(group_df2['Min'].min())
                row_values.append(group_df2['Max'].max())
            else:
                # If no rows are found for the current group, append None to the list
                row_values.append(0)
                row_values.append(100)

            allrows_values.append(row_values)
            row_values = []

        column_names = ['Group Value', 'Current', 'Min', 'Max']

        filtered_df_3_1 = pd.DataFrame(allrows_values, columns=column_names)

        filtered_df_3_1['Max-Min'] = filtered_df_3_1['Max'] - filtered_df_3_1['Min']
        figure_3_1 = px.bar(filtered_df_3_1, x='Group Value', y=['Min', 'Max-Min'])

        figure_3_1.update_traces(marker_color='#3D555E', width=0.3, opacity=0,
                          selector=dict(name='Min'))  # Set color, width, and opacity for 'Min' bars
        # figure_3_1.update_traces(marker_color='#3D555E', width=0.3,
        #                   selector=dict(name='Max-Min'))  # Set color and width for 'Max-Min' bars

        figure_3_1.update_traces(marker_color='#3D555E', width=0.3,
                          selector=dict(name='Max-Min'))  # Set color and width for 'Max-Min' bars

        scatter_fig = px.scatter(filtered_df_3_1, x='Group Value', y='Current',
                                 title='Current', color_discrete_sequence=['#1DC8F2'])
        for trace in scatter_fig.data:
            figure_3_1.add_trace(trace)

        figure_3_1.update_layout(
            showlegend=False,
            title={
                "text": f"As at {dt_end_date:%d-%b-%Y}",
                "font": {"size": 11}  # Adjust the font size as needed
            },
            margin=dict(r=0, l=0),  # Reduce right margin to maximize visible area
            yaxis_title='Allocation Range (%)'
        )


        filtered_df_3_3 = pd.concat([Selected_Portfolio.df_L2vsL1_relw.loc[dt_start_date:dt_end_date,
                       ['P_' + groupName + '_' + n]] for n in groupList], axis=1)
        filtered_df_3_3.columns = groupList

        figure_3_3 = px.bar(
            filtered_df_3_3,
            x=filtered_df_3_3.index,
            y=[c for c in filtered_df_3_3.columns],
            labels={"x": "Date", "y": "Values"},
            template="plotly_white",
            barmode='relative'
        )
        figure_3_3.update_layout(
            yaxis_title="Asset Allocation (%)",
            xaxis_title="",
            legend=dict(
                orientation="h",
                yanchor="top",  # Change this to "top" to move the legend below the chart
                y=-0.3,  # Adjust the y value to position the legend below the chart
                xanchor="center",  # Center the legend horizontally
                x=0.5,  # Center the legend horizontally
                title=None,
                font=dict(size=11)
            ),
            margin=dict(r=0),  # Reduce right margin to maximize visible area
        )

        filtered_df_3_4 = pd.concat([Selected_Portfolio.df_L3_w.loc[dt_start_date:dt_end_date,
                       ['P_' + groupName + '_' + n]] for n in groupList], axis=1)
        filtered_df_3_4.columns = groupList

        figure_3_4 = px.bar(
            filtered_df_3_4,
            x=filtered_df_3_4.index,
            y=[c for c in filtered_df_3_4.columns],
            labels={"x": "Date", "y": "Values"},
            template="plotly_white",
            barmode='stack'
        )
        figure_3_4.update_layout(
            yaxis_title="Asset Allocation (%)",
            xaxis_title="",
            legend=dict(
                orientation="h",
                yanchor="top",  # Change this to "top" to move the legend below the chart
                y=-0.3,  # Adjust the y value to position the legend below the chart
                xanchor="center",  # Center the legend horizontally
                x=0.5,  # Center the legend horizontally
                title=None,
                font=dict(size=11)
            ),
            margin=dict(r=0),  # Reduce right margin to maximize visible area
        )


        filtered_df_3_5 = Selected_Portfolio.df_L3_w.loc[dt_end_date:dt_end_date, Selected_Portfolio.df_L3_w.columns.isin(Product_List)].tail(1)
        filtered_df_3_5 = filtered_df_3_5.loc[:, (filtered_df_3_5 != 0).any()].T
        filtered_df_3_5 = filtered_df_3_5.rename_axis('Code')
        filtered_df_3_5 = filtered_df_3_5.merge(Selected_Portfolio.df_productList[['Name', 'G0', 'G1', 'G2', 'G3', 'G4']], on='Code')
        filtered_df_3_5 = filtered_df_3_5.rename(columns={dt_end_date: 'Current Weight'})

        figure_3_5 = px.sunburst(
            filtered_df_3_5,
            path=['G0', 'G1', 'G4', 'Name'],
            names='Name',
            values='Current Weight',
            template="plotly_white"
        )
        figure_3_5.update_layout(
            title={
                "text": f"As at {dt_end_date:%d-%b-%Y}",
                "font": {"size": 11}  # Adjust the font size as needed
            },
            margin=dict(r=0, l=0),  # Reduce right margin to maximize visible area
        )

        filtered_df_3_6 = filtered_df_3_5

        figure_3_6 = px.sunburst(
            filtered_df_3_6,
            path=['G1', 'Name'],
            names='Name',
            values='Current Weight',
            template="plotly_white"
        )
        figure_3_6.update_layout(
            title={
                "text": f"As at {dt_end_date:%d-%b-%Y}",
                "font": {"size": 11}  # Adjust the font size as needed
            },
            margin=dict(r=0, l=0),  # Reduce right margin to maximize visible area
        )

        filtered_df_3_7 = filtered_df_3_5
        underlying_df_3_7 = []
        # Find if any of the held investments - are also available in the dataset as products with look through holdings
        for index, value in enumerate(filtered_df_3_7.index):
            if value in availablePortfolios:
                print("Matched value:", value)
                Underlying_Portfolio = All_Portfolios[availablePortfolios.index(value)]

                underlying_df_3_7 = Underlying_Portfolio.df_L3_w.loc[dt_end_date:dt_end_date,
                                  Underlying_Portfolio.df_L3_w.columns.isin(Product_List)].tail(1)
                underlying_df_3_7 = underlying_df_3_7.loc[:, (underlying_df_3_7 != 0).any()].T
                underlying_df_3_7 = underlying_df_3_7.rename_axis('Code')

                underlying_df_3_7 = underlying_df_3_7.merge(
                    Selected_Portfolio.df_productList[['Name', 'G0', 'G1', 'G2', 'G3', 'G4']], on='Code')
                underlying_df_3_7 = underlying_df_3_7.rename(columns={dt_end_date: 'Current Weight'})

                # Find and print the 'Current Weight' in filtered_df_3_7
                parent_weight_value = filtered_df_3_7.loc[value, 'Current Weight']
                print("Current Weight in filtered_df_3_7:", parent_weight_value)

                # Multiply each value in 'Current Weight' column of underlying_df_3_7
                underlying_df_3_7['Current Weight'] *= (parent_weight_value/100)

                # Remove the matched row from filtered_df_3_7
                filtered_df_3_7 = filtered_df_3_7.drop(index=value)

                # Merge all rows from underlying_df_3_7 into filtered_df_3_7
                filtered_df_3_7 = pd.concat([filtered_df_3_7, underlying_df_3_7])

        figure_3_7 = px.sunburst(
            filtered_df_3_7,
            path=['G1', 'Name'],
            names='Name',
            values='Current Weight',
            template="plotly_white"
        )
        figure_3_7.update_layout(
            title={
                "text": f"As at {dt_end_date:%d-%b-%Y}",
                "font": {"size": 11}  # Adjust the font size as needed
            },
            margin=dict(r=0, l=0),  # Reduce right margin to maximize visible area
        )


        figure_3_8 = px.sunburst(
            filtered_df_3_7,  # This needs updating to 3_78
            path=['G1', 'G4', 'Name'],
            names='Name',
            values='Current Weight',
            template="plotly_white"
        )
        figure_3_8.update_layout(
            title={
                "text": f"As at {dt_end_date:%d-%b-%Y}",
                "font": {"size": 11}  # Adjust the font size as needed
            },
            margin=dict(r=0, l=0),  # Reduce right margin to maximize visible area
        )



        ## Populate Charts for Page 3-Allocation
        return [
            html.Div(style={'height': '2rem'}),
            html.H2('Allocation / Exposure Analysis',
                    style={'textAlign': 'center', 'color': "#3D555E"}),
            html.Hr(),
            html.Hr(style={'border-color': "#3D555E", 'width': '70%', 'margin': 'auto auto'}),
            html.Hr(),

            dbc.Row([
                # Left Gutter
                dbc.Col("", width=2, align="center", className="mb-3"),
                # Centre Work Area
                dbc.Col([

                    # Tab 3- Allocations
                    dbc.Row([
                        dbc.Col(dbc.Card([
                            dbc.CardHeader("Chart 1: Current Allocation"),
                            dbc.CardBody(dcc.Graph(figure=figure_3_2)),
                            dbc.CardFooter("Enter some dot point automated analysis here....")
                        ], color="primary", outline=True), align="center", className="mb-3"),
                        dbc.Col(dbc.Card([
                            dbc.CardHeader("Chart 2: Current "+groupName+" Policy Ranges"),
                            dbc.CardBody(dcc.Graph(figure=figure_3_1)),
                            dbc.CardFooter("Enter some dot point automated analysis here....")
                        ], color="primary", outline=True), align="center", className="mb-3"),
                    ], align="center", className="mb-3"),

                    dbc.Row([
                        dbc.Col(dbc.Card([
                            dbc.CardHeader("Chart 3: Current Asset Allocation"),
                            dbc.CardBody(dcc.Graph(figure=figure_3_5, style={'height': '1000px'})),
                            dbc.CardFooter("Enter some dot point automated analysis here....")
                        ], color="primary", outline=True), align="center", className="mb-3"),
                    ], align="center", className="mb-3"),

                    dbc.Row([
                        dbc.Col(dbc.Card([
                            dbc.CardHeader("Chart 4: Current Asset Allocation"),
                            dbc.CardBody(dcc.Graph(figure=figure_3_6, style={'height': '1000px'})),
                            dbc.CardFooter("Enter some dot point automated analysis here....")
                        ], color="primary", outline=True), align="center", className="mb-3"),
                    ], align="center", className="mb-3"),

                    dbc.Row([
                        dbc.Col(dbc.Card([
                            dbc.CardHeader("Chart 5: Current Asset Allocation - Drill Through"),
                            dbc.CardBody(dcc.Graph(figure=figure_3_7, style={'height': '1000px'})),
                            dbc.CardFooter("Enter some dot point automated analysis here....")
                        ], color="primary", outline=True), align="center", className="mb-3"),
                    ], align="center", className="mb-3"),

                    dbc.Row([
                        dbc.Col(dbc.Card([
                            dbc.CardHeader("Chart 5: Current Asset Allocation - Drill Through"),
                            dbc.CardBody(dcc.Graph(figure=figure_3_8, style={'height': '1000px'})),
                            dbc.CardFooter("Enter some dot point automated analysis here....")
                        ], color="primary", outline=True), align="center", className="mb-3"),
                    ], align="center", className="mb-3"),

                    dbc.Row([
                        dbc.Col(dbc.Card([
                            dbc.CardHeader(
                                "Chart 6: Portfolio Sleeve Overweights/Underweights Through Time"),
                            dbc.CardBody(dcc.Graph(figure=figure_3_3)),
                            dbc.CardFooter("Enter some dot point automated analysis here....")
                        ], color="primary", outline=True), align="center", className="mb-3"),
                        dbc.Col(dbc.Card([
                            dbc.CardHeader("Chart 5: Portfolio Sleeve Weights Through Time"),
                            dbc.CardBody(dcc.Graph(figure=figure_3_4)),
                            dbc.CardFooter("Enter some dot point automated analysis here....")
                        ], color="primary", outline=True), align="center", className="mb-3"),
                    ], align="center", className="mb-3"),



                    dbc.Row([
                        # Left Gutter
                        dbc.Col("", width=2, align="center", className="mb-3"),
                        # Centre Work Area
                        dbc.Col([
                            dbc.Table.from_dataframe(filtered_df_3_7, striped=True, bordered=True, hover=True)
                            # End of Centre Work Area
                        ], width=12, align="center", className="mb-3"),

                        # Right Gutter
                        dbc.Col("", width=2, align="center", className="mb-3"),

                    ], align="center", className="mb-3"),



                    # End of Centre Work Area
                ], width=8, align="center", className="mb-3"),

                # Right Gutter
                dbc.Col("", width=2, align="center", className="mb-3"),

            ], align="center", className="mb-3")

        ]


    elif pathname == "/4-Attribution":
        filtered_df_4_1 = (((Selected_Portfolio.df_L3_1FAttrib.loc[dt_start_date:dt_end_date, ['P_TOTAL_G1 -- Allocation Effect',
                                                                                     'P_TOTAL_G1 -- Selection Effect']] + 1).cumprod() - 1) * 100)
        figure_4_1 = px.line(
            filtered_df_4_1,
            x=filtered_df_4_1.index,
            y=[c for c in filtered_df_4_1.columns],
            template="plotly_white"
        )
        figure_4_1.update_layout(
            yaxis_title="Value-Add Return (%)",
            xaxis_title="",
            legend=dict(
                orientation="h",
                yanchor="top",  # Change this to "top" to move the legend below the chart
                y=-0.3,  # Adjust the y value to position the legend below the chart
                xanchor="center",  # Center the legend horizontally
                x=0.5,  # Center the legend horizontally
                title=None,
                font=dict(size=11)
            ),
            margin=dict(r=0),  # Reduce right margin to maximize visible area
        )

        filtered_df_4_2 = (((Selected_Portfolio.df_L3_1FAttrib.loc[dt_start_date:dt_end_date,
                         ['G1_Australian Shares-- Allocation Effect',
                          'G1_Australian Shares-- Selection Effect',
                          'G1_International Shares-- Allocation Effect',
                          'G1_International Shares-- Selection Effect']] + 1).cumprod() - 1) * 100)

        figure_4_2 = px.line(
            filtered_df_4_2,
            x=filtered_df_4_2.index,
            y=[c for c in filtered_df_4_2.columns],
            template="plotly_white"
        )
        figure_4_2.update_layout(
            yaxis_title="Value-Add Return (%)",
            xaxis_title="",
            legend=dict(
                orientation="h",
                yanchor="top",  # Change this to "top" to move the legend below the chart
                y=-0.3,  # Adjust the y value to position the legend below the chart
                xanchor="center",  # Center the legend horizontally
                x=0.5,  # Center the legend horizontally
                title=None,
                font=dict(size=11)
            ),
            margin=dict(r=0),  # Reduce right margin to maximize visible area
        )

        filtered_df_4_3 = (
                    ((Selected_Portfolio.df_L3_1FAttrib.loc[dt_start_date:dt_end_date, ['G1_Real Assets-- Allocation Effect',
                                                                                  'G1_Real Assets-- Selection Effect',
                                                                                  'G1_Alternatives-- Allocation Effect',
                                                                                  'G1_Alternatives-- Selection Effect']] + 1).cumprod() - 1) * 100)

        figure_4_3 = px.line(
            filtered_df_4_3,
            x=filtered_df_4_3.index,
            y=[c for c in filtered_df_4_3.columns],
            template="plotly_white"
        )
        figure_4_3.update_layout(
            yaxis_title="Value-Add Return (%)",
            xaxis_title="",
            legend=dict(
                orientation="h",
                yanchor="top",  # Change this to "top" to move the legend below the chart
                y=-0.3,  # Adjust the y value to position the legend below the chart
                xanchor="center",  # Center the legend horizontally
                x=0.5,  # Center the legend horizontally
                title=None,
                font=dict(size=11)
            ),
            margin=dict(r=0),  # Reduce right margin to maximize visible area
        )

        filtered_df_4_4 = (((Selected_Portfolio.df_L3_1FAttrib.loc[dt_start_date:dt_end_date,
                         ['G1_Long Duration-- Allocation Effect',
                          'G1_Long Duration-- Selection Effect',
                          'G1_Floating Rate-- Allocation Effect',
                          'G1_Floating Rate-- Selection Effect',
                          'G1_Cash-- Allocation Effect',
                          'G1_Cash-- Selection Effect',
                          ]] + 1).cumprod() - 1) * 100)

        figure_4_4 = px.line(
            filtered_df_4_4,
            x=filtered_df_4_4.index,
            y=[c for c in filtered_df_4_4.columns],
            template="plotly_white"
        )
        figure_4_4.update_layout(
            yaxis_title="Value-Add Return (%)",
            xaxis_title="",
            legend=dict(
                orientation="h",
                yanchor="top",  # Change this to "top" to move the legend below the chart
                y=-0.3,  # Adjust the y value to position the legend below the chart
                xanchor="center",  # Center the legend horizontally
                x=0.5,  # Center the legend horizontally
                title=None,
                font=dict(size=11)
            ),
            margin=dict(r=0),  # Reduce right margin to maximize visible area
        )

        filtered_df_4_5 = (f_CalcReturnTable(Selected_Portfolio.df_L3_1FAttrib.loc[dt_start_date:dt_end_date,
                                            ['G1_Australian Shares-- Allocation Effect',
                                             'G1_Australian Shares-- Selection Effect',
                                             'G1_International Shares-- Allocation Effect',
                                             'G1_International Shares-- Selection Effect',
                                             'G1_Real Assets-- Allocation Effect',
                                             'G1_Real Assets-- Selection Effect',
                                             'G1_Alternatives-- Allocation Effect',
                                             'G1_Alternatives-- Selection Effect',
                                             'G1_Long Duration-- Allocation Effect',
                                             'G1_Long Duration-- Selection Effect',
                                             'G1_Floating Rate-- Allocation Effect',
                                             'G1_Floating Rate-- Selection Effect',
                                             'G1_Cash-- Allocation Effect',
                                             'G1_Cash-- Selection Effect'
                                             ]],
            Selected_Portfolio.tME_dates) * 100).T

        ## Populate Charts for Page 4 Attribution
        return [
            html.Div(style={'height': '2rem'}),
            html.H2('Multi-Period Brinson-Fachler Attribution Analysis',
                    style={'textAlign': 'center', 'color': "#3D555E"}),
            html.Hr(),
            html.Hr(style={'border-color': "#3D555E", 'width': '70%', 'margin': 'auto auto'}),
            html.Hr(),

            dbc.Row([
                # Left Gutter
                dbc.Col("", width=2, align="center", className="mb-3"),
                # Centre Work Area
                dbc.Col([
                    # Tab 4- Attribution Analysis
                    dbc.Row([
                        dbc.Col(dbc.Card([
                            dbc.CardHeader(
                                "Chart 1: Portfolio Attribution Analysis vs Reference Portfolio"),
                            dbc.CardBody(dcc.Graph(figure=figure_4_1)),
                            dbc.CardFooter("Enter some dot point automated analysis here....")
                        ], color="primary", outline=True), align="center", className="mb-3"),
                        dbc.Col(dbc.Card([
                            dbc.CardHeader("Chart 2: L3 SAA to TAA Attribution Analysis (Equities)"),
                            dbc.CardBody(dcc.Graph(figure=figure_4_2)),
                            dbc.CardFooter("Enter some dot point automated analysis here....")
                        ], color="primary", outline=True), align="center", className="mb-3"),
                    ], align="center", className="mb-3"),

                    dbc.Row([
                        dbc.Col(dbc.Card([
                            dbc.CardHeader("Chart 3: L3 SAA to TAA Attribution Analysis (Alternatives)"),
                            dbc.CardBody(dcc.Graph(figure=figure_4_3)),
                            dbc.CardFooter("Enter some dot point automated analysis here....")
                        ], color="primary", outline=True), align="center", className="mb-3"),
                        dbc.Col(dbc.Card([
                            dbc.CardHeader("Chart 4: L3 SAA to TAA Attribution Analysis (Defensives)"),
                            dbc.CardBody(dcc.Graph(figure=figure_4_4)),
                            dbc.CardFooter("Enter some dot point automated analysis here....")
                        ], color="primary", outline=True), align="center", className="mb-3"),
                    ], align="center", className="mb-3"),

                    dbc.Row([
                        dbc.Col(dbc.Card([
                            dbc.CardHeader(
                                "Chart 5: Portfolio Risk Metrics Chart - Daily Asset Sleeve Returns"),
                            dbc.CardBody([dbc.Table.from_dataframe(filtered_df_4_5.T.round(2), index=True,
                                                                   striped=True, bordered=True, hover=True)
                                          ]),
                            dbc.CardFooter("Enter some dot point automated analysis here....")
                        ], color="primary", outline=True), align="center", className="mb-3"),
                    ], align="center", className="mb-3"),

                    # End of Centre Work Area
                ], width=8, align="center", className="mb-3"),

                # Right Gutter
                dbc.Col("", width=2, align="center", className="mb-3"),

            ], align="center", className="mb-3")
        ]
    elif pathname == "/5-Contribution":

        filtered_df_5_1 = pd.concat([(((Selected_Portfolio.df_L3_contrib.loc[dt_start_date:dt_end_date, ['P_' + groupName + '_' + n]] + 1).cumprod() - 1) * 100)
                                     for n in groupList], axis=1)
        filtered_df_5_1.columns = groupList

        figure_5_1 = px.line(
            filtered_df_5_1,
            x=filtered_df_5_1.index,
            y=[c for c in filtered_df_5_1.columns],
            labels={"x": "Date", "y": "Values"},
            template="plotly_white",
        )
        figure_5_1.update_layout(
            yaxis_title="Cumulative Contribution (%)",
            xaxis_title="",
            legend=dict(
                orientation="h",
                yanchor="top",  # Change this to "top" to move the legend below the chart
                y=-0.3,  # Adjust the y value to position the legend below the chart
                xanchor="center",  # Center the legend horizontally
                x=0.5,  # Center the legend horizontally
                title=None,
                font=dict(size=11)
            ),
            margin=dict(r=0),  # Reduce right margin to maximize visible area
        )

        listq_5_2 = f_AssetClassContrib(Selected_Portfolio.df_L3_contrib, "Australian Shares")
        filtered_df_5_2 = (((Selected_Portfolio.df_L3_contrib.loc[dt_start_date:dt_end_date, listq_5_2] + 1).cumprod() - 1) * 100)

        figure_5_2 = px.line(
            filtered_df_5_2,
            x=filtered_df_5_2.index,
            y=[c for c in filtered_df_5_2.columns],
            labels={"x": "Date", "y": "Values"},
            template="plotly_white",
        )
        figure_5_2.update_layout(
            yaxis_title="Cumulative Contribution (%)",
            xaxis_title="",
            legend=dict(
                orientation="h",
                yanchor="top",  # Change this to "top" to move the legend below the chart
                y=-0.3,  # Adjust the y value to position the legend below the chart
                xanchor="center",  # Center the legend horizontally
                x=0.5,  # Center the legend horizontally
                title=None,
                font=dict(size=11)
            ),
            margin=dict(r=0),  # Reduce right margin to maximize visible area
        )

        checkData = Selected_Portfolio.df_L3_w.loc[dt_end_date, ['P_' + groupName + '_' + "International Shares"]]

        if checkData[0] > 0:
            listq_5_3 = f_AssetClassContrib(Selected_Portfolio.df_L3_contrib, "International Shares")
            filtered_df_5_3 = (((Selected_Portfolio.df_L3_contrib.loc[dt_start_date:dt_end_date, listq_5_3] + 1).cumprod() - 1) * 100)
        else:
            filtered_df_5_3 = []

        figure_5_3 = px.line(
            filtered_df_5_3,
            x=filtered_df_5_3.index,
            y=[c for c in filtered_df_5_3.columns],
            labels={"x": "Date", "y": "Values"},
            template="plotly_white",
        )
        figure_5_3.update_layout(
            yaxis_title="Cumulative Contribution (%)",
            xaxis_title="",
            legend=dict(
                orientation="h",
                yanchor="top",  # Change this to "top" to move the legend below the chart
                y=-0.3,  # Adjust the y value to position the legend below the chart
                xanchor="center",  # Center the legend horizontally
                x=0.5,  # Center the legend horizontally
                title=None,
                font=dict(size=11)
            ),
            margin=dict(r=0),  # Reduce right margin to maximize visible area
        )

        checkData = Selected_Portfolio.df_L3_w.loc[dt_end_date, ['P_' + groupName + '_' + "Real Assets"]]

        if checkData[0] > 0:
            listq_5_4 = f_AssetClassContrib(Selected_Portfolio.df_L3_contrib, "Real Assets")
            filtered_df_5_4 = (((Selected_Portfolio.df_L3_contrib.loc[dt_start_date:dt_end_date, listq_5_4] + 1).cumprod() - 1) * 100)
        else:
            filtered_df_5_4 = []
            print("avoided error 2")

        figure_5_4 = px.line(
            filtered_df_5_4,
            x=filtered_df_5_4.index,
            y=[c for c in filtered_df_5_4.columns],
            labels={"x": "Date", "y": "Values"},
            template="plotly_white",
        )
        figure_5_4.update_layout(
            yaxis_title="Cumulative Contribution (%)",
            xaxis_title="",
            legend=dict(
                orientation="h",
                yanchor="top",  # Change this to "top" to move the legend below the chart
                y=-0.3,  # Adjust the y value to position the legend below the chart
                xanchor="center",  # Center the legend horizontally
                x=0.5,  # Center the legend horizontally
                title=None,
                font=dict(size=11)
            ),
            margin=dict(r=0),  # Reduce right margin to maximize visible area
        )

        checkData = Selected_Portfolio.df_L3_w.loc[dt_end_date, ['P_' + groupName + '_' + "Alternatives"]]

        if checkData[0] > 0:
            listq_5_5 = f_AssetClassContrib(Selected_Portfolio.df_L3_contrib, "Alternatives")
            filtered_df_5_5 = (((Selected_Portfolio.df_L3_contrib.loc[dt_start_date:dt_end_date, listq_5_5] + 1).cumprod() - 1) * 100)
        else:
            filtered_df_5_5 = []
            print("avoided error 2")

        figure_5_5 = px.line(
            filtered_df_5_5,
            x=filtered_df_5_5.index,
            y=[c for c in filtered_df_5_5.columns],
            labels={"x": "Date", "y": "Values"},
            template="plotly_white",
        )
        figure_5_5.update_layout(
            yaxis_title="Cumulative Contribution (%)",
            xaxis_title="",
            legend=dict(
                orientation="h",
                yanchor="top",  # Change this to "top" to move the legend below the chart
                y=-0.3,  # Adjust the y value to position the legend below the chart
                xanchor="center",  # Center the legend horizontally
                x=0.5,  # Center the legend horizontally
                title=None,
                font=dict(size=11)
            ),
            margin=dict(r=0),  # Reduce right margin to maximize visible area
        )

        checkData = Selected_Portfolio.df_L3_w.loc[dt_end_date, ['P_' + groupName + '_' + "Long Duration"]]

        if checkData[0] > 0:
            listq_5_6 = f_AssetClassContrib(Selected_Portfolio.df_L3_contrib, "Long Duration")
            filtered_df_5_6 = (((Selected_Portfolio.df_L3_contrib.loc[dt_start_date:dt_end_date, listq_5_6] + 1).cumprod() - 1) * 100)
        else:
            filtered_df_5_6 = []
            print("avoided error 2")

        figure_5_6 = px.line(
            filtered_df_5_6,
            x=filtered_df_5_6.index,
            y=[c for c in filtered_df_5_6.columns],
            labels={"x": "Date", "y": "Values"},
            template="plotly_white",
        )
        figure_5_6.update_layout(
            yaxis_title="Cumulative Contribution (%)",
            xaxis_title="",
            legend=dict(
                orientation="h",
                yanchor="top",  # Change this to "top" to move the legend below the chart
                y=-0.3,  # Adjust the y value to position the legend below the chart
                xanchor="center",  # Center the legend horizontally
                x=0.5,  # Center the legend horizontally
                title=None,
                font=dict(size=11)
            ),
            margin=dict(r=0),  # Reduce right margin to maximize visible area
        )

        checkData = Selected_Portfolio.df_L3_w.loc[dt_end_date, ['P_' + groupName + '_' + "Floating Rate"]]

        if checkData[0] > 0:
            listq_5_7 = f_AssetClassContrib(Selected_Portfolio.df_L3_contrib, "Floating Rate")
            filtered_df_5_7 = (((Selected_Portfolio.df_L3_contrib.loc[dt_start_date:dt_end_date, listq_5_7] + 1).cumprod() - 1) * 100)
        else:
            filtered_df_5_7 = []
            print("avoided error 2")

        figure_5_7 = px.line(
            filtered_df_5_7,
            x=filtered_df_5_7.index,
            y=[c for c in filtered_df_5_7.columns],
            labels={"x": "Date", "y": "Values"},
            template="plotly_white",
        )
        figure_5_7.update_layout(
            yaxis_title="Cumulative Contribution (%)",
            xaxis_title="",
            legend=dict(
                orientation="h",
                yanchor="top",  # Change this to "top" to move the legend below the chart
                y=-0.3,  # Adjust the y value to position the legend below the chart
                xanchor="center",  # Center the legend horizontally
                x=0.5,  # Center the legend horizontally
                title=None,
                font=dict(size=11)
            ),
            margin=dict(r=0),  # Reduce right margin to maximize visible area
        )

        checkData = Selected_Portfolio.df_L3_w.loc[dt_end_date, ['P_' + groupName + '_' + "Cash"]]

        if checkData[0] > 0:
            listq_5_7 = f_AssetClassContrib(Selected_Portfolio.df_L3_contrib, "Cash")
            filtered_df_5_7 = (((Selected_Portfolio.df_L3_contrib.loc[dt_start_date:dt_end_date, listq_5_7] + 1).cumprod() - 1) * 100)
        else:
            filtered_df_5_7 = []
            print("avoided error 2")

        listq_5_8 = f_AssetClassContrib(Selected_Portfolio.df_L3_contrib, "Cash")
        filtered_df_5_8 = (((Selected_Portfolio.df_L3_contrib.loc[dt_start_date:dt_end_date, listq_5_8] + 1).cumprod() - 1) * 100)

        figure_5_8 = px.line(
            filtered_df_5_8,
            x=filtered_df_5_8.index,
            y=[c for c in filtered_df_5_8.columns],
            labels={"x": "Date", "y": "Values"},
            template="plotly_white",
        )
        figure_5_8.update_layout(
            yaxis_title="Cumulative Contribution (%)",
            xaxis_title="",
            legend=dict(
                orientation="h",
                yanchor="top",  # Change this to "top" to move the legend below the chart
                y=-0.3,  # Adjust the y value to position the legend below the chart
                xanchor="center",  # Center the legend horizontally
                x=0.5,  # Center the legend horizontally
                title=None,
                font=dict(size=11)
            ),
            margin=dict(r=0),  # Reduce right margin to maximize visible area
        )

        filtered_df_5_9 = (f_CalcReturnTable(Selected_Portfolio.df_L3_1FAttrib.loc[dt_start_date:dt_end_date,
                                             ['G1_Australian Shares-- Allocation Effect',
                                              'G1_Australian Shares-- Selection Effect',
                                              'G1_International Shares-- Allocation Effect',
                                              'G1_International Shares-- Selection Effect',
                                              'G1_Real Assets-- Allocation Effect',
                                              'G1_Real Assets-- Selection Effect',
                                              'G1_Alternatives-- Allocation Effect',
                                              'G1_Alternatives-- Selection Effect',
                                              'G1_Long Duration-- Allocation Effect',
                                              'G1_Long Duration-- Selection Effect',
                                              'G1_Floating Rate-- Allocation Effect',
                                              'G1_Floating Rate-- Selection Effect',
                                              'G1_Cash-- Allocation Effect',
                                              'G1_Cash-- Selection Effect'
                                              ]],
                                             Selected_Portfolio.tME_dates) * 100).T

        ## Populate Charts for Page 5 Contribution
        return [
            html.Div(style={'height': '2rem'}),
            html.H2('Multi-Period Weighted Return Contribution Analysis',
                    style={'textAlign': 'center', 'color': "#3D555E"}),
            html.Hr(),
            html.Hr(style={'border-color': "#3D555E", 'width': '70%', 'margin': 'auto auto'}),
            html.Hr(),

            dbc.Row([
                # Left Gutter
                dbc.Col("", width=2, align="center", className="mb-3"),
                # Centre Work Area
                dbc.Col([
                    # Tab 6- Underlying Detail Analysis
                    dbc.Row([
                        dbc.Col(dbc.Card([
                            dbc.CardHeader("Chart 1: Asset Sleeve Weighted Return Contributions"),
                            dbc.CardBody(dcc.Graph(figure=figure_5_1)),
                            dbc.CardFooter("Enter some dot point automated analysis here....")
                        ], color="primary", outline=True), align="center", className="mb-3"),
                        dbc.Col(dbc.Card([
                            dbc.CardHeader("Chart 2: Australian Shares Sleeve - Contributions"),
                            dbc.CardBody(dcc.Graph(figure=figure_5_2)),
                            dbc.CardFooter("Enter some dot point automated analysis here....")
                        ], color="primary", outline=True), align="center", className="mb-3"),
                    ], align="center", className="mb-3"),
                    dbc.Row([
                        dbc.Col(dbc.Card([
                            dbc.CardHeader("Chart 3: International Shares Sleeve - Contributions"),
                            dbc.CardBody(dcc.Graph(figure=figure_5_3)),
                            dbc.CardFooter("Enter some dot point automated analysis here....")
                        ], color="primary", outline=True), align="center", className="mb-3"),
                        dbc.Col(dbc.Card([
                            dbc.CardHeader("Chart 4: Real Assets Sleeve - Contributions"),
                            dbc.CardBody(dcc.Graph(figure=figure_5_4)),
                            dbc.CardFooter("Enter some dot point automated analysis here....")
                        ], color="primary", outline=True), align="center", className="mb-3"),
                    ], align="center", className="mb-3"),
                    dbc.Row([
                        dbc.Col(dbc.Card([
                            dbc.CardHeader("Chart 5: Alternatives Sleeve - Contributions"),
                            dbc.CardBody(dcc.Graph(figure=figure_5_5)),
                            dbc.CardFooter("Enter some dot point automated analysis here....")
                        ], color="primary", outline=True), align="center", className="mb-3"),
                        dbc.Col(dbc.Card([
                            dbc.CardHeader("Chart 6: Long Duration Sleeve - Contributions"),
                            dbc.CardBody(dcc.Graph(figure=figure_5_6)),
                            dbc.CardFooter("Enter some dot point automated analysis here....")
                        ], color="primary", outline=True), align="center", className="mb-3"),
                    ], align="center", className="mb-3"),
                    dbc.Row([
                        dbc.Col(dbc.Card([
                            dbc.CardHeader("Chart 7: Floating Rate Sleeve - Contributions"),
                            dbc.CardBody(dcc.Graph(figure=figure_5_7)),
                            dbc.CardFooter("Enter some dot point automated analysis here....")
                        ], color="primary", outline=True), align="center", className="mb-3"),
                        dbc.Col(dbc.Card([
                            dbc.CardHeader("Chart 8: Cash Sleeve - Contributions"),
                            dbc.CardBody(dcc.Graph(figure=figure_5_8)),
                            dbc.CardFooter("Enter some dot point automated analysis here....")
                        ], color="primary", outline=True), align="center", className="mb-3"),
                    ], align="center", className="mb-3"),
                    # End of Centre Work Area
                ], width=8, align="center", className="mb-3"),

                # Right Gutter
                dbc.Col("", width=2, align="center", className="mb-3"),

            ], align="center", className="mb-3")

        ]
    elif pathname == "/6-Component":

        filtered_df_6_1 = pd.concat([(((Selected_Portfolio.df_L3_r.loc[dt_start_date:dt_end_date, ['P_' + groupName + '_' + n]] + 1).cumprod() - 1) * 100)
                                     for n in groupList], axis=1)
        filtered_df_6_1.columns = groupList

        figure_6_1 = px.line(
            filtered_df_6_1,
            x=filtered_df_6_1.index,
            y=[c for c in filtered_df_6_1.columns],
            labels={"x": "Date", "y": "Values"},
            template="plotly_white",
        )
        figure_6_1.update_layout(
            yaxis_title="Cumulative Return (%)",
            xaxis_title="",
            legend=dict(
                orientation="h",
                yanchor="top",  # Change this to "top" to move the legend below the chart
                y=-0.3,  # Adjust the y value to position the legend below the chart
                xanchor="center",  # Center the legend horizontally
                x=0.5,  # Center the legend horizontally
                title=None,
                font=dict(size=11)
            ),
            margin=dict(r=0),  # Reduce right margin to maximize visible area
        )

        listq_6_2 = f_AssetClassContrib(Selected_Portfolio.df_L3_contrib, "Australian Shares")
        filtered_df_6_2 = (((Selected_Portfolio.df_L3_r.loc[dt_start_date:dt_end_date, listq_6_2] + 1).cumprod() - 1) * 100)

        figure_6_2 = px.line(
            filtered_df_6_2,
            x=filtered_df_6_2.index,
            y=[c for c in filtered_df_6_2.columns],
            labels={"x": "Date", "y": "Values"},
            template="plotly_white",
        )
        figure_6_2.update_layout(
            yaxis_title="Cumulative Return (%)",
            xaxis_title="",
            legend=dict(
                orientation="h",
                yanchor="top",  # Change this to "top" to move the legend below the chart
                y=-0.3,  # Adjust the y value to position the legend below the chart
                xanchor="center",  # Center the legend horizontally
                x=0.5,  # Center the legend horizontally
                title=None,
                font=dict(size=11)
            ),
            margin=dict(r=0),  # Reduce right margin to maximize visible area
        )

        listq_6_3 = f_AssetClassContrib(Selected_Portfolio.df_L3_contrib, "International Shares")
        filtered_df_6_3 = (((Selected_Portfolio.df_L3_r.loc[dt_start_date:dt_end_date, listq_6_3] + 1).cumprod() - 1) * 100)

        figure_6_3 = px.line(
            filtered_df_6_3,
            x=filtered_df_6_3.index,
            y=[c for c in filtered_df_6_3.columns],
            labels={"x": "Date", "y": "Values"},
            template="plotly_white",
        )
        figure_6_3.update_layout(
            yaxis_title="Cumulative Return (%)",
            xaxis_title="",
            legend=dict(
                orientation="h",
                yanchor="top",  # Change this to "top" to move the legend below the chart
                y=-0.3,  # Adjust the y value to position the legend below the chart
                xanchor="center",  # Center the legend horizontally
                x=0.5,  # Center the legend horizontally
                title=None,
                font=dict(size=11)
            ),
            margin=dict(r=0),  # Reduce right margin to maximize visible area
        )

        listq_6_4 = f_AssetClassContrib(Selected_Portfolio.df_L3_contrib, "Real Assets")
        filtered_df_6_4 = (((Selected_Portfolio.df_L3_r.loc[dt_start_date:dt_end_date, listq_6_4] + 1).cumprod() - 1) * 100)

        figure_6_4 = px.line(
            filtered_df_6_4,
            x=filtered_df_6_4.index,
            y=[c for c in filtered_df_6_4.columns],
            labels={"x": "Date", "y": "Values"},
            template="plotly_white",
        )
        figure_6_4.update_layout(
            yaxis_title="Cumulative Return (%)",
            xaxis_title="",
            legend=dict(
                orientation="h",
                yanchor="top",  # Change this to "top" to move the legend below the chart
                y=-0.3,  # Adjust the y value to position the legend below the chart
                xanchor="center",  # Center the legend horizontally
                x=0.5,  # Center the legend horizontally
                title=None,
                font=dict(size=11)
            ),
            margin=dict(r=0),  # Reduce right margin to maximize visible area
        )

        listq_6_5 = f_AssetClassContrib(Selected_Portfolio.df_L3_contrib, "Alternatives")
        filtered_df_6_5 = (((Selected_Portfolio.df_L3_r.loc[dt_start_date:dt_end_date, listq_6_5] + 1).cumprod() - 1) * 100)

        figure_6_5 = px.line(
            filtered_df_6_5,
            x=filtered_df_6_5.index,
            y=[c for c in filtered_df_6_5.columns],
            labels={"x": "Date", "y": "Values"},
            template="plotly_white",
        )
        figure_6_5.update_layout(
            yaxis_title="Cumulative Return (%)",
            xaxis_title="",
            legend=dict(
                orientation="h",
                yanchor="top",  # Change this to "top" to move the legend below the chart
                y=-0.3,  # Adjust the y value to position the legend below the chart
                xanchor="center",  # Center the legend horizontally
                x=0.5,  # Center the legend horizontally
                title=None,
                font=dict(size=11)
            ),
            margin=dict(r=0),  # Reduce right margin to maximize visible area
        )

        listq_6_6 = f_AssetClassContrib(Selected_Portfolio.df_L3_contrib, "Long Duration")
        filtered_df_6_6 = (((Selected_Portfolio.df_L3_r.loc[dt_start_date:dt_end_date, listq_6_6] + 1).cumprod() - 1) * 100)

        figure_6_6 = px.line(
            filtered_df_6_6,
            x=filtered_df_6_6.index,
            y=[c for c in filtered_df_6_6.columns],
            labels={"x": "Date", "y": "Values"},
            template="plotly_white",
        )
        figure_6_6.update_layout(
            yaxis_title="Cumulative Return (%)",
            xaxis_title="",
            legend=dict(
                orientation="h",
                yanchor="top",  # Change this to "top" to move the legend below the chart
                y=-0.3,  # Adjust the y value to position the legend below the chart
                xanchor="center",  # Center the legend horizontally
                x=0.5,  # Center the legend horizontally
                title=None,
                font=dict(size=11)
            ),
            margin=dict(r=0),  # Reduce right margin to maximize visible area
        )

        listq_6_7 = f_AssetClassContrib(Selected_Portfolio.df_L3_contrib, "Floating Rate")
        filtered_df_6_7 = (((Selected_Portfolio.df_L3_r.loc[dt_start_date:dt_end_date, listq_6_7] + 1).cumprod() - 1) * 100)

        figure_6_7 = px.line(
            filtered_df_6_7,
            x=filtered_df_6_7.index,
            y=[c for c in filtered_df_6_7.columns],
            labels={"x": "Date", "y": "Values"},
            template="plotly_white",
        )
        figure_6_7.update_layout(
            yaxis_title="Cumulative Return (%)",
            xaxis_title="",
            legend=dict(
                orientation="h",
                yanchor="top",  # Change this to "top" to move the legend below the chart
                y=-0.3,  # Adjust the y value to position the legend below the chart
                xanchor="center",  # Center the legend horizontally
                x=0.5,  # Center the legend horizontally
                title=None,
                font=dict(size=11)
            ),
            margin=dict(r=0),  # Reduce right margin to maximize visible area
        )

        listq_6_8 = f_AssetClassContrib(Selected_Portfolio.df_L3_contrib, "Cash")
        filtered_df_6_8 = (((Selected_Portfolio.df_L3_r.loc[dt_start_date:dt_end_date, listq_6_8] + 1).cumprod() - 1) * 100)

        figure_6_8 = px.line(
            filtered_df_6_8,
            x=filtered_df_6_8.index,
            y=[c for c in filtered_df_6_8.columns],
            labels={"x": "Date", "y": "Values"},
            template="plotly_white",
        )
        figure_6_8.update_layout(
            yaxis_title="Cumulative Return (%)",
            xaxis_title="",
            legend=dict(
                orientation="h",
                yanchor="top",  # Change this to "top" to move the legend below the chart
                y=-0.3,  # Adjust the y value to position the legend below the chart
                xanchor="center",  # Center the legend horizontally
                x=0.5,  # Center the legend horizontally
                title=None,
                font=dict(size=11)
            ),
            margin=dict(r=0),  # Reduce right margin to maximize visible area
        )

        ## Populate Charts for Page 6 Component
        return [
            html.Div(style={'height': '2rem'}),
            html.H2('Sector Sleeve - Look Through Component Analysis',
                    style={'textAlign': 'center', 'color': "#3D555E"}),
            html.Hr(),
            html.Hr(style={'border-color': "#3D555E", 'width': '70%', 'margin': 'auto auto'}),
            html.Hr(),

            dbc.Row([
                # Left Gutter
                dbc.Col("", width=2, align="center", className="mb-3"),
                # Centre Work Area
                dbc.Col([
                    # Tab 5- Contribution Analysis
                    dbc.Row([
                        dbc.Col(dbc.Card([
                            dbc.CardHeader("Chart 1: Asset Sleeve Performance"),
                            dbc.CardBody(dcc.Graph(figure=figure_6_1)),
                            dbc.CardFooter("Enter some dot point automated analysis here....")
                        ], color="primary", outline=True), align="center", className="mb-3"),
                    ], align="center", className="mb-3"),
                    dbc.Row([
                        dbc.Col(dbc.Card([
                            dbc.CardHeader("Chart 2: Australian Shares Sleeve - Underlying Components"),
                            dbc.CardBody(dcc.Graph(figure=figure_6_2)),
                            dbc.CardFooter("Enter some dot point automated analysis here....")
                        ], color="primary", outline=True), align="center", className="mb-3"),
                    ], align="center", className="mb-3"),
                    dbc.Row([
                        dbc.Col(dbc.Card([
                            dbc.CardHeader(
                                "Chart 3: International Shares Sleeve - Underlying Components"),
                            dbc.CardBody(dcc.Graph(figure=figure_6_3)),
                            dbc.CardFooter("Enter some dot point automated analysis here....")
                        ], color="primary", outline=True), align="center", className="mb-3"),
                    ], align="center", className="mb-3"),
                    dbc.Row([
                        dbc.Col(dbc.Card([
                            dbc.CardHeader("Chart 4: Real Assets Sleeve - Underlying Components"),
                            dbc.CardBody(dcc.Graph(figure=figure_6_4)),
                            dbc.CardFooter("Enter some dot point automated analysis here....")
                        ], color="primary", outline=True), align="center", className="mb-3"),
                    ], align="center", className="mb-3"),
                    dbc.Row([
                        dbc.Col(dbc.Card([
                            dbc.CardHeader("Chart 5: Alternatives Sleeve - Underlying Components"),
                            dbc.CardBody(dcc.Graph(figure=figure_6_5)),
                            dbc.CardFooter("Enter some dot point automated analysis here....")
                        ], color="primary", outline=True), align="center", className="mb-3"),
                    ], align="center", className="mb-3"),
                    dbc.Row([
                        dbc.Col(dbc.Card([
                            dbc.CardHeader("Chart 6: Long Duration Sleeve - Underlying Components"),
                            dbc.CardBody(dcc.Graph(figure=figure_6_6)),
                            dbc.CardFooter("Enter some dot point automated analysis here....")
                        ], color="primary", outline=True), align="center", className="mb-3"),
                    ], align="center", className="mb-3"),
                    dbc.Row([
                        dbc.Col(dbc.Card([
                            dbc.CardHeader("Chart 7: Floating Rate Sleeve - Underlying Components"),
                            dbc.CardBody(dcc.Graph(figure=figure_6_7)),
                            dbc.CardFooter("Enter some dot point automated analysis here....")
                        ], color="primary", outline=True), align="center", className="mb-3"),
                    ], align="center", className="mb-3"),
                    dbc.Row([
                        dbc.Col(dbc.Card([
                            dbc.CardHeader("Chart 8: Cash - Underlying Components"),
                            dbc.CardBody(dcc.Graph(figure=figure_6_8)),
                            dbc.CardFooter("Enter some dot point automated analysis here....")
                        ], color="primary", outline=True), align="center", className="mb-3"),
                    ], align="center", className="mb-3"),

                    # End of Centre Work Area
                ], width=8, align="center", className="mb-3"),

                # Right Gutter
                dbc.Col("", width=2, align="center", className="mb-3"),

            ], align="center", className="mb-3")

        ]
    elif pathname == "/10-ESG":
        listq_10_1 = f_AssetClassContrib(Selected_Portfolio.df_L3_contrib, "Australian Shares")
        filtered_df_10_1 = Selected_Portfolio.df_productList.loc[listq_10_1, ["Name", "G1", "G2", "G3", "G4", "Type",
                                                                              "E-score", "S-score", "G-score",
                                                                              "ESG-score", "Controversy-score"]]

        ## Populate Charts for Page 10 ESG
        return [
            html.Div(style={'height': '2rem'}),
            html.H2('Portfolio ESG / Controversy Analysis',
                    style={'textAlign': 'center', 'color': "#3D555E"}),
            html.Hr(),
            html.Hr(style={'border-color': "#3D555E", 'width': '70%', 'margin': 'auto auto'}),
            html.Hr(),

            dbc.Row([
                # Left Gutter
                dbc.Col("", width=2, align="center", className="mb-3"),
                # Centre Work Area
                dbc.Col([
                    dbc.Table.from_dataframe(filtered_df_10_1, striped=True, bordered=True, hover=True)
                    # End of Centre Work Area
                ], width=8, align="center", className="mb-3"),

                # Right Gutter
                dbc.Col("", width=2, align="center", className="mb-3"),

            ], align="center", className="mb-3")

        ]
    elif pathname == "/11-Fees":

        ## Populate Charts for Page 11 Fees
        return [
            html.Div(style={'height': '2rem'}),
            html.H2('Portfolio Fee Analysis',
                    style={'textAlign': 'center', 'color': "#3D555E"}),
            html.Hr(),
            html.Hr(style={'border-color': "#3D555E", 'width': '70%', 'margin': 'auto auto'}),
            html.Hr(),

            dbc.Row([
                # Left Gutter
                dbc.Col("", width=2, align="center", className="mb-3"),
                # Centre Work Area
                dbc.Col([

                    # End of Centre Work Area
                ], width=8, align="center", className="mb-3"),

                # Right Gutter
                dbc.Col("", width=2, align="center", className="mb-3"),

            ], align="center", className="mb-3")

        ]
    elif pathname == "/20-Markets":

        ## Populate Charts for Page 20 Markets
        return [
            html.Div(style={'height': '2rem'}),
            html.H2('General Market Valuation Analysis',
                    style={'textAlign': 'center', 'color': "#3D555E"}),
            html.Hr(),
            html.Hr(style={'border-color': "#3D555E", 'width': '70%', 'margin': 'auto auto'}),
            html.Hr(),

            dbc.Row([
                # Left Gutter
                dbc.Col("", width=2, align="center", className="mb-3"),
                # Centre Work Area
                dbc.Col([

                    # End of Centre Work Area
                ], width=8, align="center", className="mb-3"),

                # Right Gutter
                dbc.Col("", width=2, align="center", className="mb-3"),

            ], align="center", className="mb-3")

        ]
    elif pathname == "/21-Reports":

        rp_filtered_df_1_4 = (f_CalcReturnTable(
            Selected_Portfolio.df_L3_r.loc[:, ['P_TOTAL', 'BM_G1_TOTAL', 'Peer_TOTAL', 'Obj_TOTAL']],
            Selected_Portfolio.tME_dates) * 100).T
        rp_filtered_df_1_4.columns = [Selected_Code, 'SAA Benchmark', 'Peer Manager', 'Objective']

        rp_figure_1_4 = px.bar(
            rp_filtered_df_1_4,
            x=rp_filtered_df_1_4.index,
            y=[c for c in rp_filtered_df_1_4.columns],
            labels={"x": "Date", "y": "Values"},
            template="plotly_white",
            barmode='group'
        )
        rp_figure_1_4.update_layout(
            yaxis_title="Return (%, %p.a.)",
            legend=dict(
                orientation="h",
                yanchor="top",
                y=-0.3,
                xanchor="center",
                x=0.5,
                title=None,
                font=dict(size=11)
            ),
            margin=dict(r=0),
        )

        rp_filtered_df_3_5 = Selected_Portfolio.df_L3_w.loc[dt_end_date:dt_end_date,
                          Selected_Portfolio.df_L3_w.columns.isin(Product_List)].tail(1)
        rp_filtered_df_3_5 = rp_filtered_df_3_5.loc[:, (rp_filtered_df_3_5 != 0).any()].T
        rp_filtered_df_3_5 = rp_filtered_df_3_5.rename_axis('Code')
        rp_filtered_df_3_5 = rp_filtered_df_3_5.merge(
            Selected_Portfolio.df_productList[['Name', 'G0', 'G1', 'G2', 'G3', 'G4']], on='Code')
        rp_filtered_df_3_5 = rp_filtered_df_3_5.rename(columns={dt_end_date: 'Current Weight'})

        rp_figure_3_5 = px.sunburst(
            rp_filtered_df_3_5,
            path=['G0', 'G1', 'G4', 'Name'],
            names='Name',
            values='Current Weight',
            template="plotly_white"
        )
        rp_figure_3_5.update_layout(
            title={
                "text": f"As at {dt_end_date:%d-%b-%Y}",
                "font": {"size": 11}  # Adjust the font size as needed
            },
            margin=dict(r=0, l=0),  # Reduce right margin to maximize visible area
        )

        nowDateTime = datetime.now().strftime('%Y-%m-%d--%H-%M-%S')
        #MYDIR = ('./OutputFiles/' + Selected_Code +'/'+ nowDateTime)
        MYDIR = ('C:/AtchisonAnalytics/OutputFiles/' + Selected_Code + '/' + nowDateTime)

        print(MYDIR)
        os.makedirs(MYDIR)
        print("Got here")

        # Creating the HTML file
        file_html = open(MYDIR+"/"+Selected_Code+"-Report.html", "w")
        # Adding the input data to the HTML file
        file_html.write('''<html>
        <html>
        <body style="background-color:#3D555E; color: #E7EAEB;">
        
        <h1 style="color: #1DC8F2;">
        Atchison Portfolio Analytics
        </h1>
        
               
        <H2 style="color: #E7EAEB;">Performance
        </H2>
        
        <iframe src="./figure_1_4.html"
              height="1000px" width="950px" style="border: none;">
        </iframe>
        
        <H2 style="color: #E7EAEB;">Asset Allocation
        </H2>

 
        <iframe src="./figure_3_5.html"
              height="1000px" width="950px" style="border: none;">
        </iframe>
        </body>
        </html>''')
        # Saving the data into the HTML file
        file_html.close()

        ## Populate Charts for Page 21 Reports
        return [
            html.Div(style={'height': '2rem'}),
            html.H2('Report Generator',
                    style={'textAlign': 'center', 'color': "#3D555E"}),
            html.Hr(),
            html.Hr(style={'border-color': "#3D555E", 'width': '70%', 'margin': 'auto auto'}),
            html.Hr(),

            dbc.Row([
                # Left Gutter
                dbc.Col("", width=2, align="center", className="mb-3"),
                # Centre Work Area
                dbc.Col([

                    # End of Centre Work Area
                ], width=8, align="center", className="mb-3"),

                # Right Gutter
                dbc.Col("", width=2, align="center", className="mb-3"),

            ], align="center", className="mb-3"),

            rp_figure_3_5.write_html(MYDIR+'/figure_3_5.html'),
            rp_figure_1_4.write_html(MYDIR + '/figure_1_4.html')

        ]
    elif pathname == "/30-Help":

        ## Populate Charts for Page 30 Help
        return [
            html.Div(style={'height': '2rem'}),
            html.H2('Need Help & Model Assumptions',
                    style={'textAlign': 'center', 'color': "#3D555E"}),
            html.Hr(),
            html.Hr(style={'border-color': "#3D555E", 'width': '70%', 'margin': 'auto auto'}),
            html.Hr(),

            dbc.Row([
                # Left Gutter
                dbc.Col("", width=2, align="center", className="mb-3"),
                # Centre Work Area
                dbc.Col([

                    # End of Centre Work Area
                ], width=8, align="center", className="mb-3"),

                # Right Gutter
                dbc.Col("", width=2, align="center", className="mb-3"),

            ], align="center", className="mb-3")

        ]
    # If the user tries to reach a different page, return a 404 message
    return dbc.Jumbotron(
        [
            html.Div(style={'height': '2rem'}),
            html.H2("404: Not found", className="text-danger"),
            html.Hr(),
            html.P(f"Whoops the pathname {pathname} was not recognised... - Blame Jake!"),
        ]
    )


#@@@ CALL BACKS @@@@@
#@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@

# Callback to set Selected_Portfolio and update the dcc.Store with Portfolio_Code
@app.callback(
    Output('display-portfolio-code', 'children'),
    Output('stored-portfolio-code', 'data'),
    State('stored-portfolio-code', 'data'),
    State('url', 'pathname'),
    Input('portfolio-dropdown', 'value'),
    Input('portfolio-dropdown-alt1', 'value'),
    Input('portfolio-dropdown-alt2', 'value'),
    Input('date-picker', 'start_date'),  # Add start_date input
    Input('date-picker', 'end_date'),    # Add end_date input
)
def update_selected_portfolio(stored_value, pathname, selected_value, alt1_value, alt2_value, text_Start_Date, text_End_Date):
    global Selected_Portfolio, Selected_Code, Alt1_Portfolio, Alt1_Code, Alt2_Portfolio, Alt2_Code, dt_start_date, dt_end_date  # Declare global variables

    if pathname == "/":
        if selected_value in availablePortfolios:
            if selected_value == stored_value.get('key'):
                print("No change needed")
            else:
                print("Change triggered")
            Selected_Portfolio = All_Portfolios[availablePortfolios.index(selected_value)]
            Selected_Code = Selected_Portfolio.portfolioName  # Update Selected_Code
            Alt1_Portfolio = All_Portfolios[availablePortfolios.index(alt1_value)]
            Alt1_Code = Alt1_Portfolio.portfolioName
            Alt2_Portfolio = All_Portfolios[availablePortfolios.index(alt2_value)]
            Alt2_Code = Alt2_Portfolio.portfolioName

            dt_start_date = pd.to_datetime(text_Start_Date)
            dt_end_date = pd.to_datetime(text_End_Date)
            print(dt_start_date)

            return Selected_Code, {'key': Selected_Code}
        else:
            return None, None
    else:
        return None, None

#text_Start_Date = load_start_date
#text_End_Date = load_end_date

# Run the app
if __name__ == '__main__':
    #app.run_server(debug=True)
    app.run_server(host = '0.0.0.0', port = port_number, debug=True)
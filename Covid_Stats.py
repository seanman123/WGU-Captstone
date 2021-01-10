import numpy as np
import pandas as pd
from datetime import datetime, timedelta
from matplotlib import dates as mpl_dates
import pandas as pd
import matplotlib.dates as mdates
from sklearn.metrics import r2_score
from fractions import Fraction
import plotly
import plotly.graph_objs as go
import json

# Load in the County population data frame 
pop_df = pd.read_csv('counties.csv')
pop_df.head(10)

# dataframe used for total population 
total_pop_df = pop_df.loc[pop_df['state'] == pop_df['county']] 
total_pop_df = total_pop_df['pop2019'].sum()

class Covid_Stats:
    def __init__(self, data, date, county = "", state = ""):
        self.date = date
        self.county = county
        self.state = state
        self.data = data

    # Loads up the new COVID-19 stat data
    def load_df(self):
        # Load in the covid-19 data frame 
        df = pd.read_csv(self.data)
        df = df.sort_values(by=['state', 'county', 'date'])
        df = df[['date', 'county', 'state', 'cases', 'deaths']]
        return df

    # target data is either the county selected from the cases by county page 
    # or the state from the cases by state page 
    def target_data(self):
        df = self.load_df()
        if self.county != "":
            target_df = df[(df["county"] == self.county) & (df["state"] == self.state)]
        else:
            target_df = df.groupby(['state', 'date']).sum().reset_index()
            target_df = target_df[(target_df["state"] == self.state)]

        target_df['date']= pd.to_datetime(target_df['date'])
        target_df['date'] = self.date_to_num(target_df['date'])

        return target_df

    # helps create a dataframe grouped by either country or grouped by state
    # depedning on the circumstance needed 
    def state_data(self):
        df = self.load_df()
        state_df = df
        if self.county != "":
            state_df = df[(df["state"] == self.state)]
            state_df = state_df.groupby(['county']).tail(1).reset_index()
        else:
            state_df = state_df.groupby(['state']).tail(1).reset_index()

        return state_df

    # converts a date to a number format for the polynomial regression model
    def date_to_num(self, date):
        int_date = mdates.date2num(date)
        return int_date

    # converts a number to a date for formatting of plots 
    # so users can understand the axis 
    def num_to_date(self, date):
        new_date = mdates.num2date(date)
        return new_date
        

    # Creates a polynomial model 
    # Takes in the date on the x axis and the number of counties on the y axis 
    # Variable poly_model has a polynomial fit of 2, which is the degree of the polynomial 
    # The polynomial would look similar to y = ax^2 + bx + c
    # The r-squared value tells how how well our poly+model fits with the data
    # An r-squqred closer to 1 indicates a better fit to the data 
    # After this, we make a prediction for the mdoel and return the prediction, r-quared value
    # Info found from Frank Kane's Data Science and Machine Learning with Python - Hands On! Class
    # and from W3 Schools https://www.w3schools.com/python/python_ml_polynomial_regression.asp
    def cases_model(self):

        # our target data
        target_df = self.target_data()
        
        # set up our polymodel 
        dates = np.array(target_df['date'])
        cases = np.array(target_df['cases'])
        poly_model = np.poly1d(np.polyfit(dates, cases, 2))
        
        # calculate r-squared
        r_squared_value = self.r_squared_value(cases, poly_model, dates)
        
        # make a prediction 
        prediction_date = datetime.strptime(self.date, '%Y-%m-%d')
        prediction = poly_model(self.date_to_num(prediction_date))

        return int(prediction), r_squared_value; 

    # function to calculate the r-squared value for the cases_model function 
    def r_squared_value(self, cases, poly_model, dates):
        # calculate r squared
        r_squared_error = r2_score(cases, poly_model(dates))
        return r_squared_error

    # calculates the case percentage
    # if we are comparing the county, we take the # of cases per county divided by the population of the county
    # if we are comparing the state, we take the # of cases per state divided by the total population of the state 
    def cases_percentage(self, cases):
        case_model = self.cases_model()
        cases = case_model[0]

        # county percentage 
        if self.county != "":
            population = int(pop_df.loc[(pop_df['state'] == self.state) & (pop_df['county'] == self.county)]['pop2019'])
            print(population)
            number_of_cases = int(cases)
            print(number_of_cases)

        # state compared to nation percentage
        else:
            population = total_pop_df
            number_of_cases = int(cases)
            location = "the state compared to total population of the nation"
        percentage = round((number_of_cases / population * 100),2)
        return percentage


    # calculates the case fraction by taking in the percent previously calculated
    # if the numerator is less than 0, it automatically gets set to 1 so the function doesn't return 0 
    def cases_fraction(self, percent):
        numerator = int((round(percent, 0) / 100) * 1000)
        if numerator == 0:
            numerator = 1 
            
        frac = Fraction(numerator, 1000)
        return frac

    # Creates the line graph plot on the dashboard
    def create_plot(self):
        df = self.target_data()
        df['date'] = self.num_to_date(df['date'])
        data = [go.Scatter(
            x = df['date'],
            y = df['cases'],
            mode = 'lines',
        )]

        graphJSON = json.dumps(data, cls=plotly.utils.PlotlyJSONEncoder)

        return graphJSON

    # Creates the bar graph plot on the dashboard 
    def create_bar_graph(self):
        state_df = self.state_data()
        group_state_df = state_df.groupby("county").tail(1)
        if self.county != "":
            data=[go.Bar(x=group_state_df['county'], y=group_state_df['cases'])]
        else:
            data=[go.Bar(x=state_df['state'], y=state_df['cases'])]
        
        graphJSON = json.dumps(data, cls=plotly.utils.PlotlyJSONEncoder)

        return graphJSON
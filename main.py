from flask import Flask, request, render_template
import pandas as pd
from Covid_Stats import Covid_Stats

app = Flask(__name__)

# sets up our home page and uses a get/post request to return info selected from the County form
@app.route('/', methods=['GET', 'POST'])
def index():
    cases = ''
    error = 'Something went wrong. Please try again.'
    r_squared = ''
    county = ''
    state = ''
    date = ''
    case_data = ('', '')
    percentage = ''
    fraction = ''
    bar = ''
    bar_graph = ''
    df = pd.DataFrame()
    if request.method == 'POST' and 'county' in request.form:
        try: 
            county = request.form.get('county')
            state = request.form.get('state')
            date = request.form.get('date')
            stat = Covid_Stats(date, county, state)
            case_data = stat.cases_model()
            percentage = stat.cases_percentage(case_data)
            fraction = stat.cases_fraction(percentage)
            bar = stat.create_plot()
            bar_graph = stat.create_bar_graph()
            df = stat.target_data()
            df = df[['date', 'county', 'state', 'cases']]
            df['date'] = stat.num_to_date(df['date'])
            df = df.head(12)
        except:
            return render_template('index.html', error = error)
    return render_template('index.html', 
        date = date, cases = case_data[0], 
        county = county, state = state, 
        r_squared = case_data[1], 
        percentage = percentage, 
        fraction = fraction, 
        plot = bar,
        bar_graph = bar_graph,
        tables=[df.to_html(classes='data-table')])

# sets up our cases-by-state page and uses a get/post request to return info selected from the State form
@app.route('/cases-by-state', methods=['GET', 'POST'])
def cases_by_state():
    cases = ''
    error = 'Something went wrong. Please try again.'
    r_squared = ''
    county = ''
    state = ''
    date = ''
    case_data = ('', '')
    percentage = ''
    fraction = ''
    line_graph = ''
    bar_graph = ''
    df = pd.DataFrame()
    if request.method == 'POST' and 'state' in request.form:
        try: 
            state = request.form.get('state')
            date = request.form.get('date')
            stat = Covid_Stats(date, county, state)
            case_data = stat.cases_model()
            percentage = stat.cases_percentage(case_data)
            fraction = stat.cases_fraction(percentage)
            line_graph = stat.create_plot()
            bar_graph = stat.create_bar_graph()
            df = stat.target_data()
            df = df[['date', 'state', 'cases']]
            df['date'] = stat.num_to_date(df['date'])
            df = df.head(12)
        except:
            return render_template('cases-by-state.html', error = error)
    return render_template('cases-by-state.html', 
        date = date, 
        state = state,
        cases = case_data[0],
        r_squared = case_data[1],
        percentage = percentage, 
        fraction = fraction,
        line_graph = line_graph,
        bar_graph = bar_graph,
        tables=[df.to_html(classes='data-table')])
        
if __name__ == "__main__":
    app.run(debug=True)
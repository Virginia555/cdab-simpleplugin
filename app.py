from flask import Flask, render_template, request, redirect, url_for
from functions import run_tests
import re


app = Flask(__name__)

#Home page of the webapp
@app.route('/')
def index():
    return render_template('index.html')

#Request when the form is submitted
@app.route('/run_tests', methods=['POST'])
def run_tests_route():

    #Retrieve the data from the request
    container_name = request.form['container_name'].strip()
    delete_after_execution = 'delete_container' in request.form
    tests = request.form.getlist('tests')
    providers = request.form.getlist('providers')

    validDockerName = re.compile(r'^[a-zA-Z0-9][a-zA-Z0-9_.-]*$') #Regex for valid Docker container name

    #Backend check on the provided data
    if not tests or not providers or len(container_name)<2 or not validDockerName.match(container_name):
        return redirect(url_for('error', type='form'))

    #Run the tests (imported function from functions.py)
    results = run_tests(container_name=container_name, tests=tests, providers=providers, remove_container=delete_after_execution) 
    
    if results is False: #Result is set to false when there is something wrong with Docker
        return redirect(url_for('error', type='docker'))

    #If we got to the results, render the template with the results
    return render_template('results.html', results=results)

#Request for the error page
@app.route('/error', defaults={'type': None}) #Also possible to not specify the type of error, the template will then provide a generic message
@app.route('/error/<type>')
def error(type):
    return render_template('error.html', type=type)

#WORK IN PROGRESS
@app.route('/metrics_form', methods=['GET', 'POST'])
def metrics_form():
    # Logica per la pagina di inserimento metriche...
    return render_template('metrics_form.html')
#@app.route('/metrics_form', methods=['GET', 'POST'])
#def metrics_form():
    #if request.method == 'POST':
        #location = request.form['location']
        #company = request.form['company']
        #avg_response_time = request.form['avgResponseTime']
        #peak_response_time = request.form['peakResponseTime']
        #error_rate = request.form['errorRate']
        #avg_concurrency = request.form['avgConcurrency']
        #peak_concurrency = request.form['peakConcurrency']

        # Fai qualcosa con i dati, ad esempio salvali nel database o elaborali

        # Dopo aver elaborato i dati, reindirizza alla pagina dei risultati
        #return redirect(url_for('index')) 
    #return render_template('metrics_form.html')
    #return render_template('metrics_form.html')

#FOR DEVELOPMENT REASONS, CAN BE REMOVED BEFORE DEPLOYMENT
@app.route('/results', methods=['GET', 'POST'])
def results():
    return render_template('results.html')


if __name__ == '__main__':
    app.run(debug=False)#Set to false before deployment

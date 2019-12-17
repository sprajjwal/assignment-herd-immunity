from flask import Flask, render_template, redirect, url_for, request
from visualizer import Visualizer
from simulation import Simulation


app = Flask(__name__)
graph = Visualizer("Number of Survivors",
                   ("Herd Immunity Defense Against Disease " +
                    "Spread"))


@app.route("/", methods=['GET', 'POST'])
def simulation_params():
    '''User sees a form to input the parameters of the simulation.'''
    if request.method == 'GET':
        # render the form to input data
        return render_template("index.html")
    if request.method == 'POST':
        # run the simulation

        # redirect to the template for results
        pass


@app.route("/simulation", methods=['GET'])
def show_results():
    '''Show the steps of the simulation.'''
    pass


if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=os.environ.get('PORT', 5000))

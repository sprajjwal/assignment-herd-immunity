from flask import Flask, render_template, redirect, url_for, request
from visualizer import Visualizer
from simulation import Simulation
from virus import Virus

app = Flask(__name__)
graph = Visualizer("Number of Survivors", (
                    "Herd Immunity Defense Against Disease " +
                    "Spread"))


@app.route("/", methods=['GET', 'POST'])
def simulation_params():
    '''User sees a form to input the parameters of the simulation.'''
    if request.method == 'GET':
        # render the form to input data
        return render_template("index.html")
    if request.method == 'POST':
        # use data from user
        pop_size = int(request.form.get("pop_size"))
        vacc_percentage = float(request.form.get("vacc_percentage"))
        virus_name = request.form.get("virus_name")
        mort_rate = float(request.form.get("mortality_rate"))
        repro_rate = float(request.form.get("repro_rate"))
        virus = Virus(virus_name, repro_rate, mort_rate)
        initial_infected = int(request.form.get("initial_infected"))
        sim = Simulation(pop_size, vacc_percentage,  virus, initial_infected)
        # run the simulation
        results = sim.run_and_collect(graph)
        # redirect to the template for results
        return redirect(url_for('show_results'), results=results)

@app.route("/simulation/<results>", methods=['GET'])
def show_results(results):
    '''Show the steps of the simulation.'''
    pass


@app.route("/about", methods=['GET'])
def learn_more():
    '''Resources to learn more about why the project exists.'''
    return render_template("info.html")


if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=os.environ.get('PORT', 5000))

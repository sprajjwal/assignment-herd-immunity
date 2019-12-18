from flask import (
    Flask,
    render_template,
    redirect,
    url_for,
    request,
    Response,
    send_file)
from visualizer import Visualizer
from simulation import Simulation
from virus import Virus
import io
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
from matplotlib.figure import Figure
import random

app = Flask(__name__)
sim = None  # later initialized as a Simulation
graph = Visualizer("Number of Survivors", (
                    "Herd Immunity Defense Against Disease " +
                    "Spread"))


@app.route("/", methods=['GET'])
def simulation_params():
    '''User sees a form to input the parameters of the simulation.'''
    if request.method == 'GET':
        # render the form to input data
        return render_template("index.html")


def create_graph(simulation):
    """Construct png images from the list returned by running the
       simulation. Uses the Visualizer object ran by the Simulation object.

       Parameters:
       simulation(Simulation): initialized using form values

       Returns:
       Response: imported from flask library

    """
    # inspired by
    # https://stackoverflow.com/questions/50728328/python-how-to-show-matplotlib-in-flask
    fig = Figure()
    axis = fig.add_subplot(1, 1, 1)
    xs = range(100)
    ys = [random.randint(1, 50) for x in xs]
    axis.plot(xs, ys)
    return fig


@app.route('/calculations', methods=['POST'])
def construct_simulation():
    # make a graph to be shown on the next use case
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
        # results = sim.run_and_collect(graph)
        # redirect to the template for results, giving user the download
        return redirect(url_for('show_results'))


@app.route("/figure")
def make_graphs():
    '''Produce the figure shown in the template.'''
    # show the image in the results template
    fig = create_graph(sim)
    output = io.BytesIO()
    FigureCanvas(fig).print_png(output)
    response = Response(output.getvalue(), mimetype='image/png')
    return response


@app.route("/simulation", methods=['GET'])
def show_results():
    '''Show the steps of the simulation. Present png image to user.'''
    return render_template("results.html")


@app.route("/about", methods=['GET'])
def learn_more():
    '''Resources to learn more about why the project exists.'''
    return render_template("info.html")


if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=os.environ.get('PORT', 5000))

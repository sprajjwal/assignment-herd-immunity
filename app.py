from flask import (
    Flask,
    render_template,
    redirect,
    url_for,
    request,
    Response,
    send_file)
from visualizer import WebVisualizer
from simulation import Simulation
from virus import Virus
import io
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
from matplotlib.figure import Figure
from matplotlib.pyplot import figure
import matplotlib.pyplot as plt
import random
from pymongo import MongoClient
from bson.objectid import ObjectId
import os

app = Flask(__name__)
list_of_sim = list()
list_of_graphs = list()
client = MongoClient()
db = client.Herd
simulations = db.simulations

PEOPLE_FOLDER = os.path.dirname(os.path.realpath(__file__))
app.config['UPLOAD_FOLDER'] = PEOPLE_FOLDER


@app.route("/", methods=['GET'])
def simulation_params():
    '''User sees a form to input the parameters of the simulation.'''
    if request.method == 'GET':
        # render the form to input data
        return render_template("index.html")


def create_graphs(simulation):
    """Construct png images and text from the list returned by running the
       simulation. Uses the Visualizer object ran by the Simulation object.

       Parameters:
       simulation(Simulation): initialized using form values

       Returns:
       Response: imported from flask library

    """
    # run the simulation, get a list of bar graphs
    graph = WebVisualizer("Number of Survivors", (
                        "Herd Immunity Defense Against Disease " +
                        "Spread"))
    graphs = simulation.run_and_collect(graph)
    return graphs
    '''
    # inspired by
    # https://stackoverflow.com/questions/50728328/python-how-to-show-matplotlib-in-flask
    fig = Figure()
    axis = fig.add_subplot(1, 1, 1)
    xs = range(100)
    ys = [random.randint(1, 50) for x in xs]
    axis.plot(xs, ys)
    return fig
    '''


@app.route('/calculations', methods=['GET', 'POST'])
def construct_simulation():
    # POST: set up the Simulation
    if request.method == 'POST':
        # use data from user
        pop_size = int(request.form.get("pop_size"))
        vacc_percentage = float(request.form.get("vacc_percentage"))
        virus_name = request.form.get("virus_name")
        mort_rate = float(request.form.get("mortality_rate"))
        repro_rate = float(request.form.get("repro_rate"))
        virus = Virus(virus_name, repro_rate, mort_rate)
        initial_infected = int(request.form.get("initial_infected"))
        simulator = Simulation(pop_size, vacc_percentage,  virus,
                               initial_infected)
        list_of_sim.append(simulator)
        # list_of_sim = []
        # list_of_sim.append(simulator)
        # simulation = {'simulator': list_of_sim}
        # insert into db
        # sim_id = simulations.insert_one(simulation).inserted_id
        print(f'Simulation: {simulator}')
        # run the simulation
        # results = sim.run_and_collect(graph)
        # redirect to the template for results, giving user the download
        return redirect(url_for('show_results',
                                sim_id=list_of_sim.index(simulator)))


"""
@app.route("/figure")
def make_graphs():
    '''Produce the figure shown in the template.'''
    # show the image in the results template
    figures = create_graph(sim)
    output = io.BytesIO()
    FigureCanvas(fig).print_png(output)
    response = Response(output.getvalue(), mimetype='image/png')
    return response
"""


@app.route("/simulation/<sim_id>")
def show_results(sim_id):
    '''Show the steps of the simulation. Present png image to user.'''
    # GET: show the image in the results template
    sim = list_of_sim.pop(int(sim_id))
    graphs = create_graphs(sim)
    list_of_graphs.append(graphs)
    full_filename = os.path.join(app.config['UPLOAD_FOLDER'], graphs[1][1])
    return render_template("results.html", file=full_filename)
    '''
    results = list()  # stores Response object for each graph
    for tuple in graphs:
        if len(tuple) > 1:  # the tuple contains more than a report (str)
            figure = tuple[1]
            output = io.BytesIO()
            FigureCanvas(fig).print_png(output)
            png_graph = Response(output.getvalue(), mimetype='image/png')
            results.append(png_graph)
    return render_template("results.html", results=results)
    '''


@app.route('/image')
def process_image():
    '''Make the graphs accessible from the browser.'''
    '''
    graphs = list_of_graphs[0]
    # create a full graph
    graph1 = graphs[1][1]
    fig = plt.figure(figsize=(4.5, 2.5))
    fig = plt.bar(graph1.y_pos, graph1.num_alive, align='center', alpha=0.5)
    fig = plt.xticks(graph1.y_pos, graph1.populations)
    fig = plt.ylabel(graph1.y_label)
    fig = plt.xlabel(graph1.x_label)
    fig = plt.title(graph1.title)
    # make graph visible in template
    # fig = plt.savefig("matplot.png")
    output = io.BytesIO()
    FigureCanvas(fig).print_png(output)
    png_graph = Response(output.getvalue(), mimetype='image/png')
    return png_graph
    '''
    '''
    fig = Figure()
    axis = fig.add_subplot(1, 1, 1)
    xs = range(100)
    ys = [random.randint(1, 50) for x in xs]
    axis.plot(xs, ys)
    output = io.BytesIO()
    FigureCanvas(fig).print_png(output)
    png_graph = Response(output.getvalue(), mimetype='image/png')
    return png_graph
    '''


@app.route("/about", methods=['GET'])
def learn_more():
    '''Resources to learn more about why the project exists.'''
    return render_template("info.html")


if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=os.environ.get('PORT', 5000))

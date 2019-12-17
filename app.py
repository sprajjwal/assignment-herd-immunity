from flask import Flask, render_template, redirect, url_for
from visualizer import Visualizer
from simulation import Simulation


app = Flask(__name__)
graph = visualizer.Visualizer("Number of Survivors",
                              ("Herd Immunity Defense Against Disease " +
                               "Spread"))


if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=os.environ.get('PORT', 5000))

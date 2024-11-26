from flask import Flask, render_template
from prometheus_flask_exporter.multiprocess import GunicornInternalPrometheusMetrics

app = Flask(__name__)

metrics = GunicornInternalPrometheusMetrics(app)
metrics.info("frontend_app", "Application info", version="1.0")


@app.route("/")
def homepage():
    return render_template("main.html")


if __name__ == "__main__":
    app.run()

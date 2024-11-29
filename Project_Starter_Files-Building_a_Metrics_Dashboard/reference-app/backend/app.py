from os import getenv
from jaeger_client import Config
from flask import Flask, request, jsonify
from prometheus_flask_exporter import PrometheusMetrics
from flask_opentracing import FlaskTracing
from flask_pymongo import PyMongo

app = Flask(__name__)

app.config["MONGO_DBNAME"] = "example-mongodb"
app.config[
    "MONGO_URI"
] = "mongodb://example-mongodb-svc.default.svc.cluster.local:27017/example-mongodb"

mongo = PyMongo(app)
metrics = PrometheusMetrics(app)
metrics.info("backend_app", "Application info", version="1.0")

JAEGER_HOST = getenv("JAEGER_HOST")


def init_tracer(service):
    config = Config(
        config={
            "sampler": {"type": "const", "param": 1},
            "logging": True,
            "reporter_batch_size": 1,
            "local_agent": {"reporting_host": JAEGER_HOST},
        },
        service_name=service,
    )
    return config.initialize_tracer()


tracer = init_tracer("backend")
FlaskTracing(tracer, True, app)


@app.route("/")
def homepage():
    with tracer.start_span('homepage') as span:
        span.set_tag("route", "/")
        return "Hello World"


@app.route("/api")
def my_api():
    with tracer.start_span('api') as span:
        span.set_tag("route", "/api")

        answer = "something"
        return jsonify(repsonse=answer)


@app.route("/star", methods=["POST"])
def add_star():
    with tracer.start_span('add_star') as span:
        span.set_tag("route", "/star")
        star = mongo.db.stars
        name = request.json["name"]
        distance = request.json["distance"]
        star_id = star.insert({"name": name, "distance": distance})
        new_star = star.find_one({"_id": star_id})
        output = {"name": new_star["name"], "distance": new_star["distance"]}
        return jsonify({"result": output})


if __name__ == "__main__":
    app.run()

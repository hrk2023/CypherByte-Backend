from flask import Flask, Blueprint,jsonify
from flask_cors import CORS
from os import environ
from . import config
from flask_pymongo import PyMongo
from .routes import adminRoutes, applicationRoutes


def create_app():
    app = Flask(__name__)
    cors = CORS(app, origins='*')
    app.config.from_object(environ.get("CONFIG_FROM",config.Devlopment()))
    cluster = PyMongo(app)


    app.register_blueprint(adminRoutes.admin)
    app.register_blueprint(applicationRoutes.bp)

    @app.route("/",methods = ["GET"])
    def status():
        return jsonify({"status" : "app is running"})

    return app


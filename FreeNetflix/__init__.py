from flask import Flask, Blueprint
from .routes import userRoutes, adminRoutes, applicationRoutes
app = Flask(__name__)

app.config["SECRET_KEY"] = "dAmNSimPLeSecREtKeY"
app.register_blueprint(userRoutes.bp)
app.register_blueprint(adminRoutes.admin)
app.register_blueprint(applicationRoutes.bp)
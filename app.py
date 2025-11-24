from flask import Flask
from flask_cors import CORS
from endpoints.routes.seguro_bp import seguro_bp
from endpoints.routes.auto_bp import auto_bp
from endpoints.routes.empleado_bp import empleado_bp
from endpoints.routes.client_bp import client_bp
from endpoints.routes.reportes_bp import reportes_bp
from endpoints.routes.rentals_bp import rentals_bp
from endpoints.routes.mantenimiento_bp import mantenimiento_bp
from endpoints.routes.sanciones_bp import sanciones_bp
from endpoints.routes.daños_bp import daño_bp


def main():
    app = Flask(__name__)
    CORS(app)

    app.register_blueprint(client_bp)
    app.register_blueprint(empleado_bp)
    app.register_blueprint(auto_bp)
    app.register_blueprint(reportes_bp)
    app.register_blueprint(rentals_bp)
    app.register_blueprint(seguro_bp)
    app.register_blueprint(mantenimiento_bp)
    app.register_blueprint(sanciones_bp)
    app.register_blueprint(daño_bp)

    @app.route("/")
    def hello_world():
        return "<h1>Hello, World!</h1>"

    @app.route("/about")
    def about_page():
        return "<h2>This is the About Page.</h2>"

    app.run(debug=True, port=3000)


if __name__ == "__main__":
    main()

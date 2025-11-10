from flask import Flask
from endpoints.routes.empleado_bp import empleado_bp
from endpoints.routes.client_bp import client_bp

def main():

  app = Flask(__name__)
  
  app.register_blueprint(client_bp)
  app.register_blueprint(empleado_bp)
  
  @app.route("/")
  def hello_world():
      return "<h1>Hello, World!</h1>"
  
  
  @app.route("/about")
  def about_page():
      return "<h2>This is the About Page.</h2>"
      
  app.run(debug=True)

if __name__ == "__main__":
  main()
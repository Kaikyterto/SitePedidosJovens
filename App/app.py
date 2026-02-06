from flask import Flask
from controllers.routes import cliente

app = Flask(__name__)

app.register_blueprint(cliente)

if __name__ == "__main__":
    app.run(debug=True)

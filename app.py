from flask import Flask

from routes import register_routes

app = Flask(__name__, template_folder="templates", static_folder="static", static_url_path="/")

register_routes(app)

if __name__ == "__main__":
    app.run(debug=True)
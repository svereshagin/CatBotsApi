from flask import Flask
from catbotsapi.routers.cats import cats_bp
from catbotsapi.repository.database import cat_colors_create_data, fullfill_cat_options
from catbotsapi.extensions import limiter


app_name = "Cats Service"
app = Flask(__name__)

# Инициализация limiter
limiter.init_app(app)
app.register_blueprint(cats_bp)

@app.route("/ping", methods=["GET"])
def ping():
    return f"{app_name}. Version 0.1", 200

if __name__ == "__main__":
    cat_colors_create_data()
    fullfill_cat_options()
    app.run(host="0.0.0.0", port=8080, debug=True)

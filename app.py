from flask_api import FlaskAPI
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

app = FlaskAPI(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:////tmp/payroll.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app=app)
migrate = Migrate(app=app, db=db)

@app.route('/health', methods=['GET'])
def health():
    return {}


if __name__ == "__main__":
    app.run()

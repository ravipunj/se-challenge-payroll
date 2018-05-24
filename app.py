from flask_api import FlaskAPI

app = FlaskAPI(__name__)


@app.route('/health', methods=['GET'])
def health():
    return {}


if __name__ == "__main__":
    app.run()

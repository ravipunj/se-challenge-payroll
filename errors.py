from flask import jsonify
from app import app


class BaseClientError(Exception):
    error_code = 400

    def __init__(self, message, error_code=None):
        self.message = message
        if error_code is not None:
            self.error_code = error_code

    def to_dict(self):
        return {"message": self.message}


class CSVParsingError(BaseClientError):
    pass


class ReportAlreadyExistsError(BaseClientError):
    pass


@app.errorhandler(BaseClientError)
def handle_base_client_error(error):
    response = jsonify(error.to_dict())
    response.status_code = error.error_code
    return response

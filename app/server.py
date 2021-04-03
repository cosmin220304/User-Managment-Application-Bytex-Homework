"""
    The Python server entry point.
"""

from flask import Flask

from database_management import init_database_connection
from src.endpoints.user import user_bp
from src.endpoints.login import login_bp


def configure_app(app):
    init_database_connection(app)


app = Flask(__name__)
configure_app(app)
app.register_blueprint(user_bp)
app.register_blueprint(login_bp)


@app.route('/status', methods=['GET'])
def get_status():
    return 'The server is up and running!'


def main():
    """
       User Managment Application - Server main
    """
    app.run(debug=True)


if __name__ == '__main__':
    main()

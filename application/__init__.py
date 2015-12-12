from flask import Flask

app = Flask(__name__)
from application import routes

# Set up logging if application has not been started in debug mode
if not app.debug:
    import logging
    import sys

    # Create log format
    formatter = logging.Formatter('%(asctime)s [%(levelname)s] %(message)s','%Y-%m-%d %H:%M:%S')

    # Create console handler
    console = logging.StreamHandler(sys.stdout)
    console.setLevel(logging.INFO)
    console.setFormatter(formatter)

    # Enable log handlers
    app.logger.addHandler(console)

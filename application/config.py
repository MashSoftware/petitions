import os

DEBUG = os.getenv('DEBUG', True)
HOST = os.getenv('HOST', '0.0.0.0')
PORT = os.getenv('PORT', 5000)
TWFY_API_KEY = os.getenv('TWFY_API_KEY')
GA_KEY = os.getenv('GA_KEY')

from flask import Flask
# predeifned variable that set a reference (module name - "app")

app = Flask(__name__)

# workaround for cyclic import
from app import routes


##
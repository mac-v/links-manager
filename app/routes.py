from app import app
# decorator - modifies function that follows it
@app.route('/')
@app.route('/index')
def index():
    return "Hello world"




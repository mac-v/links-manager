from app import app, db
from sqlalchemy import text
# decorator - modifies function that follows it
@app.route('/')
@app.route('/index')
def index():
    return "Hello world"
@app.route('/users')
def get_users():
    result = db.session.execute(text("SELECT * FROM auth.users"))
    users = []
    for row in result:
        users.append(dict(row._mapping))
    return {"users": users}


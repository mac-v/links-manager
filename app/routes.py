from app import app

from app.models import Link, User

# decorator - modifies function that follows it

@app.route('/')
@app.route('/index')
def index():
    return "Hello world"
@app.route('/users')
def get_users():
    users = User.query.all()
    return {"users": [user.to_dict() for user in users]}


@app.route("/links")
def get_user_links():
    #implement grabing links with loggedin user
    user_id = '8034c76f-a60f-410d-a864-bd33ab5b284f'
    links = Link.query.filter_by(user_id=user_id).all()

    return [links.to_dict() for links in links]

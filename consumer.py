from flask import session, redirect, url_for, request, flash, Blueprint
from flask import render_template
from db_file import get_from_db, add_to_db, auth_user

bp = Blueprint("user", __name__)
global user_list
global active_user


@bp.before_app_first_request
# @bp.before_request
def set_user_list():
    global user_list
    global active_user
    active_user = []
    user_list = get_from_db("first_name")
    print(user_list)


@bp.route('/')
def index():
    if 'username' in session:
        return render_template('home.html', loginas=session['username'])
    return redirect(url_for('user.login'))


@bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if len(username) == 0 or len(password) == 0:
            flash("username or password is empty")
            return redirect(request.url)
        if auth_user(username, password):
            session['username'] = request.form['username']
            active_user.append(session['username'])
            return redirect(url_for('user.index'))
        else:
            flash("incorrect username or password ")
            return redirect(request.url)
    return render_template('index.html', name="!", user_list=user_list, userCount=len(user_list),
                           active_user=active_user, activeUserCount=len(active_user))


@bp.route('/logout')
def logout():
    # remove the username from the session if it's there
    active_user.remove(session['username'])
    session.pop('username', None)
    return redirect(url_for('user.index'))


@bp.route('/register', methods=['GET'])
def register():
    return render_template('register.html')


@bp.route('/add', methods=['POST'])
def add():
    user = []
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        add_to_db(username, password)
        if len(username) == 0 or len(password) == 0:
            flash("username or password is empty")
            return redirect(url_for('user.register'))
        if len(password) > 8:
            flash("password should not greater then 8")
            return redirect(url_for('user.register'))
        user.append(username)
        user.append(password)
        user_list.append(user)
        tmp = ""
        get_from_db()
        print(tmp)
        return redirect(url_for('user.login'))
    else:
        return render_template('register.html')


@bp.route('/user/list', methods=['GET'])
def listing():
    print(user_list)
    return active_user

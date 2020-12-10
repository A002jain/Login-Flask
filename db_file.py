from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    active = db.Column('is_active', db.Boolean(), nullable=False, server_default='1')

    # User authentication information. The collation='NOCASE' is required
    # to search case insensitively when USER_IFIND_MODE is 'nocase_collation'.
    email = db.Column(db.String(100, collation='NOCASE'), nullable=False, unique=True)
    password = db.Column(db.String(255), nullable=False, server_default='')

    # User information
    first_name = db.Column(db.String(100, collation='NOCASE'), nullable=False, server_default='')
    last_name = db.Column(db.String(100, collation='NOCASE'), nullable=False, server_default='')


def add_to_db(username, password):
    user_in_db = User(email=username+"@gmail.com", password=password, first_name=username)
    db.session.add(user_in_db)
    db.session.commit()


def get_from_db(filtering=None):
    if filtering is None:
        db_db = db.session.execute("select * from users")
    else:
        db_db = db.session.execute("select " + filtering + " from users")
    return db_db.fetchall()


def auth_user(user_name, password):
    db_db = db.session.execute("select * from users where first_name='"+user_name+"' and password='"+password+"'")
    if len(db_db.fetchall()) > 0:
        return True
    return False

from login import app
from login.db import db
from login.pwd import bcrypt


if __name__ == '__main__':
    db.init_app(app)
    bcrypt.init_app(app)
    app.run(debug=True)

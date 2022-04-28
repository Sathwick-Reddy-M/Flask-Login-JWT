from flask import request, render_template, make_response, jsonify
from flask_restful import Resource
from flask_jwt_extended import create_access_token, set_access_cookies, unset_jwt_cookies, get_jwt_identity, jwt_required, get_jwt, unset_access_cookies, verify_jwt_in_request

from login.forms import LoginForm, SignUpForm
from login.db import db
from login.models import User

from login.blocklist import BLOCKED


class Home(Resource):
    @jwt_required(optional=True)
    def get(self):
        return make_response(render_template('home.html', is_login=(get_jwt_identity() is not None)))


class Protected(Resource):
    @jwt_required(fresh=True)
    def get(self):
        return make_response(render_template('secret.html', is_login=(get_jwt_identity() is not None)))


class LessProtected(Resource):
    @jwt_required()
    def get(self):
        return make_response(render_template('less_secret.html', is_login=(get_jwt_identity() is not None)))


class Login(Resource):
    @jwt_required(optional=True)
    def get(self):
        if get_jwt_identity() is not None:
            return make_response(render_template('error.html', error='You are already logged in!!!'))
        return make_response(render_template('login.html', form=LoginForm(), is_login=(get_jwt_identity() is not None)))

    def post(self):
        form = LoginForm()

        if form.validate_on_submit():
            username = request.form.get('username')
            pwd = request.form.get('pwd')

            user = User.query.filter((User.user_name == username) &
                                     (User.user_pwd == pwd)).first()
            if user:
                access_token = create_access_token(
                    identity=str(user.user_id), fresh=True)
                response = make_response(
                    render_template('home.html', is_login=True))
                set_access_cookies(response, access_token)
                return response
            return make_response(render_template('error.html', error='Invalid User Credentials'))

        return make_response(render_template('error.html', error='Form Validation Error'))


class SignUp(Resource):
    @jwt_required(optional=True)
    def get(self):
        if get_jwt_identity() is not None:
            return make_response(render_template('error.html', error='You are logged in!!! Please logout to SignUp'))
        return make_response(render_template('signup.html', form=SignUpForm(), is_login=(get_jwt_identity() is not None)))

    def post(self):
        form = SignUpForm()

        if form.validate_on_submit():
            username = request.form.get('username')
            pwd = request.form.get('pwd')

            user = User.query.filter((User.user_name == username) &
                                     (User.user_pwd == pwd)).first()

            if not user:
                db.session.add(User(user_name=username, user_pwd=pwd))
                db.session.commit()
                return make_response(render_template('error.html', error='SignUp Success'))

            return make_response(render_template('error.html', error='Username taken'))

        return make_response(render_template('error.html', error='Form Validation Error'))


class LogOut(Resource):
    @jwt_required(optional=True)
    def get(self):
        response = make_response(render_template('home.html', is_login=False))
        if get_jwt():
            BLOCKED.add(get_jwt()['jti'])
        unset_jwt_cookies(response)
        return response

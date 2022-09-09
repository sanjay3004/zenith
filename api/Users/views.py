import datetime
import json
import os
import re
from random import randint

from werkzeug.utils import redirect

import config
from api.Users.models import Users, Verification, Device, UserDevice, Membership, Roles, Actions, RoleActions
from api.exceptions.exceptions import Exception, Error
from common.blueprint import Blueprint
from common.connection import add_item, update_item
from common.response import success, failure
from common.utils.validator import validate_name, validate_password
from app import db, bcrypt
from common.utils.validator import validate_email, validate_mobile_number
from middleware import auth
from middleware.auth import get_jwt, validate_token, token_required
from flask import request, g, url_for, session
# from flasgger import swag_from
# from application import oauth

users_api = Blueprint('user', __name__, url_postfix='user')
verification_api = Blueprint('verification', __name__, url_postfix='verification')


# user registeration/signup
@verification_api.route('/signup', methods=['POST'])
def singup_verification_request():
    return registration()


def registration():
    try:
        data = request.get_json()
        verification_detail = data.get('verification_detail', None)
        new_email = verification_detail.get('email', None)
        new_phone = verification_detail.get('phone', None)
        name = verification_detail.get('name', None)
        password = verification_detail.get('password', None)
        dob = verification_detail.get('dob', None)
        if new_email:
            is_user = Users.query.filter_by(email=new_email,deleted_at=None).first()
            print(is_user,"==========")
            if is_user:
                return success('SUCCESS',meta={'message':'This email is already registered!'})
            # create user
            else:
                password = bcrypt.generate_password_hash(password).decode('utf-8')
                new_user = Users(email=new_email,
                                 first_name=name,password=password,date_of_birth=dob)
                add_item(new_user)
                return success('SUCCESS',meta={'message':'User created'})

    except Exception as e:
        return failure("Something went wrong.")


# user login
@verification_api.route('/login', methods=['POST'])
def login():
    return user_login()


def user_login():
    try:
        data = request.get_json()
        verification_detail = data.get('verification_detail', None)
        email = verification_detail.get('email', None)
        password = verification_detail.get('password', None)
        if email and password:
            existing_user = Users.query.filter_by(email=email,deleted_at=None).first()
            if existing_user:
                membership = verify_password(existing_user.id,password, existing_user.password, True)
                if membership:
                    return success('SUCCESS',membership,meta={'message':'Login successful'})
                else:
                    return success('SUCCESS', meta={'message': 'Invalid email/password'})
            # create user
            else:
                return success('SUCCESS',meta={'message':'User not found'})

    except Exception as e:
        return failure("Something went wrong.")


def verify_password(user, password,enc_password, password_required=True):
    if password_required and bcrypt.check_password_hash(str(enc_password), password):
        token = get_jwt(user, 'general')
        token['user_info'] = get_user_profile_details(user)
        return token
    else:
        return None


def get_user_profile_details(user_id):
    user = Users.query.filter_by(id=user_id, deleted_at=None).first()
    user_data = {}
    if user:
        user_data['id'] = user.id
        user_data['name'] = user.first_name
        user_data['email_id'] = user.email
        user_data['dob'] = user.date_of_birth
        return user_data

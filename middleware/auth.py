import datetime
import json
from functools import wraps

import jwt
from flask import request, jsonify, g

import config
# from api.Users.models import Membership, Roles, Actions, RoleActions
from common import strings
from common.blueprint import Blueprint
from common.response import success, failure
from common.utils.time_utils import get_auth_exp

auth_api_v1 = Blueprint('auth', __name__, url_postfix='auth')


class AuthMiddleware(object):

    def __init__(self, app):
        self.app = app
        # sample_jwt()

    def __call__(self, environ, start_response):
        path = str(environ['PATH_INFO'])
        token = environ.get('HTTP_AUTHORIZATION', None)

        if not config.ENABLE_AUTH:
            print("authentication skipped")
            return self.app(environ, start_response)

        if path.__contains__('/signup') or path.__contains__('/signin') or path.__contains__('/get-token'):
            print("authentication skipped")
            return self.app(environ, start_response)

        if not token:
            return self.token_missing(environ, start_response)

        token_validation = self.authenticated(token)

        print(token_validation)

        if not token_validation[0]:
            return self.token_expired(environ, start_response)

        if token_validation[1]:
            return self.app(environ, start_response)
        else:
            return self.token_missing(environ, start_response)

    @staticmethod
    def authenticated(token):
        try:

            payload = jwt.decode(token, config.SECRET_KEY, algorithms=[config.JWT_ALGORITHM])

            # todo replace with get users by id and email
            is_authorised = check_valid_user(payload)
            print("IS_AUTHORISED", is_authorised)
            return True, is_authorised
        except Exception as err:
            print(err)
            return False, None

    @staticmethod
    def token_missing(environ, start_response):
        start_response('401 Unauthorized', [('Content-Type', 'text/html')])
        return [b'Unauthorized']

    @staticmethod
    def token_expired(environ, start_response):
        start_response('419 Authentication Timeout', [('Content-Type', 'text/html')])
        return [b'Authentication Timeout']


def get_jwt(user_id, membership_type, session_code=None):
    try:
        user_id = str(user_id)
        access_token_data = {'identity': str(user_id), 'membership_type': membership_type, 'iat': datetime.datetime.utcnow(),
                             "exp": get_auth_exp(config.JWT_ACCESS_TOKEN_TIME_OUT_IN_MINUTES)}
        if session_code:
            access_token_data['session_code'] = session_code
        access_token = jwt.encode(access_token_data, config.SECRET_KEY, config.JWT_ALGORITHM)
        token = {"access_token": access_token.decode("utf-8")}

        if session_code:
            refresh_token_data = {'identity': user_id, 'membership_type': membership_type,
                                  'iat': datetime.datetime.utcnow(),
                                  "exp": get_auth_exp(config.JWT_REFRESH_TOKEN_TIME_OUT_IN_MINUTES),
                                  'session_code': session_code}

            refresh_token = jwt.encode(refresh_token_data, config.SECRET_KEY, config.JWT_ALGORITHM)
            token['refresh_token'] = refresh_token.decode('utf-8')
        return token
    except Exception as err:
        print("get_jwt EXCEPTION ===> ", str(err))
        return None


# def get_jwt_session(session_code, user_id, api_key):
#     try:
#         print('HI get jwt=========>', user_id)
#         access_token_data = {'identity': user_id, "session_code": session_code, 'api_key': api_key,
#                              'iat': datetime.datetime.utcnow(),
#                              "exp": get_auth_exp(config.JWT_ACCESS_TOKEN_TIME_OUT_IN_MINUTES)}
#         print('payload', access_token_data)
#         refresh_token_data = {'identity': user_id, "session_code": session_code, 'api_key': api_key,
#                               'iat': datetime.datetime.utcnow(),
#                               "exp": get_auth_exp(config.JWT_REFRESH_TOKEN_TIME_OUT_IN_MINUTES)}
#         print('payload', refresh_token_data)
#
#         access_token = jwt.encode(access_token_data, config.SECRET_KEY, config.JWT_ALGORITHM)
#         refresh_token = jwt.encode(refresh_token_data, config.SECRET_KEY, config.JWT_ALGORITHM)
#         token = {"access_token": access_token.decode("utf-8"),
#                  "refresh_token": refresh_token.decode('utf-8')}
#         return token
#     except Exception as err:
#         print("get_jwt", err)
#         return None
def get_access_token(_id, membership_type, session_code=None):
    try:
        access_token_data = {'identity': _id, 'iat': datetime.datetime.utcnow(),
                             "exp": get_auth_exp(config.JWT_ACCESS_TOKEN_TIME_OUT_IN_MINUTES)}
        if session_code:
            access_token_data['session_code'] = session_code
            access_token_data['membership_type'] = membership_type
        access_token = jwt.encode(access_token_data, config.SECRET_KEY, config.JWT_ALGORITHM)
        token = {"access_token": access_token.decode("utf-8")}

        # if session_code:
        #     refresh_token_data = {'identity': _id, 'api_key': api_key, 'iat': datetime.datetime.utcnow(),
        #                           "exp": get_auth_exp(config.JWT_REFRESH_TOKEN_TIME_OUT_IN_MINUTES)}
        #     refresh_token = jwt.encode(refresh_token_data, config.SECRET_KEY, config.JWT_ALGORITHM)
        #     token['refresh_token'] = refresh_token.decode('utf-8')
        return token
    except Exception as err:
        print("get_jwt", err)
        return None


def check_valid_user(payload):
    try:
        obj = get_user_by_id(payload['identity'])

        # print("----------------------", obj)

        if not obj:
            return False

        return payload['api_key'] is not None
    except Exception as err:
        print("check_valid_user", str(err))
        return False


@auth_api_v1.route('/get-token', methods=['POST'])
def get_token():
    try:
        data = json.loads(request.data.decode('utf-8'))
        _id = data.get('uid', None)
        api_key = data.get('api_key', 'DEFAULT')
        payload = {'identity': _id, 'api_key': api_key}
        print('payload', payload)
        if not check_valid_user(payload):
            return failure(strings.invalid_credentials)
        token = get_jwt(_id, api_key)

        if token:
            token = {'token': str(token)}
            return success(strings.retrieved_success, token)
        else:
            return failure(strings.verification_failed)

    except Exception as e:
        print("get_token", e)
        return failure(str(e))


@auth_api_v1.route('/refresh_token', methods=['POST'])
def get_refresh_token():
    try:
        data = request.json
        refresh_token = data['refresh_token']
        try:
            decoded_token = jwt.decode(refresh_token, config.SECRET_KEY, algorithms=[config.JWT_ALGORITHM])
        except Exception as e:
            print(e)
            return failure("token expired")

        print(decoded_token)
        uesr_id = decoded_token['identity']
        membership_type = decoded_token['membership_type']
        session_code = decoded_token['session_code']
        # remove refreshtoken
        token = get_jwt(uesr_id, membership_type, session_code)
        return success("SUCCESS", token)

    except Exception as e:
        print("get_token", e)
        return failure(str(e))


@auth_api_v1.route('/token', methods=['POST'])
def get_jwtoken():
    try:
        from api.Users.models import Users
        data = json.loads(request.data.decode('utf-8'))
        email_id = data.get('email')
        users_data = Users.query.filter_by(email=email_id).first()
        _id = str(users_data.id)
        if not users_data:
            return failure(strings.invalid_credentials)
        api_key = data.get('api_key', 'DEFAULT')
        payload = {'identity': _id, 'api_key': api_key}
        token = get_jwt(_id, api_key)

        if token:
            token = {'token': token}
            return token
        else:
            return failure(strings.verification_failed)

    except Exception as e:
        print("get_token", e)
        return failure(str(e))


def sample_jwt():
    actual = {'uid': '1', 'api_key': 'api-secret-key',
              'exp': get_auth_exp(config.JWT_REFRESH_TOKEN_TIME_OUT_IN_MINUTES)}
    token = get_jwt(actual['uid'], actual['api_key'])
    return token


def get_user_by_id(_id):
    try:
        # Don't remove from here
        from api.Users.models import Users
        obj = Users.query.get(_id)._asdict()
        # print(obj)
        return obj
    except Exception as err:
        print("get_user_by_id - ", str(err))
        return None


def validate_token(action=None, session=True, membership_status='active'):
    from api.Users.models import Membership, Roles, Actions, RoleActions
    def decorator(f):
        def wrapper(*args, **kwargs):
            token = None
            # jwt is passed in the request header
            if 'x-access-token' in request.headers:
                token = request.headers['x-access-token']
                # return 401 if token is not passed
            if not token:
                return jsonify({'message': 'Token is missing !!'}), 401

            from api.Users.models import Users
            from api.Users.models import UserDevice
            # decoding the payload to fetch the stored details
            try:
                data = jwt.decode(token, config.SECRET_KEY, algorithms=[config.JWT_ALGORITHM])
            except Exception as e:
                return jsonify({
                    'message': 'Unauthorized !!'
                }), 401
            id = data.get('identity')
            device = False
            if session:
                session_code = data.get('session_code')
                device = UserDevice.query.filter_by(user_id=id, session_code=session_code).first()
                g.session_code = session_code
            current_user = Users.query.filter(Users.id == id).first()
            if current_user and (not session or session and device):
                g.user_id = current_user.id
                # take user role
                membership_type = data.get('membership_type')
                g.membership_type = membership_type
                user_role = Membership.query.filter_by(user_id=current_user.id, membership_type=membership_type).first()
                print('&7&&&&&',user_role.role)
                if user_role.role != 'super_admin':
                    # filter role_actions table with  action and user role
                    if membership_status and user_role.membership_status != membership_status:
                        return jsonify({
                            'message': 'Access Denied 2!!'
                        }), 403
                    if user_role:
                        print("ROLE============>", user_role.role)
                        print("ACTION============>", action)
                        role_action = RoleActions.query.filter_by(role_key=user_role.role, action_key=action).first()
                        if not role_action:
                            return jsonify({
                                'message': 'Access Denied 3!!'
                            }), 403
                # else:
                #     return jsonify({
                #         'message': 'Access Denied@@@@@@!!'
                #     }), 403
                # if record not fund throw error
                return f(current_user, *args, **kwargs)
            else:
                return jsonify({
                    'message': 'unauthorized !!'
                }), 401

        wrapper.__name__ = f.__name__
        return wrapper

    return decorator


# decorator for verifying the JWT
def token_required(f, session=True):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None
        # jwt is passed in the request header
        if 'x-access-token' in request.headers:
            token = request.headers['x-access-token']
            print("Token in headers", token)
            # return 401 if token is not passed
        if not token:
            return jsonify({'message': 'Token is missing !!'}), 401

        from api.Users.models import Users
        from api.Users.models import UserDevice
        # decoding the payload to fetch the stored details
        try:
            data = jwt.decode(token, config.SECRET_KEY, algorithms=[config.JWT_ALGORITHM])
        except Exception as e:
            print(e, "decode jwt exception==========")
            # ToDo If got error return 400
            return jsonify({
                'message': 'Unauthorized !!'
            }), 401
        # ToDo validate is this type of token Other than access return 404
        # ToDo validity check, if Expires 401
        id = data.get('identity')
        print('id=========>', id)
        device = False
        if session:
            session_code = data.get('session_code')
            device = UserDevice.query.filter_by(user_id=id, session_code=session_code).first()
            g.session_code = session_code
            print("+++++++++++++++++++++device===", device)
        print("User id after decoding =====>", id)
        current_user = Users.query.filter(Users.id == id).first()
        # ToDo If no user return 404
        print("=====current_user==", current_user)
        # ToDo if not found 404
        print("hi--------------")
        if current_user and (not session or session and device):
            g.user_id = current_user.id
            print("=====g.user=====", g.user_id)
            print(g, "============")
            return f(current_user, *args, **kwargs)
        else:
            # ToDo if not found 404
            return jsonify({
                'message': 'unauthorized !!'
            }), 401
        # returns the current logged in users contex to the routes
        return f(current_user, *args, **kwargs)

    return decorated


# def token_only_required(f):
#     @wraps(f)
#     def decorated(*args, **kwargs):
#         token = None
#         # jwt is passed in the request header
#         if 'x-access-token' in request.headers:
#             token = request.headers['x-access-token']
#             print("Token in headers", token)
#             # return 401 if token is not passed
#         if not token:
#             return jsonify({'message': 'Token is missing !!'}), 401
#
#         from api.Users.models import Users
#         from api.Users.models import UserDevice
#         # decoding the payload to fetch the stored details
#         try:
#             data = jwt.decode(token, config.SECRET_KEY, algorithms=[config.JWT_ALGORITHM])
#         except Exception as e:
#             print(e, "decode jwt exception==========")
#             # ToDo If got error return 400
#             return jsonify({
#                 'message': 'Unauthorized !!'
#             }), 401
#         # ToDo validate is this type of token Other than access return 404
#         # ToDo validity check, if Expires 401
#         id = data.get('identity')
#         print("User id after decoding =====>", id)
#         current_user = Users.query.filter(Users.id == id).first()
#         # ToDo If no user return 404
#         print("=====current_user==", current_user)
#         # ToDo if not found 404
#         print("hi--------------")
#         if current_user:
#             g.user_id = current_user.id
#             print("=====g.user=====", g.user_id)
#             print(g, "============")
#             return f(current_user, *args, **kwargs)
#         else:
#             # ToDo if not found 404
#             return jsonify({
#                 'message': 'unauthorized !!'
#             }), 401
#         # returns the current logged in users contex to the routes
#         return f(current_user, *args, **kwargs)
#
#     return decorated


def verificatio_token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None
        # jwt is passed in the request header
        if 'x-access-token' in request.headers:
            token = request.headers['x-access-token']
            print("Token in headers", token)
        # return 401 if token is not passed
        if not token:
            return jsonify({'message': 'Token is missing !!'}), 401
        try:
            from api.Users.models import Verification
            # decoding the payload to fetch the stored details
            data = jwt.decode(token, config.SECRET_KEY, algorithms=[config.JWT_ALGORITHM])
            id = data.get('identity')
            current_user = Verification.query.filter_by(id=id).first()
            print("verified token================")
            g.user_id = id

            # if current_user:
        except:
            return jsonify({
                'message': 'Token is invalid !!'
            }), 401
        # returns the current logged in users contex to the routes
        return f(current_user, *args, **kwargs)

    return decorated


def test():
    print("Hello this test function from auth")
    return True


def get_access_token(_id, membership_type, session_code=None):
    try:
        access_token_data = {'identity': _id, 'iat': datetime.datetime.utcnow(),
                             "exp": get_auth_exp(config.JWT_ACCESS_TOKEN_TIME_OUT_IN_MINUTES)}
        if session_code:
            access_token_data['session_code'] = session_code
            access_token_data['membership_type'] = membership_type
        access_token = jwt.encode(access_token_data, config.SECRET_KEY, config.JWT_ALGORITHM)
        token = {"access_token": access_token.decode("utf-8")}

        # if session_code:
        #     refresh_token_data = {'identity': _id, 'api_key': api_key, 'iat': datetime.datetime.utcnow(),
        #                           "exp": get_auth_exp(config.JWT_REFRESH_TOKEN_TIME_OUT_IN_MINUTES)}
        #     refresh_token = jwt.encode(refresh_token_data, config.SECRET_KEY, config.JWT_ALGORITHM)
        #     token['refresh_token'] = refresh_token.decode('utf-8')
        return token
    except Exception as err:
        print("get_jwt", err)
        return None

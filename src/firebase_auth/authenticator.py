import firebase_admin
import jwt
from firebase_admin import auth, credentials

cred = credentials.Certificate("src/serviceAccountKey.json")
default_app = firebase_admin.initialize_app(cred)


def generate_custom_token(user_profile):
    uid = str(user_profile["_id"])

    custom_token = auth.create_custom_token(uid)
    return custom_token


def verify_custom_token(id_token):
    # decoded_token = jwt.decode(custom_token,  algorithms=["RS256"])
    # uid = decoded_token.get('uid')
    # print (decoded_token)
    # uid = decoded_token['uid']
    return True

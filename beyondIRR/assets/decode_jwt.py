import jwt
from jwt.exceptions import InvalidTokenError, ExpiredSignatureError
from django.conf import settings
import os

def decode_jwt(auth_header):
    try:
        token = auth_header.split(' ')[1]
        public_key_path = os.path.join(settings.BASE_DIR, 'public_key.pem')
        with open(public_key_path, 'r') as key_file:
            public_key = key_file.read()
        
        decoded_token = jwt.decode(token, public_key, algorithms=['RS256'])
        
        return decoded_token
    
    except ExpiredSignatureError:
        raise Exception('Token has expired')
    except InvalidTokenError:
        raise Exception('Invalid token')


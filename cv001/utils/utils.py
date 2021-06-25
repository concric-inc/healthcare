from cv001.settings import SECRET_KEY
import jwt
def get_uid(token):
   
    result = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
    return result['UID']

def get_JWT_token(request):
    return request.META['HTTP_AUTHORIZATION'].split('Bearer ')[1]



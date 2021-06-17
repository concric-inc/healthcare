from cv001.settings import SECRET_KEY
import jwt
def get_uid(token):
   
    result = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
    return result['UID']

def get_JWT_token(request):
    return request.META['HTTP_AUTHORIZATION'].split('Bearer ')[1]


ACCOUNT_CREATED = 'account successfully created'
UPDATED = 'data updated'
UNABLE_TO_PROCESS = 'we are unable to process your request at this moment'
OTP_INVALID = 'invalid otp'
SOMTHING_WENT_WRONG = 'somthing went wrong'
OTP_SENT = 'a otp has been send to this number'
USER_ALREADY_EXISTS = 'a user is already registered on this number'
INVALID_PHONE_NUMBER ='invalid phone number'
EMAIL_CONFIRMED  = 'email is confirmed'
EMAIL_TOKEN_EXPIRED ='verification token expired'
SUCCESS = 'success'
ADDRESS_STORED = 'address saved sucessfully'
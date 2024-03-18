import sys
sys.path.insert(0, 'vendor')

from utils.general_utils import search_user
import jwt

def get_user_from_token(event):
    token = event['headers']['Authorization']
    token = token.replace("Bearer ", "").replace(" ", "")
    decoded_token = jwt.decode(
        token,
        options={"verify_signature": False}
    )        
    user_uuid = decoded_token['username']
    records = search_user(user_uuid)
    if len(records) <= 0:
        return 403
    return records[0]["name"]

def get_uuid_from_token(event):
    token = event['headers']['Authorization']
    token = token.replace("Bearer ", "").replace(" ", "")
    decoded_token = jwt.decode(
        token,
        options={"verify_signature": False}
    )        
    user_uuid = decoded_token['username']
    return user_uuid
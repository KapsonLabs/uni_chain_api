import jwt
import uuid

def generate_account_number(id):
    return "AC{}".format(100000+id)

def generate_pay_id(txn_id, secret_key):
    return jwt.encode({'txn_id':str(txn_id)}, secret_key, algorithm='HS256').decode('utf-8')

def decode_pay_id(encoded_jwt, secret_key):
    try:
        return jwt.decode(encoded_jwt, secret_key, algorithms=['HS256'])
    except:
        return "Failed"

def generate_transaction_id():
    return uuid.uuid4()


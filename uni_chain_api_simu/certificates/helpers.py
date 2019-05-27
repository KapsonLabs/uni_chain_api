import hashlib

def generate_certificate_link(student_wallet_address, institution_wallet_address, unique_string, student_number):
    hash_object = hashlib.sha512(b'{0}{1}{2}{3}'.format(student_wallet_address, institution_wallet_address, unique_string, student_number))
    hex_dig = hash_object.hexdigest()
    return hex_dig
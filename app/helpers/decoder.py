import base64

def decode(args):
    basic_auth = args['Authorization']
    base64_string =basic_auth[6:]
    message_bytes = base64.b64decode(base64_string).decode('ascii')
    email, password = message_bytes.split(':')
    return {
        "email": email,
        "password": password,
    }

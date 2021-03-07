from base64 import b64decode

import jwt


class UnSupportedAuthType(Exception):
    status_code = 501

    def __init__(self, message, status_code=None, payload=None, errors=None):
        Exception.__init__(self)
        self.message = message
        if status_code is not None:
            self.status_code = status_code
        self.payload = payload
        self.errors = errors

    def to_dict(self):
        rv = dict(self.payload or ())
        rv["message"] = self.message
        if self.errors is not None:
            rv["errors"] = self.errors
        return rv


def authorization_decoder(config, auth_str: str):
    """
    Authorization token decoder based on type. This will decode the token and
    only return the owner
    Args:
        config: app.config object
        auth_str: Authorization string should be in "<type> <token>" format
    Returns:
        decoded owner from token
    """
    type, token = auth_str.split()

    if type == "Basic":
        """Basic format <user>:<password> return only the user"""
        return b64decode(token).decode().split(":")[0]
    elif type == "Bearer":
        """return only the identity， depends on JWT 2.x"""
        decoded_jwt = jwt.decode(token, config.get("JWT_SECRET_KEY"),
                                 algorithms=config.get('JWT_HASH'))
        return decoded_jwt.get("identity", '')
    else:
        raise UnSupportedAuthType("%s Authorization is not supported" % type)

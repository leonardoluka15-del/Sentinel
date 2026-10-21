import hmac
from urllib.parse import urlsplit

def authorized(handler,token):
    if not token: return True
    return hmac.compare_digest(handler.headers.get('Authorization',''),'Bearer '+token)

def same_origin(handler):
    origin=handler.headers.get('Origin')
    if not origin: return True
    parsed=urlsplit(origin)
    return parsed.scheme in ('http','https') and parsed.netloc==handler.headers.get('Host','')

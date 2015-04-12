from instagram.client import InstagramAPI
import sys

client_id = "fae19a5f499c4aff820f71ce869e5579".strip()
client_secret = "c3a8e0773e174a8caa2f785e9120d5b5".strip()
redirect_uri = "http://instat.elasticbeanstalk.com/".strip()
scope = ["basic"]

def get_access_token():
    global client_id, client_secret, redirect_uri, scope

    # Fix Input for Python 2.x.
    try:
        import __builtin__
        input = getattr(__builtin__, 'raw_input')
    except (ImportError, AttributeError):
        pass

    api = InstagramAPI(client_id=client_id, client_secret=client_secret, redirect_uri=redirect_uri)
    redirect_uri = api.get_authorize_login_url(scope = scope)

    print ("Visit this page and authorize access in your browser: \n"+ redirect_uri)

    code = (str(input("Paste in code in query string after redirect: ").strip()))

    access_token = api.exchange_code_for_access_token(code)
    print ("access token: " )
    print (access_token)
    return access_token

def login():
    """store access_token somewhere for later use"""
    access_token = get_access_token()
    pass

if __name__ == '__main__':
    get_access_token()

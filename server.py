from fastapi import FastAPI
from fastapi.middleware.httpsredirect import HTTPSRedirectMiddleware
from fastapi.middleware.trustedhost import TrustedHostMiddleware

import config
from api_routes import profiles


app = FastAPI(debug=config.DEBUG, 
              title=config.TITLE, 
              version=config.VERSION)

if config.DEPLOY == 'prod':
    app.add_middleware(HTTPSRedirectMiddleware)
    app.add_middleware(TrustedHostMiddleware)

@app.get('/')
def get_root():
    return {'UsersManagementAPI':'running'}

app.mount('/profile', profiles.profiles_router)

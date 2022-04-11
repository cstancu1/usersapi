from fastapi import FastAPI
from fastapi.middleware.httpsredirect import HTTPSRedirectMiddleware
from fastapi.middleware.trustedhost import TrustedHostMiddleware
from fastapi.middleware.cors import CORSMiddleware

import config
from api_routes import profiles, gateway_access

app = FastAPI(debug=config.DEBUG, 
              title=config.TITLE, 
              version=config.VERSION)

if config.DEPLOY == 'prod':
    app.add_middleware(HTTPSRedirectMiddleware)
    app.add_middleware(TrustedHostMiddleware)

origins = [
    "http://localhost",
    "http://localhost:8000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get('/')
def get_root():
    return {'UsersManagementAPI':'running test'}

app.mount('/profile', profiles.profiles_router)
app.mount('/', gateway_access.gateway_access)
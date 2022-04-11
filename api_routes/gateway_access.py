import requests
from fastapi import Depends, File, Response,\
     HTTPException, UploadFile, APIRouter, Request
from common.token_module import TokenRequired
from persistence.models import UserFromDb
from config import SURVEYS_API_URL

gateway_access = APIRouter()

#########################################
# PUBLIC GATEWAY
#########################################

@gateway_access.get('/public/surveys/{destination:path}')
def surveys_public(destination: str,
                  current_request: Request):
    if current_request.query_params:
        resp = requests.get(
            f"{SURVEYS_API_URL}/public/{destination}",
            params = current_request.query_params
        )
    else:
        resp = requests.get(
            f"{SURVEYS_API_URL}/public/{destination}",
        )
    return Response(
        content = resp.content,
        status_code = resp.status_code,
        headers = resp.headers
    )
    
@gateway_access.post('/public/surveys/{destination:path}')
async def surveys_post_public(destination: str, 
                  files: list[UploadFile] = File(None),
                  req: Request = None,):
    if files:
        resp = requests.post(
            f"{SURVEYS_API_URL}/public/{destination}",
            files = [(file.filename, await file.read()) for file in files])

    else:
        data = await req.body()
        data = data.decode('UTF-8')
        resp = requests.post(
            f"{SURVEYS_API_URL}/public/{destination}",
            data = data
        )

    return Response(
        content = resp.text,
        status_code = resp.status_code,
        headers = resp.headers
    )

#########################################
# SURVEYS GATEWAY
#########################################

@gateway_access.get('/surveys/{destination:path}')
def surveys_get(destination: str, 
    current_request: Request,
    current_user: UserFromDb = Depends(TokenRequired.user_active)):
    headers = {
        'Authorization': str(current_user['access']),
        'Userid': current_user['_id'],
        'Companyid': current_user['company_id'],
        'Teamid': current_user['team_id']     
        }
    if current_request.query_params:
        resp = requests.get(
            f"{SURVEYS_API_URL}/{destination}",
            headers = headers,
            params=current_request.query_params)
    else:
        resp = requests.get(
            f"{SURVEYS_API_URL}/{destination}",
            headers = headers)

    return Response(
        content = resp.text,
        status_code = resp.status_code,
        headers = resp.headers
    )
    
@gateway_access.post('/surveys/{destination:path}')
async def surveys_post(destination: str, 
    files: list[UploadFile] = File(None),
    req: Request = None,
    current_user: UserFromDb = Depends(TokenRequired.user_active)
    ):
    headers = {
        'Authorization': str(current_user['access']),
        'Userid': current_user['_id'],
        'Companyid': current_user['company_id'],
        'Teamid': current_user['team_id']     
        }

    if files:
        resp = requests.post(
            f"{SURVEYS_API_URL}/{destination}",
            headers = headers, files = [(file.filename, await file.read()) for file in files])

    else:
        data = await req.body()
        data = data.decode('UTF-8')
        resp = requests.post(
            f"{SURVEYS_API_URL}/{destination}",
            headers = headers,
            data = data
        )
        print(resp.text)
    return Response(
        content = resp.text,
        status_code = resp.status_code,
        headers = resp.headers
    )

@gateway_access.put('/surveys/{destination:path}')
async def surveys_patch(destination: str, 
    files: list[UploadFile] = File(None),
    req: Request = None,
    current_user: UserFromDb = Depends(TokenRequired.user_active)
    ):
    headers = {
        'Authorization': str(current_user['access']),
        'Userid': current_user['_id'],
        'Companyid': current_user['company_id'],
        'Teamid': current_user['team_id']     
        }

    if files:
        resp = requests.post(
            f"{SURVEYS_API_URL}/{destination}",
            headers = headers, files = [(file.filename, await file.read()) for file in files])

    else:
        data = await req.body()
        data = data.decode('UTF-8')
        resp = requests.put(
            f"{SURVEYS_API_URL}/{destination}",
            headers = headers,
            data = data
        )
    return Response(
        content = resp.text,
        status_code = resp.status_code,
        headers = resp.headers
    )

@gateway_access.put('/surveys/{company}/{destination:path}')
def gateway_test(company: str, destination: str, 
    current_user: UserFromDb = Depends(TokenRequired.user_active)):
    if current_user['company_id'] != company:
        return HTTPException(401, "unauthorized")
    return{
        "app":destination,
        "company":company
    }

@gateway_access.delete('/surveys/{company}/{destination:path}')
def gateway_test(company: str, destination: str, 
    current_user: UserFromDb = Depends(TokenRequired.user_active)):
    if current_user['company_id'] != company:
        return HTTPException(401, "unauthorized")
    return{
        "app":destination,
        "company":company
    }


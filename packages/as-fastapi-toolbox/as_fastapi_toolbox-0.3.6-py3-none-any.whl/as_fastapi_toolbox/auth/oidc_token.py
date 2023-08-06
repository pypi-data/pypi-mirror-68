import httpx
from typing import Optional
from fastapi import HTTPException
from starlette.status import HTTP_200_OK, HTTP_401_UNAUTHORIZED
from starlette.requests import Request
from fastapi.security.utils import get_authorization_scheme_param
from pydantic import HttpUrl


class OpenIDConnectClientCredentials:
    client_id: str
    client_secret: str


class OpenIDConnectRetrieveToken:
    def __hash__(self):
        return id(self)

    async def __call__(self, request: Request) -> Optional[str]:
        authorization: str = request.headers.get("Authorization")
        scheme, param = get_authorization_scheme_param(authorization)
        if not authorization or scheme.lower() != "bearer":
            raise HTTPException(status_code=HTTP_401_UNAUTHORIZED,
                                detail="Not authenticated",
                                headers={"WWW-Authenticate": "Bearer"}
                                )

        return param


class OpenIDConnectValidateToken(OpenIDConnectClientCredentials):
    def __hash__(self):
        return id(self)

    def __init__(self, client_id: str, client_secret: str, introspect_url: HttpUrl):
        super().__init__(client_id=client_id, client_secret=client_secret)
        self.introspect_url = introspect_url

    async def __call__(self, request: Request) -> Optional[str]:
        retrieve_token = OpenIDConnectRetrieveToken()
        param = await retrieve_token(request=request)

        async with httpx.AsyncClient() as client:
            resp = await client.post(self.introspect_url,
                                     data={
                                         'client_id': self.client_id,
                                         'client_secret': self.client_secret,
                                         'token': param
                                     })

        if resp.status_code != HTTP_200_OK:
            raise HTTPException(status_code=HTTP_401_UNAUTHORIZED, detail="Token could not be validated")

        if not resp.json().get('active', False):
            raise HTTPException(status_code=HTTP_401_UNAUTHORIZED, detail="Token is invalid")

        return param

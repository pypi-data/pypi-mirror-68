import asyncio
from json import JSONDecodeError
from typing import Any, Union
from fastapi import HTTPException
from starlette.status import HTTP_404_NOT_FOUND
from httpx import AsyncClient, Response, NetworkError, URL

# TODO: find a way to access the types in a clean way (not via protected modules)
from httpx._config import TimeoutTypes, UnsetType, UNSET
from httpx._models import URLTypes, RequestData, QueryParamTypes, HeaderTypes, CookieTypes
from httpx._auth import AuthTypes

from as_fastapi_toolbox.requests.circuit_breaker import CircuitBreaker


class RobustRequest:
    """
    Implementation of a more failure tolerant, asynchronous request against an external service.
    It uses a system of retrying individual failed requests and a circuit breaker to cater for overall service
    unavailability.

    If you want to run multiple requests concurrently, use the task feature of the asyncio library.
        You can either use the request function directly and specify the request method:
            req1 = asyncio.create_task(request(method1, url1))
            req2 = asyncio.create_task(request(method2, url2))
            resp1, _ = await req1
            resp2, _ = await req2

        Or you can use the shorthand methods and freely combine them:
            req1 = asyncio.create_task(get(url1))
            req2 = asyncio.create_task(post(url2))
            resp1, _ = await req1
            resp2, _ = await req2
    """
    def __init__(self, retries_max: int = 1, retries_sleep: int = 5,
                 circuit_failure_threshold: int = 3, circuit_recovery_timeout: int = 20, circuit_reset_count: int = 1,
                 raise_error_response: bool = True):
        self._retries_max = retries_max
        self._retries_sleep = retries_sleep
        self._raise_error_response = raise_error_response
        self._circuit_breaker = CircuitBreaker(failure_threshold=circuit_failure_threshold,
                                               recovery_timeout=circuit_recovery_timeout,
                                               reset_count=circuit_reset_count)

    async def request(self, method: str, url: URLTypes, *,
                      data: RequestData = None, json: Any = None, params: QueryParamTypes = None,
                      auth: AuthTypes = None, headers: HeaderTypes = None, cookies: CookieTypes = None,
                      timeout: Union[TimeoutTypes, UnsetType] = UNSET,
                      raise_error_response: bool = None) -> (Response, int):
        """ Implementation of an asyncio HTTP request with retry and circuit breaker functionality. """
        raise_error = raise_error_response if raise_error_response is not None else self._raise_error_response
        url = URL(url) if isinstance(url, str) else url
        service_name = f'{url.host}:{url.port}'

        async with AsyncClient() as client:
            response = None
            retries = 0
            while (response is None) and (retries <= self._retries_max):
                try:
                    response = await self._circuit_breaker(service_name, client.request,
                                                           method, url, data=data, json=json, params=params,
                                                           auth=auth, headers=headers, cookies=cookies,
                                                           timeout=timeout)
                except NetworkError:
                    retries += 1
                    if retries <= self._retries_max:
                        await asyncio.sleep(self._retries_sleep)

        if response is None:
            raise HTTPException(status_code=HTTP_404_NOT_FOUND,
                                detail=f'The gateway could not contact {url} after {retries-1} retries')

        if raise_error and response.status_code >= 400:
            detail = None
            try:
                detail = response.json()
            except JSONDecodeError:
                pass

            raise HTTPException(status_code=response.status_code,
                                detail=detail if detail is not None else response.text)

        return response, response.status_code

    async def get(self, url: URLTypes, *,
                  data: RequestData = None, json: Any = None, params: QueryParamTypes = None,
                  auth: AuthTypes = None, headers: HeaderTypes = None, cookies: CookieTypes = None,
                  timeout: Union[TimeoutTypes, UnsetType] = UNSET,
                  raise_error_response: bool = None) -> (Response, int):
        """ Asyncio HTTP GET request with retry and circuit breaker """
        return await self.request('GET', url, data=data, json=json, params=params, auth=auth,
                                  headers=headers, cookies=cookies, timeout=timeout,
                                  raise_error_response=raise_error_response)

    async def post(self, url: URLTypes, *,
                   data: RequestData = None, json: Any = None, params: QueryParamTypes = None,
                   auth: AuthTypes = None, headers: HeaderTypes = None, cookies: CookieTypes = None,
                   timeout: Union[TimeoutTypes, UnsetType] = UNSET,
                   raise_error_response: bool = None) -> (Response, int):
        """ Asyncio HTTP POST request with retry and circuit breaker """
        return await self.request('POST', url, data=data, json=json, params=params, auth=auth,
                                  headers=headers, cookies=cookies, timeout=timeout,
                                  raise_error_response=raise_error_response)

    async def put(self, url: URLTypes, *,
                  data: RequestData = None, json: Any = None, params: QueryParamTypes = None,
                  auth: AuthTypes = None, headers: HeaderTypes = None, cookies: CookieTypes = None,
                  timeout: Union[TimeoutTypes, UnsetType] = UNSET,
                  raise_error_response: bool = None) -> (Response, int):
        """ Asyncio HTTP PUT request with retry and circuit breaker """
        return await self.request('PUT', url, data=data, json=json, params=params, auth=auth,
                                  headers=headers, cookies=cookies, timeout=timeout,
                                  raise_error_response=raise_error_response)

    async def delete(self, url: URLTypes, *,
                     data: RequestData = None, json: Any = None, params: QueryParamTypes = None,
                     auth: AuthTypes = None, headers: HeaderTypes = None, cookies: CookieTypes = None,
                     timeout: Union[TimeoutTypes, UnsetType] = UNSET,
                     raise_error_response: bool = None) -> (Response, int):
        """ Asyncio HTTP DELETE request with retry and circuit breaker """
        return await self.request('DELETE', url, data=data, json=json, params=params, auth=auth,
                                  headers=headers, cookies=cookies, timeout=timeout,
                                  raise_error_response=raise_error_response)


rr = RobustRequest()

get = rr.get
post = rr.post
put = rr.put
delete = rr.delete

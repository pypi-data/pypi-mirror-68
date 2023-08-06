from datetime import datetime, timedelta
from typing import Any, Callable, Coroutine
from dataclasses import dataclass
from fastapi import HTTPException
from starlette.status import HTTP_404_NOT_FOUND
from httpx import Response, NetworkError


class CircuitBreakerException(HTTPException):
    pass


class CircuitBreakerState:
    OPEN = 1
    HALFOPEN = 2
    CLOSED = 3


@dataclass
class CircuitBreakerService:
    """ The data for the circuit breaker state for a single service """
    failed_requests: int = 0
    reset_requests: int = 0
    last_failed_at: datetime = datetime.utcnow()
    current_state: CircuitBreakerState = CircuitBreakerState.CLOSED

    def reset(self, status: CircuitBreakerState = CircuitBreakerState.CLOSED):
        self.failed_requests = 0
        self.reset_requests = 0
        self.current_state = status


class CircuitBreaker:
    """
    Implementation of a circuit breaker for handling failures in calls to external services, particularly if the
    remote service is not accessible. It follows the pattern as described here:

        https://martinfowler.com/bliki/CircuitBreaker.html

    The circuit has three states:
        - closed: all traffic is allowed through as there are no problems detected
        - open: the number of failed requests has reached a threshold, all traffic is denied.
        - half-open: the timout of an open circuit has expired and traffic is allowed through again. If, after allowing
                     traffic through, a pre-defined number of subsequent requests are successful, the circuit is closed
                     and traffic can flow. However, if a request fails while the circuit breaker is half-open, it will
                     be opened immediately.

    This is a simple implementation with a threshold based on the number of failed requests, not on a failure rate.
    Each successful request resets the number of failed requests to avoid build-up of historic failed requests.
    """
    def __init__(self, failure_threshold: int = 3, recovery_timeout: int = 30, reset_count: int = 1):
        """
        Args:
            failure_threshold: The number of subsequent failed requests that trips the circuit breaker
            recovery_timeout: The time in seconds the circuit breaker stays open before it tries to contact the remote service again
            reset_count: The number of successful requests before a remote service is considered stable and a half-open circuit is closed again
        """
        self._failure_threshold = failure_threshold
        self._recovery_timeout = recovery_timeout
        self._reset_count = reset_count
        self._map = {}

    async def __call__(self, service_name: str, func: Callable[..., Response], *args, **kwargs) -> Coroutine[Any, Any, Response]:
        # get the circuit breaker data for the service or create an initial dataset if it doesn't exist yet
        if service_name not in self._map:
            self._map[service_name] = CircuitBreakerService()
        srv = self._map[service_name]

        # the circuit breaker is open, which means the remote service is not accessible. Check whether the timout has
        # expired, if it has expired set the state to half-open, otherwise deny traffic by returning immediately
        if srv.current_state == CircuitBreakerState.OPEN:
            if datetime.utcnow() >= srv.last_failed_at + timedelta(seconds=self._recovery_timeout):
                srv.current_state = CircuitBreakerState.HALFOPEN
                srv.reset_requests = 0
            else:
                raise CircuitBreakerException(status_code=HTTP_404_NOT_FOUND,
                                              detail=f'The circuit breaker for {service_name} is open')

        try:
            response = await func(*args, **kwargs)

            # we have a successful request, if the circuit was half-open and we have reached the number of successful
            # requests in order to reset the circuit breaker, set it to closed and reset the service data
            if srv.current_state == CircuitBreakerState.HALFOPEN:
                srv.reset_requests += 1
                if srv.reset_requests >= self._reset_count:
                    srv.reset(status=CircuitBreakerState.CLOSED)

            # reset the number of failed requests for every successful request when the circuit breaker is closed,
            # so that we don't build up a history of long-gone failed requests
            if srv.current_state == CircuitBreakerState.CLOSED:
                srv.failed_requests = 0

            return response

        except NetworkError:
            srv.last_failed_at = datetime.utcnow()

            # the request was not successful. If the circuit is half-open, open it immediately, otherwise check number
            # of failed requests and if above the threshold, trip the circuit breaker by setting it to open
            srv.failed_requests += 1
            if (srv.current_state == CircuitBreakerState.HALFOPEN) or (srv.failed_requests >= self._failure_threshold):
                srv.current_state = CircuitBreakerState.OPEN
                raise CircuitBreakerException(status_code=HTTP_404_NOT_FOUND,
                                              detail=f'The circuit breaker for {service_name} is open')
            raise

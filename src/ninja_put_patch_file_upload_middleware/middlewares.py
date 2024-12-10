from collections.abc import Awaitable, Callable
from typing import Any, TypeAlias, Final

from asgiref.sync import iscoroutinefunction, sync_to_async
from django.http import HttpRequest, HttpResponse
from django.utils.decorators import sync_and_async_middleware

ResponseType: TypeAlias = HttpResponse | Any
RequestHandler: TypeAlias = Callable[[HttpRequest], ResponseType]
AsyncRequestHandler: TypeAlias = Callable[[HttpRequest], Awaitable[ResponseType]]

TARGET_METHODS: Final[set[str]] = {"PUT", "PATCH"}
CONTENT_TYPE: Final[str] = "application/json"


@sync_and_async_middleware
def process_put_patch(
    get_response: RequestHandler | AsyncRequestHandler,
) -> RequestHandler | AsyncRequestHandler:
    """
    Middleware to handle PUT and PATCH requests when content type is not JSON.
    Converts the request method to POST temporarily to enable file/post data parsing.

    Args:
        get_response: The next middleware or view handler in the request processing chain.

    Returns:
        An async or sync middleware function based on the input handler type.
    """
    if iscoroutinefunction(get_response):

        async def async_middleware(request: HttpRequest) -> ResponseType:
            if (
                request.method in TARGET_METHODS
                and request.content_type != CONTENT_TYPE
            ):
                initial_method = request.method
                request.method = "POST"
                request.META["REQUEST_METHOD"] = "POST"
                await sync_to_async(request._load_post_and_files)()
                request.META["REQUEST_METHOD"] = initial_method
                request.method = initial_method

            return get_response(request)

        return async_middleware
    else:

        def sync_middleware(request: HttpRequest) -> ResponseType:
            if (
                request.method in TARGET_METHODS
                and request.content_type != CONTENT_TYPE
            ):
                initial_method = request.method
                request.method = "POST"
                request.META["REQUEST_METHOD"] = "POST"
                request._load_post_and_files()
                request.META["REQUEST_METHOD"] = initial_method
                request.method = initial_method

            return get_response(request)

        return sync_middleware

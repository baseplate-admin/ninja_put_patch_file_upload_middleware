from collections.abc import Callable
from typing import Any, Union

from asgiref.sync import iscoroutinefunction, sync_to_async
from django.http import HttpRequest, HttpResponse
from django.utils.decorators import sync_and_async_middleware


@sync_and_async_middleware
def process_put_patch(
    get_response: Union[
        Callable[[HttpRequest], HttpResponse], Callable[[HttpRequest], Any]
    ],
) -> Union[Callable[[HttpRequest], Any], Callable[[HttpRequest], HttpResponse]]:
    async def async_middleware(request: HttpRequest) -> Union[HttpResponse, Any]:
        if (
            request.method in ("PUT", "PATCH")
            and request.content_type != "application/json"
        ):
            initial_method = request.method
            request.method = "POST"
            request.META["REQUEST_METHOD"] = "POST"
            await sync_to_async(request._load_post_and_files)()
            request.META["REQUEST_METHOD"] = initial_method
            request.method = initial_method

        return await get_response(request)

    def sync_middleware(request: HttpRequest) -> Union[HttpResponse, Any]:
        if (
            request.method in ("PUT", "PATCH")
            and request.content_type != "application/json"
        ):
            initial_method = request.method
            request.method = "POST"
            request.META["REQUEST_METHOD"] = "POST"
            request._load_post_and_files()
            request.META["REQUEST_METHOD"] = initial_method
            request.method = initial_method

        return get_response(request)

    return async_middleware if iscoroutinefunction(get_response) else sync_middleware

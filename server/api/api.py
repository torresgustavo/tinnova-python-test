from ninja import NinjaAPI
from django.http.request import HttpRequest
from api.errors.base_error import BaseError
from ninja.errors import ValidationError

api = NinjaAPI(title="Rural Producers API")


@api.exception_handler(BaseError)
def handling_base_error(request: HttpRequest, exception: BaseError):
    return api.create_response(
        request=request,
        data=exception.to_dict(),
        status=exception.status.value,
    )


@api.exception_handler(ValidationError)
def handling_base_error(request: HttpRequest, exception: ValidationError):
    return api.create_response(request=request, data=exception.errors, status=400)


api.add_router("/rural-producers", "api.views.rural_producer_view.router")
api.add_router("/dashboard", "api.views.dashboard_view.router")

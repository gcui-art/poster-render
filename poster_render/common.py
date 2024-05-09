from enum import Enum

from pydantic import BaseModel


class BizCode(Enum):
    OK = 0


class HttpResponse(BaseModel):
    code: int
    data: object


def response_ok(data: object) -> HttpResponse:
    return HttpResponse(code=BizCode.OK.value, data=data)

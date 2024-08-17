from fastapi import Request
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.responses import JSONResponse

class AuthenticationMiddleware(BaseHTTPMiddleware):
    def __init__(self, app, instagram_service):
        super().__init__(app)
        self.instagram_service = instagram_service

    async def dispatch(self, request: Request, call_next):
        if request.url.path == "/v1/api/media_likers":
            username = request.query_params.get("username")
            if not username or not self.instagram_service.get_client(username):
                return JSONResponse(
                    status_code=401,
                    content={"message": "Authentication required. Please login first using the /v1/api/login endpoint."}
                )
        response = await call_next(request)
        return response

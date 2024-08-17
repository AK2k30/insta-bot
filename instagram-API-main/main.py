from fastapi import FastAPI, HTTPException, Query
from fastapi.responses import JSONResponse
from starlette.middleware import Middleware
from time_middleware import TimeoutMiddleware
from typing import Optional
from pydantic import BaseModel

# Import the functions from the other scripts
from profile_data import retrieve_profile_info
from user_post import retrieve_post_metrics
from media import get_post_details

# Import the Instagram service
from instagram_service import instagram_service
from authentication_middleware import AuthenticationMiddleware

class Credentials(BaseModel):
    username: str
    password: str

app = FastAPI(middleware=[
    Middleware(TimeoutMiddleware, timeout=600),
    Middleware(AuthenticationMiddleware, instagram_service=instagram_service)
])


@app.post('/v1/api/login')
def login(credentials: Credentials):
    try:
        username = instagram_service.login(credentials.username, credentials.password)
        return JSONResponse(content={"meassege": "Login Successful", "username": username})
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=str(e)
        )


@app.get('/v1/api/profile')
def profile_info(username: str = Query(..., description="Username of the profile to retrieve")):
    try:
        profile_data = retrieve_profile_info(username)
        if profile_data is None:
            raise HTTPException(status_code=404, detail="Profile not found")
        return JSONResponse(content=profile_data)
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# Still needs work
@app.get('/v1/api/user_posts')
def user_posts(
    username: str = Query(..., description="Username to retrieve posts for"),
    from_date: Optional[str] = Query(None, description="Start date for post retrieval (YYYY-MM-DD), Optional"),
    to_date: Optional[str] = Query(None, description="End date for post retrieval (YYYY-MM-DD), Optional")
):
    try:
        posts = retrieve_post_metrics(username, from_date, to_date)
        if not posts:
            raise HTTPException(status_code=404, detail="Posts for user not found")
        return JSONResponse(content=posts)
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))



@app.get('/v1/api/media')
def media_posts(url: str = Query(..., description="URL of the media to retrieve details for")):
    try:
        media_url = get_post_details(url)
        if media_url is None:
            raise HTTPException(status_code=404, detail="Media Info not found")
        return JSONResponse(content=media_url)
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))



@app.get('/v1/api/media_likers')
def media_likers(
    media_id: str = Query(..., description="media_id = {post_id}_{owner_id} to retrieve likers for the post"),
    username: str = Query(..., description="Username of the logged-in user")
):
    try:
        likers = instagram_service.get_media_likers(username, media_id)
        if not likers:
            raise HTTPException(
                status_code=404,
                detail="Likers for this media not found"
            )
        return JSONResponse(content=likers)
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=str(e)
        )

if __name__ == '__main__':
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000, log_level="debug")

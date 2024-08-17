from instagpy import InstaGPy
from typing import Optional

def retrieve_post_metrics(username: str, from_date: Optional[str] = None, to_date: Optional[str] = None):
    insta = InstaGPy()
    try:
        profile_dets = insta.get_profile_media(username, end_cursor=None, from_date=from_date, to_date=to_date, total=None, pagination=True)
        return profile_dets
    except Exception as e:
        raise Exception(f"An error occurred while retrieving posts: {str(e)}")

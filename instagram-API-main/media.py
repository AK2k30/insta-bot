import instaloader

def get_post_details(post_url: str):
    # Create an instance of Instaloader
    loader = instaloader.Instaloader()

    try:
        # Get details of the post
        post = instaloader.Post.from_shortcode(loader.context, post_url.split("/")[-2])
        
        post_date_human_readable = post.date.strftime("%A, %Y-%m-%d %H:%M:%S")
        
        # Extract post details
        post_details = {
            'Media_id': post.mediaid,
            'shortcode': post.shortcode,
            'author':{
                'unquiID': post.owner_username,
                'owner_ID': post.owner_id,
                
            },
            'Stats':{
                'Likes': post.likes,
                'Comments': post.comments,
                "caption": post.caption,
                "caption_mentions": post.caption_mentions,
                "caption_hashtag": post.caption_hashtags,
            },
            'Post_type': post.typename,
            'Post_date': post_date_human_readable,
            'is_pinned': post.is_pinned,
            'is_sponsored': post.is_sponsored,
            'Location': post.location,
            'Video': {
                'is_video': post.is_video,
                'Duration': post.video_duration,
                'Video_url': post.video_url,
                'View_count': post.video_view_count
            }
        }

        return post_details

    except instaloader.exceptions.InvalidArgumentException:
        return {'error': "Invalid Instagram URL"}
    except instaloader.exceptions.ProfileNotExistsException:
        return {'error': "Profile does not exist"}
    except instaloader.exceptions.PostTooRecentException:
        return {'error': "The post is too recent, Instaloader cannot fetch it yet"}
    except instaloader.exceptions.ConnectionException as e:
        return {'error': f"Connection error: {e}"}
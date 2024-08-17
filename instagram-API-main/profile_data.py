import instaloader
import re

# Function to retrieve profile information
def retrieve_profile_info(username: str):
    # Create an instance of Instaloader
    loader = instaloader.Instaloader()

    try:
        # Load the profile
        profile = instaloader.Profile.from_username(loader.context, username)

        # Access profile details
        biography = profile.biography
        
        # Regex patterns for emails and phone numbers
        email_pattern = r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}'
        phone_pattern = r'\+?\d[\d -]{8,12}\d'
        
        # Find all matches
        emails = re.findall(email_pattern, biography)
        phone_numbers = re.findall(phone_pattern, biography)
        
        # Access profile details
        profile_info = {
            'user_info':{
                'uniqueID': profile.userid,
                'Username': profile.username,
                'Full_Name': profile.full_name,
                'Followers': profile.followers,
                'Following': profile.followees,
                'Bio': profile.biography,
                'Bio_hashtags': profile.biography_hashtags,
                'Bio_mentions': profile.biography_mentions,
                'Number_of_Posts': profile.mediacount,
                'External_URL': profile.external_url,
            },
            'Contact_info': {
                'Emails': emails,
                'Phone_numbers': phone_numbers
            }
        }

        return profile_info

    except instaloader.exceptions.ProfileNotExistsException:
        return None

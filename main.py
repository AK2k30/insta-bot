from flask import Flask, render_template, request, abort
import requests
import json
import logging
from logging.handlers import RotatingFileHandler

app = Flask(__name__)

# Set up logging
handler = RotatingFileHandler('app.log', maxBytes=10000, backupCount=1)
handler.setLevel(logging.INFO)
app.logger.addHandler(handler)
app.logger.setLevel(logging.INFO)

def nFormatter(num):
    if num >= 1000000000:
        return f"{num/1000000000:.1f}G".rstrip('0').rstrip('.')
    if num >= 1000000:
        return f"{num/1000000:.1f}M".rstrip('0').rstrip('.')
    if num >= 1000:
        return f"{num/1000:.1f}K".rstrip('0').rstrip('.')
    return str(num)

def fetch_instagram_data(username):
    url = f"https://reeteshghimire.com.np/instagram-api/?user={username}"
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()  # Raises an HTTPError for bad responses
        return response.json()
    except requests.exceptions.RequestException as e:
        app.logger.error(f"Error fetching data from API: {str(e)}")
        return None
    except json.JSONDecodeError as e:
        app.logger.error(f"Error decoding JSON: {str(e)}")
        app.logger.error(f"Raw response: {response.text}")
        return None

@app.route('/')
def index():
    user = request.args.get('user', '')
    if user:
        data = fetch_instagram_data(user)
        if data is None:
            app.logger.warning(f"Failed to fetch data for user: {user}")
            return render_template('error.html', message="Unable to fetch Instagram data. Please try again later.")
        
        try:
            user_data = data['graphql']['user']
            posts = user_data['edge_owner_to_timeline_media']['edges']
            
            formatted_posts = []
            for post in posts:
                formatted_posts.append({
                    'url': post['node']['display_url'],
                    'likes': nFormatter(post['node']['edge_liked_by']['count']),
                    'comments': nFormatter(post['node']['edge_media_to_comment']['count'])
                })
            
            return render_template('profile.html',
                profile_pic=user_data['profile_pic_url'],
                name=user_data['full_name'],
                biography=user_data['biography'],
                username=user_data['username'],
                number_of_posts=user_data['edge_owner_to_timeline_media']['count'],
                followers=nFormatter(user_data['edge_followed_by']['count']),
                following=nFormatter(user_data['edge_follow']['count']),
                posts=formatted_posts
            )
        except KeyError as e:
            app.logger.error(f"KeyError when processing data: {str(e)}")
            app.logger.error(f"Received data structure: {data}")
            return render_template('error.html', message="Error processing Instagram data. Please try again later.")
    
    return render_template('index.html')

@app.errorhandler(404)
def page_not_found(e):
    return render_template('error.html', message="Page not found"), 404

@app.errorhandler(500)
def internal_server_error(e):
    app.logger.error(f"Internal Server Error: {str(e)}")
    return render_template('error.html', message="Internal server error. Please try again later."), 500

if __name__ == '__main__':
    app.run(debug=True)
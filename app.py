from flask import Flask, render_template, request, jsonify
import instaloader

app = Flask(__name__)

# Initialize Instaloader
L = instaloader.Instaloader()

# Function to extract the media URL from an Instagram URL (Posts & Reels)
def get_instagram_media_url(instagram_url):
    try:
        # Determine if it's a Post or Reel
        if '/p/' in instagram_url:
            shortcode = instagram_url.split('/p/')[1].split('/')[0]
        elif '/reel/' in instagram_url:
            shortcode = instagram_url.split('/reel/')[1].split('/')[0]
        else:
            return None  # If not a Post or Reel URL, return None

        # Load the post/reel using instaloader
        post = instaloader.Post.from_shortcode(L.context, shortcode)
        
        # Check if the post is a video or an image and return the media URL
        if post.is_video:
            return post.video_url
        else:
            return post.url
    except Exception as e:
        return None

# Route for serving the homepage (index.html)
@app.route('/')
def index():
    return render_template('index.html')

# Route for handling the download logic
@app.route('/download')
def download():
    instagram_url = request.args.get('url')

    if not instagram_url:
        return jsonify({'success': False, 'message': 'URL is required'})

    # Get the media URL from the Instagram URL
    media_url = get_instagram_media_url(instagram_url)

    if media_url:
        return jsonify({'success': True, 'download_url': media_url})
    else:
        return jsonify({'success': False, 'message': 'Could not fetch media from this URL'})

if __name__ == '__main__':
    app.run(debug=True)


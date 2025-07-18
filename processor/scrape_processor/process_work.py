import logging

from .utils import utc_to_str
from .comment_logic import extract_comments

def parse_json(json_content):
    """Process the JSON content to extract post details and comments."""
    def extract_post_media_urls(post): 
        """Extract image and video URLs from the post. 
        With gemini's help, we keep just the highest resolution."""
        image_urls = []
        video_urls = []
        # 1. url_overridden_by_dest (main image or video page)
        if post.get('url_overridden_by_dest'):
            url = post['url_overridden_by_dest']
            if any(url.lower().endswith(ext) for ext in ['.jpg', '.jpeg', '.png', '.gif', '.webp']):
                image_urls.append(url)
            # If it's a v.redd.it link, we ignore it here and handle the direct video below
        # 2. media_metadata (only highest resolution)
        media_metadata = post.get('media_metadata')
        if media_metadata and isinstance(media_metadata, dict):
            for media in media_metadata.values():
                if 's' in media and 'u' in media['s']:
                    url = media['s']['u'].replace('&amp;', '&')
                    if url not in image_urls:
                        image_urls.append(url)
        # 3. gallery_data (order of images in gallery, only highest resolution)
        gallery_data = post.get('gallery_data')
        if gallery_data and 'items' in gallery_data:
            for item in gallery_data['items']:
                media_id = item.get('media_id')
                if media_id and media_metadata and media_id in media_metadata:
                    media = media_metadata[media_id]
                    if 's' in media and 'u' in media['s']:
                        url = media['s']['u'].replace('&amp;', '&')
                        if url not in image_urls:
                            image_urls.append(url)
        # 4. reddit_video (direct video file)
        reddit_video = None
        if post.get('media') and post['media'].get('reddit_video'):
            reddit_video = post['media']['reddit_video']
        elif post.get('secure_media') and post['secure_media'].get('reddit_video'):
            reddit_video = post['secure_media']['reddit_video']
        if reddit_video and reddit_video.get('fallback_url'):
            video_url = reddit_video['fallback_url']
            if video_url not in video_urls:
                video_urls.append(video_url)
        return image_urls, video_urls

    post = json_content[0]['data']['children'][0]['data']
    post_dict = {
        'number': "",
        'subreddit': post.get('subreddit_name_prefixed'),
        'author': post.get('author'),   
        'title': post.get('title'),
        'body': post.get('selftext'),
        'created_at': utc_to_str(post.get('created_utc')),
        'score': post.get('score'),
    }
    image_urls, video_urls = extract_post_media_urls(post)
    if image_urls:
        post_dict['image_urls'] = image_urls
        logging.info(f"Extracted {len(image_urls)} image URL(s) from post by {post.get('author')}")
    if video_urls:
        post_dict['video_urls'] = video_urls
        logging.info(f"Extracted {len(video_urls)} video URL(s) from post by {post.get('author')}")
    post_dict['comments'] = extract_comments(json_content[1]['data']['children'])
    logging.info(f"Processed post: {post.get('title')} by {post.get('author')}")
    return post_dict
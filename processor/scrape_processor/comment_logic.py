import logging
from .utils import utc_to_str

def extract_media_urls_from_comment(comment_data):
    """Extract all image URLs from media_metadata and body, always replace &amp; with &. Returns a list."""
    image_urls = []
    media_metadata = comment_data.get('media_metadata')
    if media_metadata and isinstance(media_metadata, dict):
        for media in media_metadata.values():
            # Only add the highest resolution (source/original)
            if 's' in media and 'u' in media['s']:
                url = media['s']['u'].replace('&amp;', '&')
                if url not in image_urls:
                    image_urls.append(url)
    # Extract all valid image URLs from the comment body
    if comment_data.get('body'):
        import re
        urls = re.findall(r'(https?://\S+)', comment_data['body'])
        for url in urls:
            comment_data['body'] = comment_data['body'].replace(url, "")
            url = url.replace('&amp;', '&')
            if (
                'preview.redd.it' in url or 'i.redd.it' in url or
                any(url.lower().endswith(ext) for ext in ['.jpg', '.jpeg', '.png', '.gif', '.webp'])
            ):
                # Only add unique URLs
                if url not in image_urls:
                    image_urls.append(url)
    if image_urls:
        logging.info(f"Extracted {len(image_urls)} image URL(s) from comment by {comment_data.get('author')}")
    return image_urls

def extract_comments(children):
    """Recursively extract comments and their replies from the JSON structure."""
    comments = []
    for child in children:
        if child['kind'] == 't1':  # 't1' indicates a comment
            comment_data = child['data']
            replies = comment_data.get('replies')
            if isinstance(replies, dict):
                replies_list = extract_comments(replies.get('data', {}).get('children', []))
            else: # if replies is empty
                replies_list = []
            image_urls = extract_media_urls_from_comment(comment_data)
            comment = {
                'author': comment_data.get('author'),
                'body': comment_data.get('body').replace('&amp;', '&'),
                'created_at': utc_to_str(comment_data.get('created_utc')),
                'score': comment_data.get('score'),
            }
            if image_urls:
                comment['image_urls'] = image_urls
            comment['replies'] = replies_list
            comments.append(comment)
            logging.info(f"Processed comment by {comment_data.get('author')}, score: {comment_data.get('score')}")
    return comments

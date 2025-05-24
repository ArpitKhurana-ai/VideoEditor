import re
from datetime import datetime

def validate_youtube_url(url):
    """Validate a YouTube URL"""
    youtube_regex = (
        r'(https?://)?(www\.)?'
        r'(youtube|youtu|youtube-nocookie)\.(com|be)/'
        r'(watch\?v=|embed/|v/|.+\?v=)?([^&=%\?]{11})')
    
    youtube_match = re.match(youtube_regex, url)
    return youtube_match is not None

def validate_timestamp(timestamp):
    """Validate a timestamp in the format HH:MM:SS"""
    try:
        datetime.strptime(timestamp, "%H:%M:%S")
        return True
    except ValueError:
        return False

def validate_input(data):
    """Validate the input data for the process endpoint"""
    errors = []
    
    # Required fields
    required_fields = ['url', 'start', 'end', 'row_id']
    for field in required_fields:
        if field not in data:
            errors.append(f"Missing required field: {field}")
    
    # If any required fields are missing, return errors
    if errors:
        return False, errors
    
    # Validate YouTube URL
    if not validate_youtube_url(data['url']):
        errors.append("Invalid YouTube URL")
    
    # Validate start and end timestamps
    if not validate_timestamp(data['start']):
        errors.append("Invalid start time format, expected HH:MM:SS")
    
    if not validate_timestamp(data['end']):
        errors.append("Invalid end time format, expected HH:MM:SS")
    
    # Validate row_id (filename)
    if not re.match(r'^[a-zA-Z0-9_-]+$', data['row_id']):
        errors.append("Invalid row_id format. Use only letters, numbers, underscores, and hyphens.")
    
    return len(errors) == 0, errors

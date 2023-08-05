IMAGE = [".png", ".jpg", ".jpeg", ".gif", ".svg"]
VIDEO = [".mp4", ".avi", ".wmv"]
AUDIO = [".mp3", ".wav", ".ogg"]
DOCUMENTS = [".txt", ".pdf"]
# category for json and stuff? programming? .py .js etc


def get_category(ext):
    if ext in IMAGE:
        return "image"
    if ext in AUDIO:
        return "audio"
    if ext in VIDEO:
        return "video"
    if ext in DOCUMENTS:
        return "document"
    return "other"

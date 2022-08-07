from enum import Enum
class MediaType(Enum):
    none = 0
    photo = 1
    document = 2
    video = 3
    audio = 4

    @staticmethod
    def FromEvent(event):
        if event.photo:
            return MediaType.photo
        elif event.audio or event.voice:
            return MediaType.audio
        elif event.video:
            return MediaType.video
        elif event.document:
            return MediaType.document
        return MediaType.none



class Media:
    def __init__(self, name, _type : MediaType, path):
        self.name = name
        self.type = _type
        self.path = path
    
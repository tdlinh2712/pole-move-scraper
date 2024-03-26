from dataclasses import dataclass

@dataclass

class RoutineInfo:
    class_name: str = ""
    song_name: str = ""
    artist: str = ""
    def __init__(self, class_name: str, song_name: str, artist: str):
        self.class_name = class_name
        self.song_name = song_name
        self.artist = artist

    def toIterable(self):
        return iter(
            [
                self.class_name,
                self.song_name,
                self.artist
            ]
        )

    def toHeader(self):
        return [
            "Class",
            "Song",
            "Artist",
        ]

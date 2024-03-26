from dataclasses import dataclass

@dataclass

class PoleMove:
    name: str = ""
    img_src: str = ""
    difficulty: str = ""
    def __init__(self, name: str, img_src: str, difficulty: str):
        self.name = name
        self.img_src = img_src
        self.difficulty = difficulty

    def toIterable(self):
        return iter(
            [
                self.name,
                self.difficulty,
                self.img_src
            ]
        )

    def toHeader(self):
        return [
            "name",
            "difficulty",
            "img_src",
        ]

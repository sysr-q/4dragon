# -*- coding: utf-8 -*-
import random

class Boss(object):
    elements = ["fire", "earth", "water", "ice", "electric"]
    healths = {
        "noob": int(1e4),
        "easy": int(12e3),
        "medium": int(16e3),
        "hard": int(20e3),
    }
    def __init__(self, name=None, difficulty=None, element=None, health=None):
        if name is None:
            self.name = "Dragon Overlord"
        else:
            self.name = name.replace("_", " ")
        if difficulty is None:
            self.difficulty = "medium"
        else:
            self.difficulty = difficulty
        if element is None or element == "random":
            self.element = random.choice(self.elements)
        else:
            self.element = element
        if health is None:
            self.health = self.healths[self.difficulty]
        else:
            self.health = int(health)

    def __repr__(self):
        return "Boss(name={0!r}, difficulty={1!r}, element={2!r}, health={3!r})".format(
            self.name,
            self.difficulty,
            self.element,
            self.health
        )

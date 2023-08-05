import inspect
import os

from sfml import sf

from ..reslib import Res
from ..data.game_obj import GameObject


class Logger(GameObject):
    @classmethod
    def log(cls, *args):
        line = inspect.stack()[1][2]
        path = inspect.stack()[1][1].split(os.sep)
        file = path[-2]+'/'+path[-1]
        metadata = '[' + str(line) + '|' + file + ']'
        while len(metadata) < 25:
            metadata += ' '
        if cls.game.debug:
            print(metadata, end=" ")
            for arg in args:
                print(arg, end=" ")
            print()


class DebugText(sf.Text):
    def __init__(self, instance: object, attr_name: str, position: tuple, float_round=2):
        super().__init__()
        self.obj_instance = instance
        self.attr_name = attr_name
        self._float_round = float_round
        self.string = attr_name+" : "+str(getattr(instance, attr_name))
        self.font = Res.Fonts.arial
        self.character_size = 16
        self.color = sf.Color.WHITE
        self.position = position

    def update(self):
        value = getattr(self.obj_instance, self.attr_name)
        if isinstance(value, float):
            value = round(value, self._float_round)
        elif isinstance(value, sf.Vector2):
            value = (round(value.x, self._float_round), round(value.y,self._float_round))
        self.string = self.attr_name+" : "+str(value)


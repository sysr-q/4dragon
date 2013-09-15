# -*- coding: utf-8 -*-
# Why "heroes" and not "classes"? Because I didn't want
# to have anything too close to the word "class".
import inspect
import re

class Hero(object):
    _match = r"^$"  # So we don't match anyone

    def __init__(self, id=None, **kwargs):
        self.id = id
        for k, v in kwargs.iteritems():
            self.__dict__[k] = v
    
    def __repr__(self):
        parts = ["{0}={1}".format(n, repr(v))
                 for n, v
                 in inspect.getmembers(self)
                 if not n.startswith("_") and not inspect.ismethod(v)]
        return "{0}({1})".format(
            self.__class__.__name__,
            ", ".join(parts)
        )

    @classmethod
    def from_id(cls, id_):
        """ Here be dragons!

            Returns the Hero class a particular id should be.
            Uses funky python black magic to loop through all subclasses,
            matches against their regex and returns the class.
        """
        others = None
        for subcls in cls.__subclasses__():
            # Hopefully only *one* child class sets _match=None
            if subcls._match is None:
                others = subcls
                continue
            if re.search(subcls._match, id_):
                return subcls
        if others is not None:
            return others
        return cls

## Support

class Healer(Hero):
    _match = r"^[0-9]"

class Bard(Hero):
    _match = r"^[AEIOUaeiou]"

## Damage

class Warlock(Hero):
    _match = r"^[WRLCKwrlck]"

class Knight(Hero):
    _match = None

class Ranger(Hero):
    _match = r"^[XYZxyz]"

## Special

# We put this guy above Paladin/DeathKnight since it's
# a more exact regex, so we'd prefer to match it first.
class DragonBorn(Hero):
    _match = r"^[/+].+[/+]$"

class Paladin(Hero):
    _match = r"^[/+]"

class DeathKnight(Hero):
    _match = r"[/+]$"

class Plebeian(Hero):
    _match = r"^Heaven$"

__all__ = ["Hero", "Healer", "Bard", "Warlock",
           "Knight", "Ranger", "Paladin", "DeathKnight",
           "DragonBorn", "Plebeian"]

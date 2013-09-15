# -*- coding: utf-8 -*-
import fourch
import fourdragon
import re

""" THIS IS HOW I'D LIKE THE MODULE TO WORK:

>>> r = Raid("123456789", verbose=True)
Found Boss(name=$name, type=$type, element=$element, difficulty=$difficulty, hp=$hp)
>>> r.sync()
Found Bard(id=$id, )  # unsure what Bards will have
Found Knight(id=$id, )  # same here
Knight(id=$id, ) hit the beast for $n!
Found Healer(id=$id, )
>>> r.sync()
Healer(id=$id, ) revived Knight(id=$id, ).
>>> r.events
# Just a list of things that's happened:
[{"text": "Found boss blah blah", ...},
 {"text": "Found Bard $id blah", ...},
 {"text": "Found Knight $id blah", ...},
 ...]
"""

class Raid(object):
    min_roll = 11  # less than this: you die
    max_revive_times = 6
    max_avenge_times = 6

    def __init__(self, thread, verbose=False):
        if verbose:
            self.thread = thread
        else:
            self.thread = fourch.board("b").thread(thread)
        self.verbose = verbose
        self.boss = None
        self._post_dead = False
        self._fetch()

    def sync(self):
        pass

    def _parse_command(self, name, matcher, comment, flags=re.I):
        r = "{0}@{1}".format(name, matcher)
        search = re.search(r, comment, flags=flags)
        if search:
            return search.group(1)
        return None

    def _fetch(self):
        """ Pulls the OP comment from the thread and sets up required
            variables (read: the boss) from the post.
        """
        if self.verbose:
            op = "blah\nBLAH BLAH: difficulty@noob\nname@SomeDude\nelement@random"
        else:
            op = self.thread.op.comment_text
        boss = {
            "difficulty": self._parse_command("difficulty", r"(noob|easy|medium|hard)", op),
            "name": self._parse_command("name", r"(\w+)", op),
            "element": self._parse_command("element", r"(random|fire|earth|water|ice|electric)", op),
            "health": self._parse_command("health", r"(\d+)", op)
        }
        self.boss = fourdragon.Boss(**boss)

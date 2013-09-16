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

    def __init__(self, thread, board="q", verbose=False, debug=False):
        self.thread = fourch.board(board).thread(thread)
        self.verbose = verbose
        self.debug = debug
        self.boss = None
        self._post_dead = False
        self._fresh = True
        self._fetch()
        self.heroes = {}
        self.events = []

    def sync(self):
        # Post/Boss is dead.
        if not self.thread.alive or self.boss.health <= 0:
            return
        new = self.thread.update()
        if not self._fresh and new == 0:
            return
        if self._fresh:
            self._fresh = False
        # Slice [-new:] so we just iterate the new posts.
        for post in self.thread.replies[-new:]:
            hero = self.hero(post)
            if hero.dead and not hero.can_attack_when_dead:
                # YOU'RE DEAD, DON'T EVEN TRY THAT CRAP.
                continue
            # TODO: Bard bonus~?

    def hero(self, post, **kwargs):
        if post.id not in self.heroes:
            hero = fourdragon.Hero.from_id(post.id)(**kwargs)
            self.heroes[post.id] = hero
        else:
            hero = self.heroes[post.id]
        nickname = self._parse_command("nickname", r"(\w{,14})", post.comment_text)
        if nickname is not None:
            hero.nickname = nickname
        post.roll = self.roll(post.number, 2)
        hero.posts.append(post)
        return hero

    def roll(self, no, n):
        """TODO: improve this.
        """
        r = int(str(no)[-n:])
        while r == 0:
            n += 1
            r = int(str(no)[-n:])
        return r

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
        if self.debug:
            op = ("It's dragon slaying time, bitches!\n"
                  "SOME INFO BOUT DIS DRAGON:\n"
                  "difficulty@noob\n"
                  "name@SomeDude\n"
                  "element@random")
        else:
            op = self.thread.op.comment_text
        boss = {
            "difficulty": self._parse_command("difficulty", r"(noob|easy|medium|hard)", op),
            "name": self._parse_command("name", r"(\w+)", op),
            "element": self._parse_command("element", r"(random|fire|earth|water|ice|electric)", op),
            "health": self._parse_command("health", r"(\d+)", op)
        }
        self.boss = fourdragon.Boss(**boss)

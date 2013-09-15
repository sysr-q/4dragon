# -*- coding: utf-8 -*-
import fourch

"""
>>> r = Raid("123456789", verbose=True)
Found Boss(name=$name, type=$type, element=$element, difficulty=$difficulty, hp=$hp)
>>> r.sync()
Found Bard(id=$id, )
Found Knight(id=$id, )
"""

class Raid(object):
    def __init__(self, thread, verbose=False):
        self.thread = thread
        self.verbose = verbose
        self._post_dead = False
        self._fetch()

    def sync(self):
        pass

    def _fetch(Self):
        """ Pulls the OP comment from the thread and sets up required
            variables from the post.
        """
        pass

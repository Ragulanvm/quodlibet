# Copyright 2012 Christoph Reiter
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License version 2 as
# published by the Free Software Foundation

from tests import TestCase

from quodlibet.qltk.edittags import *
from quodlibet.formats._audio import AudioFile
from quodlibet.library import SongLibrary
import quodlibet.config


class TEditTags(TestCase):
    def setUp(self):
        quodlibet.config.init()

    def tearDown(self):
        quodlibet.config.quit()

    def test_items(self):
        SplitValues("foo", "bar").destroy()
        SplitDisc("foo", "bar").destroy()
        SplitTitle("foo", "bar").destroy()
        SplitArranger("foo", "bar").destroy()

    def test_addtag_dialog(self):
        lib = SongLibrary()
        AddTagDialog(None, ["artist"], lib).destroy()


class GroupSong(AudioFile):

    def __init__(self, can_multiple):
        self._can_multiple = can_multiple

    def can_multiple_values(self, key=None):
        if key is None:
            return self._can_multiple
        if self._can_multiple is True:
            return True
        return key in self._can_multiple


class TAudioFileGroup(TestCase):

    def test_multiple_values(self):
        group = AudioFileGroup([GroupSong(True), GroupSong(True)])
        self.assertTrue(group.can_multiple_values() is True)
        self.assertTrue(group.can_multiple_values("foo") is True)

        group = AudioFileGroup([GroupSong(["ha"]), GroupSong(True)])
        self.assertEqual(group.can_multiple_values(), set(["ha"]))
        self.assertFalse(group.can_multiple_values("foo"))
        self.assertTrue(group.can_multiple_values("ha"))

        group = AudioFileGroup([GroupSong(["foo", "ha"]), GroupSong(["ha"])])
        self.assertEqual(group.can_multiple_values(), set(["ha"]))
        self.assertFalse(group.can_multiple_values("foo"))
        self.assertTrue(group.can_multiple_values("ha"))

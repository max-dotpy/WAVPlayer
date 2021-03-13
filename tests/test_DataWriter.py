from wavPlayer.DataWriter import DataWriter
from wavPlayer.constants import MOCKING_COLLECTED_DATA_PATH, MOCKING_PLAYLIST_DATA_PATH
from os.path import exists
from os import remove
import json
import unittest


class testDataWriter(unittest.TestCase):
    def setUp(self):
        self.dataWriter = DataWriter(MOCKING_PLAYLIST_DATA_PATH, MOCKING_COLLECTED_DATA_PATH)

    @classmethod
    def tearDownClass(cls):
        remove(MOCKING_PLAYLIST_DATA_PATH)
        remove(MOCKING_COLLECTED_DATA_PATH)

    def test___init__(self):
        self.assertTrue(
            exists(MOCKING_COLLECTED_DATA_PATH) and exists(MOCKING_PLAYLIST_DATA_PATH),
            msg="DataWriter failed to create the json files.")

    def test_saveData(self):
        self.dataWriter.collectedData["Playlists data"]["(DELETED) Example of deleted playlist"] = "Correct output"
        self.dataWriter.playlistsData["(DELETED) Example of deleted playlist"] = "Correct output"
        self.dataWriter.saveData()

        with open(MOCKING_COLLECTED_DATA_PATH) as file:
            collectedData = json.load(file)
        output = collectedData["Playlists data"]["(DELETED) Example of deleted playlist"]
        self.assertEqual("Correct output", output)

        with open(MOCKING_PLAYLIST_DATA_PATH) as file:
            playlistData = json.load(file)
        output = playlistData["(DELETED) Example of deleted playlist"]
        self.assertEqual("Correct output", output)

    def test_changeNameOfPlaylist(self):
        self.dataWriter.changeNameOfPlaylist("All", "New name")

        with open(MOCKING_PLAYLIST_DATA_PATH) as file:
            playlistData = json.load(file)

        self.assertFalse("All" in playlistData)
        self.assertTrue("New name" in playlistData)
        self.assertRaises(ValueError, self.dataWriter.changeNameOfPlaylist, "Non existent playlist", "Something")


if __name__ == '__main__':
    unittest.main()

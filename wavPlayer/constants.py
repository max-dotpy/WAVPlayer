from pathlib import Path
from os.path import split, join


BASE_DIRECTORY = split(split(Path(__file__))[0])[0]
WAV_DIRECTORY_PATH = join(BASE_DIRECTORY, "wavFiles")
USERDATA_PATH = join(BASE_DIRECTORY, "userData")
PLAYLISTS_DATA_PATH = join(USERDATA_PATH, "playlistsData.json")
COLLECTED_DATA_PATH = join(USERDATA_PATH, "collectedData.json")
ICONS_PATH = join(BASE_DIRECTORY, "resources", "icons")

# Paths needed for tests
MOCKING_WAV_PATH = join(BASE_DIRECTORY, "resources", "mockingWavFiles", "sampleForTests.wav")
MOCKING_PLAYLIST_DATA_PATH = join(BASE_DIRECTORY, "resources", "mockingUserData", "playlistsData.json")
MOCKING_COLLECTED_DATA_PATH = join(BASE_DIRECTORY, "resources", "mockingUserData", "collectedData.json")

# GUI dimensions
GUI_HEIGHT = 260
GUI_WIDTH = 710
GUI_LEFTSIDE_WIDTH = 210
GUI_RIGHTSIDE_WIDTH = GUI_WIDTH - GUI_LEFTSIDE_WIDTH
GUI_X_OFFSET = 720
GUI_Y_OFFSET = 100

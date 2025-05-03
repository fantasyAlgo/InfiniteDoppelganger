import pyray as rl
from Settings import *

class MusicHandler:
    def __init__(self) -> None:
        self.soundEffects = {}
        def load_sound(name, path, volume=0.4):
            sound = rl.load_sound(path)
            rl.set_sound_volume(sound, volume)
            self.soundEffects[name] = sound

        self.backgroundMusic = rl.load_music_stream(str(baseDir / "music" / "part2.wav"))
        self.inGameMusic = rl.load_music_stream(str(baseDir / "music" / "part3.wav"))
        load_sound("arrow", str(baseDir / "music" /         "arrowWent2.wav"), 0.3)
        load_sound("gameOver", str(baseDir / "music" /       "gameOver2.wav"), 0.6)
        load_sound("whoosh", str(baseDir / "music" /            "whoosh.mp3"), 0.2)
        load_sound("damage", str(baseDir / "music" /       "damageSound.mp3"), 0.4)
        load_sound("shoutout", str(baseDir / "music" /        "shoutout.wav"), 0.8)
        self.currentSong = 0
        rl.set_music_volume(self.backgroundMusic, 0.5)
        rl.set_music_volume(self.inGameMusic, 0.5)

        rl.play_music_stream(self.backgroundMusic)
    def stopUIAndPlay(self):
        #rl.stop_audio_stream(self.backgroundMusic)
        self.currentSong = 1
        rl.play_music_stream(self.inGameMusic)
    def add(self, name):
        rl.play_sound(self.soundEffects[name])

    def addGameOver(self):
        self.add("gameOver")
        self.currentSong = 2



    def update(self):
        if self.currentSong == 0:
            rl.update_music_stream(self.backgroundMusic)
        elif self.currentSong == 1:
            rl.update_music_stream(self.inGameMusic)

        timePlayed = rl.get_music_time_played(self.backgroundMusic)/rl.get_music_time_length(self.backgroundMusic);
        if (timePlayed > 1.0):
            timePlayed = 1.0;

        #Lo§adMusicStream("resources/country.mp3");


import pyray as rl
from Settings import *

class MusicHandler:
    def __init__(self) -> None:
        self.backgroundMusic = rl.load_music_stream(str(baseDir / "music" / "part2.wav"))
        self.inGameMusic = rl.load_music_stream(str(baseDir / "music" / "part3.wav"))
        self.arrowSound = rl.load_sound(str(baseDir / "music" / "arrowWent2.wav"))
        self.gameOverSound = rl.load_sound(str(baseDir / "music" / "gameOver2.mp3"))
        self.whooshSound = rl.load_sound(str(baseDir / "music" / "whoosh.mp3"))
        self.damageSound = rl.load_sound(str(baseDir / "music" / "damageSound.mp3"))
        self.currentSong = 0
        rl.set_music_volume(self.backgroundMusic, 0.5)
        rl.set_music_volume(self.inGameMusic, 0.5)
        rl.set_sound_volume(self.whooshSound, 0.2)
        rl.set_sound_volume(self.damageSound, 0.4)

        rl.play_music_stream(self.backgroundMusic)
    def stopUIAndPlay(self):
        #rl.stop_audio_stream(self.backgroundMusic)
        self.currentSong = 1
        rl.play_music_stream(self.inGameMusic)
    def addArrow(self):
        rl.play_sound(self.arrowSound)
    def addGameOver(self):
        rl.play_sound(self.gameOverSound)
        self.currentSong = 2
    def addWhoosh(self):
        rl.play_sound(self.whooshSound)
    def addDamage(self):
        rl.play_sound(self.damageSound)



    def update(self):
        if self.currentSong == 0:
            rl.update_music_stream(self.backgroundMusic)
        elif self.currentSong == 1:
            rl.update_music_stream(self.inGameMusic)

        timePlayed = rl.get_music_time_played(self.backgroundMusic)/rl.get_music_time_length(self.backgroundMusic);
        if (timePlayed > 1.0):
            timePlayed = 1.0;

        #Lo§adMusicStream("resources/country.mp3");


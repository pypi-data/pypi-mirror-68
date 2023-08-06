import simpleaudio as sa
import threading
import sys
import os
import subprocess
import wave


class WavFile:
    """
    Class contains parameters of sound file
    """
    def __init__(self, path):
        with wave.open(path, "rb") as f:
            self.width = f.getsampwidth()
            self.channels = f.getnchannels()
            self.rate = f.getframerate()
            self.frames = f.getnframes()
            self.data = f.readframes(self.frames)
            self.duration = float(self.frames) / self.rate


class WavPlayer:
    """
    Class load sounds from files and play sounds
    """
    def __init__(self):

        self._sounds = dict()
        self._sounds_files = dict()
        self._threads = []

        if sys.platform.startswith("linux"):
            self.play = self.__play_linux
        elif sys.platform.startswith("win"):
            import winsound
            self.winsound = winsound
            self.play = self.__play_win
        else:
            self.play = self.__play_sa

    def add_sound(self, file: str, name: str):
        """
        Function add sound to class from file
        :param file: filename with sound
        :param name: name of sound
        :return:
        """
        wave_obj = sa.WaveObject.from_wave_file(file)
        self._sounds[name] = wave_obj
        self._sounds_files[name] = file

    def stop(self):
        """
        Function stop thread with sound
        :return:
        """
        for th in self._threads:
            th.join()

    def __play_sa(self, sound_name: str):
        """
        Function play sound in another OS
        :param sound_name: name of sound in class
        :return:
        """
        def _play():
            self._sounds[sound_name].play()
        thread = threading.Thread(target=_play, args=())
        self._threads.append(thread)
        thread.start()

    def __play_win(self, sound_name: str):
        """
        Function play sound on windows
        :param sound_name: name of sound in class
        :return:
        """
        self.winsound.PlaySound(self._sounds_files[sound_name], self.winsound.SND_NOSTOP)

    def __play_linux(self, sound_name: str):
        """
        Function play sound on linux
        :param sound_name: name of sound in class
        :return:
        """
        proc = subprocess.Popen(['aplay', self._sounds_files[sound_name]])
        proc.wait()

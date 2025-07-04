# sound_manager.py
import pygame
import os
import config # Import config để truy cập các biến global

try:
    import winsound
except ImportError:
    winsound = None

class SoundManager:
    def __init__(self):
        try:
            pygame.mixer.init()
            self.mixer_initialized = True
        except pygame.error:
            self.mixer_initialized = False
            print("Cảnh báo: Không thể khởi tạo pygame.mixer.")

        self.can_use_winsound = (winsound is not None)
        self.sounds = {}
        self.music_path = None
        
        self.volume_music = config.DEFAULT_VOLUME_MUSIC
        self.volume_sfx = config.DEFAULT_VOLUME_SFX

        self.load_all_sounds()

    def load_all_sounds(self):
        sound_files = {
            'click': 'assets/sounds/click.mp3',
            'place': 'assets/sounds/place.mp3',
            'win': 'assets/sounds/win.mp3',
            'lose': 'assets/sounds/lose.mp3',
        }
        
        if self.mixer_initialized:
            for name, path in sound_files.items():
                if os.path.exists(path):
                    try:
                        self.sounds[name] = pygame.mixer.Sound(path)
                        self.sounds[name].set_volume(self.volume_sfx)
                        print(f"SoundManager: Đã tải '{path}' thành công.")
                    except pygame.error as e:
                        print(f"SoundManager: Lỗi khi tải file '{path}': {e}")
                else:
                    print(f"SoundManager: File '{path}' không tồn tại, sẽ dùng winsound (nếu có).")
        
        music_file_path = 'assets/sounds/music.mp3'
        if self.mixer_initialized and os.path.exists(music_file_path):
            self.music_path = music_file_path
            print(f"SoundManager: Đã tìm thấy nhạc nền '{self.music_path}'.")
        else:
            print("SoundManager: Không tìm thấy file nhạc nền.")

    def play(self, sound_name):
        if sound_name in self.sounds:
            self.sounds[sound_name].play()
        elif self.can_use_winsound:
            self._play_winsound(sound_name)

    def _play_winsound(self, sound_name):
        if sound_name == 'click': winsound.Beep(2500, 30)
        elif sound_name == 'place': winsound.Beep(800, 50)
        elif sound_name == 'win': winsound.Beep(1000, 100); winsound.Beep(1500, 100); winsound.Beep(2000, 200)
        elif sound_name == 'lose': winsound.Beep(800, 200); winsound.Beep(400, 300)

    def play_music(self):
        if self.music_path:
            try:
                pygame.mixer.music.load(self.music_path)
                pygame.mixer.music.set_volume(self.volume_music)
                pygame.mixer.music.play(-1)
            except pygame.error as e:
                print(f"SoundManager: Lỗi khi phát nhạc nền - {e}")

    def stop_music(self):
        if self.mixer_initialized:
            pygame.mixer.music.stop()

    def set_music_volume(self, volume):
        self.volume_music = max(0.0, min(1.0, volume))
        if pygame.mixer.music.get_busy():
            pygame.mixer.music.set_volume(self.volume_music)

    def set_sfx_volume(self, volume):
        self.volume_sfx = max(0.0, min(1.0, volume))
        if self.mixer_initialized:
            for sound in self.sounds.values():
                sound.set_volume(self.volume_sfx)

    def update_volumes(self):
        self.set_music_volume(self.volume_music)
        self.set_sfx_volume(self.volume_sfx)
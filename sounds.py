from pygame import mixer

mixer.init()

SOUND_GUESSED = mixer.Sound('data/sounds/guessed.wav')
SOUND_FAILED = mixer.Sound('data/sounds/failed.wav')
SOUND_NONE = mixer.Sound('data/sounds/none.wav')
SOUND_VICTORY = mixer.Sound('data/sounds/victory.wav')
SOUND_DEFEAT = mixer.Sound('data/sounds/defeat.wav')
SOUND_PENCIL = mixer.Sound('data/sounds/pencil.wav')
SOUND_ERASER = mixer.Sound('data/sounds/eraser.wav')

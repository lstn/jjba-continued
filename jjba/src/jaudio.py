import moviepy.editor as mp
from jjba.src import jutils

def get_meme_audio(freeze_time, tbc_duration):
    meme_audio = mp.AudioFileClip(jutils.PATHS.DATA.AUDIO.TBC_MP3)
    audiofreeze = mp.cvsecs('00:00:44.36')
    actual_audio = meme_audio.subclip(audiofreeze-freeze_time,audiofreeze+tbc_duration)
    return actual_audio
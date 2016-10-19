import moviepy.editor as mp
import time
import os
from jjba.src import jaudio, jutils, jfilters

def get_tfreeze(freeze_time):
    if freeze_time >= 60:
        raise Exception
    if freeze_time >= 10:
        tstr = '00:00:' + str(freeze_time)
    else:
        tstr = '00:00:0' + str(freeze_time)

    tfreeze = mp.cvsecs(tstr)
    return tfreeze

def extract_clip_av(file, freeze_time, clip_start, clip_end, audio_end):
    cut_tern = lambda d: [cut_clip(c, clip_start, clip_end) if (clip_start != 0.0 or clip_end is not "end") else c for c in [d["v"], d["a"]]]

    tfreeze = get_tfreeze(freeze_time)

    o_clips = {}
    o_clips["v"], o_clips["a"] = get_av_clips(file)

    if audio_end is not "end":
        o_clips["a"] = cut_clip(o_clips["a"], clip_start, audio_end - clip_start)

    new_vclip, new_aclip = cut_tern(o_clips)

    clip_before_tbc = cut_clip(new_vclip, tfreeze - freeze_time + clip_start, tfreeze - clip_start)

    return new_vclip, new_aclip, clip_before_tbc

def get_av_clips(file):
    video_clip = mp.VideoFileClip(file)
    audio_clip = mp.AudioFileClip(file)

    return video_clip, audio_clip

def cut_clip(clip, start, end):
    end = clip.duration if end is "end" else end
    end = clip.duration if end > clip.duration else end

    new_clip = clip.subclip(start, end)

    return new_clip

def overlay_meme_audio(clip_audio, freeze_time, tbc_duration):
    meme_audio = jaudio.get_meme_audio(freeze_time, tbc_duration)
    overlayed_audio = mp.CompositeAudioClip([meme_audio.volumex(1.2), clip_audio.volumex(0.6)])

    return overlayed_audio

def create_tbc_overlay_im(clip, tfreeze):
    im_freeze = clip.to_ImageClip(tfreeze)

    fade = clip.fx(mp.vfx.painting, saturation = 1.6,black = 0.006)
    fade = fade.fx(jfilters.gcolor_filt, RGB = [255/255, 211/255, 155/255]).to_ImageClip(tfreeze)

    olay_w = int(fade.w/3.7)
    print(olay_w)
    tbc_overlay = mp.ImageClip(jutils.PATHS.DATA.IMAGES.TBC_PNG).resize(width=olay_w)

    tbc_overlay = tbc_overlay.margin(bottom=int(fade.h/10), right=int(fade.w/10), opacity=0)
    tbc_overlay = tbc_overlay.set_position(('right','bottom'))

    return im_freeze, fade, tbc_overlay

def fade_freeze(im_freeze, fade, tbc_overlay, tbc_duration, fadein_duration):
    fade_fx = mp.CompositeVideoClip([fade, tbc_overlay]).add_mask().set_duration(tbc_duration).crossfadein(fadein_duration)
    faded_clip = mp.CompositeVideoClip([im_freeze, fade_fx])

    return faded_clip

def overlay_tbc_fade_clip(clip, tfreeze, tbc_duration, fadein_duration):
    im_freeze, fade, tbc_overlay = create_tbc_overlay_im(clip, tfreeze)
    faded_clip = fade_freeze(im_freeze, fade, tbc_overlay, tbc_duration, fadein_duration)

    return faded_clip

def concat_tbc_clip(clip, audio, tbc_fade, tbc_duration):
    tbc_clip = mp.concatenate_videoclips([ clip, tbc_fade.set_duration(tbc_duration) ])
    tbc_clip = tbc_clip.set_audio(audio)

    return tbc_clip

def save_clip(clip, bitrate, filename=None):
    if filename is None:
        filename = "{}.webm".format(int(time.time()))
    filepath = os.path.join(jutils.PATHS.OUTPUT_DIR, filename)

    clip.write_videofile(filepath, bitrate=bitrate)
    


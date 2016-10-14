import moviepy.editor as mp
import numpy as np
import sys
#from moviepy.video.fx.all import resize as mp_resize

def get_meme_audio(before_len, tbc_duration):
    meme_audio = mp.AudioFileClip("tbc.mp3")
    audiofreeze = mp.cvsecs('00:00:44.36')
    actual_audio = meme_audio.subclip(audiofreeze-before_len,audiofreeze+tbc_duration)
    return actual_audio

def main(argv):
    tbc_duration, before_len, file_to_tbc = parse_args(argv[1:])

    actual_audio = get_meme_audio(before_len, tbc_duration)

    clip_to_tbc = mp.VideoFileClip(file_to_tbc)
    clip_to_tbc_audio = mp.AudioFileClip(file_to_tbc)

    actual_audio = mp.CompositeAudioClip([actual_audio.volumex(1.2), clip_to_tbc_audio.volumex(0.6)])

    if before_len >= 60:
        raise Exception
    if before_len >= 10:
        tstr = '00:00:' + str(before_len)
    else:
        tstr = '00:00:0' + str(before_len)

    tfreeze = mp.cvsecs(tstr)
    
    clip_before = clip_to_tbc.subclip(tfreeze-before_len,tfreeze)

    im_freeze = clip_to_tbc.to_ImageClip(tfreeze)

    painting = clip_to_tbc.fx(mp.vfx.painting, saturation = 1.6,black = 0.006)
    painting = painting.fx(gcolor_filt, RGB = [255/255, 211/255, 155/255]).to_ImageClip(tfreeze)

    olay_w = int(painting.w/3.7)
    print(olay_w)
    tbc_overlay = mp.ImageClip("tbc.png").resize(width=olay_w)

    tbc_overlay = tbc_overlay.margin(bottom=int(painting.h/10), right=int(painting.w/10), opacity=0)
    tbc_overlay = tbc_overlay.set_position(('right','bottom'))
    
    painting_txt = (mp.CompositeVideoClip([painting, tbc_overlay])
                    .add_mask()
                    .set_duration(tbc_duration)
                    .crossfadein(0.45))

    painting_fading = mp.CompositeVideoClip([im_freeze,painting_txt])

    final_clip =  mp.concatenate_videoclips([ clip_before, painting_fading.set_duration(tbc_duration)])
    afinal_clip = final_clip.set_audio(actual_audio)
    print("h{} w{}".format(afinal_clip.h, afinal_clip.w))
    afinal_clip.write_videofile('out.webm', bitrate="38000k")

def parse_args(args):
    tbc_duration = float(args[0])
    before_len = float(args[1])
    file_to_tbc = args[2]

    return tbc_duration, before_len, file_to_tbc 

def color_filt(clip, RGB = [122/255,66/255,20/255], preserve_luminosity=True):
    """ Desaturates the picture, makes it black and white.
    Parameter RGB allows to set weights for the different color
    channels.
    If RBG is 'CRT_phosphor' a special set of values is used.
    preserve_luminosity maintains the sum of RGB to 1."""

    R,G,B = 1.0*np.array(RGB)/ (sum(RGB) if preserve_luminosity else 1)
    
    def fl(im):
        sep = np.dstack((R*im[:,:,0], G*im[:,:,1], B*im[:,:,2])).astype('uint8')
        return sep

    return clip.fl_image(fl)

def gcolor_filt(clip, RGB = [122/255,66/255,20/255], preserve_luminosity=True):
    """ Desaturates the picture, makes it black and white.
    Parameter RGB allows to set weights for the different color
    channels.
    If RBG is 'CRT_phosphor' a special set of values is used.
    preserve_luminosity maintains the sum of RGB to 1."""

    cclip = clip.fx(mp.vfx.blackwhite, preserve_luminosity=preserve_luminosity)

    return cclip.fx(gray2col, RGB = RGB)

def gray2col(clip, RGB = [122/255,66/255,20/255]):
    
    def fl(im):
        return RGB*im


    return clip.fl_image(fl)

if __name__ == "__main__": main(sys.argv)
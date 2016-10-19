import moviepy.editor as mp
import numpy as np

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
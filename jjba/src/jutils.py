import os

def set_jjba_paths_and_files(module_path):
    PATHS.MODULE_DIR = module_path

    PATHS.set_jjba_paths()
    PATHS.set_jjba_files()

class PATHS:
    MODULE_DIR = None
    OUTPUT_DIR = None
    DATA_DIR = None

    class DATA:
        AUDIO_DIR = None
        IMAGES_DIR = None

        class AUDIO:
            TBC_MP3 = None
        
        class IMAGES:
            TBC_PNG = None
    
    def set_jjba_paths():
        if PATHS.MODULE_DIR is not None:
            PATHS.OUTPUT_DIR = os.path.join(PATHS.MODULE_DIR, 'output')
            PATHS.DATA_DIR = os.path.join(PATHS.MODULE_DIR, 'data')

            PATHS.DATA.AUDIO_DIR = os.path.join(PATHS.DATA_DIR, 'audio')
            PATHS.DATA.IMAGES_DIR = os.path.join(PATHS.DATA_DIR, 'images')
            
        else:
            raise Exception

    def set_jjba_files():
        if PATHS.MODULE_DIR is not None:
            # audio
            PATHS.DATA.AUDIO.TBC_MP3 = os.path.join(PATHS.DATA.AUDIO_DIR, 'tbc.mp3')
            #images
            PATHS.DATA.IMAGES.TBC_PNG = os.path.join(PATHS.DATA.IMAGES_DIR, 'tbc.png')

        else:
            raise Exception
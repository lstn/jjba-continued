import sys, os

MODULE_DIR = os.path.dirname(os.path.realpath(os.path.join(os.getcwd(), os.path.expanduser(__file__))))
sys.path.append(os.path.normpath(os.path.join(MODULE_DIR, '..'))) # not a real package, temp

from jjba.src import command_handler as jcommand_handler
from jjba.src import jaudio, jutils, tbc

def main():
    jutils.set_jjba_paths_and_files(MODULE_DIR) # set paths, temporary ugly solution

    args = jcommand_handler.parse_argv()
    tfreeze = tbc.get_tfreeze(args.freeze_time)

    vclip, aclip, vclip_before = tbc.extract_clip_av(args.file_to_tbc, args.freeze_time, args.start_time, args.end_time, args.end_original_audio)
    overlayed_aclip = tbc.overlay_meme_audio(aclip, args.freeze_time, args.tbc_duration)
    tbc_fade = tbc.overlay_tbc_fade_clip(vclip, tfreeze - args.start_time, args.tbc_duration, 0.45)

    tbc_clip = tbc.concat_tbc_clip(vclip_before, overlayed_aclip, tbc_fade, args.tbc_duration)
    print("before resize: h{} w{}".format(tbc_clip.h, tbc_clip.w))

    _resize = jcommand_handler.get_resize_args(tbc_clip, args)
    tbc_clip = tbc_clip.resize(_resize)
    print("after resize: h{} w{}".format(tbc_clip.h, tbc_clip.w))

    tbc.save_clip(tbc_clip, args.bitrate)

if __name__ == "__main__": main()
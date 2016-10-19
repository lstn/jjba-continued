import argparse
import os
from jjba.src import structs as j_structs

def __create_arguments(parser):
    def add_positionals():
        parser.add_argument('file_to_tbc')
        parser.add_argument('freeze_time', type=float)
    
    def add_simple_args():
        parser.add_argument('-d', required=False, metavar='tbc_duration', type=float)
    
    def add_other_args():
        def add_sizing_group():
            sizing_group = parser.add_mutually_exclusive_group()
            sizing_group.add_argument('--scale', required=False, metavar='final_size_scale', type=float)
            sizing_group.add_argument('--res', nargs=2, required=False, metavar='final_resolution', type=int)
            sizing_group.add_argument('--height', required=False, metavar='final_height', type=int)
            sizing_group.add_argument('--width', required=False, metavar='final_width', type=int)
        
        def add_clipping_group():
            parser.add_argument('--start-time', required=False, metavar='start_time', type=float)
            parser.add_argument('--end-time', required=False, metavar='end_time', type=float)
            parser.add_argument('--end-original-audio', required=False, metavar='end_original_audio', type=float)
        
        add_sizing_group()
        add_clipping_group()
    
    add_positionals()
    add_simple_args()
    add_other_args()


def parse_argv():
    argument_parser = argparse.ArgumentParser(prog='jojo.py')
    
    __create_arguments(argument_parser)
    args = vars(argument_parser.parse_args())
    args = __args_to_bunch(args)
    print(args)

    return args

def __args_to_bunch(args):
    an = lambda k, d: [v if v is not None else d for v in [args.get(k, None)]][0]

    argz = j_structs.Bunch(**{
        'file_to_tbc': an('file_to_tbc', None),
        'freeze_time': an('freeze_time', 1.0),

        'tbc_duration': an('d', 5.4),

        'final_size_scale': an('scale', None),
        'final_resolution': an('res', None),
        'final_height': an('height', None),
        'final_width': an('width', None),

        'start_time': an('start_time', 0.0),
        'end_time': an('end_time', "end"),
        'end_original_audio': an('end_original_audio', "end")
    })
    if not os.path.exists(argz.file_to_tbc):
        raise argparse.ArgumentTypeError("{0} does not exist".format(argz.file_to_tbc))

    return argz

def get_resize_args(clip, args):
    res_args = ['final_size_scale', 'final_resolution', 'final_height', 'final_width']
    found = None
    for a in res_args:
        if args.get(a, None) is not None:
            found = a
            break
    if found is None:
        return 1.0
    if found is 'final_size_scale':
        return args.final_size_scale
    if found is 'final_resolution':
        return args.final_resolution
    if found is 'final_height':
        height = args.final_height/clip.h
        return height
    if found is 'final_width':
        width = args.final_width/clip.w
        return width
    return 1.0


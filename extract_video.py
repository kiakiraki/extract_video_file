#!/usr/bin/env python
# -*- coding: utf-8 -*-
import argparse
from pathlib import Path

import better_exceptions
from video_util import VideoUtil as Util


def main():
    def arg_parse() -> argparse.Namespace:
        parser = argparse.ArgumentParser()
        parser.add_argument(
            '-i',
            '--input',
            help='input video file',
            required=True,
            type=str
        )
        parser.add_argument(
            '-o',
            '--output',
            help='output dir for extracted images',
            required=True,
            type=str
        )
        parser.add_argument(
            '-b',
            '--begin',
            help='extract begin frame or seconds',
            default=0,
            required=False,
            type=int
        )
        parser.add_argument(
            '-e',
            '--end',
            help='extract end frame or seconds',
            default=-1,
            required=False,
            type=int
        )
        parser.add_argument(
            '-t',
            '--defined_by_time',
            help='define begin / end points by time[sec]',
            default=False,
            required=False,
            action='store_true'
        )
        parser.add_argument(
            '--base_name',
            help='base name for saving image, default: input movie name',
            required=False,
            type=str
        )
        return parser.parse_args()

    args = arg_parse()
    width, height, frame_len, fps = Util.retrieve_video_properties(args.input)
    if args.defined_by_time:
        begin = Util.convert_time_to_frame(args.begin, fps)
        if args.end == -1:
            end = frame_len
        else:
            end = Util.convert_time_to_frame(args.end, fps)
    else:
        begin = args.begin
        if args.end == -1:
            end = frame_len
        else:
            end = args.end

    video_path = Path(args.input)

    if args.base_name is None:
        # ファイル名(拡張子以外)をつかう
        base_name = video_path.stem
    else:
        base_name = args.base_name

    Util.extract_video(args.input, args.output, base_name, begin, end)


if __name__ == '__main__':
    main()

#!/usr/bin/env python
# -*- coding: utf-8 -*-
import argparse
import traceback
from pathlib import Path, PosixPath

import better_exceptions
from video_util import VideoUtil


def make_output_dirs(root_dir: PosixPath) -> None:
    target_paths = [
        'timeline',
    ]

    try:
        root_dir.mkdir()
    except FileExistsError:
        pass

    for target in target_paths:
        try:
            target_path = root_dir / target
            target_path.mkdir()
        except FileExistsError:
            continue


def extact_frame_in_sequense(video_path: PosixPath, out_root_dir: PosixPath, sequence) -> None:
    _, _, _, fps = VideoUtil.retrieve_video_properties(
        video_path)
    base_name = video_path.stem
    output_dir = out_root_dir / 'timeline'
    begin_sec = VideoUtil.convert_hhmmss_to_sec(sequence['begin'])
    end_sec = VideoUtil.convert_hhmmss_to_sec(sequence['end'])
    begin = VideoUtil.convert_time_to_frame(begin_sec, fps)
    end = VideoUtil.convert_time_to_frame(end_sec, fps)

    VideoUtil.extract_video(
        video_path, output_dir, base_name, begin, end, sequence['category'])


def extract_frame_in_annotation(annotations, output_dir: PosixPath) -> None:
    for anno in annotations:
        video_path = Path(anno['filepath'])
        print(video_path)
        try:
            for index, seq in enumerate(anno['sequence']):
                print(f'sequense {index+1}/{len(anno["sequence"])}')
                extact_frame_in_sequense(video_path, output_dir, seq)
        except KeyError as e:
            traceback.print_exc()
            print(f'annotation error in {video_path} sequence {index}, {seq}')


def main():
    def arg_arse() -> argparse.Namespace:
        parser = argparse.ArgumentParser()
        parser.add_argument(
            '-a',
            '--annotation',
            help='annotatiton yaml file',
            required=True,
            type=str
        )
        parser.add_argument(
            '-o',
            '--output',
            help='output root dir',
            required='true',
            type=str
        )
        return parser.parse_args()

    args = arg_arse()

    # 作業ディレクトリをつくる
    output_path = Path(args.output)
    make_output_dirs(output_path)

    # アノテーションを読んで画像に分割
    annotations = VideoUtil.load_annotation_file(Path(args.annotation))
    extract_frame_in_annotation(annotations, output_path)


if __name__ == '__main__':
    main()

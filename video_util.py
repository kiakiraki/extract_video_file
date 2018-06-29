#!/usr/bin/env python
# -*- coding: utf-8 -*-
import glob
from pathlib import Path, PosixPath
from typing import Tuple, List

import better_exceptions
import cv2
import numpy as np
import yaml
from tqdm import tqdm


class VideoUtil:

    @classmethod
    def video_frame_generator(
            cls,
            video_path: PosixPath,
            begin_frame_num: int,
            end_frame_num: int) -> np.ndarray:

        video = cv2.VideoCapture(str(video_path))
        success = True  # type: bool
        current = begin_frame_num  # type: int
        video.set(cv2.CAP_PROP_POS_FRAMES, current)

        while(success):
            success, frame = video.read()
            if not success or current > end_frame_num:
                break
            yield frame
            current += 1
        else:
            video.release()

    @classmethod
    def extract_video(
            cls,
            video_path: PosixPath,
            out_dir: PosixPath,
            file_base_name: str,
            begin_frame_num: int,
            end_frame_num: int,
            file_footer_name=None) -> None:

        if not out_dir.exists():
            raise FileNotFoundError(
                f'{out_dir} is not a directory or does not exists')

        with tqdm(total=(end_frame_num - begin_frame_num)) as pbar:
            for index, frame in enumerate(cls.video_frame_generator(
                    video_path, begin_frame_num, end_frame_num)):
                if file_footer_name is None:
                    file_name = f'{file_base_name}_{(index+begin_frame_num):0>6}.png'
                else:
                    file_name = f'{file_base_name}_{(index+begin_frame_num):0>6}_{file_footer_name}.png'
                output_path = out_dir / file_name
                cv2.imwrite(str(output_path), frame)
                pbar.update(1)

    @classmethod
    def retrieve_video_properties(
            cls,
            video_path: PosixPath) -> Tuple[int, int, int, int]:

        video = cv2.VideoCapture(str(video_path))

        width = video.get(cv2.CAP_PROP_FRAME_WIDTH)  # type: int
        height = video.get(cv2.CAP_PROP_FRAME_HEIGHT)  # type: int
        frame_len = video.get(cv2.CAP_PROP_FRAME_COUNT)  # type: int
        fps = video.get(cv2.CAP_PROP_FPS)  # type: int

        video.release()

        return width, height, frame_len, fps

    @classmethod
    def convert_time_to_frame(cls, time: int, fps: int, round_value=True) -> int:
        if round_value:
            return round(time * fps)
        return time * fps

    @classmethod
    def load_annotation_file(cls, filepath: PosixPath) -> List[dict]:
        with open(filepath, encoding='utf-8') as fp:
            return yaml.load(fp)

    @classmethod
    def convert_hhmmss_to_sec(cls, hhmmss: str) -> int:
        # ':' で文字列を分割
        splited = hhmmss.split(':')
        if not 1 <= len(splited) <= 3:
            raise ValueError('inputs should be hh:mm:ss')

        sec = int(splited[0]) * 60 * 60
        sec += int(splited[1]) * 60
        sec += int(splited[2])
        return sec

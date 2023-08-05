import argparse
from dataclasses import dataclass
from functools import partial
import os
import subprocess

import hues
import pafy
from slugify import slugify


@dataclass
class Selector:
    min_audio_quality: int
    min_video_quality: int


SELECTOR_MAP = {
    'low': Selector(min_audio_quality=50, min_video_quality=350),
    'normal': Selector(min_audio_quality=70, min_video_quality=450),
    'hd': Selector(min_audio_quality=128, min_video_quality=700),
    'music': Selector(min_audio_quality=150, min_video_quality=240),
}


def select_audiostream(vid, selector, verbose=False):
    streams = vid.audiostreams
    streams.sort(key=lambda x: (-x.get_filesize(), x.extension), reverse=True)  # favours webm over m4a
    
    for stream in streams:
        if (stream.rawbitrate / 1024) >= selector.min_audio_quality:
            return stream

    if verbose:
        hues.warn("no audio matched selector")

    return streams[-1]


def select_videostream(vid, selector, verbose=False):
    streams = vid.videostreams
    streams.sort(key=lambda x: (-x.dimensions[1], x.extension), reverse=True)  # favours webm over m4a
    
    for stream in streams:
        if stream.dimensions[1] >= selector.min_video_quality:
            return stream
    
    if verbose:
        hues.warn("no video matched selector")

    return streams[-1]


def merge(audiofile, videofile, filename, verbose=False):
    args = [
        "ffmpeg", "-protocol_whitelist", "file,http,https,tcp,tls",
        "-i", audiofile, "-i", videofile, "-c:a", "copy", "-c:v", "copy", 
        filename + ".mkv"
    ]
    if verbose:
        hues.info(f"merge args: {args}")

    proc = subprocess.run(args, stdout=subprocess.DEVNULL)
    if proc.returncode == 0:
        os.remove(audiofile)
        os.remove(videofile)
        hues.success(f"{filename} downloaded")



def download(vid, audiostream, videostream, verbose=False):
    filename = slugify(vid.title + '_' + vid.videoid)

    audiofile = filename + '-audio.' + audiostream.extension
    videofile = filename + '-video.' + videostream.extension

    audiostream.download(audiofile, quiet=True)
    videostream.download(videofile, quiet=True)

    if verbose:
        hues.info(f"merging: {audiofile} {videofile}")

    merge(audiofile, videofile, filename, verbose)


def download_yt_video(args):
    vid = pafy.new(args.url)
    if args.low:
        selector = 'low'
    elif args.hd:
        selector = 'hd'
    elif args.music:
        selector = 'music'
    else:
        selector = 'normal'

    selector = SELECTOR_MAP[selector]
    audiostream = select_audiostream(vid, selector, args.verbose)
    videostream = select_videostream(vid, selector, args.verbose)

    if args.verbose:
        hues.info(f"selected audio:{audiostream}")
        hues.info(f"selected video:{videostream}")

    download(vid, audiostream, videostream, args.verbose)


def create_arguments():
    parser = argparse.ArgumentParser(description="Download youtube videos")
    parser.add_argument('url')
    add_optional_arg = partial(parser.add_argument, action='store_true')
    
    add_optional_arg('--low')
    add_optional_arg('--hd')
    add_optional_arg('--music')
    add_optional_arg('-v', '--verbose')

    args = parser.parse_args()
    download_yt_video(args)

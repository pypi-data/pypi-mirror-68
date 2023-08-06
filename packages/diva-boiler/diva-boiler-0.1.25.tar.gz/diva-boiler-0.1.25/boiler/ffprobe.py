# flake8: noqa
import os
import pipes
import platform
import re
import subprocess

import ffprobe
from ffprobe.ffprobe import FFStream


# override upstream FFProbe to add errors='ignore' to all decode calls
# see https://github.com/gbstack/ffprobe-python/pull/5
class FFProbe(ffprobe.FFProbe):
    def __init__(self, path_to_video):
        self.path_to_video = path_to_video

        try:
            with open(os.devnull, 'w') as tempf:
                subprocess.check_call(["ffprobe", "-h"], stdout=tempf, stderr=tempf)
        except FileNotFoundError:
            raise IOError('ffprobe not found.')

        if os.path.isfile(self.path_to_video):
            if platform.system() == 'Windows':
                cmd = ["ffprobe", "-show_streams", self.path_to_video]
            else:
                cmd = ["ffprobe -show_streams " + pipes.quote(self.path_to_video)]

            p = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)

            stream = False
            ignoreLine = False
            self.streams = []
            self.video = []
            self.audio = []
            self.subtitle = []
            self.attachment = []

            for line in iter(p.stdout.readline, b''):
                line = line.decode('UTF-8', errors='ignore')

                if '[STREAM]' in line:
                    stream = True
                    ignoreLine = False
                    data_lines = []
                elif '[/STREAM]' in line and stream:
                    stream = False
                    ignoreLine = False
                    # noinspection PyUnboundLocalVariable
                    self.streams.append(FFStream(data_lines))
                elif stream:
                    if '[SIDE_DATA]' in line:
                        ignoreLine = True
                    elif '[/SIDE_DATA]' in line:
                        ignoreLine = False
                    elif ignoreLine == False:
                        data_lines.append(line)

            self.metadata = {}
            is_metadata = False
            stream_metadata_met = False

            for line in iter(p.stderr.readline, b''):
                line = line.decode('UTF-8', errors='ignore')

                if 'Metadata:' in line and not stream_metadata_met:
                    is_metadata = True
                elif 'Stream #' in line:
                    is_metadata = False
                    stream_metadata_met = True
                elif is_metadata:
                    splits = line.split(',')
                    for s in splits:
                        m = re.search(r'(\w+)\s*:\s*(.*)$', s)
                        # print(m.groups())
                        self.metadata[m.groups()[0]] = m.groups()[1].strip()

                if '[STREAM]' in line:
                    stream = True
                    data_lines = []
                elif '[/STREAM]' in line and stream:
                    stream = False
                    self.streams.append(FFStream(data_lines))
                elif stream:
                    data_lines.append(line)

            p.stdout.close()
            p.stderr.close()

            for stream in self.streams:
                if stream.is_audio():
                    self.audio.append(stream)
                elif stream.is_video():
                    self.video.append(stream)
                elif stream.is_subtitle():
                    self.subtitle.append(stream)
                elif stream.is_attachment():
                    self.attachment.append(stream)
        else:
            raise IOError('No such media file ' + self.path_to_video)

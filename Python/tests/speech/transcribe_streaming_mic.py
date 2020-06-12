""" Code written by me is commented in triple quotes. All comments by Google 
    are single lined. Although GCP gave the best results, I wasn't able to 
    use it because of the 1 minute quota set on streaming audio. Thus, I was 
    forced to find a new method of streaming audio, which I was able to get 
    in PythonSpeech Recognition.
"""
#!/usr/bin/env python

# Copyright 2017 Google Inc. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

# Google Cloud Speech API sample application using the streaming API.
# 
# NOTE: This module requires the additional dependency `pyaudio`. To install
# using pip:
# 
#     pip install pyaudio
# 
# Example usage:
#     python transcribe_streaming_mic.py

# modified example file from google, parts written by me are commented

from __future__ import division
import string
import csv
import re
import sys
import time
import decimal
import socket

from google.cloud import speech
from google.cloud.speech import enums
from google.cloud.speech import types
import pyaudio
from six.moves import queue



RATE = 16000
CHUNK = int(RATE / 10)  # 100ms


class MicrophoneStream(object):
    # Opens a recording stream as a generator yielding the audio chunks.
    def __init__(self, rate, chunk):
        self._rate = rate
        self._chunk = chunk

        # Create a thread-safe buffer of audio data
        self._buff = queue.Queue()
        self.closed = True

    def __enter__(self):
        self._audio_interface = pyaudio.PyAudio()
        self._audio_stream = self._audio_interface.open(
            format=pyaudio.paInt16,
            channels=1, rate=self._rate,
            input=True, frames_per_buffer=self._chunk,
            # Run the audio stream asynchronously to fill the buffer object.
            # This is necessary so that the input device's buffer doesn't
            # overflow while the calling thread makes network requests, etc.
            stream_callback=self._fill_buffer,
        )

        self.closed = False

        return self

    def __exit__(self, type, value, traceback):
        self._audio_stream.stop_stream()
        self._audio_stream.close()
        self.closed = True
        # Signal the generator to terminate so that the client's
        # streaming_recognize method will not block the process termination.
        self._buff.put(None)
        self._audio_interface.terminate()

    def _fill_buffer(self, in_data, frame_count, time_info, status_flags):
        # Continuously collect data from the audio stream, into the buffer.
        self._buff.put(in_data)
        return None, pyaudio.paContinue

    def generator(self):
        while not self.closed:
            # Use a blocking get() to ensure there's at least one chunk of
            # data, and stop iteration if the chunk is None, indicating the
            # end of the audio stream.
            chunk = self._buff.get()
            if chunk is None:
                return
            data = [chunk]

            # Now consume whatever other data's still buffered.
            while True:
                try:
                    chunk = self._buff.get(block=False)
                    if chunk is None:
                        return
                    data.append(chunk)
                except queue.Empty:
                    break

            yield b''.join(data)
# [END audio_stream]

def roundHalfUp(d):
    # Round to nearest with ties going away from zero.
    rounding = decimal.ROUND_HALF_UP
    return int(decimal.Decimal(d).to_integral_value(rounding=rounding))

def listen_print_loop(responses, commands, commandWriter, connection):
    # Iterates through server responses and prints them.

    # The responses passed is a generator that will block until a response
    # is provided by the server.

    # Each response may contain multiple results, and each result may contain
    # multiple alternatives; for details, see https://goo.gl/tjCPAU.  Here we
    # print only the transcription for the top alternative of the top result.

    # In this case, responses are provided for interim results as well. If the
    # response is an interim one, print a line feed at the end of it, to allow
    # the next result to overwrite it, until the response is a final one. For the
    # final one, print a newline to preserve the finalized transcription.

    num_chars_printed = 0
    for response in responses:
        if not response.results:
            continue

        # The `results` list is consecutive. For streaming, we only care about
        # the first result being considered, since once it's `is_final`, it
        # moves on to considering the next utterance.
        result = response.results[0]
        if not result.alternatives:
            continue

        # Display the transcription of the top alternative.
        transcript = result.alternatives[0].transcript

        # Display interim results, but with a carriage return at the end of the
        # line, so subsequent lines will overwrite them.
        #
        # If the previous result was longer than this one, we need to print
        # some extra spaces to overwrite the previous result
        overwrite_chars = ' ' * (num_chars_printed - len(transcript))

        if not result.is_final:
            # finds timestamp
            # sys.stdout.write(transcript + overwrite_chars + '\r')
            # sys.stdout.write('\n')
            # 
            #         
            # commandWriter.writerow([roundHalfUp(time.time()), 
            # str(transcript + overwrite_chars + '/r')])
            
            sys.stdout.flush()
            num_chars_printed = len(transcript)

        else:
            print(transcript + overwrite_chars)
            for command in set(str(transcript).strip().split(' ')):
                if command != '':
                    commandWriter.writerow([str(time.time()), 
                    str(command.strip())])
                    sys.stdout.flush()
            # if re.search(r'^(\bpose\b)', transcript, re.I):
            #     tran_list = transcript.split(' ')
            #     if tran_list[1] not in string.digits:
            #         if re.search(r'^f', tran_list[1], re.I):
            #             tran_list[1] == '4'
            #         elif re.search(r'^t', tran_list[1], re.I):
            #             tran_list[1] = '2'
            #     transcript = tran_list.join('')
            """Written by me"""
            connection.send((transcript.lower() + '~').encode('utf-8'))
            sys.stdout.write(transcript)
            sys.stdout.flush()
            """end"""
            # Exit recognition if any of the transcribed phrases could be
            # one of our keywords.
            if re.search(r'\b(exit|quit)\b', transcript, re.I):
                print('Exiting..')
                commands.close()
                connection.close()
                break

            num_chars_printed = 0


def main():
    """Written by me"""
    commands = open('testOne.csv', 'w')
    commandWriter = csv.writer(commands, lineterminator='\n')
    TCP_IP = '127.0.0.1'
    TCP_PORT = 6000
    BUFFER_SIZE = 1024
    
    sys.stdout.write("It has begun \n")
    s = socket.socket()
    s.bind((TCP_IP, TCP_PORT))
    sys.stdout.write("Listening on point " + TCP_IP + '\n')
    s.listen(1)
    
    connection, address = s.accept()
    language_code = 'en-US'  # language tag
    sys.stdout.write("It has begun \n")
    sys.stdout.flush()
    """end"""

    client = speech.SpeechClient()
    config = types.RecognitionConfig(
        encoding=enums.RecognitionConfig.AudioEncoding.LINEAR16,
        sample_rate_hertz=RATE,
        language_code=language_code)
    streaming_config = types.StreamingRecognitionConfig(
        config=config,
        single_utterance=True,
        interim_results=True)

    with MicrophoneStream(RATE, CHUNK) as stream:
        audio_generator = stream.generator()
        requests = (types.StreamingRecognizeRequest(audio_content=content)
                    for content in audio_generator)

        responses = client.streaming_recognize(streaming_config, requests)

        # Now, put the transcription responses to use.
        listen_print_loop(responses, commands, commandWriter, connection)
    

if __name__ == '__main__':
    main()

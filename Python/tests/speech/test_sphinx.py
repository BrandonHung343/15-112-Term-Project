#!/usr/bin/python

from os import environ, path
from pocketsphinx.pocketsphinx import *
from sphinxbase.sphinxbase import
import pyaudio

# Attempt to use offline processing with CMUSphinx
# Ironically did not work, and no one in CMU I asked knew how to use it
 
# sets directory to build model
MODELDIR = "C:/Users/Brandon/Documents/GitHub/pocketsphinx/model"

# CMU Sphinx is made by CMU at https://cmusphinx.github.io/
config = Decoder.default_config()
config.set_string('-hmm', path.join(MODELDIR, 'en-us/en-us'))
config.set_string('-lm', path.join(MODELDIR, 'en-us/en-us.lm.bin'))
config.set_string('-dict', path.join(MODELDIR, 'en-us/cmudict-en-us.dict'))
decoder = Decoder(config)

# opens pyaudio stream
p = pyaudio.PyAudio()
stream = p.open(format=pyaudio.paInt16, channels=2, rate=48000, input=True, frames_per_buffer=4096)
stream.start_stream() 

# results were incomprehensible for the most part
in_speech_bf = False
decoder.start_utt()
while True:
    buf = stream.read(4096)
    if buf:
        decoder.process_raw(buf, False, False)
        if decoder.get_in_speech() != in_speech_bf:
            in_speech_bf = decoder.get_in_speech()
            if not in_speech_bf:
                decoder.end_utt()
                print ('Result:', decoder.hyp().hypstr)
                decoder.start_utt()
    else:
        break
stream.close()
decoder.end_utt()
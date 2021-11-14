import sys
from pylab import *
import wave

def show_wave(speech):
    spf = wave.open(speech, 'r')
    sound_info = spf.readframes(-1)
    sound_info = fromstring(sound_info, 'Int16')

    f = spf.getframerate()

    subplot(211)
    plot(sound_info)
    title('Wave form and Spetrogram of %s' %sys.argv[1])

    subplot(212)
    spectrogram = specgram(sound_info, Fs = f, scale_by_freq=True, sides = 'default')

    savefig('Wave form and Spectrogram')
    spf.close()

fil = sys.argv[1]

show_wave(fil)

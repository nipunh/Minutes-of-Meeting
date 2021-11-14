# Import dependencies

from ibm_watson import SpeechToTextV1
from ibm_watson.websocket import RecognizeCallback, AudioSource
from os.path import join, dirname
import os
import json



def transcription_with_ibm(audiopath):


    # Initialize objects
    
    filename = 'polo.json'
    audiofile = audiopath


    # Initialize credentials

    speech_to_text = SpeechToTextV1(
        iam_apikey='QjP0vdAAHfIS8ESTSQgufTdmnG43etz2mIXlltwtVcJL',
        url='https://gateway-lon.watsonplatform.net/speech-to-text/api'
    )


    # Callback to the recoginze_using_sockets function to call after receiving response

    class MyRecognizeCallback(RecognizeCallback):
        def __init__(self):
            RecognizeCallback.__init__(self)

        def on_connected(self):
            print('Connection was successful')

        def on_listening(self):
            print('Service is listening')


    # Save the response JSON string in a local file named 'tran1.json' and appending ',' after every response to treat the response as a list for easier access from the file

        def on_data(self, data):
            with open(filename, 'a+') as outfile:
                json.dump(data, outfile, indent=2)
            with open(filename, 'a+') as outfile:
                outfile.write(',')

        def on_hypothesis(self, hypothesis):
            print('')

        def on_error(self, error):
            print('Error received: {}'.format(error))
            print(error)

        def on_inactivity_timeout(self, error):
            print('Inactivity timeout: {}'.format(error))

        def on_close(self):
            print("Connection closed")
            with open(filename,'a+') as filehandle:
                filehandle.seek(filehandle.tell()-1, os.SEEK_SET)
                filehandle.truncate()
                filehandle.write(']')

    myRecognizeCallback = MyRecognizeCallback()


    # Open file from local system and send using websockets

    with open(filename,'w') as handle:
        handle.write('[')

    with open(join(dirname(__file__), './.', audiofile), 'rb') as audio_file:
        audio_source = AudioSource(audio_file)
        speech_to_text.recognize_using_websocket(audio=audio_source,
                                                content_type='audio/mp3',
                                                recognize_callback=myRecognizeCallback,
                                                model='en-US_NarrowbandModel',
                                                inactivity_timeout=10,
                                                speaker_labels=True,
                                                interim_results=True)

transcription_with_ibm('ieltslisteningrecordingsection 1.mp3')
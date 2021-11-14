import azure.cognitiveservices.speech as speechsdk
import time

speech_key, service_region = "7746771e35864882a5eb846c6572febc", "westus"

weatherfilename = "Testing/Record-009.wav"

def speech_recognize_continuous_from_file():

    """performs continuous speech recognition with input from an audio file"""

    # <SpeechContinuousRecognitionWithFile>

    speech_config = speechsdk.SpeechConfig(subscription=speech_key, region=service_region)

    audio_config = speechsdk.audio.AudioConfig(filename=weatherfilename)



    speech_recognizer = speechsdk.SpeechRecognizer(speech_config=speech_config, audio_config=audio_config)



    done = False



    def stop_cb(evt):

        """callback that stops continuous recognition upon receiving an event `evt`"""

        print('CLOSING on {}'.format(evt))

        speech_recognizer.stop_continuous_recognition()

        nonlocal done

        done = True

    def file_op(evt):
        with open('test.txt' , 'a+') as write_file:
            write_file.write(evt.result.text+'\n')


    # Connect callbacks to the events fired by the speech recognizer

    speech_recognizer.recognizing.connect(lambda evt: print('RECOGNIZING: {}'.format(evt)))

    # speech_recognizer.recognized.connect(lambda evt: print('RECOGNIZED: {}'.format(evt)))
    speech_recognizer.recognized.connect(file_op)

    speech_recognizer.session_started.connect(lambda evt: print('SESSION STARTED: {}'.format(evt)))

    speech_recognizer.session_stopped.connect(lambda evt: print('SESSION STOPPED {}'.format(evt)))

    speech_recognizer.canceled.connect(lambda evt: print('CANCELED {}'.format(evt)))

    # stop continuous recognition on either session stopped or canceled events

    speech_recognizer.session_stopped.connect(stop_cb)

    speech_recognizer.canceled.connect(stop_cb)


    # Start continuous speech recognition

    speech_recognizer.start_continuous_recognition()

    while not done:

        time.sleep(.5)

    # </SpeechContinuousRecognitionWithFile>

speech_recognize_continuous_from_file()
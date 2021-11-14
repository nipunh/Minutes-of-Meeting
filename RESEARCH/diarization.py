# AUTHOR: KARTHIK PEDDI
"""To run this file independently the required inputs should be the audio file to perform speaker diarization
and the number of speakers participating in the audio file, this program uses google cloud-speech-to-text api for
speaker diarization of both mono and stereo audio files"""


from google.cloud import speech_v1p1beta1 as speech
from google.cloud.speech_v1p1beta1 import enums
from google.cloud.speech_v1p1beta1 import types
from pydub import AudioSegment

#Use the below commented lines incase of using this program independently
"""
print("Enter the audio file path with extension:")
speech_file=input()
print("Enter the number of speakers in the audio file:")
speaker_count=int(input())
speaker_diarization(speech_file,speaker_count)
"""

def mp3_to_wav(audio_file_name):
    if audio_file_name.split('.')[1] == 'mp3':    
        sound = AudioSegment.from_mp3(audio_file_name)
        audio_file_name = audio_file_name.split('.')[0] + '.wav'
        sound.export(audio_file_name, format="wav")

def speaker_diarization(speech_file,speaker_count,long_audio_file,model):
    #create a speech client object
    client = speech.SpeechClient()
    if model==1:
        model='phone_call'
    elif model==2:
        model='video'
    else:
        model='default'
    if long_audio_file==False:
        mp3_to_wav(speech_file)
    if long_audio_file==False:
        #read the audio file
        with open(speech_file, 'rb') as audio_file:
            content = audio_file.read()
        audio = speech.types.RecognitionAudio(content=content)
        print('Waiting for operation to complete...')
        #try block contains the speaker diarization request to cloud api for mono audio
        """This except block catches an exception if audio is
           stereo and runs the speaker diarization request for
           stereo audio""" 
        try:
            config = speech.types.RecognitionConfig(
                encoding=speech.enums.RecognitionConfig.AudioEncoding.LINEAR16,
                language_code='en-US',
                enable_speaker_diarization=True,use_enhanced=True,model=model,
                diarization_speaker_count=speaker_count,enable_word_confidence=True)
            response = client.recognize(config, audio)   
        except:
            config = speech.types.RecognitionConfig(
                encoding=speech.enums.RecognitionConfig.AudioEncoding.LINEAR16,
                language_code='en-US',
                enable_speaker_diarization=True,
                audio_channel_count=2,use_enhanced=True,
                enable_separate_recognition_per_channel=True,model=model,
                diarization_speaker_count=speaker_count)
            response = client.recognize(config, audio)
    else:
        try:
            audio = types.RecognitionAudio(uri=speech_file)
            config = types.RecognitionConfig(
                encoding=enums.RecognitionConfig.AudioEncoding.LINEAR16,
                language_code='en-US',enable_speaker_diarization=True,use_enhanced=True,model=model,enable_word_confidence=True
                    diarization_speaker_count=speaker_count)

            operation = client.long_running_recognize(config, audio)

            print('Waiting for operation to complete...')
            response = operation.result(timeout=10000)
        except:
            audio = types.RecognitionAudio(uri=speech_file)
            config = types.RecognitionConfig(
                encoding=enums.RecognitionConfig.AudioEncoding.LINEAR16,audio_channel_count=2,enable_word_confidence=True
                language_code='en-US',enable_speaker_diarization=True,use_enhanced=True,model=model,
                    diarization_speaker_count=speaker_count)

            operation = client.long_running_recognize(config, audio)

            print('Waiting for operation to complete...')
            response = operation.result(timeout=10000)
            

    """The transcript within each result is separate and sequential per result.
        However, the words list within an alternative includes all the words
        from all the results thus far. Thus, to get all the words with speaker
        tags, you only have to take the words list from the last result:"""
    #The below line gets the speaker tags for each word and then they are stored in the list tag
    tags = response.results[-1]
    words_info = tags.alternatives[0].words
    tag=[]
    for i in range(len(words_info)):
        tag.append(words_info[i].speaker_tag)

    
    #Two files "conversation.txt" and "conv_with_tags.txt" are created to store the conversation and the conversation including the tags respectively
    f1=open("conversation.txt","w")
    f2=open("conv_with_tags.txt","w")

    #The variable count stores the number of dialogues between the speakers
    count=0
    
    #This for loop iterates over the results from the response from the api and prints the speaker tag, transcript and the confidence of each dialogue.
    for i, result in enumerate(response.results):
        alternative = result.alternatives[0]
        print('-' * 20)
        print("speaker_tag: {}".format(tag[count]))
        f2.write(str(tag[count])+': ')
        count+=alternative.transcript.count(' ')
        if i==0:
            count+=1
        print(u'Transcript: {}'.format(alternative.transcript))
        f1.write(alternative.transcript.strip()+'\n')
        f2.write(alternative.transcript.strip()+'\n')
        print(u'Confidence: {}'.format(alternative.words[0].confidence))
    
    f1.close()
    f2.close()
    return 0




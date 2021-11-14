# Import dependencies

import json
import os
import numpy as np
import matplotlib.pyplot as plt
import sys
from pylab import *
import wave

def analysis_of_json():

    # Initialize objects

    transcripts = []
    speaker_labels = []
    transcript_file = 'conv_with_tags4.txt'
    conversation_file = 'conversation4.txt'
    json_file = 'polo.json'
    speakers = {}
    speaker_conf = {}
    conf_avg = {}


    #Read data from the local json file

    with open(json_file) as json_file:
        json_data = json.load(json_file)


    # Convert interior lists of dictionaries into dictionaries to access elements using keys

    for olo in json_data:
        newDict={}
        if('results' in olo.keys()):
            for item in olo['results']:
                newDict.update(item)
            olo['results']=newDict
            transcripts.append(olo['results'])
        elif('speaker_labels' in olo.keys()):
            for item in olo['speaker_labels']:
                newDict.update(item)
            olo['speaker_labels']=newDict
            speaker_labels.append(olo['speaker_labels'])


    # Only access Final transcripts and not interim results

    final_transcripts = []
    for i in range(len(transcripts)):
        if(transcripts[i]['final'] == True):
            final_transcripts.append(transcripts[i])


    # Access Speaker Labels i.e. Speaker Diarization and store the final transcript locally

    for i in range(len(speaker_labels) - 1):
        print('Speaker'+str(speaker_labels[i]['speaker'])+' : '+final_transcripts[i]['alternatives'][0]['transcript']+' ; From : '+str(final_transcripts[i]['alternatives'][0]['timestamps'][0][1])+' ; To : '+str(speaker_labels[i]['to'])+'\n\n')
        'Speaker'+str(speaker_labels[i]['speaker'])+' : '+final_transcripts[i]['alternatives'][0]['transcript']+'\n'
        with open(transcript_file, 'a+') as t_file:
            t_file.write(str(str(speaker_labels[i]['speaker'])+': '+final_transcripts[i]['alternatives'][0]['transcript']+'.\n'))
        with open(conversation_file, 'a+') as t_file:
            t_file.write(final_transcripts[i]['alternatives'][0]['transcript']+'.\n')
    with open(transcript_file,'a+') as filehandle:
            filehandle.seek(filehandle.tell()-2, os.SEEK_SET)
            filehandle.truncate()
    with open(conversation_file,'a+') as filehandle:
            filehandle.seek(filehandle.tell()-2, os.SEEK_SET)
            filehandle.truncate()


    # Calculate total time for individual speaker using python dictionaries

    for i in range(len(speaker_labels) - 1):
        if('Speaker'+str(speaker_labels[i]['speaker']) not in speakers.keys()):
            speakers['Speaker'+str(speaker_labels[i]['speaker'])] = str(float(((speaker_labels[i]['to'])-final_transcripts[i]['alternatives'][0]['timestamps'][0][1])))
        else:
            existing = float(speakers['Speaker'+str(speaker_labels[i]['speaker'])])
            current = float(((speaker_labels[i]['to'])-final_transcripts[i]['alternatives'][0]['timestamps'][0][1]))
            updated = existing + current
            speakers['Speaker'+str(speaker_labels[i]['speaker'])] = updated


    # Calculate avg confidence per speaker    

    for i in speakers.keys():
        speaker_conf[str(i)] = []

    for i in range(len(final_transcripts)):
        speaker_conf['Speaker'+str(speaker_labels[i]['speaker'])].append(float(final_transcripts[i]['alternatives'][0]['confidence']))

    for i in  speaker_conf.keys():
        conf_avg[str(i)] = sum(speaker_conf[i])/len(speaker_conf[i])


    # Plot the total time and average confidences

    talk_time = []
    for i in speakers.keys():
        talk_time.append(float(speakers[i]))

    speaker = []
    for i in conf_avg.keys():
        speaker.append(float(conf_avg[i]))

    y_pos = np.arange(len(talk_time))
    plt.bar(y_pos, talk_time, width = 0.65)
    plt.xticks(y_pos, speakers.keys())
    plt.xlabel('Speakers')
    plt.ylabel('Total Talk Time(in s)')
    plt.title('Talk time of Speakers')
    plt.savefig('Time1.png')
    plt.close()

    y_pos = np.arange(len(speaker))
    plt.bar(y_pos, speaker, width = 0.55)
    plt.xticks(y_pos, conf_avg.keys())
    plt.xlabel('Speakers')
    plt.ylabel('Confidence')
    plt.title('Confidence of Speakers')
    plt.savefig('Conf1.png')
    plt.close()


# def show_wave(speech):

#     # Plotting Spectrogram of given audio

#     spf = wave.open(speech, 'r')
#     sound_info = spf.readframes(-1)
#     sound_info = fromstring(sound_info, 'Int16')

#     f = spf.getframerate()

#     subplot(211)
#     plot(sound_info)
#     title('Wave form and Spetrogram of audio file of the conversation')

#     subplot(212)
#     spectrogram = specgram(sound_info, Fs = f, scale_by_freq=True, sides = 'default')

#     savefig('Wave form and Spectrogram')
#     spf.close()


analysis_of_json()

# show_wave('Testing/Record-010.wav')
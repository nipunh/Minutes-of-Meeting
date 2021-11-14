import json

with open('Testing/test_wav.json') as json_file:
        json_data = json.load(json_file)

transcripts = []
speaker_labels = []

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

final_transcripts = []
for i in range(len(transcripts)):
    if(transcripts[i]['final'] == True):
        final_transcripts.append(transcripts[i])

speakers = {}

for i in range(len(speaker_labels) - 1):
    if('Speaker'+str(speaker_labels[i]['speaker']) not in speakers.keys()):
        speakers[str(speaker_labels[i]['speaker'])] = str(float(((speaker_labels[i]['to'])-final_transcripts[i]['alternatives'][0]['timestamps'][0][1])))
    else:
        existing = float(speakers[str(speaker_labels[i]['speaker'])])
        current = float(((speaker_labels[i]['to'])-final_transcripts[i]['alternatives'][0]['timestamps'][0][1]))
        updated = existing + current
        speakers[str(speaker_labels[i]['speaker'])] = updated

speaker_conf = {}

for i in speakers.keys():
    speaker_conf[str(i)] = []


for i in range(len(final_transcripts)):
    speaker_conf[str(speaker_labels[i]['speaker'])].append(float(final_transcripts[i]['alternatives'][0]['confidence']))

speakConfidences={}

for i in  speaker_conf.keys():
    speakConfidences[str(i)] = sum(speaker_conf[i])/len(speaker_conf[i])

print(speakConfidences)
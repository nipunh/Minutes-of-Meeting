# Import dependencies

from __future__ import print_function
import json
from os.path import join, dirname
from ibm_watson import ToneAnalyzerV3
from ibm_watson.tone_analyzer_v3 import ToneInput


# Initialize objects

transcripted_file = "finaltest_transcript.txt"
outfile = 'tp.json'

# Initialize credentials

service = ToneAnalyzerV3(
    url='https://gateway-fra.watsonplatform.net/tone-analyzer/api',
    version='2017-09-21',
    iam_apikey='koiT-St4HSN7iVfIcHhUhY86Qv205Xr3w-AOn6_TTvOF')


# Read data and model it in list of dictionaries

with open(transcripted_file) as json_file:
    json_data = json_file.read()

json_data = json_data.split('\n')

final = []
for i in json_data:
    i = i.split(':')
    final.append(i)

t = []

for i in range(len(final)):
    a = {'user': str(final[i][0]), 'text' : str(final[i][1])}
    t.append(a)


# Request tone analysis per transcript and save it locally

for i in t:
    tone_chat = service.tone_chat(tone_input=i[0]['text'], content_type='text/plain', sentences=True).get_result()
    with open(outfile, 'a+') as outfile:
        json.dump(tone_chat, outfile, indent=2)
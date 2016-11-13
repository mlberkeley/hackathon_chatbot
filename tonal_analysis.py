import json
from watson_developer_cloud import ToneAnalyzerV3
import csv

def tone_output(text):
    tone_analyzer = ToneAnalyzerV3(
       username='8dd8976d-adb7-44aa-a1d5-ba57f2051bb2',
       password='XL2baWIDp5x1',
       version='2016-05-19')

    sentences = []
    tones = tone_analyzer.tone(text=text, tones='emotion', sentences=True)['sentences_tone']

    for i in range(len(tones)):
        sentence = []
        tone = tones[i]['tone_categories'][0]['tones']
        for i in range(5):
            sentence.append(tone[i].get('score'))
        sentences.append(sentence)

    return sentences
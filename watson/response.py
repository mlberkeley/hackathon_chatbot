import random
from watson_developer_cloud import ToneAnalyzerV3

responses = [
['f you man', 'your that guy right', 'why would you say those', 'NO','FUCK YOU','you would say that'],
['no no no never no', 'ew get away me', 'no you that', 'that is so little', 'ew', '?', 'stop bro'],
['god no', 'much many due hw', 'not mine or', 'like the Midterm isnt right'],
['Yes! of course.','Well, whaddaya know', 'I wouldnt know?!', 'I love you too','This sounds gucci', 'YES always', 'tomorrow of course', 'this is my shit'],
['sure i think so so', 'im sorry', 'by tomorrow is never', 'i wont ever now', 'aw', 'shucks']
]

def give_response(input):

    # PARSE TONE VALUES
    tone_analyzer = ToneAnalyzerV3(
       username='8dd8976d-adb7-44aa-a1d5-ba57f2051bb2',
       password='XL2baWIDp5x1',
       version='2016-05-19')

    sentences = []
    tones = tone_analyzer.tone(text=input, tones='emotion', sentences=True)['sentences_tone']

    texts = []
    for i in range(len(tones)):
        sentence = []
        if tones[i]['tone_categories']:
          texts.append(tones[i]['text'])
          tone = tones[i]['tone_categories'][0]['tones']
          for i in range(5):
              sentence.append(tone[i].get('score'))
        else:
          for i in range(5):
            texts.append('')
            sentence.append(0)
        sentences.append(sentence)

    # SELECT RESPONSE
    response = ""
    for sentence in sentences:
        max = -1
        max_index = -1
        for i in range(5):
            if sentence[i] > max:
                max = sentence[i]
                max_index = i
        response += responses[max_index][random.randrange(len(responses[max_index]))] + ". "

    return response
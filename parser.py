from html.parser import HTMLParser
from datetime import datetime
import re
import os
from random import shuffle
from tonal_analysis import tone_output

class FBMParser(HTMLParser):

	def __init__(self):
		HTMLParser.__init__(self)
		self.threads = []
		self.nextData = None
		self.currentMessage = {}
		self.currentThread = {}

	def handle_starttag(self, tag, attrs):
		if ('class', 'thread') in attrs:
			self.nextData = 'threadUsers'
			if self.currentThread:
				self.threads.append(self.currentThread)
				self.currentThread = {}
		elif ('class', 'user') in attrs:
			self.nextData = 'messSender'
			if self.currentMessage:
				self.currentThread['messages'].append(self.currentMessage)
				self.currentMessage = {}
		elif ('class', 'meta') in attrs:
			self.nextData = 'messSendTime'
		elif tag == 'p':
			self.nextData = 'messContent'

	def handle_endtag(self, tag):
	    pass
	def handle_data(self, data):
		if self.nextData == 'threadUsers':
			self.currentThread['users'] = data
			self.currentThread['messages'] = []
		elif self.nextData == 'messSender':
			self.currentMessage['sender'] = data
		elif self.nextData == 'messSendTime':
			data = re.sub( 	r'(\d\d?):(\d\d)',
		   					r'\1:\2:00',
		   					data
						 )
			data = re.sub( r'([ap])m',
							lambda pat: pat.group(1).upper() + 'M',
							data)
			self.currentMessage['time'] = datetime.strptime(data, "%A, %B %d, %Y at %X%p %Z")
		elif self.nextData == 'messContent':
			self.currentMessage['content'] = data

	def sortThreads(self):
		for thread in self.threads:
			thread['messages'] = sorted(thread['messages'], key=lambda mess: mess['time'])
			


def parseFBCorpus(filename):
	with open(filename) as f:
		data = f.read()
	parser = FBMParser()
	parser.feed(data)
	parser.sortThreads()
	return parser.threads

def createVocabFiles(filename, user):
	threads = parseFBCorpus(filename)
	with open('inputVocab.txt', 'w') as f1:
		with open('outputVocab.txt', 'w') as f2:
			for thread in threads:
				pair = ['', '']
				responseNext = False
				pairFinished = False
				for message in thread['messages']:
					if message['sender'] == user and not responseNext:
						if 'content' in message:
							pair[0] += re.sub(r'\n', r'', message['content'])
							responseNext = True
					elif responseNext and not pair[1]:
						if 'content' in message:
							pair[1] += re.sub(r'\n', r'', message['content'])
					if pair[0] and pair[1]:
						f2.write(pair[0] + '\n')
						f1.write(pair[1] + '\n')
						pairFinished = False
						responseNext = False
						pair = ['', '']


UP_SAMPLE_NUM = 10
def makeCombinedDataset(filename, user):
	createVocabFiles(filename, user)
	with open('inputVocab.txt', 'r') as i1, open('outputVocab.txt', 'r') as o1, \
		 open('data/train.enc', 'r', errors='ignore') as i2, open('data/train.dec', 'r', errors='ignore') as o2,  \
		 open('temp.in', 'w') as dataIn, open('temp.out', 'w') as dataOut:
		for fbInLine, fbOutLine in zip(i1, o1):
			movieInLine = i2.readline()
			movieOutLine = o2.readline()
			for _ in range(UP_SAMPLE_NUM):
				dataIn.write(str(fbInLine))
				dataOut.write(str(fbOutLine))
			dataIn.write(str(movieInLine))
			dataOut.write(str(movieOutLine))
	with open('temp.in', 'r') as dataIn, open('temp.out', 'r') as dataOut:
		data = []
		for tup in zip(dataIn, dataOut):
			data.append(tup)
	shuffle(data)
	with open('trainData.in', 'w') as dataIn, open('trainData.out', 'w') as dataOut:
		for tup in data:
			dataIn.write(str(tup[0]))
			dataOut.write(str(tup[1]))


def readTrainDataFile(filename):
	dataBatches = []
	currentData = ''
	count = 0
	with open(filename, 'r') as f:
	    for line in f:
	        if count >= 100:
	        	dataBatches.append(currentData)
	        	currentData = ''
	        	count = 0
	        count += 1
	        currentData += line
	ret = []
	for data in dataBatches[:]:      
		data = re.sub(r'[.]', r' ', data)
		data = re.sub(r'\n', '. ', data)
		ret.append(data)

	print(len(ret))
	return ret
def batchTone(filename, restartPoint):
	dataBatches = readTrainDataFile(filename)
	total = 0
	count = 0
	with open('tones.in', 'a') as f:
		for data in dataBatches:
			count += 1
			if count > restartPoint:
				to = tone_output(data)
				total += len(to)
				print(total)
				for scorevec in to:
					for score in scorevec:
						f.write(str(score) + ' ')
					f.write('\n')

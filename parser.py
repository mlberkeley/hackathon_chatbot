from html.parser import HTMLParser
from datetime import datetime
import re

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
			


def parseCorpus(filename):
	with open(filename) as f:
		data = f.read()
	parser = FBMParser()
	parser.feed(data)
	parser.sortThreads()
	return parser.threads
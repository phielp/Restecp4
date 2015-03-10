#
#	Students	: Philip Bouman , Alex Khawalid
#	Studentnr	: 10668667		, 10634207
#	Assignment A: step 4 NTMI
#	Date		: 06-02-2015
#
# Command-line:
# (1): python assignment2.py -c austen.txt -n 3
# (2): python assignment2.py -c austen.txt -p test2.txt
# (3): python assignment2.py -c austen.txt -n 3 -s test.txt
# (4): python assignment2.py -c austen.txt -n 3 -fo
import itertools
from optparse import OptionParser

# check if ngram is already in table
# if it is increment it, if not add it
#
## ngramkey = ngram
## ngramtable = ngramtable
def addToTable(ngramkey,ngramtable):
	if ngramkey in ngramtable:
		ngramtable[ngramkey] += 1
	else:
		ngramtable[ngramkey] = 1
	return ngramtable

# 			language model: read test set into sentences
# read a testset into a table of sentences with probabilities
# pofn contains the probabilities for ngrams from the trainset
# 
## f = file to be read
## pofn = list of probabilities for ngrams from trainset
def readSentences(f,pofn):
	stable = {}
	sentence = ""
	ngramkey = ""
	ngramcount = 0
	tempprob = 1.0
	i = 0
	remove = ['#/#','--/:',';/:','-/:','!/.','2/,',"'/:",'non-``/``','Non-``/``',"underwriters/,",
	"an/,","section/,",'US$/$','NZ$/$','C$/$','A$/$','HK$/$','M$/$','S$/$','C/$',
	'``/``',"`/``",'`/`',',/,','(/(',')/)',"''/''","'/''","'/'",":/:","$/$",
	".../:","?/.",'[',']','{/(','}/)']
	with open(f, 'r') as fread:
		fread = fread.read()
		# remove tags
		for t in remove:
			fread = fread.replace(t, "")
		fread = fread.split("\n")

		for line in fread:
			line = line.strip()
			# if line is a start or stop symbol
			if line == "======================================":
				if ngramkey == "<s>":
					continue
				elif i == 0:
					ngramkey = "<s>"
					sentence = "<s>"
					i = 1
					ngramcount = 1
					tempprob = 1
				elif i < 3:
					ngramkey = ngramkey + " </s>"
					sentence += " </s>"
					if ngramkey in pofn:
						factor = pofn[ngramkey]
					else:
						factor = p0
					stable[sentence] = tempprob*factor
					sentence = "<s>"
					ngramkey = "<s>"
					i = 1
					ngramcount = 1
				else:
					ngramkey = ngramkey.split(' ', 1)[1]
					ngramkey = ngramkey + " </s>"
					sentence += " </s>"
					if ngramkey in pofn:
						factor = pofn[ngramkey]
					else:
						factor = p0
					stable[sentence] = tempprob*factor
					sentence = "<s>"
					ngramkey = "<s>"
					i = 1
					ngramcount = 1
			elif line == "./.":
				if i <= 3:
					ngramkey = ngramkey + " </s>"
					sentence += " </s>"
					if ngramkey in pofn:
						factor = pofn[ngramkey]
					else:
						factor = p0
					stable[sentence] = tempprob*factor
					sentence = "<s>"
					ngramkey = "<s>"
					i = 1
					ngramcount = 1
				else:
					ngramkey = ngramkey.split(' ', 1)[1]
					ngramkey = ngramkey + " </s>"
					sentence += " </s>"
					if ngramkey in pofn:
						factor = pofn[ngramkey]
					else:
						factor = p0
					stable[sentence] = tempprob*factor
					sentence = "<s>"
					ngramkey = "<s>"
					i = 1
					ngramcount = 1
			else:
				splitlines = line.translate(None, '[]').split()
				for word in splitlines:
					if ngramcount < 15:
						word = word.split("/")[1]
						if i == 1:
							ngramkey += " " + word
							sentence += " " + word
							i+= 1
							ngramcount += 1
						elif i == 2:
							ngramkey += " " + word
							sentence += " " + word	
							if ngramkey in pofn:
								factor = pofn[ngramkey]
							else:
								factor = p0
							tempprob *= factor
							ngramkey = ngramkey.split(' ', 1)[1]
							ngramcount += 1
					#wordsplit = word.split("/")

	return stable

# 			language model: read tags from training set
# read a trainset into a table of tags with the number of occurences
#
## f = file to be read
def readTagfile(f):
	ngramtable = {}
	ngramkey = ""
	i = 0
	remove = ['#/#','--/:',';/:','-/:','!/.','2/,',"'/:",'non-``/``','Non-``/``',"underwriters/,",
	"an/,","section/,",'US$/$','NZ$/$','C$/$','A$/$','HK$/$','M$/$','S$/$','C/$',
	'``/``',"`/``",'`/`',',/,','(/(',')/)',"''/''","'/''","'/'",":/:","$/$",
	".../:","?/.",'[',']','{/(','}/)']

	with open(f, 'r') as fread:
		fread = fread.read()
		# remove tags
		for t in remove:
			fread = fread.replace(t, "")
		fread = fread.split("\n")

		for line in fread:
			line = line.strip()
			# if line is a start or stop symbol
			if line == "======================================":
				if ngramkey == "<s>":
					continue
				elif i == 0:
					ngramkey = "<s>"
					i = 1
				elif i < 3:
					ngramkey = ngramkey + " </s>"
					ngramtable = addToTable(ngramkey,ngramtable)
					ngramkey = "<s>"
					i = 1
				else:
					ngramkey = ngramkey.split(' ', 1)[1]
					ngramkey = ngramkey + " </s>"
					ngramtable = addToTable(ngramkey,ngramtable)
					ngramkey = "<s>"
					i = 1
			elif line == "./.":
				if i <= 3:
					ngramkey = ngramkey + " </s>"
					ngramtable = addToTable(ngramkey,ngramtable)
					ngramkey = "<s>"
					i = 1
				else:
					ngramkey = ngramkey.split(' ', 1)[1]
					ngramkey = ngramkey + " </s>"
					ngramtable = addToTable(ngramkey,ngramtable)
					ngramkey = "<s>"
					i = 1
			else:

				splitlines = line.translate(None, '[]').split()
				for word in splitlines:
					word = word.split("/")[1]
					if i == 1:
						ngramkey += " " + word
						i+= 1
					elif i == 2:
						ngramkey += " " + word
						ngramtable = addToTable(ngramkey,ngramtable)
						ngramkey = ngramkey.split(' ', 1)[1]
					#wordsplit = word.split("/")

	return ngramtable

# sort from highest frequency to lowest frequency ngrams and their counts
## ngramtable = the table which is to be sorted
def printhigh(ngramtable):
	# sort ngrams
	top =  sorted(ngramtable.iteritems(), key=lambda (k,v):(v,k), reverse=False)
	return top

# good turing
# applies good turing smoothing
#
## ngramtable = is the table to be smoothed
## pofn = a list of probabilities from using add1 smoothing
def calcProbabilityGT(ngramtable,pofn):
	nofngrams = sum(ngramtable.values())
	global p0
	p0 = float(numberofrs[1])/float(nofngrams)
	counter = -1
	k = 4
	# sort ngrams from high to low
	sortngrams = printhigh(ngramtable)

	# iterate backwards over sorted list and get p of ngrams < 5
	while sortngrams[counter][1] < k + 1:
		temp0 = numberofrs[ sortngrams[counter][1] ]
		temp1 = numberofrs[ sortngrams[counter][1]+1 ]
		pofn[sortngrams[0][0]] *= float(temp1)/float(temp0)
		counter -= 1
	return pofn

# add 1 smoothing
# applies add 1 smoothing
#
## ngramtable = the table to be smoothed
## comments = boolean which shows output for every sentence
## n = ngramlength
def calcProbabilityAdd1(ngramtable,comments,n):
	nofngrams = sum(ngramtable.values())
	pofngrams = {}
	for ngram in ngramtable:
		if ngram in ngramtable:
			pofngram = (float(ngramtable[ngram])+1) / float(nofngrams)
			if comments:
				print "The probability of the ngram '%s' occuring is %.20f" % (ngram,pofngram)
			pofngrams[ngram] = pofngram
		else:
			if comments:
				print "The probability of the ngram '%s' occuring is %f" % (ngram,0.0)
			pofngrams[ngram] = 0.0
	return pofngrams

# get number ngrams under k occurrences
# 
## ngramtable = the ngrams which are to be thresholded
def getR(ngramtable):
	i = 1
	k = 4
	while i <= k + 1:
		numberofrs[i] = listofocc.count(i)
		i += 1

# calculate probability of sentence
#
## ngramtable = the table of probabilities from the trainingset
## sfile = the file which is to be read
## n = ngramlength
def checksentence(ngramtable, sfile,n):
	# init variables
	progress = True
	ngramkey = ""
	i = 0
	ngrams = []
	pofsentence = {}
	pofn = {}
	zerocounter = 0

	# calculate probabilty with turing smoothing for trainingset
	pofn = calcProbabilityAdd1(ngramtable, False,3)
	getR(ngramtable)
	pofn = calcProbabilityGT(ngramtable, pofn)
	#probtemppre =  1.0 /float(sum(ngramtable.values()))
	#probtemppre *= float(numberofrs[1])/1.0

	# read sentences and get probabilities
	newtable = readSentences(sfile,pofn)

	return newtable

# testset and trainingset
train 	= "trainSet.txt"
test 	= "TestSet.txt"
p0 		= 0

# read tags from trainingset into table
p = readTagfile(train)

# get a list of occurences and 
# init a list for the number of ngram occurences under k
listofocc = p.values()
numberofrs = {}

# apply smoothing and calculate probabilities for trainset
# read trainset into sentences and calc probability
sentencetable = checksentence(p,test,3)
#print sentencetable


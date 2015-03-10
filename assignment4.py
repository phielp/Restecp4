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

def addToTable(ngramkey,ngramtable):
	if ngramkey in ngramtable:
		ngramtable[ngramkey] += 1
	else:
		ngramtable[ngramkey] = 1
	return ngramtable


# language model
def readTagfile(f):
	ngramtable = {}
	ngramkey = ""
	i = 0
	remove = ['``/``',"`/``",'`/`',',/,','(/(',')/)',"''/''","'/''","'/'",":/:","$/$",
	".../:","?/.",'[',']','{/(','}/)',
	'#/#','--/:',';/:','-/:','!/.','2/,',"'/:",'non-``/``','Non-``/``',"underwriters/,",
	"an/,","section/,",'US$/$','NZ$/$','C$/$','A$/$','HK$/$','M$/$','S$/$','C/$']




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

# print highest frequency ngrams and their counts
def printhigh(ngramtable):
	# sort ngrams
	top =  sorted(ngramtable.iteritems(), key=lambda (k,v):(v,k), reverse=True)

	# get the bot m results from the sorted ngrams
	return top

# good turing
def calcProbabilityGT(ngramtable,pofn):
	nofngrams = sum(ngramtable.values())
	counter = -1
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

# get ngrams under k occurrences
def getR(ngramtable):
	i = 1
	k = 4
	while i <= k + 1:
		numberofrs[i] = listofocc.count(i)
		i += 1

# calculate probability of sentence
def checksentence(ngramtable, sfile,n):
	ngrams = []
	pofsentence = {}
	pofn = {}
	zerocounter = 0

	
	pofn = calcProbabilityAdd1(ngramtable, False,n)
	getR(ngramtable)
	pofn = calcProbabilityGT(ngramtable, False,n)
	probtemppre =  1.0 /float(sum(ngramtable.values()))
	probtemppre *= float(numberofrs[1])/1.0

	countertime = 0
	lenlines = len(lines)

	# for every sentence (line)
	for line in lines:
		countertime += 1
		print "%i/%i" % (countertime,lenlines)
		# clean up and split into words
		linesplit = line.split()

		# if empty continue
		if not linesplit:
			continue

		# init variables
		i = 0
		ngramkey = ""
		probtemp = 1

		# create ngrams
		for word in linesplit:
			if i == 0:
				ngramkey = word
				i += 1
			elif i < n:
				ngramkey = ngramkey + " " + word
				i += 1
			elif i == n:
				ngrams.append(ngramkey)
				ngramkey = ngramkey + " " + word
				ngramkey = ngramkey.split(' ', 1)[1]

		ngrams.append(ngramkey)

		# calculate probability of ngrams
		for ngram in ngrams:
			if ngram in pofn:
				probtemp *= pofn[ngram]
			else:
				if smoothmethod == "no":
					probtemp = 0
					zerocounter += 1
					continue
				elif smoothmethod == "add1" or smoothmethod == "gt":
					probtemp = probtemppre
		
		if probtemp == 0:
			zerocounter += 1

		

		pofsentence[line] = probtemp

	print "There were %i sentences with zero percent chance." % (zerocounter)
	return pofsentence






p = readTagfile("smalltest.txt")
print p


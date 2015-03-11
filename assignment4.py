#
#	Students	: Philip Bouman , Alex Khawalid
#	Studentnr	: 10668667		, 10634207
#	Assignment A: step 4 NTMI
#	Date		: 06-02-2015
#
# Command-line:
# (1): python assignment4.py -c [trainset] -t [testset] -s [yes|no] -p [predictedtagsfile]
import itertools
import time
from operator import itemgetter
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
						if word == "./.":
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
							continue
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
					if word == "./.":
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
						continue
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

#						lexical model
# read trainset into dictionary with dictionaries and taglist
# so tagoccurences can be accessed as well as tagging of certain words
# f = filepath to trainset
def readTagfileLex(f):
	lextable = {}
	taglist = {}
	remove = ['#/#','--/:',';/:','-/:','!/.','2/,',"'/:",'non-``/``','Non-``/``',"underwriters/,",
	"an/,","section/,",'US$/$','NZ$/$','C$/$','A$/$','HK$/$','M$/$','S$/$','C/$',
	'``/``',"`/``",'`/`',',/,','(/(',')/)',"''/''","'/''","'/'",":/:","$/$",
	".../:","?/.",'[',']','{/(','}/)',"======================================","./.","\/","*/"]

	with open(f, 'r') as fread:
		fread = fread.read()
		# remove tags
		for t in remove:
			fread = fread.replace(t, "")
		fread = fread.replace("ChiatNNP", "Chiat/NNP")
		fread = fread.replace("\SYM", "\*/SYM")
		fread = fread.replace("\NN", "\*/NN")
		fread = fread.split("\n")

		for line in fread:
			line = line.strip().split()
			for word in line:
				[word,tag] = word.split("/")
				if word in lextable:
					if tag in lextable[word]:
						lextable[word][tag] += 1
					else:
						lextable[word][tag] = 1
				else:
					lextable[word] = {tag: 1}

				if tag in taglist:
					taglist[tag] += 1
				else:
					taglist[tag] = 1
	return [lextable,taglist]

#		 			lexical model
# calculate probabilty for lexical model
#
## lextable = lexicon word table with words and assigned tags from trainset
## taglist = list of tagoccurrences in trainset
def calcProbLex(lextable,taglist):
	for word in lextable:
		for tag in lextable[word]:
			lextable[word][tag] /= taglist[tag]
	return lextable 

#					lexical model
# calculate probabilty using smoothing
#
## lextable = lexicon word table with words and assigned tags from trainset
## taglist = list of tagoccurrences in trainset
def calcProbLexGT(lextable,taglist):
	for word in lextable:
		for tag in lextable[word]:
			if lextable[word][tag] == 1:
				lextable[word][tag] = 0.5
			elif lextable[word][tag] == 0:
				lextable[word][tag] = (numberofrs[1]/1)*0.5
			else:
				lextable[word][tag] /= taglist[tag]
	return lextable 

						
#					language model
# sort from highest frequency to lowest frequency ngrams and their counts
## ngramtable = the table which is to be sorted
def printhigh(ngramtable):
	# sort ngrams
	top =  sorted(ngramtable.iteritems(), key=lambda (k,v):(v,k), reverse=False)
	return top

#					language model
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

#					language model
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

# no smoothing probability
# calculates probability without smoothing
#
## ngramtable = the table for which probabilities must be calculated
## comments = boolean which shows output for every sentence
## n = ngramlength
def calcProbability(ngramtable,comments,n):
	nofngrams = sum(ngramtable.values())
	pofngrams = {}
	for ngram in ngramtable:
		if ngram in ngramtable:
			pofngram = (float(ngramtable[ngram])) / float(nofngrams)
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

# check how many of assigned tags were correct
#
## assigned = list of assigned tags
## correct = list of correct tags
def checkTags(assigned,correct,f):
	hits = 0
	i=1
	while i < len(assigned)-1:
		if assigned[i] == "</s>":
			continue
		if assigned[i] == correct[i]:
			hits += 1
		i += 1

	f.write(" ".join(assigned)+"\n")

	return hits

# tag input sentences based on table of probabilities from trainingset
#
## sentences = sentences read from testset
## pofn = probability of ngrams read from trainset
def tagsentences(sentences, pofn):
	# init variables
	assignedtags = []
	tot = 0
	correcttags = []
	ngram = ""
	hits = 0
	i = 0
	f = open(predictions, 'w')

	# for every given sentence
	for line in sentences:

		# split sentence into words and count total number of words
		line = line.split()
		tot += len(line)

		# sentences larger of 15 or more words are to be ignored
		if len(line) > 15:
			continue


		for word in line:
			# if starttag add to taglists
			if word == "<s>":
				assignedtags.append(word)
				correcttags.append(word)
				i = 1
				continue
			# if stop tag check taglists against eachother
			# reset lists
			elif word == "</s>":
				assignedtags.append(word)
				correcttags.append(word)
				hits += checkTags(assignedtags,correcttags,f)
				assignedtags = []
				correcttags = []
				i = 0
				continue
			# if empty item, ignore word
			elif not word:
				continue

			# if only 1 tag has been assigned
			if i == 1:
				possibilities = list(k for k,v in pofn.iteritems() if " ".join(assignedtags) in k.lower())
				if possibilities:
					temptag = possibilities[0].split()[1]
					assignedtags.append(temptag)
				i += 1
			# if 2 or more tags have been assigned
			elif i >= 2:
				# get all ngrams containing last tagged items
				# sort this list and get most probable
				possibilities = list([v,k] for k,v in pofn.iteritems() if " ".join(assignedtags[i:i+1]) in k.lower())
				possibilities = sorted(possibilities, key=itemgetter(1))
				possibilities = possibilities[0][1]
				# if something was found preferably get tag which is not the same
				if possibilities:
					temptag = possibilities.split()
					if temptag[2] != "</s>" and temptag[2] != assignedtags[-1]:
						assignedtags.append(temptag[2])
					elif temptag[1] != assignedtags[-1]:
						assignedtags.append(temptag[1])
					elif temptag[0] != assignedtags[-1] and temptag[0] != "<s>":
						assignedtags.append(temptag[0])
					else:
						assignedtags.append(temptag[1])
				# if nothing was found, loosen criteria
				else:
					possibilities = list(k for k,v in pofn.iteritems() if " ".join(assignedtags[i]) in k.lower())
					temptag = possibilities[0].split()[0]
					assignedtags.append(temptag)
				# update i
				i += 1
			# update correct tags
			correcttags.append(word.split("/")[1])
	f.close()
	# print accuracy of tagging
	print "Language Accuracy:"
	print "%i / %i = %f" % (hits,tot,float(hits)/float(tot))

#						lexical model
# assign tags to sentences
#
## sentences = list of sentences from testset
## lextable = dict of words with tags and probabilities from trainset
def tagsentencelex(sentences, lextable):
	# init variables
	assignedtags = []
	tot = 0
	correcttags = []
	ngram = ""
	hits = 0
	f = open(predictions, 'a')
	f.write("\n\n===============lexicalresults=============\n\n")


	# for every given sentence
	for line in sentences:

		# split sentence into words and count total number of words
		line = line.split()
		tot += len(line)

		# sentences larger of 15 or more words are to be ignored
		if len(line) > 15:
			continue


		for word in line:
			# if starttag add to taglists
			if word == "<s>":
				assignedtags.append(word)
				correcttags.append(word)
				continue
			# if stop tag check taglists against eachother
			# reset lists
			elif word == "</s>":
				assignedtags.append(word)
				correcttags.append(word)
				hits += checkTags(assignedtags,correcttags,f)
				assignedtags = []
				correcttags = []
				continue
			# if empty item, ignore word
			elif not word:
				continue

			# assign tag with highest probability if known
			if word in lextable:
				assignedtags.append( printhigh(lextable[word])[0])
			# if not known tag assign NN
			else:
				assignedtags.append("NN")
			# update correct tags
			correcttags.append(word.split("/")[1])
	f.close()
	# print accuracy of tagging
	print "Lexical Accuracy:"
	print "%i / %i = %f" % (hits,tot,float(hits)/float(tot))



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
	if smoothing == "yes":
		pofn = calcProbabilityAdd1(ngramtable, False,3)
		getR(ngramtable)
		pofn = calcProbabilityGT(ngramtable, pofn)
		pofnlex = calcProbLexGT(lextable,taglist)
	else:
		pofn = calcProbability(ngramtable,False,3)
		pofnlex = calcProbLex(lextable,taglist)

	# read sentences and get probabilities
	newtable = readSentences(sfile,pofn)
	# tag sentences
	tagsentences(newtable,pofn)
	tagsentencelex(newtable,pofnlex)

	return newtable


						# main code #
############################################################
starttime = time.time()
# parse options
parser = OptionParser()
parser.add_option("-c", "--trainset", dest="trainset")
parser.add_option("-p", "--testsetpredicted", dest="predictions")
parser.add_option("-t", "--testset", dest="testset")
parser.add_option("-s", "--smoothing" , dest="smoothing")

(options,args) = parser.parse_args()

# if smoothing assigned
if options.smoothing:
	smoothing = options.smoothing
else:
	smoothing = "yes"

# if trainset assigned
if options.trainset:
	train = options.trainset
else:
	train 	= "trainSet.txt"

# if testset assigned
if options.testset:
	train = options.testset
else:
	test 	= "TestSet.txt"

# if predictionsfile assigned
if options.predictions:
	predictions = options.predictions
else:
	predictions = "predictions.txt"


# init chance for unknown tags with GT smoothing
p0 		= 0

# read tags from trainingset into table
p = readTagfile(train)
[lextable,taglist] = readTagfileLex(train)

# get a list of occurences and 
# init a list for the number of ngram occurences under k
listofocc = p.values()
numberofrs = {}

# apply smoothing and calculate probabilities for trainset
# read trainset into sentences and calc probability
sentencetable = checksentence(p,test,3)
endtime = time.time()

print endtime - starttime



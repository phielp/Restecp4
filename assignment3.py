#
#	Students	: Philip Bouman , Alex Khawalid
#	Studentnr	: 10668667		, 10634207
#	Assignment A: step 2 NTMI
#	Date		: 06-02-2015
#
# Command-line:
# (1): python assignment2.py -c austen.txt -n 3
# (2): python assignment2.py -c austen.txt -p test2.txt
# (3): python assignment2.py -c austen.txt -n 3 -s test.txt
# (4): python assignment2.py -c austen.txt -n 3 -fo
import itertools
from optparse import OptionParser

# if n = 1
def getunigrams(f,n):
	ngramtable = {}
	with open(f, 'r') as f:
		for line in f:
			if line:
				if ngramtable["START"]:
					ngramtable["START"] += 1;
				else:
					ngramtable["START"] = 1;
				if ngramtable["END"]:
					ngramtable["END"] += 1;
				else:
					ngramtable["END"] = 1;
			for words in line.split():
				if words in ngramtable:
					ngramtable[words] += 1
				else:
					ngramtable[words] = 1

	return ngramtable

# reads lines from file and splits into words
def getmultigrams(f,n):
	# expression used to split words
	ngramtable = {}
	ngramkey = ""
	i = 0
	linenumber = 1

	# read all lines into words
	with open(f, 'r') as f:
		for line in f:
			j=0
			splitlines = line.split()
			for words in splitlines:
				# Add start if first line
				if j == 0:
					if i == 0:
						ngramkey = "START"
						i += 1
					else:
						ngramkey = ngramkey + " START"
						#print ngramkey
						if ngramkey in ngramtable:
							ngramtable[ngramkey] += 1
						else:
							ngramtable[ngramkey] = 1
						ngramkey = ngramkey.split(' ', 1)[1] 


				# if ngram has less than n words
				if i < n:
					if i == 0:
						ngramkey = words
					else:
						ngramkey = ngramkey + " " + words
					i += 1
					#print "\n ngramkey = %s \n linenumber = %i \n j = %i" % (ngramkey,linenumber,j)
				if i == n:
					# increment occurences of ngram
					if ngramkey in ngramtable:
						ngramtable[ngramkey] += 1
						i = n-1
						ngramkey = ngramkey.split(' ', 1)[1]
					# if new ngram add to table
					else:
						ngramtable[ngramkey] = 1
						i = n-1
						ngramkey = ngramkey.split(' ', 1)[1]
				if j == len(splitlines)-1:
					ngramkey = ngramkey + " " + "END" 
					#print ngramkey
					if ngramkey in ngramtable:
						ngramtable[ngramkey] += 1
					else:
						ngramtable[ngramkey] = 1
					ngramkey = ngramkey.split(' ', 1)[1]
				j += 1
			linenumber += 1
	return ngramtable

# get ngrams
def getngrams(f,n):
	if n > 1:
		ngramtable = getmultigrams(f,n)
	else:
		ngramtable = getunigrams(f,n)
	return ngramtable


def getR(ngramtable):
	i = 1
	while i <= k + 1:
		numberofrs[i] = listofocc.count(i)
		i += 1


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

# calculate probability of ngram
def calcProbability(ngramtable,comments,n):
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

# calculate probability of sentence
def checksentence(ngramtable, sfile,n,usefile,smoothmethod):
	ngrams = []
	pofsentence = {}
	pofn = {}
	zerocounter = 0

	# get probabilities for ngrams
	if smoothmethod == "no":
		pofn = calcProbability(ngramtable, False,n)
	elif smoothmethod == "add1":
		pofn = calcProbabilityAdd1(ngramtable, False,n)
		probtemppre =  1.0 /float(sum(ngramtable.values()))
	elif smoothmethod == "gt":
		pofn = calcProbabilityAdd1(ngramtable, False,n)
		getR(ngramtable)
		pofn = calcProbability(ngramtable, False,n)
		probtemppre =  1.0 /float(sum(ngramtable.values()))
		probtemppre *= float(numberofrs[1])/1.0
	else:
		print "Invalid method"
		return None


	# read from file or not
	if usefile:
		f = open(sfile,'r')
		lines = f.readlines()
	else:
		lines = sfile

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





##################
#    main code   #
##################

############### parse command line ################

parser = OptionParser()
parser.add_option("-c", "--corpus", dest="file_in")
parser.add_option("-n", dest="nth")
parser.add_option("-t", "--testcorpus", dest="test_corp")
parser.add_option("-s", "--smoothing" , dest="smoothmethod")

(options,args) = parser.parse_args()

# parameters manual editing
file_name = options.file_in
testcorpus = options.test_corp
if options.nth:
	orderofn = int(options.nth)
else:
	orderofn = 2

###################################################

### init variables 
ngramtable = getngrams(file_name,orderofn)
numberofrs = {}
listofocc = ngramtable.values()
k = 5

### 2.
if options.smoothmethod:
	# check probability of sentence
	pofn = checksentence(ngramtable,testcorpus,2,True,options.smoothmethod)










# end
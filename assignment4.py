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

	with open(f, 'r') as f:
		for line in f:
			# if line is a start or stop symbol
			if line == "======================================\n":
				if i == 0:
					ngramkey = "<s>"
					i = 1
				elif i < 3:
					ngramkey = ngramkey + " </s>"
					ngramtable = addToTable(ngramkey,ngramtable)
					ngramkey = ""
					i = 0
				else:
					ngramkey = ngramkey.split(' ', 1)[1]
					ngramkey = ngramkey + " </s>"
					ngramtable = addToTable(ngramkey,ngramtable)
					ngramkey = ""
					i = 0
			elif line == "./.\n":
				if i <= 3:
					ngramkey = ngramkey + " </s>"
					ngramtable = addToTable(ngramkey,ngramtable)
					ngramkey = ""
					i = 0
				else:
					ngramkey = ngramkey.split(' ', 1)[1]
					ngramkey = ngramkey + " </s>"
					ngramtable = addToTable(ngramkey,ngramtable)
					ngramkey = ""
					i = 0
			else:
				splitlines = line.translate(None, '[]').split()
				print splitlines
				for word in splitlines:
					if i == 1:
						ngramkey += " " + word
						i+= 1
					elif i == 2:
						ngramkey += " " + word
						ngramtable = addToTable(ngramkey,ngramtable)
						ngramkey = ngramkey.split(' ', 1)[1]
					#wordsplit = word.split("/")

	return ngramtable




p = readTagfile("smalltest.txt")
print p


openTrainSet = open('/Users/philipbouman/Documents/AI/NTMI/Restecp4/trainSet.txt')
trainSet = openTrainSet.read()

remove = ['``/``',"`/``",'`/`',',/,','(/(',')/)',"''/''","'/''","'/'",":/:","$/$",
".../:","?/.",'======================================','[',']','{/(','}/)','\n',
'#/#','--/:',';/:','-/:','!/.','2/,',"'/:",'non-``/``','Non-``/``',"underwriters/,",
"an/,","section/,",'US$/$','NZ$/$','C$/$','A$/$','HK$/$','M$/$','S$/$','C/$']

# remove tags
for t in remove:
	trainSet = trainSet.replace(t, "")

# remove double space
trainSet = " ".join(trainSet.split())

trainSet = "<START>/<START>" + trainSet

print trainSet
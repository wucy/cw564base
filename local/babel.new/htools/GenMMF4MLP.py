# This script is used to generate an "indexed" persudo MMF for DNN-HMM hybrid systems.
# The model structure are and the transition probs are extracted from the input MMF-in.
# The command template is,
#	python script.py UnitList-in MMF-in MMF-out option
#		option == sil3-sp1, sil2-sp2, full+sil2-sp2
#			options are joint by '+'

import os
import sys

# system arguments
UnitListPath = sys.argv[1]
InputMMFPath = sys.argv[2]
OutputMMFPath = sys.argv[3]
option = sys.argv[4]
siltgt = 'sil'
sptgt = 'sil'

#if option.count('full'):
#	sptgt = 'sp'

# auxilary methods
def WriteLines(file, lines):
	for eachline in lines:
		if not eachline.endswith(os.linesep):
			file.write(eachline + os.linesep)

def ConvName(name, kind):	#kind: could be empty string ''
	if name.startswith('~'):
		name = name.split('"')[1]
	else:
		name = '~' + kind + ' "' + name + '"'
	return name

def Line2Array(line):
	items = line.split(' ')
	array = []
	for eachitem in items:
		if eachitem != '':
			array.append(float(eachitem))
	return array

def Float2Str(value):
	strval = "%e" % value
	return strval

def Array2Line(array):
	line = ''
	for eachval in array:
		line += ' ' + Float2Str(eachval)
	return line

def ParseTransP(lines, index):
	if lines[index + 1].startswith('<TRANSP> '):
		index += 1
		transmat = []
		transdim = int(lines[index].replace(os.linesep, '').split(' ')[1])
		for tidx in range(0, transdim):
			index += 1
			transmat.append(Line2Array(lines[index]))
		return [transdim, transmat, index]

def ParseState(lines, index):
	if lines[index + 1].startswith('<NUMMIXES> ') or lines[index + 1].startswith('<MEAN> '):
		statedef = []
		mixnum = -1
		if lines[index + 1].startswith('<NUMMIXES> '):
			index += 1
			mixnum = int(lines[index].replace(os.linesep, '').split(' ')[1])
		else:
			mixnum = 1
		for midx in range(0, mixnum):
			mixidx = -1
			mixwgt = 0.0
			if lines[index + 1].startswith('<MIXTURE> '):
				index += 1
				items = lines[index].replace(os.linesep, '').split(' ')
                        	mixidx = int(items[1])
                        	mixwgt = float(items[2])
			elif lines[index + 1].startswith('<MEAN> '):
				mixidx = 1
				mixwgt = 1.0
			else:
				index -= 1
				break
			# get mean vector
			index += 1
			meandim = int(lines[index].replace(os.linesep, '').split(' ')[1])
			index += 1
			meanvec = Line2Array(lines[index])
			mean = [meandim, meanvec]
			# get variance vector
			index += 1
                        vardim = int(lines[index].replace(os.linesep, '').split(' ')[1])
                        index += 1
			varvec = Line2Array(lines[index])
			variance = [vardim, varvec]
			# gconst
			mixture = [mixidx, mixwgt, mean, variance]
			if lines[index + 1].startswith('<GCONST> '):
				index += 1
				mixture.append(float(lines[index].replace(os.linesep, '').split(' ')[1]))
			statedef.append(mixture)
		return [mixnum, statedef, index]

# data structures
unithash = {}
sillist = []
splist = []
transhash = {}
translist = []
statehash = {}
statelist = []
hmmhash = {}
hmmlist = []
tcitehash = {}
scitehash = {}
stategroups = {}

# load UnitList
file = open(UnitListPath)
lines = file.readlines()
file.close()

for eachline in lines:
	items = eachline.replace(os.linesep, '').split(' ')
	key = items[0]
	value = int(items[1]) + 1	# because tiedlist/mono.list always starts from zero while MMF starts from one
	unithash[key] = value
	if key.startswith('sil_') or key == 'sil':
		sillist.append(key)
	elif key == 'sp':
		splist.append(key)

# load model structure
file = open(InputMMFPath)
lines = file.readlines()
file.close()

index = 0
while index < len(lines):
	# save tied transp
	if lines[index].startswith('~t "'):
		transname = lines[index].replace(os.linesep, '')
		[transdim, transmat, index] = ParseTransP(lines, index)
		transhash[transname] = [transdim, transmat]
		translist.append(transname)
		tcitehash[transname] = 0	# set citation hash table
	# save hmm defs
	elif lines[index].startswith('~h "'):
		hmmname = lines[index].replace(os.linesep, '')
		index += 1
		if lines[index].startswith('<BEGINHMM>'):
			index += 1
			statedefs = []
			# load each state
			statenum = int(lines[index].replace(os.linesep, '').split(' ')[1])	#<NUMSTATES>
			for sidx in range(1, statenum - 1):
				index += 1
				stateidx = int(lines[index].replace(os.linesep, '').split(' ')[1])	#<STATE>
				if lines[index + 1].startswith('~s "'):	# previous tied state
					index += 1
					statename = lines[index].replace(os.linesep, '')
					statedefs.append(statename)
					scitehash[statename] = scitehash[statename] + 1	# increase citation s
					stategroups[statename].append(ConvName(ConvName(hmmname, '') + '[' + str(stateidx) + ']', 's'))
				else:	# untied state
					statename = ConvName(ConvName(hmmname, '') + '[' + str(stateidx) + ']', 's')
					[mixnum, mixdefs, index] = ParseState(lines, index)
					statehash[statename] = [mixnum, mixdefs]
					statedefs.append(statename)
					scitehash[statename] = 1	# set citation hash table
			# load the transp
			index += 1
			transname = ''
			if lines[index].startswith('~t "'):
				transname = lines[index].replace(os.linesep, '')
				tcitehash[transname] = tcitehash[transname] + 1	# set citation hash table
			else:
				transname = ConvName(hmmname, 't')
				[transdim, transmat, index] = ParseTransP(lines, index)
                		transhash[transname] = [transdim, transmat]
				tcitehash[transname] = 1	# set citation hash tatble
			index += 1	#<ENDHMM>
			# setup the hmmdef
			hmmdef = [statedefs, transname]
			hmmhash[hmmname] = hmmdef
			hmmlist.append(hmmname)
	# save tied state
	elif lines[index].startswith('~s "'):
		statename = lines[index].replace(os.linesep, '')
		[mixnum, mixdefs, index] = ParseState(lines, index)
		statehash[statename] = [mixnum, mixdefs]
		statelist.append(statename)
		scitehash[statename] = 0        # set citation hash table
		stategroups[statename] = []
	###else:
	###	print lines[index].replace(os.linesep, '')

	index += 1		

# patch sil/sp models, if needed
if len(sillist) == 0:
	sillist = splist
elif len(splist) == 0:
	splist = sillist
# fix sil
silhmm = hmmhash[ConvName('sil', 'h')]
print ConvName('sil', 'h')
transdim = transhash[silhmm[1]][0]
print str(len(sillist)) + '\t' + str(sillist) + '\t' + str(len(silhmm[0])) + '\t' + str(silhmm[0])
if len(silhmm[0]) != len(sillist):
	if len(sillist) == 1 and option.count('sil3-sp1'):	# only handle this case at the moment
		print 'fix sil model'
		# reset dimension
		transdim = 5
		# fix states
		statedefs = silhmm[0]
		for eachstate in statedefs:	# reduce citation for tied sil states
			if scitehash.has_key(eachstate):
				scitehash[eachstate] = scitehash[eachstate] - 1
		statedefs = [ConvName(siltgt, 's'), ConvName(siltgt, 's'), ConvName(siltgt, 's')]
		if scitehash.has_key(ConvName(siltgt, 's')):	# increase citation if tied
			scitehash[ConvName(siltgt, 's')] = scitehash[ConvName(siltgt, 's')] + 3
		if not statehash.has_key(ConvName(siltgt, 's')):
			statehash[ConvName(siltgt, 's')] = []	# if not tied, treat as untied, but no physical GMM def
		# fix transp
		if tcitehash.has_key(silhmm[1]):
			tcitehash[silhmm[1]] = tcitehash[silhmm[1]] - 1	# decrease citation 
		transmat = []
		for ridx in range(transdim):
			row = []
			for cidx in range(0, transdim):
				if ridx == 0:
					if cidx == 1:
						row.append(1.0)
					else:
						row.append(0.0)
				elif ridx != (transdim - 1):
					if cidx == ridx or cidx == (ridx + 1):
						row.append(0.5)
					else:
						row.append(0.0)
				else:
					row.append(0.0)
			transmat.append(row)
		if tcitehash.has_key(ConvName('sil', 't')):
			tcitehash[ConvName('sil', 't')] = tcitehash[ConvName('sil', 't')] + 1
                if not statehash.has_key(ConvName(sptgt, 's')):
                        statehash[ConvName(sptgt, 's')] = []   # if not tied, treat as untied, but no physical GMM def
		transhash[ConvName('sil', 't')] = [transdim, transmat]	# if has_key(transname), then just cover it (assume no other matrix would rely on it)
		# fix hmm
		hmmhash[ConvName('sil', 'h')] = [statedefs, ConvName('sil', 't')]
        elif len(sillist) == 1 and option.count('sil2-sp2'):   # only handle this case at the moment
                print 'fix sil model'
                # reset dimension
                transdim = 4
                # fix states
                statedefs = silhmm[0]
                for eachstate in statedefs:     # reduce citation for tied sil states
                        if scitehash.has_key(eachstate):
                                scitehash[eachstate] = scitehash[eachstate] - 1
                statedefs = [ConvName(siltgt, 's'), ConvName(siltgt, 's')]
                if scitehash.has_key(ConvName(siltgt, 's')):    # increase citation if tied
                        scitehash[ConvName(siltgt, 's')] = scitehash[ConvName(siltgt, 's')] + 2
                if not statehash.has_key(ConvName(siltgt, 's')):
                        statehash[ConvName(siltgt, 's')] = []   # if not tied, treat as untied, but no physical GMM def
                # fix transp
                if tcitehash.has_key(silhmm[1]):
                        tcitehash[silhmm[1]] = tcitehash[silhmm[1]] - 1 # decrease citation 
                transmat = []
                for ridx in range(transdim):
                        row = []
                        for cidx in range(0, transdim):
                                if ridx == 0:
                                        if cidx == 1:
                                                row.append(1.0)
                                        else:
                                                row.append(0.0)
                                elif ridx != (transdim - 1):
                                        if cidx == ridx or cidx == (ridx + 1):
                                                row.append(0.5)
                                        else:
                                                row.append(0.0)
                                else:
                                        row.append(0.0)
                        transmat.append(row)
                if tcitehash.has_key(ConvName('sil', 't')):
                        tcitehash[ConvName('sil', 't')] = tcitehash[ConvName('sil', 't')] + 1
                if not statehash.has_key(ConvName(sptgt, 's')):
                        statehash[ConvName(sptgt, 's')] = []   # if not tied, treat as untied, but no physical GMM def
                transhash[ConvName('sil', 't')] = [transdim, transmat]  # if has_key(transname), then just cover it (assume no other matrix would rely on it)
                # fix hmm
                hmmhash[ConvName('sil', 'h')] = [statedefs, ConvName('sil', 't')]
	elif len(sillist) == 10 and option.count('sil2-sp2'):	#for 10sil mod
		print 'fix sil model'
		#reset dimension
		transdim = 22
		statedefs = silhmm[0]
		for eachstate in statedefs:     # reduce citation for tied sil states
			print eachstate
                        if scitehash.has_key(eachstate):
                                scitehash[eachstate] = scitehash[eachstate] - 1
		statedefs = []
		silnamelist = ['sil_1', 'sil_2', 'sil_3', 'sil_4', 'sil_5', 'sil_6', 'sil_7', 'sil_8', 'sil_9', 'sil_10']
		for eachsil in silnamelist:
			statedefs.append(ConvName(eachsil, 's'))
			statedefs.append(ConvName(eachsil, 's'))
			if scitehash.has_key(ConvName(eachsil, 's')):
				scitehash[ConvName(eachsil, 's')] = scitehash[ConvName(eachsil, 's')] + 2
			if not statehash.has_key(ConvName(eachsil, 's')):
				statehash[ConvName(eachsil, 's')] = []
		# fix transp
		if tcitehash.has_key(silhmm[1]):
                        tcitehash[silhmm[1]] = tcitehash[silhmm[1]] - 1 # decrease citation 
		transmat = []
		firstrow = transhash[silhmm[1]][1][0]
		transmat.append([])
		transmat[0].append(0.0)
		for cidx in range(1, len(firstrow) - 1, 3):
			transmat[0].append(firstrow[cidx])
			transmat[0].append(0.0)
		transmat[0].append(0.0)
		for ridx in range(1, transdim - 1):
			row = []
			for cidx in range(0, transdim):
				if ridx % 2 == 1:
					if cidx == ridx or cidx == (ridx + 1):
						row.append(0.5)
					else:
						row.append(0.0)
				else:
					if cidx == ridx:
						row.append(0.5)
					elif cidx == transdim - 1:
						row.append(0.5)
					else:
						row.append(0.0)
			transmat.append(row)
		transmat.append([0 for i in range(transdim)])
		if tcitehash.has_key(ConvName('sil', 't')):
                        tcitehash[ConvName('sil', 't')] = tcitehash[ConvName('sil', 't')] + 1
		if not statehash.has_key(ConvName(sptgt, 's')):
                        statehash[ConvName(sptgt, 's')] = []
		transhash[ConvName('sil', 't')] = [transdim, transmat]
		# fix hmm
                hmmhash[ConvName('sil', 'h')] = [statedefs, ConvName('sil', 't')] 
	else:
		print 'unable to fix bad sil model!'
		#sys.exit()
# fix sp
sphmm = hmmhash[ConvName('sp', 'h')]
transdim = transhash[sphmm[1]][0]
if len(sphmm[0]) != len(splist):     
	if len(splist) == 1 and option.count('sil3-sp1'):	# only handle this case at the moment
		print 'fix sp model'
		# fix states
		statedefs = sphmm[0]
		for eachstate in statedefs:     # reduce citation for tied sp states
                        if scitehash.has_key(eachstate):
                                scitehash[eachstate] = scitehash[eachstate] - 1
		statedefs = [ConvName(sptgt, 's')]
		if scitehash.has_key(ConvName(sptgt, 's')):
			scitehash[ConvName(sptgt, 's')] = scitehash[ConvName(sptgt, 's')] + 1
		# fix transp
		if tcitehash.has_key(sphmm[1]):
                        tcitehash[sphmm[1]] = tcitehash[sphmm[1]] - 1 # decrease citation
		transmat = [[0.0, 0.5, 0.5], [0.0, 0.5, 0.5], [0.0, 0.0, 0.0]]
		if tcitehash.has_key(ConvName('sp', 't')):
                        tcitehash[ConvName('sp', 't')] = tcitehash[ConvName('sp', 't')] + 1 # decrease citation
		transhash[ConvName('sp', 't')] = [3, transmat]
		# fix hmm
		hmmhash[ConvName('sp', 'h')] = [statedefs, ConvName('sp', 't')]
        elif len(splist) == 1 and option.count('sil2-sp2'):    # only handle this case at the moment
                print 'fix sp model'
                # fix states
                statedefs = sphmm[0]
                for eachstate in statedefs:     # reduce citation for tied sp states
                        if scitehash.has_key(eachstate):
                                scitehash[eachstate] = scitehash[eachstate] - 1
                statedefs = [ConvName(sptgt, 's'), ConvName(sptgt, 's')]
                if scitehash.has_key(ConvName(sptgt, 's')):
                        scitehash[ConvName(sptgt, 's')] = scitehash[ConvName(sptgt, 's')] + 2
                # fix transp
                if tcitehash.has_key(sphmm[1]):
                        tcitehash[sphmm[1]] = tcitehash[sphmm[1]] - 1 # decrease citation
                transmat = [[0.0, 1.0, 0.0, 0.0], [0.0, 0.0, 1.0, 0.0], [0.0, 0.0, 0.5, 0.5], [0.0, 0.0, 0.0, 0.0]]
                if tcitehash.has_key(ConvName('sp', 't')):
                        tcitehash[ConvName('sp', 't')] = tcitehash[ConvName('sp', 't')] + 1 # decrease citation
                transhash[ConvName('sp', 't')] = [4, transmat]
                # fix hmm
                hmmhash[ConvName('sp', 'h')] = [statedefs, ConvName('sp', 't')]
	elif len(splist) == 10 and option.count('sil2-sp2'):
		print 'fix sp model'
                # fix states
                statedefs = sphmm[0]
                for eachstate in statedefs:     # reduce citation for tied sp states
                        if scitehash.has_key(eachstate):
                                scitehash[eachstate] = scitehash[eachstate] - 1
		statedefs = [ConvName('sil_10', 's'), ConvName('sil_10', 's')]
		if scitehash.has_key(statedefs[0]):
			scitehash[ConvName('sil_10', 's')] = scitehash[ConvName('sil_10', 's')] + 2
		# fix transp
                if tcitehash.has_key(sphmm[1]):
                        tcitehash[sphmm[1]] = tcitehash[sphmm[1]] - 1 # decrease citation
                transmat = [[0.0, 1.0, 0.0, 0.0], [0.0, 0.0, 1.0, 0.0], [0.0, 0.0, 0.5, 0.5], [0.0, 0.0, 0.0, 0.0]]
		if tcitehash.has_key(ConvName('sp', 't')):
                        tcitehash[ConvName('sp', 't')] = tcitehash[ConvName('sp', 't')] + 1 # decrease citation
                transhash[ConvName('sp', 't')] = [4, transmat]
                # fix hmm
                hmmhash[ConvName('sp', 'h')] = [statedefs, ConvName('sp', 't')]
	else:
		print 'unable to fix bad sp model!'
		#sys.exit()
# remove the unused tied states/matrices (unused untied entities are automaically reomoved)
for sidx in range(len(statelist) - 1, -1, -1):
	if scitehash[statelist[sidx]] == 0:
		print 'remove state ' + statelist[sidx]
		statelist.pop(sidx)
for tidx in range(len(translist) - 1, -1, -1):
        if tcitehash[translist[tidx]] == 0:
		print 'remove transp ' + translist[tidx]
                translist.pop(tidx)

# output model
file = open(OutputMMFPath, 'w')

# output head lines
headlines = ['~o', '<STREAMINFO> 1 ' + str(len(unithash)), '<VECSIZE> ' + str(len(unithash)) + '<NULLD><USER><DIAGC>']
WriteLines(file, headlines)

# output tied transp 
translines = []
for transname in translist:
	translines.append(transname)
	[transdim, transmat] = transhash[transname]
	translines.append('<TRANSP> ' + str(transdim))
	for eachrow in transmat:
		translines.append(Array2Line(eachrow))
	transhash.pop(transname)
WriteLines(file, translines)

# output tied-states
if option.count('full') == 0:
	statelines = []
	for statename in statelist:
		statelines.append(statename)
		statelines.append('<HYBRIDIDX> ' + str(unithash[ConvName(statename, '')]))	# name conversion needed
		statehash.pop(statename)
	WriteLines(file, statelines)

# output hmms
hmmlines = []
for hmmname in hmmlist:
	hmmlines.append(hmmname)
	[statedefs, transname] = hmmhash[hmmname]
	hmmlines.append('<BEGINHMM>')
	# output states
	hmmlines.append('<NUMSTATES> ' + str(len(statedefs) + 2))
	hmmname = ConvName(hmmname, '')
	for sidx in range(0, len(statedefs)):
		hmmlines.append('<STATE> ' + str(sidx + 2))
		#print str(sidx) + '\thmmname\t' + hmmname
		if option.count('full') and hmmname != siltgt and hmmname != 'sp':
			logsenone = ConvName(hmmname + '[' + str(sidx + 2) + ']', 's')
			if not unithash.has_key(ConvName(logsenone, '')):
				#print hmmname + '\t' + statedefs[sidx]
				group = stategroups[statedefs[sidx]]
				for gidx in range(0, len(group)):
					if unithash.has_key(ConvName(group[gidx], '')):
						#print 'Got It!\t' + group[gidx]
						logsenone = group[gidx]
						break
			statedefs[sidx] = logsenone
			statehash[statedefs[sidx]] = []
		if statehash.has_key(statedefs[sidx]):
			hmmlines.append('<HYBRIDIDX> ' + str(unithash[ConvName(statedefs[sidx], '')]))	# name conversion needed
		else:
			hmmlines.append(statedefs[sidx])
	# output transp
	if transhash.has_key(transname):
		[transdim, transmat] = transhash[transname]
        	hmmlines.append('<TRANSP> ' + str(transdim))
        	for eachrow in transmat:
                	hmmlines.append(Array2Line(eachrow))
	else:
		hmmlines.append(transname)
	hmmlines.append('<ENDHMM>')
WriteLines(file, hmmlines)

# finish writing
file.close()



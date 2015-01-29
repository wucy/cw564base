# This script includes some convinient methods for MLP by QuickNet/TNet.
# Current support functions include:
#	-1.QuickNet DPT method based on Prof. Gales' suggestion.
#	   Pos could be -1 or -2
#		python script.py -qn-dpt2 Pos size pre-trained-MLP(in) rand-MLP(out) transplanted-MLP(out)
#
#	1. QuickNet model merger: used to taper the output layer of a pre-trained MLP and transplant specified randomly obtained hidden layers and a new output layer. 
#	   Note that it is important to make the new output layer compatible with the new hidden layer (since we do not check it here). 
#		python script.py -qn-dpt pre-trained-MLP(in) pre-initialized-MLP(in) transplanted-MLP(out)
#
#	2. Show QuickNet model by translate it into text.
#	   Note that QuickNet it self does not support text format models
#		python script.py -qn-showmodel binary-MLP(in) ascii-MLP(out)
#	
#	3. Taper off the layers above the specified one
#	   Used for bottleneck feature
#		python script.py -qn-toff binary-MLP(in) layer-num(int) binary-MLP(out) 
#
#	4. Convert aligned MLF file to lab.pfile
#	   Note QuickNet does not support such conversion, context-frame-offset = (context-frame-num - 1) / 2
#		python script.py -qn-mlf2pfile ascii-MLF(in) frame-duration(int) context-frame-offset(int) binary-PFile(out) 
#
#	5. Show the statistics of a QuickNet model
#		python script.py -qn-statsmodel binary-MLP(in)
#
#	6. Generate initial values for a QuickNet model with max/min (uniform), mean/var (gauss), or N/A (normuni) specified for each layer
#		python script.py -qn-randinit binary-MLP(out) uniform/gauss/normuni topology(e.g. 468,1000,38) [p11,p12,p13,p14 p21,p22,p23,p24 ...]
#
#	7. Convert a given (CI/CD)state label pfile to the relevant (CI/CD) phone label pfile
#		python script.py -qn-state2phone state-num-file(text) phone-num-file(text) in-lab-pfile out-lab-pfile HHEd-sh-file
#
#	8. Conver a given CD phone label pfile to the relevant CI phone label pfile
#		python script.py -qn-cd2ci cd-phone-num-file(text) ci-phone-num-file(text) in-lab-pfile out-lab-pfile
#
#	9. Compare hypothesized lab pfile with referenced lab pfile
#		python script.py -qn-res ref-lab-pfile hyp-lab-pfile
#
#	10. generate lab pfile confusion matrix
#		python script.py -qn-cmat ref-lab-pfile hyp-lab-pfile
#
#	11. generate ftr pfile
#		python script.py -qn-htk2pfile (ext)scp-file contex-frame-offset(int) ftr-pfile natural/copy
#
#
# cz277@cam.ac.uk

import os
import sys
import math
import random
import struct
import os.path
#from ctypes import *

from cw564.io import *

QN_MAX_LAYER_NUM = 20
QN_WEIGHTS_NAME = 'weights'
QN_BIAS_NAME = 'bias'

def QN_GetBlockName(blockname, layerid):
	if blockname.startswith(QN_WEIGHTS_NAME):
		return QN_WEIGHTS_NAME + str(layerid) + str(layerid + 1) + '\0'#blockname[-1]
	elif blockname.startswith(QN_BIAS_NAME):
		return QN_BIAS_NAME + str(layerid + 1) + '\0'#blockname[-1]

def QN_Block_Reader(file):
	block = []
	#matrix header
	(type, mrows, mcols, imagf, namlen) = struct.unpack('iiiii', file.read(4 + 4 + 4 + 4 + 4))
	header = []
	header.append(type)
	header.append(mrows)
	header.append(mcols)
	header.append(imagf)
	header.append(namlen)
	#name string
	name = ''
	for idx in range(0, namlen):
		name += struct.unpack('c', file.read(1))[0]	
	#value matrix
	values = []
	for ridx in range(0, mrows):
		currow = []
		for cidx in range(0, mcols):
			currow.append(struct.unpack('f', file.read(4))[0])
		values.append(currow)
	#setup the block
	block.append(header)
	block.append(name)
	block.append(values)
	return block

# loader for QuickNet MLP
def QN_MLP_Reader(mlppath):
	mlpstruct = []
	file = open(mlppath, 'rb')
	while file.tell() < os.path.getsize(mlppath):
		layer = []
		layer.append(QN_Block_Reader(file))
		layer.append(QN_Block_Reader(file))
		mlpstruct.append(layer)
	file.close()
	return mlpstruct

def QN_Block_Writer(file, block):
	#matrix header
	file.write(struct.pack('iiiii', block[0][0], block[0][1], block[0][2], block[0][3], block[0][4]))
	#name sring
	#print sys.argv[1] + ': ' + str(block[1]) + '\t' + str(block[0][1]) + ': ' + str(block[0][2])
	for eachchar in block[1]:
		file.write(struct.pack('c', eachchar))
	#value matrix
	for eachrow in block[2]:
		for eachval in eachrow:
			file.write(struct.pack('f', eachval))

def QN_MLP_Writer(mlppath, mlpstruct):
	file = open(mlppath, 'wb')
	for eachlayer in mlpstruct:
		for eachblock in eachlayer:
			QN_Block_Writer(file, eachblock)
	file.close()


def QN_Block_Writer_ASCII(file, block):
	#matrix header
	file.write(' <HEADER>' + os.linesep)
	for eachval in block[0]:
		file.write(' ' + str(eachval) + os.linesep)
	#name sring
	file.write(' <BLOCKNAME> ' + block[1] + os.linesep)
	#value matrix
	file.write(' <VALUES>' + os.linesep)
	for eachrow in block[2]:
		for eachval in eachrow:
			file.write(' ' + str(eachval))
		file.write(os.linesep)

def QN_MLP_Writer_ASCII(mlppath, mlpstruct):
	file = open(mlppath, 'w')

	for lidx in range(0, len(mlpstruct)):
		for eachblock in mlpstruct[lidx]:
			file.write(' <LAYER> ' + str(lidx + 1) + os.linesep)
			QN_Block_Writer_ASCII(file, eachblock)
	file.close()

#===========start of the methods of qn-mlf2pfile============
QN_pfile_version0_string = "-pfile_header version 0 size 32768"
QN_pfile_head_size = 32768

def QN_PFile_Reader(pfilepath):
	file = open(pfilepath, 'rb')
	#A: read header
	headstr = ''
	for idx in range(0, QN_pfile_head_size):
		headstr += struct.unpack('c', file.read(1))[0]
	headstr = headstr.split('\0')[0]
	items = headstr.split('\n')
        print headstr	
	print len(items)
	print headstr
	for eachitem in items:
		print eachitem
	#--item1: pfile_version0_string
	items.pop(0)
	#--item2: num_sentences
	mQN_current_sentence = int(items[0].split(' ')[1])
	items.pop(0)
	#--item3: num_frames
	mQN_current_row = int(items[0].split(' ')[1])
	items.pop(0)
	#--item4: first_feature_column
	mQN_first_feature_column = int(items[0].split(' ')[1])
	items.pop(0)
	mQN_num_ftr_cols = int(items[0].split(' ')[1])
	items.pop(0)
	#--item5: first_label_column
	mQN_first_label_column = int(items[0].split(' ')[1])
	items.pop(0)
	mQN_num_lab_cols = int(items[0].split(' ')[1])
	items.pop(0)
	#--item6: feature_format 
	mQN_format_mask = items[0].split(' ')[1]
	items.pop(0)
	#--item7: data_size and data_offset 
	subitems = items[0].split(' ')
	mQN_data_size = int(subitems[2])
	mQN_data_offset = int(subitems[4])
	mQN_cols = mQN_num_ftr_cols + mQN_num_lab_cols + mQN_first_feature_column
	items.pop(0)
	#--item8: if has sen_table_data(option index)
	mQN_has_index = False
	mQN_index_size = 0
	mQN_index_offset = -1
	mQN_index_ndim = 0
	if items[-3].startswith('-sent_table_data'):
		subitems = items[0].split(' ')
		mQN_has_index = True
		mQN_index_size = int(subitems[2])
		mQN_index_offset = int(subitems[4])
		mQN_index_ndim = int(subitems[6])
	#--item9 and more: obmit other options until the end
	items = []
	#B: data section
	#--obmit data offset
	if mQN_data_offset > 0:
		file.read(mQN_data_offset * 4)
	#--read data
	pymask = '>' + mQN_format_mask.replace('d', 'i')
	pysize = 4 * len(mQN_format_mask)
	for frameidx in range(0, mQN_current_row):
		rettuple = struct.unpack(pymask, file.read(pysize))
		sentidx = rettuple[0]
		frameidx = rettuple[1]
		values = list(rettuple[2: ])
		#print "\t" + str(sentidx) + "\t" + str(frameidx) + "\t%e" % values[0] + "\t%e" % values[1] + "\t%e" % values[2] + "\t%e" % values[3]
	#C: (optional) index section
	#--obmit index offset
	mQN_index_offset -= mQN_data_size
	if mQN_index_offset > 0:
		file.read(mQN_index_offset * 4)
	#--read index
	if mQN_has_index:	
		for sentidx in range(0, mQN_current_sentence):
			value = struct.unpack('>i', file.read(4))
			print str(sentidx) + '\t' + str(value)
		value = struct.unpack('>i', file.read(4))
		#print str(value)
	#D: close file
	file.close()

# cw564 - mbt
def QN_Lab_PFile_Writer_WithSpkrInfo(mlfpath, framelen, ctxframenum, pfilepath, seg2spkr_fn, offset = 10000):
	#spkrfile = open(seg2spkr_fn, 'r')
	#seg2spkr = eval(spkrfile.readline())
	#spkrfile.close()
	seg2spkr = mbt.read_segmap(seg2spkr_fn)
	mfile = open(mlfpath, 'r')
	mlines = mfile.readlines()
	pfile = open(pfilepath, 'wb')
	#A: write blank header
	for idx in range(0, QN_pfile_head_size):
		pfile.write(struct.pack('c', '\0'))
	#B: scan the mlf file and generate the data section
	mindex = 0
	sentidx = 0
	sentidxes = []
	#sentframenum = 0
	mQN_current_row = 0	#??
	while mindex < len(mlines):
		if mlines[mindex].startswith('"'):
			mindex += 1
			frameidx = 0
			sentidxes.append(mQN_current_row)
			firstword = True
			#sentidxes.append(mQN_current_row)
			while not mlines[mindex].startswith('.'):
				items = mlines[mindex].split(' ')
				fsf = float(items[0]) / framelen
				fef = float(items[1]) / framelen
				startframe = int(fsf)
				endframe = int(fef)
				if fsf - int(fsf) > 0.5:
					startframe += 1
				if fef - int(fef) > 0.5:
					endframe += 1
                                senoneidx_raw = int(items[2])	#suppose the tied-states have been mapped to id(int) by HLEd
                                # cw564 - mbt
                                senoneidx = senoneidx_raw + offset * sentidx
				if firstword:	#frames for left context
					firstword = False
					for loopidx in range(0, ctxframenum):
						pfile.write(struct.pack('>i', sentidx))
						pfile.write(struct.pack('>i', frameidx))
						pfile.write(struct.pack('>i', senoneidx))
						frameidx += 1
				for loopidx in range(startframe, endframe):
					pfile.write(struct.pack('>i', sentidx))	#first int is for the sentence index
					pfile.write(struct.pack('>i', frameidx))	#second int is for the frame index
					pfile.write(struct.pack('>i', senoneidx))
					#if len(sys.argv) > 6 and senoneidx == silidx:	#cz277 - garbsil
					#	if silcnt % sildist == 0:		#cz277 - garbsil
					#		pfile.write(struct.pack('>i', silidx))	#cz277 - garbsil
					#	else:	#cz277 - garbsil
					#		pfile.write(struct.pack('>i', garbidx))	#cz277 - garbsil
					#		garbcnt += 1
					#	silcnt += 1	#cz277 - garbsil
					#else:	#cz277 - garbsil
					#	pfile.write(struct.pack('>i', senoneidx))	#cz277 - garbsil	#the left ints/floats depend on the type of pfile
					frameidx += 1
					#The following is the data section for current frame
					#pfile(ftrs): int, int, float[1], ..., float[num_ftrs_cols]
					#pfile(labs): int, int, int[1], ..., int[num_labs_cols]
					#pfile(ftrs and labs): int, int, float[1], ..., float[num_ftrs_cols], int[1], ..., int[num_labs_cols]
				if mlines[mindex + 1].startswith('.'):	#frames for right context
					for loopidx in range(0, ctxframenum):
						pfile.write(struct.pack('>i', sentidx))
                                                pfile.write(struct.pack('>i', frameidx))
                                                pfile.write(struct.pack('>i', senoneidx))
						frameidx += 1
					#endframe += ctxframenum
				mindex += 1
				#sentframenum = endframe
			sentidx += 1
			mQN_current_row += frameidx	#sentframenum		#stats: mQN_current_row
		mindex += 1
	mQN_current_sentence = sentidx	#stats: mQN_current_sentence
	mQN_first_feature_column = 2
	mQN_num_ftr_cols = 0
	mQN_first_label_column = mQN_first_feature_column + mQN_num_ftr_cols
	mQN_num_lab_cols = 1
	mQN_format_mask = 'ddd'
	mQN_data_size = mQN_current_row * len(mQN_format_mask)
	mQN_data_offset = 0
	mQN_cols = mQN_first_feature_column + mQN_num_ftr_cols + mQN_num_lab_cols
	mQN_index_size = mQN_current_sentence + 1
	mQN_index_offset = mQN_data_size
	mQN_index_ndim = 1
	mfile.close() 
	#C: index section
	for eachidx in sentidxes:
		pfile.write(struct.pack('>i', eachidx))
	pfile.write(struct.pack('>i', mQN_current_row))
	#D: update header			
	pfile.seek(0)
	taglist = []
	#--item1: pfile_version0_string
	tagstr = '-pfile_header version 0 size ' + str(32768) + '\n'
	taglist.append(tagstr)
	#--item2: num-sentences
	tagstr = '-num_sentences ' + str(mQN_current_sentence) + '\n'
	taglist.append(tagstr)
	#--item3: num-frames
	tagstr = '-num_frames ' + str(mQN_current_row) + '\n'
	taglist.append(tagstr)
	#--item4: first_feature_column
	tagstr = '-first_feature_column ' + str(mQN_first_feature_column) + '\n'
	taglist.append(tagstr)
	tagstr = '-num_features ' + str(mQN_num_ftr_cols) + '\n'
	taglist.append(tagstr)
	#--item5: first_label_column
	tagstr = '-first_label_column ' + str(mQN_first_label_column) + '\n'
        taglist.append(tagstr)
        tagstr = '-num_labels ' + str(mQN_num_lab_cols) + '\n'
        taglist.append(tagstr)
	#--item6: format information
	tagstr = '-format ' + mQN_format_mask + '\n'
        taglist.append(tagstr)
	#--item7: data section
	tagstr = '-data size ' + str(mQN_data_size) + ' offset ' + str(mQN_data_offset) + ' ndim ' + str(mQN_first_feature_column) + ' nrow ' + str(mQN_current_row) + ' ncol ' + str(mQN_cols) + '\n'
	taglist.append(tagstr)	
	#--item8: (optional) indexes
	tagstr = '-sent_table_data size ' + str(mQN_current_sentence + 1) + ' offset ' + str(mQN_data_size) + ' ndim ' + str(1) + '\n'
        taglist.append(tagstr)
	#--item9: end
	tagstr = '-end\n'
	taglist.append(tagstr)
	#--write tag strings
	for curtag in taglist:
		for eachar in curtag:
			pfile.write(struct.pack('>c', eachar))
	pfile.close()

	#print '\tsil == ' + str(silcnt) + '\t' + 'garbsil == ' + str(garbcnt)


def QN_Lab_PFile_Writer(mlfpath, framelen, ctxframenum, pfilepath):
	mfile = open(mlfpath, 'r')
	mlines = mfile.readlines()
	pfile = open(pfilepath, 'wb')
	#A: write blank header
	for idx in range(0, QN_pfile_head_size):
		pfile.write(struct.pack('c', '\0'))
	#B: scan the mlf file and generate the data section
	mindex = 0
	sentidx = 0
	sentidxes = []
	#sentframenum = 0
	mQN_current_row = 0	#??
	while mindex < len(mlines):
		if mlines[mindex].startswith('"'):
			mindex += 1
			frameidx = 0
			sentidxes.append(mQN_current_row)
			firstword = True
			#sentidxes.append(mQN_current_row)
			while not mlines[mindex].startswith('.'):
				items = mlines[mindex].split(' ')
				fsf = float(items[0]) / framelen
				fef = float(items[1]) / framelen
				startframe = int(fsf)
				endframe = int(fef)
				if fsf - int(fsf) > 0.5:
					startframe += 1
				if fef - int(fef) > 0.5:
					endframe += 1
				senoneidx = int(items[2])	#suppose the tied-states have been mapped to id(int) by HLEd
				if firstword:	#frames for left context
					firstword = False
					for loopidx in range(0, ctxframenum):
						pfile.write(struct.pack('>i', sentidx))
						pfile.write(struct.pack('>i', frameidx))
						pfile.write(struct.pack('>i', senoneidx))
						frameidx += 1
				for loopidx in range(startframe, endframe):
					pfile.write(struct.pack('>i', sentidx))	#first int is for the sentence index
					pfile.write(struct.pack('>i', frameidx))	#second int is for the frame index
					pfile.write(struct.pack('>i', senoneidx))
					#if len(sys.argv) > 6 and senoneidx == silidx:	#cz277 - garbsil
					#	if silcnt % sildist == 0:		#cz277 - garbsil
					#		pfile.write(struct.pack('>i', silidx))	#cz277 - garbsil
					#	else:	#cz277 - garbsil
					#		pfile.write(struct.pack('>i', garbidx))	#cz277 - garbsil
					#		garbcnt += 1
					#	silcnt += 1	#cz277 - garbsil
					#else:	#cz277 - garbsil
					#	pfile.write(struct.pack('>i', senoneidx))	#cz277 - garbsil	#the left ints/floats depend on the type of pfile
					frameidx += 1
					#The following is the data section for current frame
					#pfile(ftrs): int, int, float[1], ..., float[num_ftrs_cols]
					#pfile(labs): int, int, int[1], ..., int[num_labs_cols]
					#pfile(ftrs and labs): int, int, float[1], ..., float[num_ftrs_cols], int[1], ..., int[num_labs_cols]
				if mlines[mindex + 1].startswith('.'):	#frames for right context
					for loopidx in range(0, ctxframenum):
						pfile.write(struct.pack('>i', sentidx))
                                                pfile.write(struct.pack('>i', frameidx))
                                                pfile.write(struct.pack('>i', senoneidx))
						frameidx += 1
					#endframe += ctxframenum
				mindex += 1
				#sentframenum = endframe
			sentidx += 1
			mQN_current_row += frameidx	#sentframenum		#stats: mQN_current_row
		mindex += 1
	mQN_current_sentence = sentidx	#stats: mQN_current_sentence
	mQN_first_feature_column = 2
	mQN_num_ftr_cols = 0
	mQN_first_label_column = mQN_first_feature_column + mQN_num_ftr_cols
	mQN_num_lab_cols = 1
	mQN_format_mask = 'ddd'
	mQN_data_size = mQN_current_row * len(mQN_format_mask)
	mQN_data_offset = 0
	mQN_cols = mQN_first_feature_column + mQN_num_ftr_cols + mQN_num_lab_cols
	mQN_index_size = mQN_current_sentence + 1
	mQN_index_offset = mQN_data_size
	mQN_index_ndim = 1
	mfile.close() 
	#C: index section
	for eachidx in sentidxes:
		pfile.write(struct.pack('>i', eachidx))
	pfile.write(struct.pack('>i', mQN_current_row))
	#D: update header			
	pfile.seek(0)
	taglist = []
	#--item1: pfile_version0_string
	tagstr = '-pfile_header version 0 size ' + str(32768) + '\n'
	taglist.append(tagstr)
	#--item2: num-sentences
	tagstr = '-num_sentences ' + str(mQN_current_sentence) + '\n'
	taglist.append(tagstr)
	#--item3: num-frames
	tagstr = '-num_frames ' + str(mQN_current_row) + '\n'
	taglist.append(tagstr)
	#--item4: first_feature_column
	tagstr = '-first_feature_column ' + str(mQN_first_feature_column) + '\n'
	taglist.append(tagstr)
	tagstr = '-num_features ' + str(mQN_num_ftr_cols) + '\n'
	taglist.append(tagstr)
	#--item5: first_label_column
	tagstr = '-first_label_column ' + str(mQN_first_label_column) + '\n'
        taglist.append(tagstr)
        tagstr = '-num_labels ' + str(mQN_num_lab_cols) + '\n'
        taglist.append(tagstr)
	#--item6: format information
	tagstr = '-format ' + mQN_format_mask + '\n'
        taglist.append(tagstr)
	#--item7: data section
	tagstr = '-data size ' + str(mQN_data_size) + ' offset ' + str(mQN_data_offset) + ' ndim ' + str(mQN_first_feature_column) + ' nrow ' + str(mQN_current_row) + ' ncol ' + str(mQN_cols) + '\n'
	taglist.append(tagstr)	
	#--item8: (optional) indexes
	tagstr = '-sent_table_data size ' + str(mQN_current_sentence + 1) + ' offset ' + str(mQN_data_size) + ' ndim ' + str(1) + '\n'
        taglist.append(tagstr)
	#--item9: end
	tagstr = '-end\n'
	taglist.append(tagstr)
	#--write tag strings
	for curtag in taglist:
		for eachar in curtag:
			pfile.write(struct.pack('>c', eachar))
	pfile.close()

	#print '\tsil == ' + str(silcnt) + '\t' + 'garbsil == ' + str(garbcnt)

def HTK_Parse_EXTSCP_Line(curline):
	if curline.count('=') or curline.count('['):
		items = curline.split('=')
		items = items[-1].split(']')[0].split('[')
		blockpath = items[0]
		items = items[1].split(',')
		return [blockpath, int(items[0]), int(items[1])]
	else:
		return [curline.replace(os.linesep, ''), 0, -1]

def Init_Mask_Str(count, element):
	retstr = ''
	index = 0
	while len(retstr) < count:
		retstr += element
	return retstr

def Write_Frames_2_Pfile(pfile, sentidx, frameidx, framemask, frames):
	pfile.write(struct.pack('>i', sentidx))
        pfile.write(struct.pack('>i', frameidx))
        #print frames
	for eachval in frames:
		pfile.write(struct.pack('>f', eachval))
	#pfile.write(struct.pack(framemask, frames))
        return frameidx + 1

def QN_Fea_PFile_Writer(scppath, ctxframenum, pfilepath):

	sfile = open(scppath, 'r')
	slines = sfile.readlines()
	sfile.close()

	pfile = open(pfilepath, 'wb')
	#A: write blank header
	for idx in range(0, QN_pfile_head_size):
		pfile.write(struct.pack('c', '\0'))
	#B: scan the scp file and generate the data section for htk features
	sentidx = 0
	sentidxes = []
	#sentframenum = 0
	lastHTKpath = ''
	#htk feature info
	HTKsampnum = 0
	HTKsampdim = 0
	framemask = ''
	FrameCache = []
	mQN_current_row = 0	#??
	while sentidx < len(slines):
		[htkpath, startfn, endfn] = HTK_Parse_EXTSCP_Line(slines[sentidx]) 
		sentidxes.append(mQN_current_row)
		if htkpath != lastHTKpath:
			hfile = open(htkpath, 'rb')
			HTKsampnum = struct.unpack('>i', hfile.read(4))[0]
			struct.unpack('>i', hfile.read(4))
			HTKsampdim = struct.unpack('>h', hfile.read(2))[0] / 4
			framemask = '>' + Init_Mask_Str(HTKsampdim, 'f')
			struct.unpack('>h', hfile.read(2))
			##print htkpath + ' ' + str(HTKsampnum) + ' ' + str(HTKsampdim)
			FrameCache = []
			while len(FrameCache) < HTKsampnum:
				FrameCache.append(list(struct.unpack(framemask, hfile.read(HTKsampdim * 4))))
			hfile.close()	
			lastHTKpath = htkpath
			if endfn < 0:
				endfn = HTKsampnum - 1
		#reset frame index
		frameidx = 0
		#write left context
		fidx = startfn - ctxframenum
		lCTXfn = 0
		while lCTXfn < ctxframenum:
			if sys.argv[5] == 'natural':
				if fidx < 0:
					frameidx = Write_Frames_2_Pfile(pfile, sentidx, frameidx, framemask, FrameCache[0])
				else:
					frameidx = Write_Frames_2_Pfile(pfile, sentidx, frameidx, framemask, FrameCache[fidx])
			elif sys.argv[5] == 'copy':
				frameidx = Write_Frames_2_Pfile(pfile, sentidx, frameidx, framemask, FrameCache[startfn])
			fidx += 1
			lCTXfn += 1
		#write the body
		##fidx = startfn
		while fidx <= endfn:
			frameidx = Write_Frames_2_Pfile(pfile, sentidx, frameidx, framemask, FrameCache[fidx])
			fidx += 1
		#write the right context
		rCTXfn = 0
		while rCTXfn < ctxframenum:
			if sys.argv[5] == 'natural':
				if fidx < HTKsampnum:
					frameidx = Write_Frames_2_Pfile(pfile, sentidx, frameidx, framemask, FrameCache[fidx])
				else:
					frameidx = Write_Frames_2_Pfile(pfile, sentidx, frameidx, framemask, FrameCache[-1])
			elif sys.argv[5] == 'copy':
				frameidx = Write_Frames_2_Pfile(pfile, sentidx, frameidx, framemask, FrameCache[endfn])
			rCTXfn += 1
			fidx += 1
		sentidx += 1
		#The following is the data section for current frame
		#pfile(ftrs): int, int, float[1], ..., float[num_ftrs_cols]
		#pfile(labs): int, int, int[1], ..., int[num_labs_cols]
		#pfile(ftrs and labs): int, int, float[1], ..., float[num_ftrs_cols], int[1], ..., int[num_labs_cols]
		mQN_current_row += frameidx	#sentframenum		#stats: mQN_current_row
	mQN_current_sentence = sentidx	#stats: mQN_current_sentence
	mQN_first_feature_column = 2
	mQN_num_ftr_cols = HTKsampdim
	mQN_first_label_column = mQN_first_feature_column + mQN_num_ftr_cols
	mQN_num_lab_cols = 0
	mQN_format_mask = 'dd' + framemask[1: ]
	mQN_data_size = mQN_current_row * len(mQN_format_mask)
	mQN_data_offset = 0
	mQN_cols = mQN_first_feature_column + mQN_num_ftr_cols + mQN_num_lab_cols
	mQN_index_size = mQN_current_sentence + 1
	mQN_index_offset = mQN_data_size
	mQN_index_ndim = 1
	for eachidx in sentidxes:
		print str(eachidx)
		pfile.write(struct.pack('>i', eachidx))
	pfile.write(struct.pack('>i', mQN_current_row))
	#D: update header			
	pfile.seek(0)
	taglist = []
	#--item1: pfile_version0_string
	tagstr = '-pfile_header version 0 size ' + str(32768) + '\n'
	taglist.append(tagstr)
	#--item2: num-sentences
	tagstr = '-num_sentences ' + str(mQN_current_sentence) + '\n'
	taglist.append(tagstr)
	#--item3: num-frames
	tagstr = '-num_frames ' + str(mQN_current_row) + '\n'
	taglist.append(tagstr)
	#--item4: first_feature_column
	tagstr = '-first_feature_column ' + str(mQN_first_feature_column) + '\n'
	taglist.append(tagstr)
	tagstr = '-num_features ' + str(mQN_num_ftr_cols) + '\n'
	taglist.append(tagstr)
	#--item5: first_label_column
	tagstr = '-first_label_column ' + str(mQN_first_label_column) + '\n'
        taglist.append(tagstr)
        tagstr = '-num_labels ' + str(mQN_num_lab_cols) + '\n'
        taglist.append(tagstr)
	#--item6: format information
	tagstr = '-format ' + mQN_format_mask + '\n'
        taglist.append(tagstr)
	#--item7: data section
	tagstr = '-data size ' + str(mQN_data_size) + ' offset ' + str(mQN_data_offset) + ' ndim ' + str(mQN_first_feature_column) + ' nrow ' + str(mQN_current_row) + ' ncol ' + str(mQN_cols) + '\n'
	taglist.append(tagstr)	
	#--item8: (optional) indexes
	tagstr = '-sent_table_data size ' + str(mQN_current_sentence + 1) + ' offset ' + str(mQN_data_size) + ' ndim ' + str(1) + '\n'
        taglist.append(tagstr)
	#--item9: end
	tagstr = '-end\n'
	taglist.append(tagstr)
	#--write tag strings
	for curtag in taglist:
		for eachar in curtag:
			pfile.write(struct.pack('>c', eachar))
	pfile.close()

#=================-qn-statsmodel=================

def Gen_Matrix_Stats(matrix):
	min = 65535
	max = -65535
	mean = 0.0
	var = 0.0
	Nsamp = 0
	sdev = 0.0
	for ridx in range(0, len(matrix)):
		for cidx in range(0, len(matrix[ridx])):
			if matrix[ridx][cidx] > max:
				max = matrix[ridx][cidx]
			if matrix[ridx][cidx] < min:
				min = matrix[ridx][cidx]
			mean += matrix[ridx][cidx]
		Nsamp += len(matrix[ridx])
	mean /= Nsamp
	for ridx in range(0, len(matrix)):
                for cidx in range(0, len(matrix[ridx])):
                        var += math.pow(mean - matrix[ridx][cidx], 2)
	var /= Nsamp
	sdev = math.sqrt(var)
	return [Nsamp, min, max, mean, var, sdev]

def Output_Params_by_Layer(params):
	paramline = ''
	for curlayer in params:
		for blockidx in range(0, len(curlayer)):
			for paramidx in range(0, len(curlayer[blockidx])):
				if paramidx == 0 and blockidx == 0:
					paramline += ' '
				else:
					paramline += ','
				
				strval = '%f' %curlayer[blockidx][paramidx]
				paramline += strval
	return paramline

def QN_Show_MLP_Stats(mlpstruct):
	tnparam = 0
	layeridx = 0
	uvars = []
	gvars = []
	while layeridx < len(mlpstruct):
		print 'Layer ' + str(layeridx)
		blockidx = 0
		ulvars = []
		glvars = []
		while blockidx < len(mlpstruct[layeridx]):
			print '\tBlock ' + mlpstruct[layeridx][blockidx][1]
			print '\t\tRowNum ' + str(mlpstruct[layeridx][blockidx][0][1]) + '\tColNum ' + str(mlpstruct[layeridx][blockidx][0][2]) 
			retstats = Gen_Matrix_Stats(mlpstruct[layeridx][blockidx][2])
			tnparam += retstats[0]
			print '\t\tNSample = %d\tMinVal = %f\tMaxVal = %f' %(retstats[0], retstats[1], retstats[2])
			print '\t\tMeanVal = %f\tVarVal = %f\tSqrt(VarVal) = %f' %(retstats[3], retstats[4], retstats[5])
			blockidx += 1
			ulvars.append([retstats[1], retstats[2]])
			glvars.append([retstats[3], retstats[5]])
		layeridx += 1
		uvars.append(ulvars)
		gvars.append(glvars)
	print 'TotalParamNum ' + str(tnparam)
	print 'Uniform Params ' + Output_Params_by_Layer(uvars)
	print 'Gauss Params ' + Output_Params_by_Layer(gvars)
	
def QN_Compare_MLPs(lhstruct, rhstruct):
	layeridx = 0
	while layeridx < len(lhstruct):
		print 'Layer ' + str(layeridx)
		blockidx = 0
		while blockidx < len(lhstruct[layeridx]):
			rownum = lhstruct[layeridx][blockidx][0][1]
			colnum = lhstruct[layeridx][blockidx][0][2]
			print '\tBlock ' + lhstruct[layeridx][blockidx][1]
			print '\t\tRow ' + str(rownum) + '\tCol ' + str(colnum) 
			rowmean = 0.0
			rowsd = 0.0
			changecnt = 0
			ridx = 0
			while ridx < rownum:
				currow = []
				mean = 0.0
				var = 0.0
				cidx = 0
				while cidx < colnum:
					crate = abs(lhstruct[layeridx][blockidx][2][ridx][cidx] - rhstruct[layeridx][blockidx][2][ridx][cidx]) / abs(lhstruct[layeridx][blockidx][2][ridx][cidx])
					if crate != 0:
						changecnt += 1
					currow.append(crate)
					mean += crate
					cidx += 1
				rowmean += mean
				mean /= colnum
				while cidx < colnum:
					var += math.pow((currow[cidx] - mean), 2)
					cidx += 1
                                rowsd += var 
				var /= colnum
				sd = math.sqrt(var)
				ridx += 1
			rowmean /= (rownum * colnum) 
			rowsd /= (rownum * colnum)
			rowsd = math.sqrt(rowsd)
			print '\t\tNum of Different Parameter ' + str(changecnt)
			print '\t\tMean of the Changed Rates %f' % rowmean
			print '\t\tStandard Deviation of the Changed Rates %f' % rowsd
			blockidx += 1		
		layeridx += 1

#================-qn-randinit===============

def GenRandVals(randtype, nrow, ncol, param1, param2):
	randmat = []
	for ridx in range(0, nrow):
		currow = []
		for cidx in range(0, ncol):
			randval = 0.0
			if randtype == 'uniform':
				randval = random.uniform(param1, param2)
			elif randtype == 'gauss':
				randval = random.gauss(param1, math.pow(param2, 2))
			currow.append(randval)
		randmat.append(currow)
	return randmat

def QN_Gen_Rand_Inits(randtype, topology):
	items = topology.split(',')
	nlayer = len(items)
	mlpstruct = []
	for layeridx in range(0, nlayer - 1):
		nrow = int(items[layeridx + 1])
		ncol = int(items[layeridx])
		wname = 'weights' + str(layeridx + 1) + str(layeridx + 2) + '\0'
		wheader = [10, nrow, ncol, 0, len(wname)]
		if randtype == 'uniform' or randtype == 'gauss':
			params = sys.argv[5 + layeridx].split(',')
			wvalues = GenRandVals(randtype, nrow, ncol, float(params[0]), float(params[1]))
			wblock = [wheader, wname, wvalues]
			bname = 'bias' + str(layeridx + 2) + '\0'
			bheader = [10, 1, nrow, 0, len(bname)]
			bvalues = GenRandVals(randtype, 1, nrow, float(params[2]), float(params[3]))
			bblock = [bheader, bname, bvalues]
			mlpstruct.append([wblock, bblock])
		elif randtype == 'normuni':	#normalized uniform random initialisation
			normbound = math.sqrt(6) / math.sqrt(ncol + nrow)	
			#print str(normbound) + '\t' + str(ncol) + '\t' + str(nrow)
			wvalues = GenRandVals('uniform', nrow, ncol, normbound, (-1) * normbound)
                        wblock = [wheader, wname, wvalues]
                        bname = 'bias' + str(layeridx + 2) + '\0'
                        bheader = [10, 1, nrow, 0, len(bname)]
                        bvalues = GenRandVals(randtype, 1, nrow, -3.9, -4.1)
                        bblock = [bheader, bname, bvalues]
                        mlpstruct.append([wblock, bblock])
		else:
			print 'warning: none support random initialisation method'
	return mlpstruct

#===========-qn-state2phone=====================

def LoadShMappingFile(shpath):
	#setup hash table for tied-states
 	senonedct = {}
 	senonelst = []
 	log2phyid = {}
 	file = open(shpath)
 	lines = file.readlines()
 	file.close()
 	hmmlabel = ''
 	phyidx = 1
 	shlen = len(lines) - 1
 	for idx in range(2, shlen):
        	if lines[idx].count('.Name:'):
                	hmmlabel = lines[idx][0: -1].split(' ')[-1]
        	elif lines[idx].count('State '):
                	items = lines[idx][0: -1].split(':')
                	phyname = items[-1]
                 	parts = items[0].split(' ')
                 	logname = hmmlabel + '[' + parts[-1] + ']'
                 	phyidx = -1
                	if (phyname in senonedct):      #senoneset):    #physical
                        	phyidx = senonedct[phyname]
                 	else:
                         	phyidx = len(senonelst)
                         	senonedct[phyname] = phyidx
                         	#senoneset.add(phyname)
                         	senonelst.append(phyname)
                 	log2phyid[logname] = phyidx
	return senonelst

def LoadItem2IndexList(idxlstpath):
	itemidxes = []
	itemdict = {}
	file = open(idxlstpath)
	lines = file.readlines()
	file.close()
	for eachline in lines:
		items = eachline.replace(os.linesep, '').split(' ')
		itemidxes.append(items[0])
		itemdict[items[0]] = int(items[1])
	retstruct = [itemidxes, itemdict]
	return retstruct

#def QN_FrameConv
def QN_PfileEvaluateion(pfilepath, mlfpath, framedur, statelist, phonelist, phonedict, evaltype, silopt, omitrange):
        file = open(pfilepath, 'rb')
        #A: read header
        headstr = ''
        for idx in range(0, QN_pfile_head_size):
                headstr += struct.unpack('c', file.read(1))[0]
        headstr = headstr.split('\0')[0]
        items = headstr.split('\n')
        print len(items)
        print headstr
        for eachitem in items:
                print eachitem
        #--item1: pfile_version0_string
        items.pop(0)
        #--item2: num_sentences
        mQN_current_sentence = int(items[0].split(' ')[1])
        items.pop(0)
        #--item3: num_frames
        mQN_current_row = int(items[0].split(' ')[1])
        items.pop(0)
        #--item4: first_feature_column
        mQN_first_feature_column = int(items[0].split(' ')[1])
        items.pop(0)
        mQN_num_ftr_cols = int(items[0].split(' ')[1])
        items.pop(0)
        #--item5: first_label_column
        mQN_first_label_column = int(items[0].split(' ')[1])
        items.pop(0)
        mQN_num_lab_cols = int(items[0].split(' ')[1])
        items.pop(0)
        #--item6: feature_format 
        mQN_format_mask = items[0].split(' ')[1]
        items.pop(0)
        #--item7: data_size and data_offset 
        subitems = items[0].split(' ')
        mQN_data_size = int(subitems[2])
        mQN_data_offset = int(subitems[4])
        mQN_cols = mQN_num_ftr_cols + mQN_num_lab_cols + mQN_first_feature_column
        items.pop(0)
        #--item8: if has sen_table_data(option index)
        mQN_has_index = False
        mQN_index_size = 0
        mQN_index_offset = -1
        mQN_index_ndim = 0
        if items[-3].startswith('-sent_table_data'):
                subitems = items[0].split(' ')
                mQN_has_index = True
                mQN_index_size = int(subitems[2])
                mQN_index_offset = int(subitems[4])
                mQN_index_ndim = int(subitems[6])
        #--item9 and more: obmit other options until the end
        items = []
        #B: data section
        #--obmit data offset
        if mQN_data_offset > 0:
                file.read(mQN_data_offset * 4)
        #--read data
        pymask = '>' + mQN_format_mask.replace('d', 'i')
        pysize = 4 * len(mQN_format_mask)

	# load MLF file, assume they are of the same order -- aligned monophone label
	reffile = open(mlfpath)
	lines = reffile.readlines()
	reffile.close()
	#set pfile cd state list
	cds2phone = []
	for sidx in range(2, len(pymask)):
		#print str(sidx - 2) + '\t' + str(len(pymask)) + '\t' + str(len(statelist)) + '\t' + statelist[0]
		cdstate = statelist[sidx - 2]
                ciphone = ''
                if cdstate.endswith(']'):       #untied-state
			ciphone = cdstate.split('[')[0]
                        if ciphone.count('+'):
 	                       ciphone = ciphone.split('+')[1]
                        if ciphone.count('-'):
                               ciphone = ciphone.split('-')[0]
                else: 	#tied-state
                        ciphone = cdstate.split('_')[0]
		cds2phone.append(ciphone)

	tframecorr = 0.0
	tframenum = 0.0
	sentidx = 0
	refidx = 0
	while refidx < len(lines):
		if lines[refidx].startswith('"'):
			refidx += 1
			prevref = ''
			while not lines[refidx].startswith('.'):
				items = lines[refidx].split(' ')
				nxtref = ''
				if not lines[refidx + 1].startswith('.'):
					nxtref = lines[refidx + 1].split(' ')[2]
				istart = int(items[0]) / framedur
				fleft = float(items[0]) / framedur - istart
				if fleft > 0.5:
					istart += 1
				iend = int(items[1]) / framedur
				fleft = float(items[1]) / framedur - iend
				if fleft > 0.5:
					iend += 1
				frameidx = istart
				while frameidx < iend:
					# load a frame list from the pfile
					mtriple = struct.unpack(pymask, file.read(pysize))
					msentidx = mtriple[0]
					mframeidx = mtriple[1]
					postprobs = []
					for mcuridx in range(2, len(mtriple)):
						postprobs.append(mtriple[mcuridx])
					if msentidx != sentidx:
						print 'Error: Sent. No. ' + str(sentidx) + '(MLF) and Sent. No. ' + str(msentidx) + ' Unmatched!'
						return
					print 'sent: ' + str(msentidx) + '\t' + str(sentidx) + '\t' + 'frame: ' + str(mframeidx) + '\t' + str(frameidx)
					if mframeidx != frameidx:
						print 'Error: Sent. No. ' + str(sentidx) + ', Frame No. ' + str(frameidx) + ' (MLF) and Frame No. ' + str(mframeidx) + ' Unmatched!'
						return
					resphone = ''
					if evaltype == 'best':
						bestidx = 0
						for cdstateidx in range(1, len(postprobs)):
							if postprobs[cdstateidx] > postprobs[bestidx]:
								bestidx = cdstateidx
						resphone = cds2phone[bestidx]
					else:	#sum
						ciphonelist = []
						for curciphone in phonelist:
							ciphonelist.append(0.0)
						for cdstateidx in range(0, len(postprobs)):
							ciphonelist[phonedict[cds2phone[cdstateidx]]] += postprobs[cdstateidx]
						bestidx = 0
						for ciphoneidx in range(1, len(ciphonelist)):
							if ciphonelist[ciphoneidx] > ciphonelist[bestidx]: 
								bestidx = ciphoneidx
						resphone = phonelist[bestidx]
					refciphone = items[2]
					#if refciphone.count('-'):
					#	refciphone = refciphone.split('-')[1]
					#if refciphone.count('+'):
					#	refciphone = refciphone.split('+')[0]
					#if refciphone.count('^'):	#used for babel phone name
					#	refciphone = refciphone.split('^')[0]
					#print resphone + '\t' + refciphone + '\t' + items[2]
					
					if silopt != 'no-sil' or refciphone != 'sil':
						if resphone == refciphone:	#if equals
							tframecorr += 1
						elif frameidx - istart < omitrange:
							if resphone == prevref:
								tframecorr += 1
						elif iend - frameidx < omitrange:
							if resphone == nxtref:
								tframecorr += 1
						tframenum += 1
							
					frameidx += 1
				prevref = refciphone
				refidx += 1
			sentidx += 1
			print 'sent == ' + str(sentidx) + '\tcorr %f ' % float(tframecorr / tframenum)
		refidx += 1
	
	file.close()
	correctness = tframecorr / tframenum
	print 'Phone Correctness evaluated by ' + evaltype + ' == %f ' %correctness 

#===========start of the main method=============
if sys.argv[1] == '-qn-showtop':
	mlpstruct = QN_MLP_Reader(sys.argv[2])
        #get topology info
        layerinfo = []
        for lidx in range(0, len(mlpstruct)):
                layerinfo.append(mlpstruct[lidx][0][0][2])
        layerinfo.append(mlpstruct[-1][0][0][1])
        topstr = str(layerinfo[0])
        for lidx in range(1, len(layerinfo)):
                topstr += ',' + str(layerinfo[lidx])
	print topstr

if sys.argv[1] == '-qn-dptN':
	mlpstruct = QN_MLP_Reader(sys.argv[4])
	#get topology info
	layerinfo = []
	for lidx in range(0, len(mlpstruct)):
		layerinfo.append(mlpstruct[lidx][0][0][2])
	layerinfo.append(mlpstruct[-1][0][0][1])
	#remove the specified number of top layers
	pos = int(sys.argv[2])
	popnum = (-1) * pos
	for popidx in range(0, popnum):
		mlpstruct.pop()
	#generate the new rand layer if it does not exist
        
	layerinfo.insert(pos, int(sys.argv[3]))
	topstr = str(layerinfo[0])
	for lidx in range(1, len(layerinfo)):
		topstr += ',' + str(layerinfo[lidx])
	if not os.path.exists(sys.argv[5]):	#cz277
		mlprand = QN_Gen_Rand_Inits('normuni', topstr)	
	else:
		mlprand = QN_MLP_Reader(sys.argv[5])	#cz277
	#merge the network
	leftdepth = len(mlpstruct)
	for lidx in range(leftdepth, len(mlprand)):
		mlpstruct.append(mlprand[lidx])
		#update the block names
		for bidx in range(0, len(mlpstruct[lidx])):
                	mlpstruct[lidx][bidx][1] = QN_GetBlockName(mlpstruct[lidx][bidx][1], lidx + 1)
                	mlpstruct[lidx][bidx][0][4] = len(mlpstruct[lidx][bidx][1])
        #output the integrated model
        if not os.path.exists(sys.argv[5]):     #cz277
		QN_MLP_Writer(sys.argv[5], mlprand)	#cz277
	QN_MLP_Writer(sys.argv[6], mlpstruct)
	print topstr
if sys.argv[1] == '-qn-dpt':
	#load mlp models
	mlptrain = QN_MLP_Reader(sys.argv[2])
	mlprand = QN_MLP_Reader(sys.argv[3])
	#taper off the output layer
	mlptrain.pop()
	#add a new hidden layer
	midx = len(mlptrain)
	mlptrain.append(mlprand[midx])
	#add the rand output layer
	mlptrain.append(mlprand[-1])
	#update block names
	for bidx in range(0, len(mlptrain[-1])):
		mlptrain[-1][bidx][1] = QN_GetBlockName(mlptrain[-1][bidx][1], len(mlptrain))
		mlptrain[-1][bidx][0][4] = len(mlptrain[-1][bidx][1])
	#output the integrated model
	QN_MLP_Writer(sys.argv[4], mlptrain)

if sys.argv[1] == '-qn-newout':
	#load mlp models
        mlptrain = QN_MLP_Reader(sys.argv[2])
        mlprand = QN_MLP_Reader(sys.argv[3])
        #taper off the output layer
        mlptrain.pop()
        #add the rand output layer
        mlptrain.append(mlprand[-1])
        #output the integrated model
        QN_MLP_Writer(sys.argv[4], mlptrain)

if sys.argv[1] == '-qn-showmodel':
	mlptrain = QN_MLP_Reader(sys.argv[2])
	QN_MLP_Writer_ASCII(sys.argv[3], mlptrain)

if sys.argv[1] == '-qn-toff':
	mlpin = QN_MLP_Reader(sys.argv[2])
	toffnum = len(mlpin) - int(sys.argv[3]) + 1
	for toffidx in range(0, toffnum):
		mlpin.pop()
	QN_MLP_Writer(sys.argv[4], mlpin)

if sys.argv[1] == '-qn-mlf2pfile':
	QN_Lab_PFile_Writer(sys.argv[2], int(sys.argv[3]), int(sys.argv[4]), sys.argv[5])

if sys.argv[1] == '-qn-showpfile':
	QN_PFile_Reader(sys.argv[2])

if sys.argv[1] == '-qn-statsmodel':
	mlpstruct = QN_MLP_Reader(sys.argv[2])
	QN_Show_MLP_Stats(mlpstruct)

if sys.argv[1] == '-qn-randinit':
	mlpstruct = QN_Gen_Rand_Inits(sys.argv[3], sys.argv[4])
	QN_MLP_Writer(sys.argv[2], mlpstruct)

if sys.argv[1] == '-qn-eval':
	[statelist, statedict] = LoadItem2IndexList(sys.argv[5])
	[phonelist, phonedict] = LoadItem2IndexList(sys.argv[6])
	QN_PfileEvaluateion(sys.argv[2], sys.argv[3], int(sys.argv[4]), statelist, phonelist, phonedict, sys.argv[7], sys.argv[8], int(sys.argv[9]))

if sys.argv[1] == '-qn-htk2pfile':
	QN_Fea_PFile_Writer(sys.argv[2], int(sys.argv[3]), sys.argv[4])

if sys.argv[1] == '-qn-cmpmodels':
	lhmodel = QN_MLP_Reader(sys.argv[2])
	rhmodel = QN_MLP_Reader(sys.argv[3])
	QN_Compare_MLPs(lhmodel, rhmodel)

# cw564 -mbt
if sys.argv[1] == '-qn-mlf2pfile-withspkr':
    QN_Lab_PFile_Writer_WithSpkrInfo(sys.argv[2], int(sys.argv[3]), int(sys.argv[4]), sys.argv[5], sys.argv[6])



#! /usr/bin/python
import sys
import numpy as np
import xgboost as xgb

# label need to be 0 to num_class -1
#data = np.loadtxt('./data/raw/train.fealab.10k', delimiter=' ')
#np.save('./data/raw/train.fealab', data)
#exit()





xg_train = xgb.DMatrix('./data.fs/xgb/train.xgb.c0.mono')
xg_cv = xgb.DMatrix('./data.fs/xgb/cv.xgb.c0.mono')
# setup parameters for xgboost
param = {}
# use softmax multi-class classification
param['objective'] = 'multi:softmax'
# scale weight of positive examples
param['eta'] = 0.01
param['max_depth'] = 30
param['silent'] = 1
param['nthread'] = 22
param['num_class'] = 138


watchlist = [(xg_train,'train'), (xg_cv, 'cv')]
num_round = 200
bst = xgb.train(param, xg_train, num_round, watchlist );
# get prediction
#pred = bst.predict( xg_test );

#print ('predicting, classification error=%f' % (sum( int(pred[i]) != test_Y[i] for i in range(len(test_Y))) / float(len(test_Y)) ))

bst.save_model('xgb.model.depth_30')


# do the same thing again, but output probabilities
#param['objective'] = 'multi:softprob'
#bst = xgb.train(param, xg_train, num_round, watchlist );
# Note: this convention has been changed since xgboost-unity
# get prediction, this is in 1D array, need reshape to (ndata, nclass)
#yprob = bst.predict( xg_test ).reshape( test_Y.shape[0], 6 )
#ylabel = np.argmax(yprob, axis=1)

#print ('predicting, classification error=%f' % (sum( int(ylabel[i]) != test_Y[i] for i in range(len(test_Y))) / float(len(test_Y)) ))

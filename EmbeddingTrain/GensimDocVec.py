'''
Created on Apr 6, 2015 9:35:48 PM
@author: cx

what I do:
I read conf and then train gensim doc vec
what's my input:
conf:
what's my output:
doc2vec

'''
'''

dm defines the training algorithm. By default (dm=1), distributed memory is used. Otherwise, dbow is employed.

size is the dimensionality of the feature vectors.

window is the maximum distance between the current and predicted word within a sentence.

alpha is the initial learning rate (will linearly drop to zero as training progresses).

seed = for the random number generator.

min_count = ignore all words with total frequency lower than this.

sample = threshold for configuring which higher-frequency words are randomly downsampled;
default is 0 (off), useful value is 1e-5.
workers = use this many worker threads to train the model (=faster training with multicore machines).

hs = if 1 (default), hierarchical sampling will be used for model training (else set to 0).


dm_mean = if 0 (default), use the sum of the context word vectors. If 1, use the mean. Only applies when dm is used.

'''

'''
very import
implement it!
'''

import site
site.addsitedir('/bos/usr0/cx/PyCode/cxPyLib')
site.addsitedir('/bos/usr0/cx/PyCode/EmbeddingForIR')
from cxBase.Conf import cxConfC
from cxBase.base import cxBaseC

from gensim.models.doc2vec  import *

import logging

class GensimDocVecC(cxBaseC):
    
    def Init(self):
        cxBaseC.Init(self)
        self.size = 300
        self.min_count = 5
        self.sample = 0
        self.workers = 8
        self.hs = 0
        self.negative = 5
        self.dm = 0 #skipgram
        self.InName = ""
        self.OutName = ""
        
        
        
    def SetConf(self, ConfIn):
        cxBaseC.SetConf(self, ConfIn)
        self.size = int(self.conf.GetConf('size', self.size))
        self.min_count = int(self.conf.GetConf('min_count', self.min_count))
        self.sample = int(self.conf.GetConf('sample', self.sample))
        self.workers = int(self.conf.GetConf('workers', self.workers))
        self.hs = int(self.conf.GetConf('hs', self.hs))
        self.negative = int(self.conf.GetConf('negative', self.negative))
        self.dm = int(self.conf.GetConf('dm', self.dm))
        self.InName = self.conf.GetConf('in')
        self.OutName = self.conf.GetConf('out')
    
    
    @staticmethod
    def ShowConf():
        cxBaseC.ShowConf()    
        print "dm defines the training algorithm. By default (dm=1), distributed memory is used. Otherwise, dbow is employed."
        print "size is the dimensionality of the feature vectors."
        print "window is the maximum distance between the current and predicted word within a sentence."
        print "alpha is the initial learning rate (will linearly drop to zero as training progresses)."
        print "seed = for the random number generator."
        print "min_count = ignore all words with total frequency lower than this."
        print "sample = threshold for configuring which higher-frequency words are randomly downsampled;"
        print "default is 0 (off), useful value is 1e-5."
        print "workers = use this many worker threads to train the model (=faster training with multicore machines)."
        print "hs = if 1 (default), hierarchical sampling will be used for model training (else set to 0)."
        print "negative = if > 0, negative sampling will be used, the int for negative specifies."
        print "dm_mean = if 0 (default), use the sum of the context word vectors. If 1, use the mean. Only applies when dm is used."
        print "in\nout"
    
    def Train(self):
        sentence = LabeledLineSentence(self.InName)
        logging.info('start training on [%s]',self.InName)
        model = Doc2Vec(sentence,size=self.size,min_count=self.min_count,sample=self.sample,workers=self.workers,dm=self.dm,hs=self.hs,negative=self.negative)
        
        logging.info('training complete')
        model.save(self.OutName)
        logging.info('saved to [%s]',self.OutName)
        return True
    
    
    def Process(self):
        self.Train()
        
        
if __name__=='__main__':
    import sys
    if 2 != len(sys.argv):
        GensimDocVecC.ShowConf()
        sys.exit()
        
    root = logging.getLogger()
    root.setLevel(logging.INFO)
    
    ch = logging.StreamHandler(sys.stdout)
    ch.setLevel(logging.DEBUG)
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    ch.setFormatter(formatter)
    root.addHandler(ch)
    
    
    module = GensimDocVecC(sys.argv[1])
    module.Process()
    
    logging.info('complete')
        
        
        
        
        
    



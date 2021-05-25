import dirtyopts as opts
import biofilm.util.data as datautil
import numpy as np
import structout as so
from hpsklearn import HyperoptEstimator
from hyperopt import tpe
from sklearn.metrics import  f1_score


optidoc='''
--method str any_classifier  svc knn random_forest extra_trees ada_boost gradient_boosting sgd
--out str numpycompressdumpgoeshere_lol
--features str whereIdumpedMyFeatures
'''

from hpsklearn.components import *
#pip install git+https://github.com/hyperopt/hyperopt-sklearn 
def optimize(X,Y,x,y, args):
    estim = HyperoptEstimator(
            classifier=eval(args.method)('myguy'),
            algo=tpe.suggest,
            max_evals = 50,
            #loss_fn = lambda a,b: (1 - f1_score(a,b)),
            preprocessing=[],
            ex_preprocs=[]
            )
    estim.fit(X,Y)
    res = f1_score(y,estim.predict(x) )
    print("TESTSCORE:",res)
    return res
    


if __name__ == "__main__":
    args = opts.parse(optidoc)
    data = datautil.getfolds()
    res = [optimize(X,Y,x,y,args) for X,Y,x,y in data]
    print(np.mean(res))
    np.savez_compressed( args.out,res)





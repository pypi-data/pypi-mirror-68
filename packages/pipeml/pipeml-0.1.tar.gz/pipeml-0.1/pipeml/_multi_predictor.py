# -*- coding: utf-8 -*-
"""
Created on Tue May 12 21:52:28 2020

@author: yoelr
"""
import numpy as np

__all__ = ('MultiPredictor',)

class MultiPredictor:
    __slots__ = ('predictors',)
    
    def __init__(self, predictors):
        self.predictors = predictors
        
    def fit(self, X, y):
        for predictor, yi in zip(self.predictors, y.transpose()): predictor.fit(X, yi)
        
    def predict(self, xs):
        return np.array([i.predict(xs) for i in self.predictors], float).transpose()
    
    @property
    def metrics(self):
        return [i.metric for i in self.predictors]
    
    def __repr__(self):
        names = ', '.join([str(i) for i in self.metrics])
        return f"<{type(self).__name__}: {names}>"
        
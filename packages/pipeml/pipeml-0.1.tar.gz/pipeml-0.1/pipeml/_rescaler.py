# -*- coding: utf-8 -*-
"""
Created on Mon Nov 11 07:38:24 2019

@author: yoelr
"""
__all__ = ('Rescaler',)

class Rescaler:
    __slots__ = ('mean', 'std', 'factor')
    
    @classmethod
    def from_data(cls, X, factor=0.5, axis=None):
        if axis is None:
            axis = list(range(X.ndim))
            axis.remove(axis[-1])
            axis = tuple(axis)
        return cls(X.mean(axis=axis, keepdims=True),
                   X.std(axis=axis, keepdims=True),
                   factor)
    
    @staticmethod
    def rescale(X, factor=0.5, dim=-1):
        axis = list(range(X.ndim))
        axis.remove(axis[dim])
        axis = tuple(axis)
        mean = X.mean(axis=axis, keepdims=True),
        std = X.std(axis=axis, keepdims=True),
        return factor*(X - mean) / std
    
    def __init__(self, mean, std, factor):
        self.mean = mean
        self.std = std
        self.factor = factor
        
    def __call__(self, X, scale=True):
        return self.scale(X) if scale else self.unscale(X)
        
    def scale(self, X):
        return self.factor*(X - self.mean) / self.std
    
    def unscale(self, X):
        return (X * self.std / self.factor) + self.mean
    
    def __repr__(self):
        return f"<{type(self).__name__}(factor={self.factor})>"
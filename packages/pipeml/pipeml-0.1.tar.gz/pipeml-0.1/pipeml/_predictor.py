# -*- coding: utf-8 -*-
"""
Created on Tue May 12 22:20:36 2020

@author: yoelr
"""

__all__ = ('Predictor',)

class Predictor:
    """Abstract Predictor class."""
    
    def __init_subclass__(cls):
        assert hasattr(cls, 'fit'), 'Predictor must implement a `fit` method'
        assert hasattr(cls, 'predict'), 'Predictor must implement a `predict` method'
        assert hasattr(cls, 'get_params'), 'Predictor must implement a `get_params` method'
        
    def __init__(self, metric):
        self.metric = metric
    
    def __repr__(self):
        return f"<{type(self).__metric__}: {self.metric}>"
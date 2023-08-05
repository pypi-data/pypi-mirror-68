#!/usr/bin/env python3
"""Modules"""
from enum import Enum


# WayPoint12
class CachingStrategy(Enum):
    """
    class of enum represents download method, which are fifo and lifo
    """
    FIFO = 1
    LIFO = 2
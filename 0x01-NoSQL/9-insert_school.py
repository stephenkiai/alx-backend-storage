#!/usr/bin/env python3
"""Defines a function `insert_school`"""


def insert_school(mongo_collection, **kwargs):
    """Inserts a new document in a collection based on kwargs"""
    return mongo_collection.insert(kwargs)
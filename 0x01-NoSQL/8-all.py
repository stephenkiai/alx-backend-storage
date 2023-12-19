#!/usr/bin/env python3
"""Defines a function `list_all`"""


def list_all(mongo_collection):
    """lists all documents in a collection"""
    document_list = mongo_collection.find()
    return document_list
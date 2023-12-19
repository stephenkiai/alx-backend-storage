#!/usr/bin/env python3
"""Defines a function `schools_by_topic`"""


def schools_by_topic(mongo_collection, topic):
    """Returning list of school having a specific topic"""
    school_list = mongo_collection.find(
        {"topics": topic}
    )
    return school_list
#!/usr/bin/env python3
"""Change school topics"""
import pymongo


def update_topics(mongo_collection, name, topics):
    """
    function that changes all topics of a school document based on the name
    """
    updated = mongo_collection.update_many({
        "name": name}, {"$set": {"topics": topics}})
    return updated

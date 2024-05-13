#!/usr/bin/env python3
"""Insert a document in Python"""
import pymongo


def insert_school(mongo_collection, **kwargs):
    """nserts a new document in a collection based on kwargs"""
    doc = mongo_collection.insert_one(kwargs)
    return doc.inserted_id

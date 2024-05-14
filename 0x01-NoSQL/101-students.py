#!/usr/bin/env python3
""" Top students """
from pymongo import MongoClient


def top_students(mongo_collection):
    """unction that returns all students sorted by average score"""
    return mongo_collection.aggregate([
        {'$addFields': {'averageScore': {'$avg': "$topics.score"}}},
        {'$sort': {'averageScore': -1}}
    ])

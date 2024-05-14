#!/usr/bin/env python3
""" Log stats """
from pymongo import MongoClient


if __name__ == "__main__":
    client = MongoClient('mongodb://127.0.0.1:27017')
    # localhost on port associated to mongodb
    n_logs = client.logs.nginx
    n_doc = n_logs.count_documents({})
    n_get = n_logs.count_documents({'method': 'GET'})
    n_post = n_logs.count_documents({'method': 'POST'})
    n_put = n_logs.count_documents({'method': 'PUT'})
    n_patch = n_logs.count_documents({'method': 'PATCH'})
    n_delete = n_logs.count_documents({'method': 'DELETE'})
    g_sts = n_logs.count_documents({'method': 'GET', 'path': '/status'})

    print("{} logs\nMethods:".format(n_doc))
    print("\tmethod GET: {}".format(n_get))
    print("\tmethod POST: {}".format(n_post))
    print("\tmethod PUT: {}".format(n_put))
    print("\tmethod PATCH: {}".format(n_patch))
    print("\tmethod DELETE: {}".format(n_delete))
    print("{} status check".format(g_sts))

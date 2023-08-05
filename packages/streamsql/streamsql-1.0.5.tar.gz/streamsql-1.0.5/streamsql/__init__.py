from .execution import Executor
from .client import Ingester, Reader
from .const import DEFAULT_HOST, ResourceTypes, FieldTypes
import requests
import json

class SimpleClient:

    def __init__(self, apikey, host=DEFAULT_HOST):
        self.apikey = apikey
        self.host = host
        self.exc = Executor(apikey, host)
        self.ig = Ingester(apikey, host)
        self.reader = Reader(apikey, host)

    def create_stream(self, name):
        self.exc.register_stream(name).commit()

    def delete_stream(self, name):
        self.exc.deregister_stream(name)

    def create_lookup(self, name):
        self.exc.register_lookup(name).commit()
        return self.exc.register_transformation(name).sink(name, ResourceTypes.Lookup)

    def create_lookup_set(self, name):
        self.exc.create_lookup_set(name)

    def delete_lookup_set(self, name):
        self.exc.delete_lookup_set(name)

    def list_lookup_sets(self):
        self.exc.list_lookup_sets()

    def add_to_lookup(self, table, key, value):
        self.exc.add_to_lookup(table, key, value)

    def delete_from_lookup(self, table, key):
        self.exc.delete_from_lookup(table, key)

    def list_lookup_values(self, table):
        self.exc.list_lookup_sets(table)

    def delete_lookup(self, name):
        self.exc.deregister_lookup(name)
        self.exc.deregister_transformation(name)

    def lookup(self, table, key=None):
        return self.reader.lookup(table, key)

    def list_resources(self):
        return self.exc.get_resources()

    def list_transforms(self):
        return self.exc.get_transformations()

    def get_transform_status(self, name):
        return self.exc.get_transformation_status(name)

    def send(self, stream, data):
        self.ig.put(stream, data)

    def subscribe(self, transform, callback):
        self.reader.subscribe(transform, callback)

    def unsubscribe(self, transform):
        self.reader.unsubscribe(transform)


class Matrix:

    def __init__(self, apikey, host=DEFAULT_HOST):
        self.__apikey = apikey
        self.__host = host

    def list_features(self, name):
        endpoint = "/api/matrix/features"
        params = {
            'matrix': name
        }
        headers = {
            'X-StreamSQL-Admin-Key': self.__apikey
        }
        resp = requests.get(self.__host+endpoint, params=params, headers=headers)
        return json.loads(resp.text)

    def list_entities(self, name):
        endpoint = "/api/matrix/entities"
        params = {
            'matrix': name
        }
        headers = {
            'X-StreamSQL-Admin-Key': self.__apikey
        }
        resp = requests.get(self.__host + endpoint, params=params, headers=headers)
        return json.loads(resp.text)

    def get_nearest_neighbor(self, name, entity, num, vector=False):
        endpoint = "/api/matrix/nn"
        if vector:
            entity = json.dumps(entity)
        params = {
            'matrix': name,
            'entity': entity,
            'num': num,
            'vector': vector
        }
        headers = {
            'X-StreamSQL-Admin-Key': self.__apikey
        }
        resp = requests.get(self.__host + endpoint, params=params, headers=headers)
        return json.loads(resp.text)

    def get_entity_vectors(self, name, entities):
        endpoint = "/api/matrix/entities/vectors"
        params = {
            'matrix': name,
            'entities': ",".join(entities)
        }
        headers = {
            'X-StreamSQL-Admin-Key': self.__apikey
        }
        resp = requests.get(self.__host + endpoint, params=params, headers=headers)
        return json.loads(resp.text)

    def store_tree(self, name):
        endpoint = "/api/matrix/store"
        params = {
            'matrix': name
        }
        headers = {
            'X-StreamSQL-Admin-Key': self.__apikey
        }
        resp = requests.get(self.__host+endpoint, params=params, headers=headers)
        return resp.text

    def store_job(self, name):
        endpoint = "/api/matrix/store"
        params = {
            'matrix': name
        }
        headers = {
            'X-StreamSQL-Admin-Key': self.__apikey
        }
        resp = requests.post(self.__host + endpoint, params=params, headers=headers)
        return resp.text

    def remove_job(self, name):
        endpoint = "/api/matrix/store"
        params = {
            'matrix': name
        }
        headers = {
            'X-StreamSQL-Admin-Key': self.__apikey
        }
        resp = requests.post(self.__host + endpoint, params=params, headers=headers)
        return resp.text


ResourceTypes = ResourceTypes
FieldTypes = FieldTypes

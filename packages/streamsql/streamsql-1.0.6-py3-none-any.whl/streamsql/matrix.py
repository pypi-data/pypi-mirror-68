import json
import re
import requests
from urllib.parse import parse_qs, urlsplit, urlunsplit, urlencode
from annoy import AnnoyIndex

GET_TABLE = '/api/get'


class Matrix:

    def __init__(self, lamda_name, apikey, host='https://streamsql.io'):
        self.__features = []
        self.__entities = []
        self.__matrix = {}
        self.__apikey = apikey
        self.__host = host
        self.__matrix_arr = None
        self.__lamda_name = lamda_name
        self.__create_from_lambda(lamda_name)

    def __create_from_lambda(self, lamda):
        '''
        Loads a lambda lookup into the matrix.
        When creating the lambda, the resulting output needs to be in the form of Key: Map
        e.g. example_id: {"page1": 6} where 'example_id' is the key, and the map is k/v pairs of a page id and a view
        count.

        This can be done with an SQL query in the form:
            "SELECT entity, COLLECT(feature) FROM table GROUP BY entity"

        Example:
            "SELECT user_id, COLLECT(page) FROM pageviews GROUP BY entity"

        Where user_id will become the unique entity (primary key) and where 'page' is the name of the page in each event
        where COLLECT creates a map of the total counts for each page name. Pageviews is the name of the lambda to use
        for the source of the query.

        Ex
        | user_id  |       COLLECT(page)           |
        |----------|-------------------------------|
        | sterling | {/=10, /docs=13, /register=1} |
        | simba    | {/=3, /login=9, /examples=12} |

        self.entities() will return:
        ['sterling', 'simba']

        self.features() will return:
        ['/', '/docs', '/register', '/login', '/examples']

        self.entity('sterling') will return:
        [10, 13, 1, None, None] //(since /login and /examples don't exist for entity sterling)

        self.as_matrix() will return:
        [
        [10, 13, 1, None, None],  // sterling
        [3, None, None, 9, 12 ]   // simba
        ]

        The matrix is stored as a dict for ease of modifications, but can be converted to a 2D array within
        this object by calling self.compile(). The value is stored in self.__matrix_arr

        :param lamda: name of the lambda to convert into a matrix
        '''

        url = "{host}{path}".format(host=self.__host, path=GET_TABLE)
        headers = {'X-StreamSQL-Admin-Key': self.__apikey}

        scheme, netloc, path, query_string, fragment = urlsplit(url)
        query_params = parse_qs(query_string)

        query_params['table'] = [lamda]

        new_query_string = urlencode(query_params, doseq=True)
        url = urlunsplit((scheme, netloc, path, new_query_string, fragment))

        r = requests.get(url=url, headers=headers)
        if r.status_code >= 400:
            raise ValueError(r.text)
        map = self._parse_map(json.loads(r.text))
        for k in map.keys():
            self.set(k, map[k])

    def _parse_map(self, map):
        '''
        Parses the map from the format stored in the lookup to a python dict().
        e.g. { "key": '{feature=value}'} -> { "key": { "feature": value } }
        NOTE: DOES NOT CURRENTLY WORK IF MAP CONTAINS '=' OR ','
        :param map:
        :return:
        '''
        pmap = {}
        for k, v in map.items():
            pmap[k] = {}
            for feature in v.replace("{", "").replace("}", "").replace(" ", "").split(","):
                feat = feature.split("=")
                name = feat[0]
                val = feat[1]
                pmap[k][name] = int(val)
        return pmap

    def set(self, entity, features):
        '''
        Set an entity manually
        :param entity: Name of the entity to modify
        :param features: A dictionary of features to change for entity, unlisted features will stay the same. Features
        can already exist or not
        :return:
        Ex:
        features = {
            '/': 10,
            '/docs': 14
        }

        set('sterling', features)
        '''
        for k, v in features.items():
            self.__set_single(entity, k, v)

    def __set_single(self, entity, feature, value):
        '''
        Sets a value for an entity and value
        :param entity:
        :param feature:
        :param value:
        :return:
        '''
        if self.entity_index(entity) is None:
            self.__entities.append(entity)
            self.__matrix[entity] = {}

        if self.feature_index(feature) is None:
            self.__features.append(feature)

        self.__matrix[entity][feature] = value

    def set_by_index(self, entity, feature, value):
        '''
        Manually set a feature by index
        :param entity: entity index
        :param feature: feature index
        :param value: value to store
        :return:
        '''
        if not self.__matrix_arr:
            raise ValueError("Run Matrix.compile() before trying to set a value")
        self.__matrix_arr[entity][feature] = value

    def entities(self):
        '''
        Returns a list of all entities in order
        :return:
        '''
        return self.__entities

    def features(self):
        '''
        Returns a list of all features in order
        :return:
        '''
        return self.__features

    def entity(self, entity):
        '''
        Returns the matrix row for a single entity
        :param entity:
        :return:
        '''
        if entity not in self.__entities:
            return []
        features = []
        for feature in self.__features:
            if feature not in self.__matrix[entity]:
                features.append(0)
            else:
                features.append(self.__matrix[entity][feature])
        return features

    def feature_index(self, feature):
        '''
        Gets index of stored feature
        :param feature:
        :return:
        '''
        if feature in self.__features:
            return self.__features.index(feature)
        return None

    def entity_index(self, entity):
        '''
        Gets index of stored entity
        :param entity:
        :return:
        '''
        if entity in self.__entities:
            return self.__entities.index(entity)
        return None

    def compile(self):
        '''
        Builds and stores the matrix
        :return:
        '''
        matrix = []
        for entity in self.__entities:
            features = []
            for feature in self.__features:
                if feature not in self.__matrix[entity]:
                    features.append(0)
                else:
                    features.append(self.__matrix[entity][feature])
            matrix.append(features)

        self.__matrix_arr = matrix

    def as_matrix(self):
        '''
        Returns data as matrix
        :return:
        '''
        return self.__matrix_arr

    def as_dict(self):
        '''
        Returns data as key/value pairs
        :return:
        '''
        return self.__matrix

    def build_tree(self):
        self.compile()
        f = len(self.__features)
        t = AnnoyIndex(f, 'angular')
        for i, v in enumerate(self.__matrix_arr):
            print(v)
            t.add_item(i, v)

        t.build(100)

        t.save("{apikey}_{ln}.ann".format(apikey=self.__apikey, ln=self.__lamda_name))

    def nn(self, i, n):
        f = len(self.__features)
        u = AnnoyIndex(f, 'angular')
        u.load("{apikey}_{ln}.ann".format(apikey=self.__apikey, ln=self.__lamda_name))  # super fast, will just mmap the file
        return u.get_nns_by_item(i, n)




m = Matrix("pixelviews", "MTFmMWQ4OWEtNGI0My00NzVjLTk3NzYtZTFjN2JjNWJlY2M3")
m.build_tree()
print(m.nn(m.entity_index('008e460f-7698-46d2-8a2b-531c7423a0b5'), 5))
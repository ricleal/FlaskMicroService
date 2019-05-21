import abc
import os
import json
from pymongo import MongoClient


class BookDAO(object):
    '''
    '''

    __metaclass__ = abc.ABCMeta

    @abc.abstractmethod
    def __init__(self):
        return

    @abc.abstractmethod
    def get(self, id):
        return

    @abc.abstractmethod
    def create(self, data):
        return

    @abc.abstractmethod
    def update(self, id, data):
        return

    @abc.abstractmethod
    def delete(self, id):
        return

    @abc.abstractmethod
    def get_all(self):
        return


class BookDAOMongo(BookDAO):
    '''
    Data Access Object
    Class that manages the books in MongoDB
    We exclude the mongodb '_id' in the return value
    '''

    def __init__(self):
        client = MongoClient()
        db = client.testdb
        self.book_collection = db.books

    def get(self, id):
        book = self.book_collection.find_one({'id': id}, {'_id': False})
        return book

    def create(self, data):
        result = self.book_collection.insert_one(data)
        return str(result.inserted_id)

    def update(self, id, data):
        result = self.book_collection.update_one({'id': id}, {"$set": data})
        return result.matched_count

    def delete(self, id):
        result = self.book_collection.delete_one({'id': id})
        return result.deleted_count

    def get_all(self):
        '''This probably needs to be paginated, TODO!'''
        book_list = list(self.book_collection.find({}, {'_id': False}))
        return book_list


class BookDAODict(BookDAO):
    '''
    DAO with a dictionary
    '''

    def __init__(self):
        # Directory of this file
        dir_path = os.path.dirname(os.path.realpath(__file__))
        with open(os.path.join(dir_path, "..", "db", 'catalog.books.json')) \
                as json_file:
            data = json.load(json_file)
            # add an id to every book
            for index, d in enumerate(data):
                d['id'] = index+1
            self.book_collection = data

    def get(self, id):
        book_list = list(filter(lambda item: item['id'] == id,
                                self.book_collection))
        if book_list:
            return book_list[0]
        else:
            return None

    def create(self, data):
        self.book_collection.append(data)
        return str(data['id'])

    def update(self, id, data):
        # from pprint import pprint
        # pprint(self.book_collection)

        for d in self.book_collection:
            if d['id'] == id:
                d.update(data)

        return 1

    def delete(self, id):
        self.book_collection = [
            item for item in self.book_collection if not item["id"] == id]
        return 1

    def get_all(self):
        '''This probably needs to be paginated, TODO!'''
        book_list = self.book_collection
        return book_list

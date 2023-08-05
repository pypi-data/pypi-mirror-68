# -*- coding: utf-8 -*-
"""
    pip_services3_data.persistence.IdentifiableMemoryPersistence
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    
    Identifiable memory persistence implementation
    
    :copyright: Conceptual Vision Consulting LLC 2018-2019, see AUTHORS for more details.
    :license: MIT, see LICENSE for more details.
"""

import random
import threading

from pip_services3_commons.refer import IReferenceable
from pip_services3_commons.config import IConfigurable
from pip_services3_commons.run import IOpenable, IClosable, ICleanable
from pip_services3_components.log import CompositeLogger
from pip_services3_commons.data import PagingParams, DataPage, IdGenerator
from ..IWriter import IWriter
from ..IGetter import IGetter
from ..ISetter import ISetter

from .MemoryPersistence import MemoryPersistence

# This function will be overriden in the code
filtered = filter

class IdentifiableMemoryPersistence(MemoryPersistence, IConfigurable, IWriter, IGetter, ISetter):
    """
    Abstract persistence component that stores data in memory
    and implements a number of CRUD operations over data items
    with unique ids. The data items must implement IIdentifiable
    interface.

    In basic scenarios child classes shall only override
    [[getPageByFilter]], [[getListByFilter]] or [[deleteByFilter]]
    operations with specific filter function. All other operations
    can be used out of the box.

    In complex scenarios child classes can implement additional
    operations by accessing cached items via this._items property
    and calling [[save]] method on updates.

    ### Configuration parameters ###

        - options:
            - max_page_size:       Maximum number of items returned in a single page (default: 100)

    ### References ###

        - *:logger:*:*:1.0       (optional) ILogger components to pass log messages

    Example:
        class MyMemoryPersistence(IdentifiableMemoryPersistence):

            def get_page_by_filter(self, correlationId, filter, paging):
                super().get_page_by_filter(correlationId, filter, paging, None)

            persistence = MyMemoryPersistence("./data/data.json")

            item = persistence.create("123", MyData("1", "ABC"))

            mydata = persistence.get_page_by_filter("123", FilterParams.from_tuples("name", "ABC"), None, None)
            print str(mydata.get_data())

            persistence.delete_by_id("123", "1")
            ...
    """
    _max_page_size = 100

    def __init__(self, loader = None, saver = None):
        """
        Creates a new instance of the persistence.

        :param loader: (optional) a loader to load items from external datasource.

        :param saver: (optional) a saver to save items to external datasource.
        """
        super(IdentifiableMemoryPersistence, self).__init__(loader, saver)

    def configure(self, config):
        """
        Configures component by passing configuration parameters.

        :param config: configuration parameters to be set.
        """
        self._max_page_size = config.get_as_integer_with_default("options.max_page_size", self._max_page_size)


    def get_page_by_filter(self, correlation_id, filter, paging, sort = None, select = None):
        """
        Gets a page of data items retrieved by a given filter and sorted according to sort parameters.

        This method shall be called by a public getPageByFilter method from child class that
        receives FilterParams and converts them into a filter function.

        :param correlation_id: (optional) transaction id to trace execution through call chain.

        :param filter: (optional) a filter function to filter items

        :param paging: (optional) paging parameters

        :param sort: (optional) sorting parameters

        :param select: (optional) projection parameters (not used yet)

        :return: a data page of result by filter.
        """
        self._lock.acquire()
        try:
            items = list(self._items)
        finally:
            self._lock.release()
            
        # Filter and sort
        if filter != None:
            items = list(filtered(filter, items))
        if sort != None:
            items = list(items.sort(key=sort))
            # items = sorted(items, sort)

        # Prepare paging parameters
        paging = paging if paging != None else PagingParams()
        skip = paging.get_skip(-1)
        take = paging.get_take(self._max_page_size)
        
        # Get a page
        data = items
        if skip > 0:
            data = data[skip:]
        if take > 0:
            data = data[:take+1]
                
        # Convert values
        if select != None:
            data = map(select, data)
                
        self._logger.trace(correlation_id, "Retrieved " + str(len(data)) + " items")

        # Return a page
        return DataPage(data, len(items))


    def get_list_by_filter(self, correlation_id, filter, sort = None, select = None):
        """
        Gets a list of data items retrieved by a given filter and sorted according to sort parameters.

        This method shall be called by a public getListByFilter method from child class that
        receives FilterParams and converts them into a filter function.

        :param correlation_id: (optional) transaction id to trace execution through call chain.

        :param filter: (optional) a filter function to filter items

        :param sort: (optional) sorting parameters

        :param select: (optional) projection parameters (not used yet)

        :return: a data list of results by filter.
        """
        self._lock.acquire()
        try:
            items = list(self._items)
        finally:
            self._lock.release()

        # Filter and sort
        if filter != None:
            items = list(filtered(filter, items))
        if sort != None:
            items = list(sorted(items, key=sort))
                        
        # Convert values      
        if select != None:
            items = map(select, items)
                
        # Return a list
        return list(items)

    def get_list_by_ids(self, correlation_id, ids):
        """
        Gets a list of data items retrieved by given unique ids.

        :param correlation_id: (optional) transaction id to trace execution through call chain.

        :param ids: ids of data items to be retrieved

        :return: a data list of results by ids.
        """
        def filter(item):
            return item['id'] in ids

        return self.get_list_by_filter(correlation_id, filter)


    def _find_one(self, id):
        for item in self._items:
            if item['id'] == id:
                return item
        return None


    def get_one_by_id(self, correlation_id, id):
        """
        Gets a data item by its unique id.

        :param correlation_id: (optional) transaction id to trace execution through call chain.

        :param id: an id of data item to be retrieved.

        :return: data item by id.
        """
        self._lock.acquire()
        try:
            item = self._find_one(id)
        finally:
            self._lock.release()

        if item != None:
            self._logger.trace(correlation_id, "Retrieved " + str(item) + " by " + str(id))
        else:
            self._logger.trace(correlation_id, "Cannot find item by " + str(id))
        return item


    def get_one_random(self, correlation_id):
        """
        Gets a random item from items that match to a given filter.

        This method shall be called by a public getOneRandom method from child class
        that receives FilterParams and converts them into a filter function.

        :param correlation_id: (optional) transaction id to trace execution through call chain.

        :return: a random item.
        """
        self._lock.acquire()
        try:
            if len(self._items) == 0:
                return None

            index = random.randint(0, len(self._items))
            item = self._items[index]
        finally:
            self._lock.release()
            
        if item != None:
            self._logger.trace(correlation_id, "Retrieved a random item")
        else:
            self._logger.trace(correlation_id, "Nothing to return as random item")
                        
        return item


    def create(self, correlation_id, item):
        """
        Creates a data item.

        :param correlation_id: (optional) transaction id to trace execution through call chain.

        :param item: an item to be created.

        :return: a created item
        """
        if 'id' not in item or item['id'] == None:
            item['id'] = IdGenerator.next_long()

        self._lock.acquire()
        try:
            self._items.append(item)
        finally:
            self._lock.release()

        self._logger.trace(correlation_id, "Created " + str(item))

        # Avoid reentry
        self.save(correlation_id)
        return item


    def set(self, correlation_id, item):
        """
        Sets a data item. If the data item exists it updates it, otherwise it create a new data item.

        :param correlation_id: (optional) transaction id to trace execution through call chain.

        :param item: an item to be set.

        :return: an updated item
        """
        if 'id' not in item or item['id'] == None:
            item['id'] = IdGenerator.next_long()

        self._lock.acquire()
        try:
            old_item = self._find_one(item['id'])
            if old_item == None:
                self._items.append(item)
            else:
                index = self._items.index(old_item)
                if index < 0:
                    self._items.append(item)
                else:
                    self._items[index] = item
        finally:
            self._lock.release()

        self._logger.trace(correlation_id, "Set " + str(item))

        # Avoid reentry
        self.save(correlation_id)
        return item


    def update(self, correlation_id, new_item):
        """
        Updates a data item.

        :param correlation_id: (optional) transaction id to trace execution through call chain.

        :param new_item: an item to be updated.

        :return: an updated item.
        """
        self._lock.acquire()
        try:
            old_item = self._find_one(new_item['id'])
            if old_item == None:
                return None
            
            index = self._items.index(old_item)
            if index < 0: return None

            self._items[index] = new_item
        finally:
            self._lock.release()

        self._logger.trace(correlation_id, "Updated " + str(new_item))

        # Avoid reentry
        self.save(correlation_id)
        return new_item

    def update_partially(self, correlation_id, id, data):
        """
        Updates only few selected fields in a data item.

        :param correlation_id: (optional) transaction id to trace execution through call chain.

        :param id: an id of data item to be updated.

        :param data: a map with fields to be updated.

        :return: an updated item.
        """
        new_item = None

        self._lock.acquire()
        try:
            old_item = self._find_one(id)
            if old_item == None:
                return None
            
            for (k, v) in data.items():
                old_item[k] = v

            new_item = old_item
        finally:
            self._lock.release()

        self._logger.trace(correlation_id, "Partially updated " + str(old_item))

        # Avoid reentry
        self.save(correlation_id)
        return new_item


    def delete_by_id(self, correlation_id, id):
        """
        Deleted a data item by it's unique id.

        :param correlation_id: (optional) transaction id to trace execution through call chain.

        :param id: an id of the item to be deleted

        :return: a deleted item.
        """
        self._lock.acquire()
        try:
            item = self._find_one(id)
            if item == None: return None
            
            index = self._items.index(item)
            if index < 0: return None

            del self._items[index]
        finally:
            self._lock.release()

        self._logger.trace(correlation_id, "Deleted " + str(item))

        self.save(correlation_id)
        return item


    def delete_by_filter(self, correlation_id, filter):
        """
        Deletes data items that match to a given filter.

        This method shall be called by a public deleteByFilter method from child class that
        receives FilterParams and converts them into a filter function.

        :param correlation_id: (optional) transaction id to trace execution through call chain.

        :param filter: (optional) a filter function to filter items.
        """
        def negative_filter(item):
            return not filter(item)

        old_length = len(list(self._items))

        self._lock.acquire()
        try:
            self._items = list(filtered(negative_filter, self._items))
        finally:
            self._lock.release()
        deleted = old_length - len(list(self._items))
        self._logger.trace(correlation_id, "Deleted " + str(deleted) + " items")

        if (deleted > 0):
            self.save(correlation_id)


    def delete_by_ids(self, correlation_id, ids):
        """
        Deletes multiple data items by their unique ids.

        :param correlation_id: (optional) transaction id to trace execution through call chain.

        :param ids: ids of data items to be deleted.
        """
        def filter(item):
            return item['id'] in ids
        
        self.delete_by_filter(correlation_id, filter)
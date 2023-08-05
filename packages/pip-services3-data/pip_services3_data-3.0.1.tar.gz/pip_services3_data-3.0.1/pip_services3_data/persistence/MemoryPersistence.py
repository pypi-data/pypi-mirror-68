# -*- coding: utf-8 -*-
"""
    pip_services3_data.persistence.MemoryPersistence
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    
    Memory persistence implementation
    
    :copyright: Conceptual Vision Consulting LLC 2018-2019, see AUTHORS for more details.
    :license: MIT, see LICENSE for more details.
"""

import random
import threading

from pip_services3_commons.refer import IReferenceable
from pip_services3_commons.config import IReconfigurable
from pip_services3_commons.run import IOpenable, IClosable, ICleanable
from pip_services3_components.log import CompositeLogger
from pip_services3_commons.data import PagingParams, DataPage, IdGenerator

class MemoryPersistence(IReferenceable, IOpenable, ICleanable):
    """
    Abstract persistence component that stores data in memory.

    This is the most basic persistence component that is only
    able to store data items of any type. Specific CRUD operations
    over the data items must be implemented in child classes by
    accessing <code>this._items</code> property and calling
    [[save]] method.

    The component supports loading and saving items from another
    data source. That allows to use it as a base class for file
    and other types of persistence components that cache all data
    in memory.

    ### References ###
        - *:logger:*:*:1.0   (optional) ILogger components to pass log messages

    Example:
        class MyMemoryPersistence(MemoryPersistence):

            def get_by_name(self, correlationId, name):
                item = self.find(name)
                ...
                return item

        persistence = MyMemoryPersistence()

        persistence.set("123", MyData("ABC"))
        print str(persistence.get_by_name("123", "ABC")))
    """
    _logger = None
    _items = None
    _loader = None
    _saver = None
    _lock = None
    _opened = False

    def __init__(self, loader = None, saver = None):
        """
        Creates a new instance of the persistence.

        :param loader: (optional) a loader to load items from external datasource.

        :param saver: (optional) a saver to save items to external datasource.
        """
        self._lock = threading.Lock()
        self._logger = CompositeLogger()
        self._items = []
        self._loader = loader
        self._saver = saver

    def set_references(self, references):
        """
        Sets references to dependent components.

        :param references: references to locate the component dependencies.
        """
        self._logger.set_references(references)

    def is_opened(self):
        """
        Checks if the component is opened.

        :return: true if the component has been opened and false otherwise.
        """
        return self._opened

    def open(self, correlation_id):
        """
        Opens the component.

        :param correlation_id: (optional) transaction id to trace execution through call chain.
        """
        self.load(correlation_id)
        self._opened = True

    def close(self, correlation_id):
        """
        Closes component and frees used resources.

        :param correlation_id: (optional) transaction id to trace execution through call chain.
        """
        self.save(correlation_id)
        self._opened = False

    def _convert_to_public(self, value):
        return value

    def _convert_from_public(self, value):
        return value

    def load(self, correlation_id):
        if self._loader == None: return

        self._lock.acquire()
        try:
            items = self._loader.load(correlation_id)
            self._items = []
            for item in items:
                item = self._convert_to_public(item)
                self._items.append(item)
        finally:
            self._lock.release()

        self._logger.trace(correlation_id, "Loaded " + str(len(self._items)) + " items")

    def save(self, correlation_id):
        """
        Saves items to external data source using configured saver component.

        :param correlation_id: (optional) transaction id to trace execution through call chain.
        """
        if self._saver == None: return

        self._lock.acquire()
        try:
            items = []
            for item in self._items:
                item = self._convert_from_public(item)
                items.append(item)
            self._saver.save(correlation_id, items)
        finally:
            self._lock.release()

        self._logger.trace(correlation_id, "Saved " + str(len(self._items)) + " items")

    def clear(self, correlation_id):
        """
        Clears component state.

        :param correlation_id: (optional) transaction id to trace execution through call chain.
        """
        self._lock.acquire()
        
        try:
            del self._items[:]
        finally:
            self._lock.release()

        self._logger.trace(correlation_id, "Cleared items")

        # Outside of lock to avoid reentry
        self.save(correlation_id)

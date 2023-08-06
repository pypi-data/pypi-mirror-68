"""
Base class and utilities for all TGN objects.

@author yoram@ignissoft.com
"""

from collections import OrderedDict
import gc
from abc import ABCMeta, abstractmethod
import json

from trafficgenerator.tgn_utils import TgnError


# Workaround IXN object reference bugs.
# Object reference with float sequential number instead of integer.
#    For example, endpointset->sources attribute might return:
#    vport:1/protocols/bgp/neighborRange:1.0/routeRange:1.
# Object reference with neighborPairs (plural) instead of neighborPair (single).
def _WA_norm_obj_ref(obj_ref):
    return obj_ref.replace('.0', '').replace('neighborPairs:', 'neighborPair:')


class TgnObjectsDict(OrderedDict):
    """ Dictionary to map from TgnObjects to whatever data.

    Dictionary keys must be TgnObject but then it can be accessed by the object itself, the object reference or the
    object name.
    """

    def __setitem__(self, key, value):
        if not isinstance(key, TgnObject):
            raise TgnError('tgn_object_dict keys must be TgnObject, not {}'.format(type(key)))
        return OrderedDict.__setitem__(self, key, value)

    def __getitem__(self, key):
        if key in self.keys():
            return OrderedDict.__getitem__(self, key)
        else:
            for obj in self:
                if obj.name == key or obj.ref == key:
                    return OrderedDict.__getitem__(self, obj)

    def dumps(self, indent=1):
        """ Returns nested string representation of the dictionary (like json.dumps).

        :param indent: indentation level.
        """

        str_keys_dict = OrderedDict({str(k): v for k, v in self.items()})
        for k, v in str_keys_dict.items():
            if isinstance(v, dict):
                str_keys_dict[k] = OrderedDict({str(k1): v1 for k1, v1 in v.items()})
                for k1, v1 in str_keys_dict[k].items():
                    if isinstance(v1, dict):
                        str_keys_dict[k][k1] = OrderedDict({str(k2): v2 for k2, v2 in v1.items()})
        return json.dumps(str_keys_dict, indent=indent)


class TgnSubStatsDict(TgnObjectsDict):
    """ Dictionary that assumes it contains sub dictionary so if a requested key does not exit it will assume it is a
        key of the first sub-dictionary.

    Port and stream statistics should be hierarchical - {rx port, {key, value}} - to support multicast traffic.
    However, in most cases there is only one RX port so the rx port level is redundant.
    """

    def __getitem__(self, key):
        if super(self.__class__, self).__getitem__(key) is not None:
            return super(self.__class__, self).__getitem__(key)
        else:
            if len(self) > 1:
                raise KeyError('multiple values')
            return list(self.values())[0][key]


class TgnObject(object):
    """ Base class for all TGN classes. """

    objects = OrderedDict()
    """ Dictionary of child objects <object reference: object name>. """

    def __init__(self, **data):
        """ Create new TGN object in the API.

        If object does not exist on the chassis, create it on the chassis as well.

        :param parent: object parent. If == None the api and logger attributes must be set explicitly by the caller.
        """

        super(TgnObject, self).__init__()
        self._data = {}
        self.objects = OrderedDict()
        self._set_data(**data)
        if self._data['parent']:
            self.api = self.obj_parent().api
            self.logger = self.obj_parent().logger
        if 'objRef' not in self._data:
            self._data['objRef'] = self._create()
        if 'name' not in self._data:
            self._data['name'] = self.ref
        if self._data.get('parent', None):
            # todo: make sure each object has parent and test only for None parents (STC project and IXN root)..
            self._data['parent'].objects[self.obj_ref()] = self

    def __str__(self):
        return self.name

    def get_child(self, *types):
        """
        :param types: list of requested types.
        :return: the first (and in most useful cases only) child of specific type(s).
        """
        children = list(self.get_children(*types))
        return children[0] if any(children) else None

    def get_object_by_ref(self, obj_ref):
        """
        :param obj_ref: requested object reference.
        :return: the first object with the requested object reference in the object branch.
        """
        return self._get_object_by_key('objRef', _WA_norm_obj_ref(obj_ref))

    def get_object_by_name(self, obj_name):
        """
        :param obj_name: requested object name.
        :return: the first object with the requested object name in the object branch.
        """
        return self._get_object_by_key('name', obj_name)

    def _get_object_by_key(self, key, value, *types):
        if self._data[key] == value and (types and self.obj_type() in types or not types):
            return self
        else:
            if not types:
                children = self.objects.values()
            else:
                children = self.get_objects_by_type(*types)
            for child in children:
                obj = child._get_object_by_key(key, value, *types)
                if obj is not None:
                    return obj

    def get_objects_by_type(self, *types):
        """ Returned objects stored in memory (without re-reading them from the TGN).

        Use this method for fast access to objects in case of static configurations.

        :param types: requested object types.
        :return: all children of the specified types.
        """

        if not types:
            return self.objects.values()
        types_l = [o.lower() for o in types]
        return [o for o in self.objects.values() if o.obj_type().lower() in types_l]

    def get_object_by_type(self, *types):
        """
        :param types: requested object types.
        :return: the child of the specified types.
        """
        children = self.get_objects_by_type(*types)
        return children[0] if any(children) else None

    def get_objects_by_type_in_subtree(self, *types):
        """
        :param types: requested object types.
        :return: all children of the specified types.
        """

        typed_objects = self.get_objects_by_type(*types)
        for child in self.objects.values():
            typed_objects += child.get_objects_by_type_in_subtree(*types)
        return typed_objects

    def get_objects_or_children_by_type(self, *types):
        """ Get objects if children already been read or get children.

        Use this method for fast access to objects in case of static configurations.

        :param types: requested object types.
        :return: all children of the specified types.
        """

        objects = self.get_objects_by_type(*types)
        return objects if objects else self.get_children(*types)

    def get_object_or_child_by_type(self, *types):
        """ Get object if child already been read or get child.

        Use this method for fast access to objects in case of static configurations.

        :param types: requested object types.
        :return: all children of the specified types.
        """

        objects = self.get_objects_or_children_by_type(*types)
        return objects[0] if any(objects) else None

    def get_objects_with_object(self, obj_type, *child_types):
        """
        :param obj_type: requested object type.
        :param child_type: requested child types.
        :return: all children of the requested type that have the requested child types.
        """

        return [o for o in self.get_objects_by_type(obj_type) if
                o.get_objects_by_type(*child_types)]

    def get_objects_without_object(self, obj_type, *child_types):
        """
        :param obj_type: requested object type.
        :param child_type: unrequested child types.
        :return: all children of the requested type that do not have the unrequested child types.
        """
        return [o for o in self.get_objects_by_type(obj_type) if
                not o.get_objects_by_type(*child_types)]

    def get_objects_with_attribute(self, obj_type, attribute, value):
        """
        :param obj_type: requested object type.
        :param attribute: requested attribute.
        :param value: requested attribute value.
        :return: all children of the requested type that have the requested attribute == requested value.
        """
        return [o for o in self.get_objects_by_type(obj_type) if o.get_attribute(attribute) == value]

    def get_ancestor_object_by_type(self, obj_type):
        """
        :param obj_type: requested ancestor type.
        :return: the ancestor of the object who's type is obj_type if exists else None.
        """

        if self.type.lower() == obj_type.lower():
            return self
        else:
            if not self.parent:
                return None
            return self.parent.get_ancestor_object_by_type(obj_type)

    def get_object_from_attribute(self, attribute):
        return self.get_objects_from_attribute(attribute)[0] if self.get_objects_from_attribute(attribute) else None

    @abstractmethod
    def get_objects_from_attribute(self, attribute):
        pass

    def del_object_from_parent(self):
        """ Delete object from parent object. """
        if self.parent:
            self.parent.objects.pop(self.ref)

    def del_objects_by_type(self, type_):
        """ Delete all children objects.

        :param type_: type of objects to delete.
        """
        [o.del_object_from_parent() for o in self.get_objects_by_type(type_)]

    @classmethod
    def get_objects_of_class(cls):
        """
        :return: all instances of the requested class.
        """
        return list(o for o in gc.get_objects() if isinstance(o, cls))

    #
    # Simple utilities to return object _data. Maybe it's not Pythonic (more like Java) but after
    # changing the key name couple of times I decided to go for it.
    #

    def obj_name(self):
        """
        :return: object name.
        """
        return self._data['name']
    name = property(obj_name)

    def obj_ref(self):
        """ Object refernce is unique, descriptive, ID within the objects tree.

        In some TGs (IxNetwork, STC, IxLoad...) the refernece is maintained by the TG itself and is used for API calls.
        In others (Xena, TRex...) the reference is maintained by the TG package and may (Xena REST) or may not be used
            for API calls.
        If the reference is not used for API calls, use index or relative index for API calls.

        :return: object reference.
        """
        return str(self._data['objRef'])
    ref = property(obj_ref)

    def obj_type(self):
        """
        :return: object type.
        """
        return self._data['objType']
    type = property(obj_type)

    def obj_parent(self):
        """
        :return: object parent.
        """
        return self._data['parent']
    parent = property(obj_parent)

    def obj_index(self):
        """ Object index is the index string used for API calls when object reference there is not used.

        Object index structure is something like chassis/card/port.

        :return: object index.
        """
        return str(self._data['index'])
    index = property(obj_index)

    def obj_id(self):
        """ Object ID is the relative ID of the object.

        :return: object relative ID.
        """
        return int(self.index.split('/')[-1]) if self.index else None
    id = property(obj_id)

    #
    # Private methods.
    #

    def _set_data(self, **data):
        self._data.update(data)

    def _build_children_objs(self, child_type, children):
        children_objs = OrderedDict()
        child_obj_type = self.get_obj_class(child_type)
        for child in (c for c in children if c != ''):
            child_object = child_obj_type(objRef=child, objType=child_type, parent=self)
            child_object._set_data(name=child_object.get_name())
            children_objs[child_object.obj_ref()] = child_object
        self.objects.update(children_objs)
        return children_objs

    #
    # Abstract API methods.
    #

    @abstractmethod
    def get_attribute(self, attribute):
        """ Get single attribute value.

        :param attribute: attribute name.
        :return: attribute value.
        """
        pass

    @abstractmethod
    def get_children(self, *types):
        """ Get all children of the requested types.

        :param attribute: requested children types.
        :return: list of all children of the requested types.
        """
        pass


class TgnL3(object):
    """ ABC for all L3 objects. """

    __metaclass__ = ABCMeta

    @abstractmethod
    def ip(self):
        """
        :return: IP address.
        """
        pass

    @abstractmethod
    def num_ips(self):
        """
        :return: number of IP addresses.
        """
        pass

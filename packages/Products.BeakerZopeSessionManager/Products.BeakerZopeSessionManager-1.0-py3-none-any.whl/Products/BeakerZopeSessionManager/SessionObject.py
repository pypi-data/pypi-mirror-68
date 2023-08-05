from collections import UserDict
import time

from AccessControl.class_init import InitializeClass
from AccessControl.SecurityInfo import ClassSecurityInfo
# from Acquisition import Implicit
from zope.interface import implementer

from .Interfaces import ISessionDataObject


def session_mutator(func):
    """Decorator to make a UserDict mutator save the session."""
    def mutating_func(self, *args, **kw):
        """."""
        res = func(self, *args, **kw)
        self.data.save()
        return res
    return mutating_func


@implementer(ISessionDataObject)
class SessionObject(UserDict):
    """Docstring for SessionObject."""

    security = ClassSecurityInfo()
    security.setDefaultAccess('allow')
    security.declareObjectPublic()

    def __init__(self, session):
        """."""
        self.data = self.session = session
        self._valid = True

    clear = session_mutator(UserDict.clear)
    update = session_mutator(UserDict.update)
    setdefault = session_mutator(UserDict.setdefault)
    pop = session_mutator(UserDict.pop)
    popitem = session_mutator(UserDict.popitem)
    __setitem__ = session_mutator(UserDict.__setitem__)
    __delitem__ = session_mutator(UserDict.__delitem__)
    set = __setitem__
    __guarded_setitem__ = __setitem__
    __guarded_delitem__ = __delitem__
    delete = __delitem__

    def __len__(self):
        """."""
        try:
            return self.data.__len__()
        except:
            return len(self.data.keys())

    def getId(self):
        """."""
        return self.session.id

    def invalidate(self):
        """."""
        self.session.invalidate()

    def isValid(self):
        """."""
        return self._valid

    def getCreated(self):
        """."""
        return time.mktime(self.session['_creation_time'].timetuple())

    getContainerKey = getId

    def _get_p_changed(self):
        return 1

    def _set_p_changed(self, v):
        if v:
            self.session.save()
    _p_changed = property(_get_p_changed, _set_p_changed)

InitializeClass(SessionObject)

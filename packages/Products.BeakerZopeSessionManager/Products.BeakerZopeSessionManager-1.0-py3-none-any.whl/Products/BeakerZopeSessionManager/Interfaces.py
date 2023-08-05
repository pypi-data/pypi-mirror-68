from zope.interface.common.mapping import IMapping
from zope.interface import Interface


class SessionDataManagerErr(ValueError):
    """Error raised during some session data manager operations.

    o See ISesseionDataManager.

    o This exception may be caught in PythonScripts.  A successful
      import of the exception for PythonScript use would need to be::

       from Products.Sessions.interfaces import SessionDataManagerErr
    """


class ISessionDataObject(IMapping):
    """ Supports a mapping interface plus expiration- and container-related
    methods """
    def getId():
        """
        Returns a meaningful unique id for the object.  Note that this id
        need not the key under which the object is stored in its container.
        """

    def invalidate():
        """
        Invalidate (expire) the transient object.

        Causes the transient object container's "before destruct" method
        related to this object to be called as a side effect.
        """

    def isValid():
        """
        Return true if transient object is still valid, false if not.
        A transient object is valid if its invalidate method has not been
        called.
        """

    def getCreated():
        """
        Return the time the transient object was created in integer
        seconds-since-the-epoch form.
        """

    def getContainerKey():
        """
        Return the key under which the object was placed in its
        container.
        """

    def set(k, v):
        """ Alias for __setitem__ """

    def __guarded_setitem__(k, v):
        """ Alias for __setitem__ """

    def delete(k):
        """ Alias for __delitem__ """

    def __guarded_delitem__(k):
        """ Alias for __delitem__ """


class ISessionDataManager(Interface):
    """Zope Session Data Manager interface.

    A Zope Session Data Manager is responsible for maintaining Session
    Data Objects, and for servicing requests from application code
    related to Session Data Objects.  It also communicates with a Browser
    Id Manager to provide information about browser ids.
    """
    def getBrowserIdManager():
        """Return the nearest acquirable browser id manager.

        o Raise SessionDataManagerErr if no browser id manager can be found.

        o Permission required: Access session data
        """

    def getSessionData(create=1):
        """Return a Session Data Object for the current browser id.

        o If there is no current browser id, and create is true,
          return a new Session Data Object.

        o If there is no current browser id and create is false, returns None.

        o Permission required: Access session data
        """

    def hasSessionData():
        """Does a Session Data Object exist for the current browser id?

        o Do not create a Session Data Object if one does not exist.

        o Permission required: Access session data
        """

    def getSessionDataByKey(key):
        """Return a Session Data Object associated with 'key'.

        o If there is no Session Data Object associated with 'key',
          return None.

        o Permission required: Access arbitrary user session data
        """

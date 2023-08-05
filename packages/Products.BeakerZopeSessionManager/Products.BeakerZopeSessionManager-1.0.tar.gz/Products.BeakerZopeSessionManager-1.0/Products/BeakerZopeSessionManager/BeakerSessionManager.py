from OFS.SimpleItem import SimpleItem
from App.special_dtml import DTMLFile
from AccessControl.class_init import InitializeClass
from AccessControl.SecurityInfo import ClassSecurityInfo
from Acquisition import aq_inner, aq_parent
from OFS.PropertyManager import PropertyManager
from zope.interface import implementer
from collective.beaker.interfaces import ISession
from ZPublisher.BeforeTraverse import registerBeforeTraverse
from ZPublisher.BeforeTraverse import unregisterBeforeTraverse

from .BeakerPermissions import ACCESS_CONTENTS_PERM
from .BeakerPermissions import ACCESS_SESSIONDATA_PERM
from .BeakerPermissions import ARBITRARY_SESSIONDATA_PERM
from .Interfaces import SessionDataManagerErr, ISessionDataManager
from .SessionTraversal import SessionDataManagerTraverser
from .SessionObject import SessionObject


def constructBeakerSessionManager(self, id, title='', REQUEST=None):
    """."""
    ob = BeakerSessionManager(id, title)
    self._setObject(id, ob)
    if REQUEST is not None:
        return self.manage_main(self, REQUEST, update_menu=1)

constructBeakerSessionManagerForm = DTMLFile('dtml/addDataManager', globals())


@implementer(ISessionDataManager)
class BeakerSessionManager(SimpleItem, PropertyManager):
    """Docstring for BeakerSessionManager."""

    meta_type = 'Beaker Session Data Manager'
    zmi_icon = 'far fa-clock'

    ok = {
        'meta_type': 1,
        'id': 1,
        'title': 1,
        'zmi_icon': 1,
        'title_or_id': 1,
    }

    _properties = (
        {'id': 'title', 'type': 'string', 'mode': 'w', 'label': 'Title'},
    )

    manage_options = (
        PropertyManager.manage_options + SimpleItem.manage_options
    )

    _requestSessionName = 'SESSION'
    _environ_key = 'beaker.session'

    security = ClassSecurityInfo()
    security.setDefaultAccess(ok)
    security.declareObjectPublic()

    def __init__(self, id, title):
        """."""
        self.id = id
        self.title = title

    def _session(self):
        """Here's the core logic which looks up the Beaker session."""
        session = ISession(self.REQUEST)
        return SessionObject(session)

    def manage_afterAdd(self, item, container):
        """Add our traversal hook."""
        self.updateTraversalData(self._requestSessionName)

    def manage_beforeDelete(self, item, container):
        """Clean up on delete."""
        self.updateTraversalData(None)

    @security.protected(ACCESS_SESSIONDATA_PERM)
    def getSessionData(self):
        """."""
        return self._session()

    @security.protected(ACCESS_SESSIONDATA_PERM)
    def hasSessionData(self):
        """."""
        return True

    @security.protected(ARBITRARY_SESSIONDATA_PERM)
    def getSessionDataByKey(self, key):
        """."""
        raise SessionDataManagerErr(
            'Beaker session data manager does not support retrieving' +
            'arbitrary sessions.'
        )

    @security.protected(ACCESS_CONTENTS_PERM)
    def getBrowserIdManager(self):
        """."""
        raise SessionDataManagerErr(
            'Beaker session data manager does not support browser id managers.'
        )

    def updateTraversalData(self, requestSessionName=None):
        """."""
        parent = aq_parent(aq_inner(self))

        if getattr(self, '_hasTraversalHook', None):
            unregisterBeforeTraverse(parent, 'BeakerSessionDataManager')
            del self._hasTraversalHook
            self._requestSessionName = None

        if requestSessionName:
            hook = SessionDataManagerTraverser(requestSessionName, self.id)
            registerBeforeTraverse(parent, hook,
                                   'BeakerSessionDataManager', 50)
            self._hasTraversalHook = 1
            self._requestSessionName = requestSessionName

InitializeClass(BeakerSessionManager)

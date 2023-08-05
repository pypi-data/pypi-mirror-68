import sys
from logging import getLogger
from Persistence import Persistent

LOG = getLogger('SessionDataManager')


class SessionDataManagerTraverser(Persistent):
    """."""

    def __init__(self, requestSessionName, sessionDataManagerName):
        """."""
        self._requestSessionName = requestSessionName
        self._sessionDataManager = sessionDataManagerName

    def __call__(self, container, request):
        """
        Method.

        This method places a session data object reference in
        the request.  It is called on each and every request to Zope in
        Zopes after 2.5.0 when there is a session data manager installed
        in the root.
        """
        try:
            sdm = getattr(container, self._sessionDataManager)
            getSessionData = sdm.getSessionData
        except Exception:
            msg = 'Session automatic traversal failed to get session data'
            LOG.warn(msg, exc_info=sys.exc_info())
            return

        # set the getSessionData method in the "lazy" namespace
        if self._requestSessionName is not None:
            request.set_lazy(self._requestSessionName, getSessionData)

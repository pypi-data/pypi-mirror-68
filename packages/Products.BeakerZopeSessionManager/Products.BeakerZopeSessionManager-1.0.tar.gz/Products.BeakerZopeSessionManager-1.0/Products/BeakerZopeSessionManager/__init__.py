def commit(note):
    """."""
    import transaction
    transaction.get().note(note)
    transaction.commit()


def install_session_data_manager(app):
    """."""
    # Ensure that a session data manager exists
    if hasattr(app, 'beaker_session_data_manager'):
        return

    from . import BeakerSessionManager
    sdm = BeakerSessionManager.BeakerSessionManager(
        'beaker_session_data_manager',
        title='Beaker Session Data Manager',
    )
    app._setObject('beaker_session_data_manager', sdm)
    commit(u'Added beaker_session_data_manager')


def initialize(context):
    """."""
    from . import BeakerSessionManager
    context.registerClass(
        BeakerSessionManager.BeakerSessionManager,
        constructors=(BeakerSessionManager.constructBeakerSessionManagerForm,
                      BeakerSessionManager.constructBeakerSessionManager))

    app = context.getApplication()
    if app is not None:
        install_session_data_manager(app)

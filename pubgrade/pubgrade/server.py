"""Controllers for pubgrade endpoints"""

from flask import request
from foca.utils.logging import log_traffic

from pubgrade.pubgrade.endpoints.builds import (
    build_completed,
    get_build_info,
    get_builds,
    register_builds
)
from pubgrade.pubgrade.endpoints.repositories import (
    delete_repository,
    get_repositories,
    get_repository,
    modify_repository_info,
    register_repository
)
from pubgrade.pubgrade.endpoints.subscriptions import (
    delete_subscription,
    get_subscription_info,
    get_subscriptions,
    register_subscription,
)


@log_traffic
def getRepositories():
    """Get available Repositories.

    Returns:
        An array of Repository Objects"""
    return get_repositories()


@log_traffic
def postRepositories():
    """Register a new Repository.

    Returns:
        id: Identifier of Repository created.
        access_token: Secret to be used to identify the source when
        accessing repository operations next time

    """
    return register_repository(request.json)


@log_traffic
def getRepository(id: str):
    """Get Repository info.

    Args:
        id: Identifier of Repository to be retrieved.

    Returns:
        Repository Object containing build_list, subscription_list, id, url.
        """
    return get_repository(id)


@log_traffic
def putRepositories(id: str):
    """Modify already registered Repository.

    Args:
        id: Identifier of Repository to be modified.

    Returns:
        id: Identifier of Repository modified.
        access_token: Secret to be used to identify the source when
        accessing repository operations next time
    """
    return modify_repository_info(id,
                                  request.headers['X-Project-Access-Token'],
                                  request.json)


@log_traffic
def deleteRepository(id: str):
    """Delete Repository.

    Args:
        id: Identifier of Repository to be deleted

    Returns:
        "message": "Repository deleted successfully"

    """
    if delete_repository(id, request.headers['X-Project-Access-Token']) != 0:
        return {"message": "Repository deleted successfully"}


@log_traffic
def postBuild(id: str):
    """Register a new build.

    Args:
        id: Identifier of Repository for which build is to be registered.

    Returns:
        build_id: Identifier of Build created.
    """
    return register_builds(id, request.headers['X-Project-Access-Token'],
                           request.json)


@log_traffic
def getBuilds(id: str):
    """Get available builds for this Repository.

    Args:
        id: Identifier of Repository to list available builds.

    Returns:
        An array of available build objects for the repository.
    """
    return get_builds(id)


@log_traffic
def getBuildInfo(id: str, build_id: str):
    """Get build information.

    Args:
        id: Identifier of Repository  # Not used only build_id is sufficient.
        build_id: Identifier of Build to be retrieved.

    Returns:
        Build information (JSON object).
    """
    return get_build_info(build_id)


@log_traffic
def updateBuild(id: str, build_id: str):
    """Update build complete status.

    Args:
        id: Identifier of Repository
        build_id: Identifier of Build to be updated.

    Returns:
        build_id: Identifier of Build updated.
    """
    return build_completed(id,
                           build_id, request.headers['X-Project-Access-Token'])


@log_traffic
def postSubscription():
    """Register new subscription.

    Returns:
        subscription_id: Identifier of subscription created.
    """
    # test_create_user()
    return register_subscription(request.headers['X-User-Id'],
                                 request.headers['X-User-Access-Token'],
                                 request.json)


@log_traffic
def getSubscriptions():
    """Get all registered subscriptions for the user.

     Returns:
         An array of registered subscription_id's.
         """
    return get_subscriptions(request.headers['X-User-Id'],
                             request.headers['X-User-Access-Token'])


@log_traffic
def getSubscriptionInfo(subscription_id: str):
    """Get subscription information for this subscription_id.

    Args:
        subscription_id: Identifier of subscription to be retrieved.

    Returns:
        Subscription Information (JSON object)
        """
    return get_subscription_info(request.headers['X-User-Id'],
                                 request.headers['X-User-Access-Token'],
                                 subscription_id)


@log_traffic
def deleteSubscription(subscription_id: str):
    """Delete subscription.

    Args:
        subscription_id: Identifier of subscription to be deleted.

    Returns:
        subscription_id for deleted subscription.
    """
    if delete_subscription(request.headers['X-User-Id'],
                           request.headers['X-User-Access-Token'],
                           subscription_id) != 0:
        return {"subscription_id": subscription_id}

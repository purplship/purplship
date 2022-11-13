import logging
from django.conf import settings
from huey import crontab
from huey.contrib.djhuey import db_task, db_periodic_task

import karrio.server.core.utils as utils

logger = logging.getLogger(__name__)
DEFAULT_TRACKERS_UPDATE_INTERVAL = int(
    getattr(settings, "DEFAULT_TRACKERS_UPDATE_INTERVAL", 7200) / 60
)


@db_periodic_task(crontab(minute=f"*/{DEFAULT_TRACKERS_UPDATE_INTERVAL}"))
def background_trackers_update():
    from karrio.server.events.task_definitions.base import tracking

    @utils.run_on_all_tenants
    def _run(**kwargs):
        try:
            tracking.update_trackers()
        except Exception as e:
            logger.error(f"failed to crawl tracking statuses: {e}")

    _run()


@db_task()
@utils.tenant_aware
def notify_webhooks(*args, **kwargs):
    from karrio.server.events.task_definitions.base import webhook

    utils.failsafe(
        lambda: webhook.notify_webhook_subscribers(*args, **kwargs),
        "An error occured during webhook notification: $error",
    )


TASK_DEFINITIONS = [
    background_trackers_update,
    notify_webhooks,
]

"""APScheduler-based background scheduler for SmartHire."""
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.cron import CronTrigger

from app.core.logging import get_logger

logger = get_logger(__name__)

scheduler = AsyncIOScheduler()


def _register_jobs() -> None:
    from app.services.notification_service import (
        notify_pending_feedback,
        notify_offer_expiry,
        cleanup_export_files,
        notify_l2_aging,
    )

    # Daily at 09:00 — pending feedback reminders
    scheduler.add_job(
        notify_pending_feedback,
        CronTrigger(hour=9, minute=0),
        id="pending_feedback",
        replace_existing=True,
    )

    # Daily at 10:00 — offer expiry reminders
    scheduler.add_job(
        notify_offer_expiry,
        CronTrigger(hour=10, minute=0),
        id="offer_expiry",
        replace_existing=True,
    )

    # Daily at 02:00 — export file cleanup
    scheduler.add_job(
        cleanup_export_files,
        CronTrigger(hour=2, minute=0),
        id="export_cleanup",
        replace_existing=True,
    )

    # Daily at 11:00 — L2 aging alerts
    scheduler.add_job(
        notify_l2_aging,
        CronTrigger(hour=11, minute=0),
        id="l2_aging",
        replace_existing=True,
    )

    logger.info("APScheduler jobs registered: pending_feedback, offer_expiry, export_cleanup, l2_aging")


def start_scheduler() -> None:
    _register_jobs()
    scheduler.start()
    logger.info("APScheduler started")


def stop_scheduler() -> None:
    if scheduler.running:
        scheduler.shutdown(wait=False)
        logger.info("APScheduler stopped")

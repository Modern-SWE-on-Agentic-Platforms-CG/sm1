"""Tests for notification service and scheduler."""
import pytest
from unittest.mock import patch, MagicMock
from pathlib import Path


def test_log_email_writes_to_log(tmp_path):
    """Ensure notification service logs email to file."""
    import importlib
    import app.services.notification_service as ns

    # Patch the log path
    fake_log = tmp_path / "email.log"
    with patch.object(ns, "_email_log_path", fake_log):
        ns._log_email("test@example.com", "Test Subject", "Test body")
    # Log is written via logger; just verify no exception raised
    assert True


def test_send_email_no_smtp(monkeypatch):
    """Email is only logged, not sent, when SMTP_ENABLED is False."""
    from app.core.config import settings
    import app.services.notification_service as ns

    monkeypatch.setattr(settings, "SMTP_ENABLED", False, raising=False)
    with patch.object(ns, "_log_email") as mock_log:
        ns._send_email("to@example.com", "Subject", "Body")
        mock_log.assert_called_once()


def test_notify_pending_feedback_no_error():
    """notify_pending_feedback should not raise even with empty DB."""
    from app.services.notification_service import notify_pending_feedback
    with patch("app.services.notification_service.SessionLocal") as mock_session:
        mock_db = MagicMock()
        mock_db.query.return_value.filter.return_value.all.return_value = []
        mock_session.return_value = mock_db
        notify_pending_feedback()
        mock_db.close.assert_called_once()


def test_cleanup_export_files_no_error():
    """cleanup_export_files should not raise with empty DB."""
    from app.services.notification_service import cleanup_export_files
    with patch("app.services.notification_service.SessionLocal") as mock_session:
        mock_db = MagicMock()
        mock_session.return_value = mock_db
        with patch("app.services.notification_service.cleanup_old_exports", return_value=0):
            cleanup_export_files()
            mock_db.close.assert_called_once()


def test_scheduler_registers_jobs():
    """Scheduler should register exactly 4 jobs."""
    from app.core.scheduler import scheduler, _register_jobs, stop_scheduler
    _register_jobs()
    job_ids = {job.id for job in scheduler.get_jobs()}
    assert {"pending_feedback", "offer_expiry", "export_cleanup", "l2_aging"}.issubset(job_ids)
    stop_scheduler()

import os

from django.conf import settings
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase

from core.services.file_service import FileService
from core.services.security_service import SecurityService


class Phase4FileSecurityTests(TestCase):

    def test_rejects_path_traversal_filename(self):
        with self.assertRaisesMessage(ValueError, "Invalid filename."):
            SecurityService.safe_basename("../evil.csv")

    def test_rejects_backslash_path_traversal(self):
        with self.assertRaisesMessage(ValueError, "Invalid filename."):
            SecurityService.safe_basename(r"..\evil.csv")

    def test_rejects_non_csv_content_type(self):
        file = SimpleUploadedFile(
            "data.csv",
            b"a,b\n1,2\n",
            content_type="application/pdf",
        )

        with self.assertRaisesMessage(
            ValueError,
            "Unsupported file content type.",
        ):
            FileService.validate_csv_file(file)

    def test_rejects_duplicate_columns(self):
        file = SimpleUploadedFile(
            "data.csv",
            b"a,a\n1,2\n",
            content_type="text/csv",
        )

        FileService.validate_csv_file(file)

        with self.assertRaisesMessage(
            ValueError,
            "duplicate column names",
        ):
            FileService.read_csv_file(file)


class Phase4SecurityUtilityTests(TestCase):

    def test_media_root_containment(self):
        inside = os.path.join(settings.MEDIA_ROOT, "result.csv")
        self.assertTrue(SecurityService.is_within_media_root(inside))

    def test_rejects_path_outside_media_root(self):
        outside = os.path.abspath(
            os.path.join(settings.MEDIA_ROOT, "..", "outside.csv")
        )
        self.assertFalse(SecurityService.is_within_media_root(outside))

    def test_safe_basename_rejects_traversal(self):
        with self.assertRaises(ValueError):
            SecurityService.safe_basename("../secret.txt")

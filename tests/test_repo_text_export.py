import tempfile
import unittest
from pathlib import Path

import repo_text_export


class RepoTextExportTests(unittest.TestCase):
    def test_creates_plain_text_bundle_without_git_metadata(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            root = Path(tmpdir)
            (root / "README.md").write_text("hello world\n", encoding="utf-8")
            (root / "notes.txt").write_text("more text\n", encoding="utf-8")
            (root / ".git").mkdir()
            (root / ".git" / "config").write_text("ignore me\n", encoding="utf-8")

            output_path = root / "repo_bundle.txt"
            repo_text_export.generate_repo_text_bundle(root, output_path)

            content = output_path.read_text(encoding="utf-8")
            self.assertIn("README.md", content)
            self.assertIn("hello world", content)
            self.assertIn("notes.txt", content)
            self.assertNotIn(".git", content)
            self.assertNotIn("ignore me", content)


if __name__ == "__main__":
    unittest.main()

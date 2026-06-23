import json
import tempfile
import unittest
from pathlib import Path

import validate_missions


class MissionValidationTests(unittest.TestCase):
    def test_accepts_valid_single_mission_file(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            path = Path(tmpdir) / "mission.json"
            path.write_text(
                json.dumps({
                    "id": "demo_mission",
                    "number": 11,
                    "title": "Demo Mission",
                    "skill": "python",
                    "challenge": "What is 2 + 2?",
                    "answer": "4"
                }),
                encoding="utf-8"
            )

            errors = validate_missions.validate_path(path)
            self.assertEqual(errors, [])

    def test_accepts_valid_mission_index_file(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            path = Path(tmpdir) / "missions.json"
            path.write_text(
                json.dumps({
                    "missions": [{
                        "id": "demo_mission",
                        "number": 11,
                        "title": "Demo Mission",
                        "skill": "python",
                        "challenge": "What is 2 + 2?",
                        "answer": "4"
                    }]
                }),
                encoding="utf-8"
            )

            errors = validate_missions.validate_path(path)
            self.assertEqual(errors, [])

    def test_accepts_folder_style_mission_file(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            mission_dir = Path(tmpdir) / "missions"
            mission_dir.mkdir()
            path = mission_dir / "mission02.json"
            path.write_text(
                json.dumps({
                    "id": "demo_folder_mission",
                    "number": 2,
                    "title": "Folder Mission",
                    "skill": "python",
                    "tag": "Python",
                    "philosophy": "A short philosophy note.",
                    "economics": "A short economics note.",
                    "techconcept": "A short tech note.",
                    "lesson": "A short lesson note.",
                    "challenge": "What is 2 + 2?",
                    "hint": "Think carefully.",
                    "answer": ["4"],
                    "answertype": "exact",
                    "honorreward": 20,
                    "bonusfirsttry": 5
                }),
                encoding="utf-8"
            )

            errors = validate_missions.validate_path(path)
            self.assertEqual(errors, [])

    def test_reports_missing_required_fields(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            path = Path(tmpdir) / "mission.json"
            path.write_text(json.dumps({"id": "broken"}), encoding="utf-8")

            errors = validate_missions.validate_path(path)
            self.assertTrue(any("Missing required field" in error for error in errors))


if __name__ == "__main__":
    unittest.main()

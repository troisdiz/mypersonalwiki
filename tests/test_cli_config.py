import unittest
from pathlib import Path

from gitwiki.cli.cli_config import parse_config


class TestCliConfig(unittest.TestCase):
    def setUp(self):
        self.test_data_dir : Path = Path(__file__).parent / "testdata" / "config"

    def test_empty_config(self):
        config_empty_path: Path = self.test_data_dir / "config_empty.yaml"
        config_empty = parse_config(str(config_empty_path))
        self.assertEqual(len(config_empty.locations), 0)

    def test_no_location_config(self):
        config_no_location_path: Path = self.test_data_dir / "config_no_location.yaml"
        config_no_location = parse_config(str(config_no_location_path))
        self.assertEqual(len(config_no_location.locations), 0)

    def test_one_location_config(self):
        config_one_location_path: Path = self.test_data_dir / "config_one_location.yaml"
        config_one_location = parse_config(str(config_one_location_path))
        self.assertEqual(len(config_one_location.locations), 1)
        self.assertEqual(config_one_location.locations["toto"].path, Path("/tutu"))

if __name__ == '__main__':
    unittest.main()

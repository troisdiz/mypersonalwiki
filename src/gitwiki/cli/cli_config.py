from dataclasses import dataclass
from pathlib import Path

import yaml


@dataclass(frozen=True)
class GitWikiLocation:
    path: Path

@dataclass
class GitWikiCLIConfig:
    locations: dict[str, GitWikiLocation]

def parse_config(config_str_path: str | None) -> GitWikiCLIConfig:
    if config_str_path is None:
        config_path : Path = Path("~/.config/gitwiki/cli.yaml").expanduser()
    else:
        config_path : Path = Path(config_str_path)

    if config_path.exists():
        with open(config_path) as f:
            data = yaml.safe_load(f)
        locations: dict[str, GitWikiLocation] = dict()
        if data is None:
            return GitWikiCLIConfig(dict())

        if "locations" in data:
            if data["locations"] is None:
                return GitWikiCLIConfig(dict())

            for location in data["locations"]:
                if "id" in location:
                    config_id: str = location["id"]
                else:
                    raise f"Cannot find path for location"
                if "path" in location:
                    config_path : Path = Path(location["path"])
                else:
                    raise f"Cannot find path for location {config_id}"
                loc_config : GitWikiLocation = GitWikiLocation(config_path)
                locations[config_id] = loc_config
        return GitWikiCLIConfig(locations)

    raise FileNotFoundError(config_path)
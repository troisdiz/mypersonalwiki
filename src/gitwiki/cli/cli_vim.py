import subprocess

from pathlib import Path


class GitWikiVimHander:
    def __init__(self, server_name: str, base_path: Path):
        self.server_name = server_name
        self.base_path = base_path

    def __check_running(self) -> bool:
        result = subprocess.run(
            ["gvim", "--serverlist"],
            capture_output=True,
            text=True,
            check=True,  # raises CalledProcessError if it exits non-zero
        )
        if result.returncode != 0:
            raise RuntimeError("Could not run gvim")
        for line in result.stdout.splitlines():
            if line == self.server_name.upper():
                return True
        return False

    def __launch_and_edit(self, file_path: Path) -> bool:
        result = subprocess.run(
            ["gvim", "--servername", f"{self.server_name}", str(file_path)],
            cwd=str(self.base_path),
            capture_output=True,
            text=True,
        )
        return result.returncode == 0

    def edit(self, relative_path: str) -> bool:
        file_abs_path = self.base_path / relative_path

        launch_args = ["gvim", "--servername", f"{self.server_name}", str(file_abs_path)]
        edit_args = ["gvim", "--servername", f"{self.server_name}", "--remote", str(file_abs_path)]

        if self.__check_running():
            args = edit_args
        else:
            args = launch_args

        print("CLI:" + " ".join(args))
        result = subprocess.Popen(
            args,
            cwd=str(self.base_path),
        )
        return True

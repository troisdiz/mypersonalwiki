import argparse
import sys

from gitwiki.cli.cli_config import parse_config, GitWikiCLIConfig, GitWikiLocation
from gitwiki.cli.cli_vim import GitWikiVimHander


def edit(args):
    config: GitWikiCLIConfig = parse_config(args.config)
    if args.id in config.locations:
        location: GitWikiLocation = config.locations[args.id]
    else:
        print(f"Cannot find location with id {args.id}", file=sys.stderr)
        sys.exit(1)
    vim_handler: GitWikiVimHander = GitWikiVimHander(server_name=args.id, base_path=location.path)
    edit_success = vim_handler.edit(args.file)
    if not edit_success:
        print(f"Failed to edit {args.file}", file=sys.stderr)
        sys.exit(1)
    else:
        sys.exit(0)

def version(args):
    print("gitwiki cli v0.1.1")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        prog="GitWiki CLI",
        description="A Cobra-like Python CLI"
    )
    parser.add_argument("-c",  "--config", type=str,
                        help="Path of the configuration file")
    commands = parser.add_subparsers(
        title="commands",
        dest="command",
        required=True,
    )
    edit_cmd = commands.add_parser("edit",
                                   help="Edit file in Gitwiki repository")
    edit_cmd.add_argument("file", type=str,
                          help="File Path to edit")
    edit_cmd.add_argument("-i", "--id", type=str, required=True,
                           help="Id of the repository to edit")
    edit_cmd.set_defaults(func=edit)

    version_cmd = commands.add_parser("version", help="Show version")
    version_cmd.set_defaults(func=version)

    # Parse command line arguments
    # Parse config file

    """
    Commands:
     * create
     * edit
     * move
    """

    args = parser.parse_args()
    args.func(args)

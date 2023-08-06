import glob
import re
from pydoc import ModuleScanner
from typing import Any, Optional, Set

import click
from nbconvert import ScriptExporter  # type: ignore

from_regexp = re.compile(r"^from (\w+)")
import_regexp = re.compile(r"^import (\w+)")


def get_imported_modules(glob_path: str) -> Set[str]:
    nb_paths = glob.glob(glob_path, recursive=True)
    se: Any = ScriptExporter()

    all_imported_modules = set()
    for path in nb_paths:
        [script, _] = se.from_filename(path)
        lines = script.split("\n")

        for line in lines:
            from_match = from_regexp.match(line)
            if from_match:
                all_imported_modules.add(from_match.group(1))
                continue

            import_match = import_regexp.match(line)
            if import_match:
                all_imported_modules.add(import_match.group(1))
                continue

    return all_imported_modules


def get_installed_modules() -> Set[str]:
    modules = set()

    def callback(path: Optional[str], modname: str, desc: str):
        if modname and modname.endswith(".__init__"):
            modname = modname.replace(".__init__", " (package)")

        if modname.find(".") == -1:
            modules.add(modname)

    def onerror(modname: str):
        pass

    ModuleScanner().run(callback, onerror=onerror)
    return modules


def check_imports():
    click.echo(f"🌲 Checking for potentially missing imports...\n")
    imported_modules = get_imported_modules("**/*ipynb")
    installed_modules = get_installed_modules()

    missing_modules = imported_modules.difference(installed_modules)

    joined = "\n  - ".join(sorted(missing_modules))
    click.echo(
        f"\n❗ You *may* be missing project requirements, the following modules are imported from your notebooks but can't be imported from your project root directory\n"
        f"{joined}"
    )


if __name__ == "__main__":
    check_imports()

from pants.backend.python.subsystems.python_tool_base import PythonToolBase
from pants.backend.python.target_types import ConsoleScript
from pants.option.option_types import StrOption


class PyMarkdown(PythonToolBase):
    options_scope = "markdownlint"
    help = "The PyMarkdown linter (https://pymarkdown.readthedocs.io/)."

    default_main = ConsoleScript("pymarkdown")

    register_interpreter_constraints = True
    default_interpreter_constraints = ["CPython>=3.12"]

    default_lockfile_resource = ("markdown", "pymarkdown.lock")
    config = StrOption(
        default=None,
        advanced=True,
        help="Path to pymarkdown config file",
    )


def rules():
    return []

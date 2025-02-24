from dataclasses import dataclass
from typing import Any

from pants.backend.adhoc.target_types import (
    AdhocToolDependenciesField,
)
from pants.backend.python.subsystems.python_tool_base import PythonToolBase
from pants.backend.python.target_types import ConsoleScript
from pants.core.goals.lint import LintResult, LintTargetsRequest
from pants.core.goals.resolves import ExportableTool
from pants.core.util_rules.external_tool import (
    DownloadedExternalTool,
    ExternalToolRequest,
)
from pants.core.util_rules.partitions import PartitionerType
from pants.core.util_rules.source_files import (
    SourceFiles,
    SourceFilesRequest,
)
from pants.engine.fs import (
    Digest,
    GlobMatchErrorBehavior,
    MergeDigests,
    PathGlobs,
)
from pants.engine.platform import Platform
from pants.engine.process import FallibleProcessResult, Process
from pants.engine.rules import Get, MultiGet, collect_rules, rule
from pants.engine.target import FieldSet, SingleSourceField
from pants.engine.unions import UnionRule
from pants.option.option_types import SkipOption, StrOption
from pants.util.logging import LogLevel
from pants.util.strutil import pluralize


class PyMarkdown(PythonToolBase):
    name = "pymarkdown"
    options_scope = "markdownlint"
    help = "The PyMarkdown linter (https://pymarkdown.readthedocs.io/)."

    default_main = ConsoleScript("pymarkdown")

    register_interpreter_constraints = True
    default_requirements = ["pymarkdownlnt"]
    default_interpreter_constraints = ["CPython==3.9.*"]

    default_lockfile_resource = ("markdown", "pymarkdown.lock")

    config = StrOption(
        default=None,
        advanced=True,
        help="Path to pymarkdown config file",
    )
    skip = SkipOption("lint")


class MarkdownDependenciesField(AdhocToolDependenciesField):
    pass


class MarkdownSourceField(SingleSourceField):
    expected_file_extensions = (".md",)


@dataclass(frozen=True)
class PyMarkdownFieldSet(FieldSet):
    required_fields = (MarkdownSourceField,)

    sources: MarkdownSourceField
    dependencies: MarkdownDependenciesField


class MarkdownLintRequest(LintTargetsRequest):
    field_set_type = PyMarkdownFieldSet
    tool_subsystem = PyMarkdown
    partitioner_type = PartitionerType.DEFAULT_SINGLE_PARTITION


@rule
async def run_markdownlint(
    request: MarkdownLintRequest.Batch[PyMarkdownFieldSet, Any],
    markdownlint: PyMarkdown, platform: Platform
) -> LintResult:
    download_markdownlint_request = Get(
        DownloadedExternalTool,
        ExternalToolRequest,
        markdownlint.get_request(platform),
    )

    sources_request = Get(
        SourceFiles,
        SourceFilesRequest(field_set.sources for field_set in request.elements),
    )

    # If the user specified `--markdownlint-config`, we must search for the file they specified with
    # `PathGlobs` to include it in the `input_digest`. We error if the file cannot be found.
    config_digest_request = Get(
        Digest,
        PathGlobs(
            globs=[markdownlint.config] if markdownlint.config else [],
            glob_match_error_behavior=GlobMatchErrorBehavior.error,
            description_of_origin="the option `[markdownlint].config`",
        ),
    )

    downloaded_markdownlint, sources, config_digest = await MultiGet(
        download_markdownlint_request, sources_request, config_digest_request
    )

    # The Process needs one single `Digest`, so we merge everything together.
    input_digest = await Get(
        Digest,
        MergeDigests(
            (
                downloaded_markdownlint.digest,
                sources.snapshot.digest,
                config_digest,
            )
        ),
    )

    process_result = await Get(
        FallibleProcessResult,
        Process(
            argv=[
                downloaded_markdownlint.exe,
                *markdownlint.args,
                *sources.snapshot.files,
            ],
            input_digest=input_digest,
            description=f"Run Pymarkdown on {pluralize(len(request.elements), 'file')}.",
            level=LogLevel.DEBUG,
        ),
    )
    return LintResult.create(request, process_result)


def rules():
    return [
        *collect_rules(),
        *MarkdownLintRequest.rules(),
        UnionRule(ExportableTool, PyMarkdown),  # allows exporting the `pymarkdown` binary
    ]

"""Test code snippets embedded in the docs with output checking.

Convention for ``.. code-block:: python`` blocks:

- ``# expected``  after an expression → verified against actual output
- ``## note``     → documentation comment, never checked as output

Comments after imports and assignments are never treated as output
(they can't produce any). Output comparison uses ``doctest.OutputChecker``
with ELLIPSIS and NORMALIZE_WHITESPACE support.

Reference: https://sybil.readthedocs.io/en/latest/use.html#pytest
"""

import ast
import builtins
import doctest
import sys
from io import StringIO

from sybil import Sybil
from sybil.parsers.rest.codeblock import CodeBlockParser
from sybil.parsers.rest.skip import SkipParser


def _is_import_or_assignment(code_line):
    """Check whether a single source line is an import or assignment."""
    stripped = code_line.strip()
    if not stripped or stripped.startswith("#"):
        return False
    try:
        tree = ast.parse(stripped)
        if tree.body:
            return isinstance(
                tree.body[0],
                (
                    ast.Import,
                    ast.ImportFrom,
                    ast.Assign,
                    ast.AugAssign,
                    ast.AnnAssign,
                ),
            )
    except SyntaxError:
        pass
    return False


def _last_code_line(lines):
    """Return the last non-blank, non-comment line (stripped), or None."""
    for line in reversed(lines):
        s = line.strip()
        if s and not s.startswith("#"):
            return s
    return None


def _parse_segments(source, true_comment_prefix):
    """Split *source* into ``(code, expected_output | None)`` pairs.

    A ``# value`` comment line after a non-import / non-assignment code line
    is treated as expected output.  ``## value`` lines are always plain code
    comments and never collected as output.
    """
    lines = source.split("\n")
    segments = []
    code_lines = []
    i = 0

    while i < len(lines):
        stripped = lines[i].strip()

        # Blank line — just accumulate.
        if not stripped:
            code_lines.append(lines[i])
            i += 1
            continue

        # ``## …`` — always a documentation note.
        if stripped.startswith(true_comment_prefix):
            code_lines.append(lines[i])
            i += 1
            continue

        # Possible output comment: ``# …`` (single hash + space) or bare ``#``.
        is_comment = stripped.startswith("# ") or stripped == "#"
        if is_comment:
            last_code = _last_code_line(code_lines)

            if last_code and not _is_import_or_assignment(last_code):
                # Collect consecutive output-comment lines.
                comments = []
                j = i
                while j < len(lines):
                    s = lines[j].strip()
                    if s.startswith(true_comment_prefix):
                        break  # doc-comment stops collection
                    elif s.startswith("# "):
                        comments.append(s[2:])
                        j += 1
                    elif s == "#":
                        comments.append("")
                        j += 1
                    else:
                        break

                code = "\n".join(code_lines)
                expected = "\n".join(comments)
                segments.append((code, expected))
                code_lines = []
                i = j
                continue

        # Regular code line *or* non-output comment.
        code_lines.append(lines[i])
        i += 1

    # Flush remaining code.
    if code_lines:
        code = "\n".join(code_lines)
        if code.strip():
            segments.append((code, None))

    return segments


def _split_last_expr(code):
    """If the last top-level statement is an expression, split it out.

    Returns ``(prefix, expr)`` or ``(code, None)``.
    """
    try:
        tree = ast.parse(code)
    except SyntaxError:
        return code, None

    if not tree.body:
        return code, None

    last = tree.body[-1]
    if isinstance(last, ast.Expr) and last.end_lineno is not None:
        lines = code.split("\n")
        prefix = "\n".join(lines[: last.lineno - 1])
        expr = "\n".join(lines[last.lineno - 1 : last.end_lineno])
        return prefix, expr

    return code, None


class _Want:
    """Minimal stand-in expected by ``doctest.OutputChecker.output_difference``."""

    def __init__(self, want):
        self.want = want


class CommentAsOutputEvaluator:
    """Sybil evaluator that checks ``# comment`` lines as expected output.

    * Expression results are captured via ``compile(…, 'single')`` which
      triggers ``sys.displayhook`` (like the interactive interpreter).
    * Printed output is captured by replacing ``sys.stdout``.
    * Comparison uses ``doctest.OutputChecker`` so that ``...`` (ELLIPSIS)
      and whitespace normalization work out of the box.
    """

    def __init__(self, optionflags=0, true_comment_prefix="## "):
        self.optionflags = optionflags
        self.true_comment_prefix = true_comment_prefix
        self._checker = doctest.OutputChecker()

    def __call__(self, example):
        source = str(example.parsed)
        segments = _parse_segments(source, self.true_comment_prefix)
        path = str(example.path)

        for code, expected in segments:
            if not code.strip():
                continue
            if expected is not None:
                self._run_and_check(code, expected, path, example.namespace)
            else:
                self._run(code, path, example.namespace)

        example.namespace.pop("__builtins__", None)

    # ------------------------------------------------------------------

    def _run(self, code, path, namespace):
        compiled = compile(code, path, "exec")
        exec(compiled, namespace)

    def _run_and_check(self, code, expected, path, namespace):
        prefix, expr = _split_last_expr(code)
        captured = StringIO()

        if expr:
            # Run everything before the final expression normally.
            if prefix and prefix.strip():
                self._run(prefix, path, namespace)

            # Run the expression with output capture.
            old_stdout = sys.stdout
            old_displayhook = sys.displayhook

            def _displayhook(value):
                if value is not None:
                    builtins._ = value
                    captured.write(repr(value))
                    captured.write("\n")

            try:
                sys.stdout = captured
                sys.displayhook = _displayhook
                compiled = compile(expr, path, "single")
                exec(compiled, namespace)
            finally:
                sys.stdout = old_stdout
                sys.displayhook = old_displayhook
        else:
            # No trailing expression (e.g. a for-loop that prints).
            # Run the whole segment and capture stdout only.
            old_stdout = sys.stdout
            try:
                sys.stdout = captured
                compiled = compile(code, path, "exec")
                exec(compiled, namespace)
            finally:
                sys.stdout = old_stdout

        actual = captured.getvalue()
        want = expected + "\n"

        if not self._checker.check_output(want, actual, self.optionflags):
            diff = self._checker.output_difference(
                _Want(want), actual, self.optionflags
            )
            raise AssertionError(f"Output mismatch:\n{diff}")


pytest_collect_file = Sybil(
    parsers=[
        CodeBlockParser(
            language="python",
            evaluator=CommentAsOutputEvaluator(
                optionflags=doctest.ELLIPSIS | doctest.NORMALIZE_WHITESPACE,
                true_comment_prefix="## ",
            ),
        ),
        SkipParser(),
    ],
    pattern="*.rst",
).pytest()

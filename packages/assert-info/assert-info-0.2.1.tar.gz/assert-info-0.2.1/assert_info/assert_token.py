from __future__ import print_function
import asttokens
import ast
import tokenize
from six import StringIO, PY2
import logging

LOG = logging.getLogger(__name__)

ASSERT_REPLACEMENTS = {
    ast.Eq: "assert_equal",
    ast.NotEq: "assert_not_equal",
    ast.Is: "assert_is",
    ast.IsNot: "assert_is_not",
    ast.In: "assert_in",
    ast.NotIn: "assert_not_in",
    ast.Lt: "assert_less",
    ast.LtE: "assert_less_equal",
    ast.Gt: "assert_greater",
    ast.GtE: "assert_greater_equal",
    "AssertTrue": "assert_true",
    "AssertFalse": "assert_false",
}

ASSERT_CALL_TMPL = "{indent}{function}({args})"
STATEMENTS = (
    (
        ast.Name,
        ast.Attribute,
        ast.Call,
        ast.Dict,
        ast.List,
        ast.Str,
        ast.Num,
        ast.UnaryOp,
    ),
)
if not PY2:
    STATEMENTS += (ast.NameConstant,)


class AssertToken(object):
    """
    Parse the AST for basic assertions.

    Handle the basic cases, for instance:

    - `assert X == Y` for `==` and other operators:
        Assert(
            test=Compare(
                left=Name(id='X', ctx=Load()),
                ops=[
                  Eq()
                ],
                comparators=[
                    Name(id='Y', ctx=Load())
                ]
            ),
            msg=None
        )

    - `assert X`:
        Assert(
            test=Name(
                id='X',
                ctx=Load()
            ),
            msg=None
        )

    - `assert not X`:
        Assert(
            test=UnaryOp(
                op=Not(),
                operand=Name(
                    id='X',
                    ctx=Load()
                )
            ),
            msg=None
        )

    """

    def __init__(self, atok, lines, token):
        self.atok = atok
        self.lines = lines
        self.token = token
        self.function_used = None

    @property
    def has_msg(self):
        return self.token.msg is not None

    @property
    def is_comparison(self):
        """
        Check the test uses `Compare` and that it compares only a single thing.

        For now, comparisons like A < B < C are too complicated so we ignore them
        """
        return (
            isinstance(self.token.test, ast.Compare) and len(self.token.test.ops) == 1
        )

    @property
    def single_statement(self):
        return isinstance(self.token.test, STATEMENTS)

    @property
    def is_not(self):
        return isinstance(self.token.test, ast.UnaryOp) and isinstance(
            self.token.test.op, ast.Not
        )

    @property
    def supported_test(self):
        return self.is_comparison or self.single_statement or self.is_not

    @property
    def has_replacement(self):
        return (
            self.single_statement
            or self.is_not
            or self.comparitor in ASSERT_REPLACEMENTS
        )

    @property
    def comparitor(self):
        return type(self.token.test.ops[0])

    @property
    def left(self):
        return self.atok.get_text(self.token.test.left)

    @property
    def right(self):
        return self.atok.get_text(self.token.test.comparators[0])

    @property
    def indent(self):
        line_start = self.lines.line_to_offset(self.token.lineno, 0)
        token_start = self.token.first_token.startpos
        return " " * (token_start - line_start)

    @property
    def original(self):
        return "{}{}".format(self.indent, self.atok.get_text(self.token))

    @property
    def extra_lines(self):
        return self.original.count("\n")

    @property
    def linenum(self):
        return self.token.lineno

    @property
    def replacement(self):
        if self.has_msg or not self.supported_test or not self.has_replacement:
            LOG.debug("Skipped: {}".format(self.original))
            LOG.debug(ast.dump(self.token))
            return self.original

        if self.is_comparison:
            self.function_used = ASSERT_REPLACEMENTS[self.comparitor]
            args = [self.left, self.right]
        elif self.is_not:
            self.function_used = ASSERT_REPLACEMENTS["AssertFalse"]
            args = [self.atok.get_text(self.token.test.operand)]
        elif self.single_statement:
            self.function_used = ASSERT_REPLACEMENTS["AssertTrue"]
            args = [self.atok.get_text(self.token.test)]
        else:
            assert False, "Unknown token, {}".format(ast.dump(self.token))

        return ASSERT_CALL_TMPL.format(
            indent=self.indent, function=self.function_used, args=", ".join(args)
        )


def fixed_text(filename):
    with open(filename, "r") as fh:
        text = fh.read()

    return fix_text(text, filename=filename)


def comment(text):
    comments = [
        t[1]
        for t in tokenize.generate_tokens(StringIO(text).readline)
        if t[0] == tokenize.COMMENT
    ]

    if comments:
        assert len(comments) == 1, text
        return "  " + comments[0]
    return ""


def fix_text(text, filename="<unknown>"):
    # Parse the test into an AST and wrap that with an AssertToken
    atok = asttokens.ASTTokens(text, parse=True, filename=filename)
    lines = asttokens.LineNumbers(text)
    assert_tokens = []
    for token in ast.walk(atok.tree):
        if isinstance(token, ast.Assert):
            assert_tokens.append(AssertToken(atok, lines, token))

    # Create a mpapping of zero indexed line numbers to their replacement
    line_replacements = {a.linenum - 1: a for a in assert_tokens}

    # Loop over the text making replacements
    skip_lines = 0
    fixed = []
    functions = set()
    for python_line, contents in enumerate(text.splitlines()):
        if skip_lines:
            skip_lines -= 1
            continue
        if python_line in line_replacements:
            a = line_replacements[python_line]

            try:
                fixed.append(a.replacement)
            except AttributeError:
                print(a.original)
                print(ast.dump(a.token))
                raise

            if a.function_used:
                functions.add(a.function_used)
                # If we made a replacement, include any comments on that line.
                try:
                    fixed[-1] += comment(contents)
                except tokenize.TokenError:
                    LOG.warning(
                        "If lines {}-{} have comments, they will be lost".format(
                            a.linenum, a.linenum + a.extra_lines
                        )
                    )
            skip_lines = a.extra_lines
        else:
            fixed.append(contents)

    fixed += [""]

    # Add an import statement at the top of the file (this may need fixing)
    if functions:
        import_line = "from assertions import {}".format(
            ", ".join(f for f in sorted(functions))
        )
        fixed = [import_line] + fixed + [""]

    return "\n".join(fixed)

from markdown import markdownlint


def rules():
    return [*markdownlint.rules()]

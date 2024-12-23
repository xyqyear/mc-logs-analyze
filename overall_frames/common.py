def escape_latex(text: str) -> str:
    """Escape special LaTeX characters"""
    chars = {
        "_": "\\_",
        "&": "\\&",
        "%": "\\%",
        "$": "\\$",
        "#": "\\#",
        "^": "\\^{}",
        "{": "\\{",
        "}": "\\}",
        "~": "\\~{}",
        "\\": "\\textbackslash{}",
    }
    return "".join(chars.get(c, c) for c in text)

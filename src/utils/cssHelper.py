import re


# Code from https://stackoverflow.com/questions/222581/python-script-for-minifying-css
# modified

regexCommentRule = r"/\*(.|\s)*?\*/"
regexAtRule = r"@[^{}]*?(;|\{[^}]*\})"
regexRuleSet = r"([^{}]+)\{([^}]*)\}"
cssBlockRule = "(\\s|%s|%s|%s)" % (regexCommentRule, regexAtRule, regexRuleSet)


def processCSS(css, cssWriter):
    output = []

    for block in re.findall(cssBlockRule, css):
        block = block[0]
        if block == "\n":
            output.append("\n")
            continue

        if re.match(regexCommentRule, block) or re.match(regexAtRule, block):
            output.append(block)
            continue

        # Remove comments in block before processing ruleset
        blockWithoutComment = re.sub(r"/\*[\s\S]*?\*/", "", block)
        match = re.match(regexRuleSet, blockWithoutComment)
        if match:
            selectorList = match[1]
            propertyList = match[2]

            # we don't need spaces around operators
            selectors = [
                re.sub(
                    r"(?<=[\[\(>+=])\s+|\s+(?=[=~^$*|>+\]\)])", r"", selector.strip()
                )
                for selector in selectorList.split(",")
            ]

            # order is important, but we still want to discard repetitions
            properties = []
            keys = set()
            for prop in re.findall("(.*?):(.*?)(;|$)", propertyList):
                key = prop[0].strip().lower()
                if key not in keys:
                    keys.add(key)
                properties.append((key, prop[1].strip()))

            # output rule if it contains any declarations
            output.append(block)
            continue

    return "".join(output)


def minifyCSS(css):
    def cssWriter(selectors, properties):
        # output rule if it contains any declarations
        if properties:
            return "%s{%s}" % (
                ",".join(selectors),
                "".join("%s:%s;" % (key, value) for key, value in properties),
            )
        else:
            return ""

    return processCSS(css, cssWriter)


def prettifyCSS(css):
    def cssWriter(selectors, properties):
        # output rule if it contains any declarations
        if properties:
            return "%s {\n%s}\n\n" % (
                ",\n".join(selectors),
                "".join("  %s: %s;\n" % (key, value) for key, value in properties),
            )
        else:
            return ""

    return processCSS(css, cssWriter)


if __name__ == "__main__":
    exampleCSS = """
/** Css styling of visible cloze on the back */

@import url("_editor_button_styles.css");

cloze2 {
  display: none;
}

.cloze cloze2_w {
  display: none;
}

.cloze cloze2 {
  display: inline;
}

.cloze {
    font-weight: bold;
    color: blue;
}
"""
    print(minifyCSS(exampleCSS))
    print("----------------------------")
    print(prettifyCSS(prettifyCSS(prettifyCSS(exampleCSS))))

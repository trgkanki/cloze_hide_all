import re
from ....utils.cssHelper import processCSS


def removeRuleContainingSelectorFromCSS(css, selector):
    def cssWriter(selectors, properties):
        if any(selector in target for target in selectors):
            return ""

        # output rule if it contains any declarations
        if not properties:
            return ""

        return "%s {\n%s}\n\n" % (
            ",\n".join(selectors),
            "".join("  %s: %s;\n" % (key, value) for key, value in properties),
        )

    return processCSS(css, cssWriter)


def removeCSSRuleContainingSelectorFromHtml(html, selector):
    def replacer(matchObj):
        return "<style>\n%s</style>" % removeRuleContainingSelectorFromCSS(
            matchObj[1], selector
        )

    return re.sub(r"<style>((.|\n)*?)</style>", replacer, html)


if __name__ == "__main__":
    h = """\
<style>
.cloze
.cloze
cloze2.reveal-
cloze2_w.reveal-cloze2  { display: inline; width: inherit; height: inherit; background-color: inherit; }
.cloze2-toggle { -webkit-appearance:none; display: block; max-width: 800px; font-size:1.3em; height: 2em; background-color: #ffffff; width: 100%; margin: 20px auto; }
.cloze2-toggle:active { background-color: #ffffaa; }
</style>
"""

    print(removeCSSRuleContainingSelectorFromHtml(h, "cloze2_w"))

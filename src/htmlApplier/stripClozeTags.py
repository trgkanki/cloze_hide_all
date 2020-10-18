import re


def stripClozeTags(html):
    # opening tag
    html = re.sub(r"<(cloze2_w|cloze2)[^>]*?class=(\"|')cz-\d+(\"|')[^>]*?>", "", html)

    # closing tag
    html = re.sub(r"</?(cz_hide|cloze2|cloze2_w)[^>]*?>", "", html)

    return html

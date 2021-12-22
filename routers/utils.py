from lxml import html as html_parser


# A HTML parser for decoding HTML entities like '&#x27' using lxml.
def decode_html_entities(html: str) -> str:
    """Decode HTML entities like `&#x27` using lxml.
    
    Parameters:
        html (`str`): The HTML to decode.
    
    Returns:
        `str`: The decoded HTML.
    """
    return html_parser.fromstring(html).text_content()

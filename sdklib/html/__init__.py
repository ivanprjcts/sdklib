from sdklib.compat import html_lxml

if html_lxml:
    from sdklib.html.html import HTMLxml as HTML
else:
    from sdklib.html.html import HTML5lib as HTML


__all__ = [
    'HTML'
]

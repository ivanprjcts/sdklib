from sdklib.compat import html_lxml

if html_lxml:
    from sdklib.html.base import HTMLxml as HTML
else:
    from sdklib.html.base import HTML5lib as HTML


__all__ = [
    'HTML'
]

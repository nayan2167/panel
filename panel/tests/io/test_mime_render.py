import json
import pathlib

from bokeh.models import Slider

from panel.io.mime_render import UNDEFINED, exec_with_return, format_mime
from panel.widgets import FloatSlider


class HTML:
    def __init__(self, html):
        self.html = html
    def _repr_html_(self):
        return self.html

class Javascript:
    def __init__(self, js):
        self.js = js
    def _repr_javascript_(self):
        return self.js

class Markdown:
    def __init__(self, md):
        self.md = md
    def _repr_markdown_(self):
        return self.md

class PNG:
    def _repr_png_(self):
        with open(pathlib.Path(__file__).parent.parent / 'test_data' / 'logo.png', 'rb') as f:
            return f.read()


def test_exec_with_return_multi_line():
    assert exec_with_return('a = 1\nb = 2\na + b') == 3

def test_exec_with_return_no_return():
    assert exec_with_return('a = 1') is UNDEFINED

def test_exec_with_return_None():
    assert exec_with_return('None') is None

def test_format_mime_None():
    assert format_mime(None) == ('None', 'text/plain')

def test_format_mime_str():
    assert format_mime('foo') == ('foo', 'text/plain')

def test_format_mime_str_with_escapes():
    assert format_mime('foo>bar') == ('foo&gt;bar', 'text/plain')

def test_format_mime_repr_html():
    assert format_mime(HTML('<b>BOLD</b>')) == ('<b>BOLD</b>', 'text/html')

def test_format_mime_repr_javascript():
    assert format_mime(Javascript('1+1')) == ('<script>1+1</script>', 'text/html')

def test_format_mime_repr_markdown():
    assert format_mime(Markdown('**BOLD**')) == ('<p><strong>BOLD</strong></p>', 'text/html')

def test_format_mime_repr_png():
    img, mime_type = format_mime(PNG())
    assert mime_type == 'text/html'
    assert img.startswith('<img src="data:image/png')

def test_format_mime_panel_obj():
    model_json, mime_type = format_mime(FloatSlider())
    assert mime_type == 'application/bokeh'
    assert 'doc' in json.loads(model_json)

def test_format_mime_bokeh_obj():
    model_json, mime_type = format_mime(Slider())
    assert mime_type == 'application/bokeh'
    assert 'doc' in json.loads(model_json)
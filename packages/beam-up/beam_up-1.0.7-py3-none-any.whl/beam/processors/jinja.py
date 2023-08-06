from .base import BaseProcessor

import markdown2
import textwrap

from jinja2 import Environment, FileSystemLoader, ChoiceLoader, DictLoader

try:
    from pygments import highlight
    from pygments.styles import get_style_by_name
    from pygments.lexers import get_lexer_by_name
    from pygments.formatters import HtmlFormatter
    with_pygments = True
except ImportError:
    with_pygments = False

try:
    from bs4 import BeautifulSoup as bs
    with_bs = True
except ImportError:
    with_bs = False

class JinjaProcessor(BaseProcessor):

    def highlight_styles(self, code, style_name=None):
        if style_name is None:
            style_name = self.site.config.get('pygments', {}).get('style', 'monokai')
        style = get_style_by_name(style_name)
        return '<style type="text/css">{}</style>'.format(HtmlFormatter(style=style).get_style_defs('.highlight .{}'.format(style_name)))

    def highlight(self, code, language='python', style_name=None, strip=True, deindent=True):
        if style_name is None:
            style_name = self.site.config.get('pygments', {}).get('style', 'monokai')
        lexer = get_lexer_by_name(language)
        style = get_style_by_name(style_name)
        if deindent:
            code = textwrap.dedent(code)
        if strip:
            code = code.strip()
        return highlight(code, lexer, HtmlFormatter(style=style, cssclass='{}'.format(style_name)))

    def markdown(self, text):
        result = markdown2.markdown(text, extras=['footnotes', 'fenced-code-blocks'])
        return result

    def translate(self, key, *args, **kwargs):
        result = super().translate(key, *args, **kwargs)
        translate_hint = self.site.config.get('translate-hint')
        if translate_hint:
            return translate_hint.format(value=result, key=key, args=args, kwargs=kwargs)
        return result

    def get_jinja_env(self, input):
        dict_loader = DictLoader({'input' : input})
        choice_loader = ChoiceLoader([dict_loader, FileSystemLoader('{}/templates'.format(self.site.src_path)), FileSystemLoader(self.site.src_path)])
        env = Environment(loader=choice_loader)

        # we add some useful filters
        env.filters['href'] = self.href
        env.filters['full_href'] = self.full_href
        env.filters['file'] = self.file
        env.filters['markdown'] = self.markdown

        if with_pygments:
            env.filters['highlight'] = self.highlight
            env.filters['highlight_styles'] = self.highlight_styles
        env.filters['translate'] = self.translate
        for filters in self.site.addons['jinja-filters']:
            for name, f in filters:
                env.filters[name] = f
        return env

    def process(self, input, vars):
        env = self.get_jinja_env(input)
        template = env.get_template('input')
        result = template.render(**vars)
        if with_bs and False:
            soup=bs(result, "html.parser")
            return soup.prettify()
        return result
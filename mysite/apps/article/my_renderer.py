import mistune


class HightlightRenderer(mistune.Renderer):
    """
    customize block code renderer
    """

    def block_code(self, code, lang):
        if lang:
            return '<pre><code class="%s">%s</code></pre>' % (lang, mistune.escape(code))
        return '<pre><code class="plaintext">%s</code></pre>' % mistune.escape(code)

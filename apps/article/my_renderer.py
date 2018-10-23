import mistune


class HightlightRenderer(mistune.Renderer):
    """
    customize block code renderer
    """

    def block_code(self, code, lang):
        if lang:
            return '<pre class="block-code"><code>%s</code></pre>' % \
                mistune.escape(code)
        return '<pre><code>%s</code></pre>' % mistune.escape(code)

import mistune


class HightlightRenderer(mistune.Renderer):
    """
    customize block code renderer
    """

    def block_code(self, code, lang):
        if lang:
            return '\n<pre class="block-code"><code>%s</code></pre>\n' % \
                mistune.escape(code)
        return '\n<pre><code>%s</code></pre>\n' % mistune.escape(code)

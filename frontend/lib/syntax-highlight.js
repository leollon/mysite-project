// lib/with-post.js

import React from 'react';
import marked from 'marked';
import dynamic from 'next/dynamic';

marked.setOptions({
  gfm: true,
  tables: true,
  breaks: true
});

const Highlight = dynamic(() => import('react-highlight'));


export default function SyntaxHighlight(options) {

  function renderMarkdown() {
    if (/```/.test(options.content) || /~~~/.test(options.content)) {
      return (
        <main>
          <Highlight innerHTML>{marked(options.content)}</Highlight>
        </main>
      )
    }
    return (
      <main dangerouslySetInnerHTML={{__html: marked(options.content)}}></main>
    )
  }

  return (
    renderMarkdown()
  )
}

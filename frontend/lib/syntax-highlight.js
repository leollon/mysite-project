// lib/syntax-highlight.js

import React from 'react';
import marked from 'marked';
import dynamic from 'next/dynamic';
import insane from 'insane';

marked.setOptions({
  gfm: true,
  tables: true,
  breaks: true
});

const Highlight = dynamic(() => import('react-highlight'));


export default function SyntaxHighlight(options) {

  if (/```/.test(options.content) || /~~~/.test(options.content)) {
    return (
      <main>
        <Highlight innerHTML>{insane(marked(options.content))}</Highlight>
      </main>
    )
  }
  return (
    <main dangerouslySetInnerHTML={{__html: insane(marked(options.content))}} />
  )
}

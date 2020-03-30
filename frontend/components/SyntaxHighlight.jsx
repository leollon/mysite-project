// components/SyntaxHighlight.jsx

import React from 'react'
import marked from 'marked'
import dynamic from 'next/dynamic'
import insane from 'insane'

marked.setOptions({
    gfm: true,
    tables: true,
    breaks: true,
})

const Highlight = dynamic(() => import('react-highlight'))

export default function SyntaxHighlight(options) {
    const html = insane(marked(options.content))

    if (/```/.test(options.content) || /~~~/.test(options.content)) {
        return <Highlight innerHTML={true}>{html}</Highlight>
    }

    return <div dangerouslySetInnerHTML={{ __html: html }} />
}

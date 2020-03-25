// pages/about/index.js

import React from 'react'

import about from '../../data/about.json'

import Layout from '../../components/Layout'
import SyntaxHighlight from '../../components/SyntaxHighlight'


export default function About() {

  return (
    <Layout
      title={about.title}
      description={about.title}
    >
      <article className="article-body">
        <SyntaxHighlight content={about.article_body} />
        <p className="text-muted empty">-- EOF --</p>
      </article>
    </Layout>);
}
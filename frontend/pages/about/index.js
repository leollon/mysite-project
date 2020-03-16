// pages/about/index.js

import React from 'react';

import about from '../../data/about.json';
import Layout from '../../components/layout';
import SyntaxHighlight from '../../lib/syntax-highlight';


export default function About() {

  return (
    <Layout
      title={about.title}
      description={about.title}
    >
      <article className="article-body">
        <SyntaxHighlight content={about.article_body} />
        <p className="text-muted" id="eof">-- EOF --</p>
      </article>
    </Layout>);
}
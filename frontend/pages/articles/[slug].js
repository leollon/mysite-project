// pages/articles/[slug].js

import React from 'react';
import PropTypes from 'prop-types';
import fetch from 'isomorphic-unfetch';
import SyntaxHighlight from '../../lib/syntax-highlight';


import Layout from '../../components/layout';
import Comments from '../../components/comment';

const API_URL = 'http://web:8000/api/v1/articles/';


const Post = props => {
  return (
    <Layout
      title={props.article.title}
      description={props.article.title}
    >
      <article className="article-body">
        <SyntaxHighlight
          content={props.article.article_body} />

        <p className="text-muted" id="eof">-- EOF --</p>
        <Comments
          id={props.article.id}
          slug={props.article.slug}
          comments={props.comments}
          statistics={props.article.comment_statistics} />
        <script src="/static/js/blog.js" />
      </article>
    </Layout>
  );
}


Post.propTypes = {
  article: PropTypes.object.isRequired,
  comments: PropTypes.object.isRequired,
}


Post.getInitialProps = async function (context) {
  const query = context.query;
  const slug = query.slug;
  const cursor = query.cur ? '?cur=' + query.cur : '';
  
  const articleResponse = await fetch(`${API_URL}${slug}`);
  const article = await articleResponse.json();

  const commentsResponse = await fetch(`${API_URL}${slug}/comments${cursor}`);
  const comments = await commentsResponse.json();

  return { article, comments };
}

export default Post;

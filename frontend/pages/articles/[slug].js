// pages/articles/[slug].js

import React from 'react';
import PropTypes from 'prop-types'
import Markdown from 'react-markdown';
import fetch from 'isomorphic-unfetch';
import Layout from '../../components/layout';
import Comments from '../../components/comment';

const API_URL = 'http://web:8000/api/v1/articles/';


const Post = props => {
  return (
    <Layout
      title={props.article.title}
      description={props.article.article_body}
    >
      <h1>{props.article.title}</h1>
      <Markdown source={props.article.article_body} />
      <Comments comments={props.comments} statistics={props.article.comment_statistics} />
      <script src="/static/js/blog.js" />
    </Layout>
  );
}


Post.propTypes = {
  article: PropTypes.object.isRequired,
}


Post.getInitialProps = async function (context) {
  const query = context.query;
  const slug = query.slug;
  const cursor = query.cur ? '?cur=' + query.cur : '';
  
  const articleResponse = await fetch(`${API_URL}${slug}/`);
  const article = await articleResponse.json();

  const commentsResponse = await fetch(`${API_URL}${slug}/comments/${cursor}`);
  const comments = await commentsResponse.json();

  return { article, comments };
}

export default Post;

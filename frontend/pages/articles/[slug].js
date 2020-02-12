// pages/articles/[slug].js

import React from 'react';
import PropTypes from 'prop-types'
import Markdown from 'react-markdown';
import fetch from 'isomorphic-unfetch';
import Layout from '../../components/layout';

const API_URL = 'http://web:8000/api/v1/articles/';


const Post = props => (
  <Layout>
    <h1>{props.article.title}</h1>
    <Markdown source={props.article.article_body} />
  </Layout>
)


Post.propTypes = {
    article: PropTypes.object.isRequired,
    'article.title': PropTypes.string.isRequired,
    'article.article_body': PropTypes.string.isRequired
}


Post.getInitialProps = async function (context) {
    const { slug } = context.query;
    const res = await fetch(`${API_URL}${slug}/`);
    const article = await res.json();

    return { article };
}

export default Post;

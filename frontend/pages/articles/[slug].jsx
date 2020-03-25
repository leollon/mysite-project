// pages/articles/[slug].js

import React from 'react'
import PropTypes from 'prop-types'

import Error from '../_error'
import fetcher from '../../lib/fetch'
import Layout from '../../components/Layout'
import Comments from '../../components/Comment'
import SyntaxHighlight from '../../components/SyntaxHighlight'

const API_URL = 'http://web:8000/api/v1/articles/'


const Post = props => {
  if (props.errorCode) {
    return (<Error errorCode={props.errorCode} />);
  }
  return (
    <Layout
      title={props.article.title}
      description={props.article.title}
    >
      <article className="article-body">
        <SyntaxHighlight
          content={props.article.article_body}
        />

        <p className="text-muted empty">-- EOF --</p>
        <Comments
          id={props.article.id}
          slug={props.article.slug}
          comments={props.comments}
          statistics={props.article.comment_statistics}
        />
        <script src="/static/js/blog.js" />
      </article>
    </Layout>
  );
}


Post.propTypes = {
  errorCode: PropTypes.any.isRequired,
  article: PropTypes.object.isRequired,
  comments: PropTypes.object.isRequired,
}


Post.getInitialProps = async function (context) {
  const query = context.query;
  const slug = query.slug;
  const cursor = query.cur ? '?cur=' + query.cur : '';
  let errorCode = false,
    article = {},
    comments = {};
  
  article = await fetcher(`${API_URL}${slug}`)
    .catch((error) => {
      if (error.name === "FetchError") {
        errorCode = "500 Server Error";
      } else if(error.name === "AbortError") {
        errorCode = "Request Cancelled"
      } else {
        errorCode = error.message;
      }
    });

  if (!errorCode) {
    comments = await fetcher(`${API_URL}${article.slug}/comments${cursor}`)
      .catch((error) => {
        if (error.name === "FetchError") {
          errorCode = "500 Server Error";
        } else if(error.name === "AbortError") {
          errorCode = "Request Cancelled"
        } else {
          errorCode = error.message;
        }
      });
  }
  return { errorCode, article, comments, };
}

export default Post;

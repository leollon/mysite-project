// pages/tags/[name].js

import React from 'react';
import PropTypes from 'prop-types';

import Error from '../_error';
import fetcher from '../../lib/fetch';
import Layout from '../../components/Layout';
import ArticleList from '../../components/Post';
import PageList from '../../components/Pagination';

const API_URL = 'http://web:8000/api/v1/tags/';


export default function taggedArticles({ articles, name, errorCode }) {

  if (errorCode) {
    return (<Error errorCode={errorCode} />);
  }
  return (
    <Layout
      title={name}
      description={name}
    >
      <ArticleList articles={articles.results} />
      <PageList links={articles.links} />
    </Layout>
  );
}

taggedArticles.propTypes = {
  articles: PropTypes.array.isRequired,
  name: PropTypes.string.isRequired,
  errorCode: PropTypes.any.isRequired,
}

taggedArticles.getInitialProps = async function (context) {
  const { name, cur } = context.query;
  let errorCode = false;
  const articles = await fetcher(`${API_URL}${name}/articles/${cur ? '?cur=' + cur : ''}`)
    .catch((error) => {
      if (error.name === "FetchError") {
        errorCode = "500 Server Error";
      } else if(error.name === "AbortError") {
        errorCode = "Request Cancelled"
      } else {
        errorCode = error.message;
      }
    });
  return { errorCode, articles, name, };
}

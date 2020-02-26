// pages/tags/[name].js

import React from 'react';
import Error from '../_error';

import fetcher from '../../lib/fetch';
import Layout from '../../components/layout';
import ArticleList from '../../components/post';
import PageList from '../../components/pagination';

const API_URL = 'http://web:8000/api/v1/tags/';


export default function taggedArticles({ data, name, errorCode }) {

  if (errorCode) {
    return <Error statusCode={errorCode} />
  }
  return (
    <Layout
      title={name}
      description={name}
    >
      <ArticleList articles={data.results} />
      <PageList links={data.links} />
    </Layout>
  );
}


taggedArticles.getInitialProps = async function (context) {
  const { name, cur } = context.query;
  let errorCode = false;
  const data = await fetcher(`${API_URL}${name}/article${cur ? '?cur=' + cur : ''}`)
    .then((response) => response.json())
    .catch((error) => {
      errorCode = error.message;
    });
  return { data, name, errorCode};
}

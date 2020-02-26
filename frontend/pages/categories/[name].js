// pages/categories/[name].js

import React from 'react';
import fetcher from '../../lib/fetch';
import Layout from '../../components/layout';
import ArticleList from '../../components/post';
import PageList from '../../components/pagination';

const API_URL = 'http://web:8000/api/v1/categories/';


export default function CategorizedArticles({data, name}) {

  return (
    <Layout
      title={name}
      description='categories'
    >
      <ArticleList
        articles={data.results}
        category_name={name}
        statistics={data.article_statistics} />
      <PageList links={data.links} />
    </Layout>
  );
}

CategorizedArticles.getInitialProps = async (context) => {
  const { name, cur } = context.query;
  const data = await fetcher(`${API_URL}${name}/articles${cur ? '?cur=' + cur : ''}`);
  return { data, name };
}
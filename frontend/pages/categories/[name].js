// pages/categories/[name].js

import React from 'react';
import useSWR from 'swr';
import { useRouter } from 'next/router';
import fetcher from '../../utils/fetchData';
import Layout from '../../components/layout';
import ArticleList from '../../components/post';
import PageList from '../../components/pagination';

const API_URL = 'http://dev.django.com/api/v1/categories/';


export default function CategorizedArticles() {
  const router = useRouter();
  const { name } = router.query;

  const { data, error } = useSWR(
    `${API_URL}${name}/articles${router.query.cur ? '?cur=' + router.query.cur : ''}`,
    fetcher
  );

  if (!data) { return <div>Loading...</div>; }
  if (error) { return <div>error</div> }
  
  return (
    <Layout
      title={name}
      description='categories'
    >
      <ArticleList articles={data.results} category_name={name} statistics={data.article_statistics}/>
      <PageList links={data.links} />
    </Layout>
  )
}

// pages/tags/[name].js

import React from 'react';
import useSWR from 'swr';
import { useRouter } from 'next/router';

import fetcher from '../../utils/fetchData';
import Layout from '../../components/layout';
import ArticleList from '../../components/post';
import PageList from '../../components/pagination';

const API_URL = 'http://dev.django.com/api/v1/tags/';


export default function TaggedArticles() {
  const router = useRouter();
  const { name } = router.query;

  const { data, error } = useSWR(
    `${API_URL}${name}/${router.query.cur ? '?cur=' + router.query.cur : ''}`,
    fetcher
  )
  
  if (!data) { return <div>Loading...</div>; }
  if (error) { return <div>Error</div>; }

  return (
    <Layout>
      <ArticleList articles={data.results} />
      <PageList links={data.links} />
    </Layout>
  );
}

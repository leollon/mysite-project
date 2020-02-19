// pages/index.js

import React from 'react';
import useSWR from 'swr';
import { useRouter } from 'next/router';

import fetcher from '../utils/fetchData';
import Layout from './../components/layout';
import ArticleList from '../components/post';
import PageList from '../components/pagination';

const API_URL = 'http://dev.django.com/api/v1/articles/'


export default function Index() {
  const { query } = useRouter();

  let { data, error } = useSWR(
    `${API_URL}${query.cur ? '?cur=' + query.cur : ''}`,
    fetcher
  );

  if (!data) { return <div>Loading...</div> }
  if (error) { return <div>error</div> }
  
  return (
    <Layout
      title="I'm 🤔"
      description="Leollon の blog powered by Django and Bootstrap"
    >
      <ArticleList articles={data.results} />
      <PageList links={data.links} />
    </Layout>
  );
}

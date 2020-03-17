// pages/index.js

import React from 'react';
import useSWR from 'swr';
import { useRouter } from 'next/router';

import Error from './_error';
import fetcher from '../lib/fetch';
import Layout from './../components/layout';
import ArticleList from '../components/post';
import PageList from '../components/pagination';

const API_URL = 'http://dev.django.com/api/v1/articles/'


export default function Index() {
  const router = useRouter();
  const query = router.query;

  let { data, error } = useSWR(
    `${API_URL}${query.cur ? '?cur=' + query.cur : ''}`,
    fetcher
  );

  if (error) { return (<Error errorCode={error.message} />); }
  if (!data) {
    return (
      <Layout title={'Loading'} description={'Loading'}>
        <div className="empty"><h1>Loading</h1></div>
      </Layout>);
  }

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

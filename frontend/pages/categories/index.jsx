// pages/categories/index.js

import React from 'react';
import useSWR from 'swr';

import Error from '../_error';
import fetcher from '../../lib/fetch';
import Layout from '../../components/Layout';
import CategoryList from '../../components/Category';


const API_URL = 'http://dev.django.com/api/v1/categories';


export default function Categories() {
  let { data, error } = useSWR(`${API_URL}`, fetcher);

  if (error) { return (<Error errorCode={error.message} />); }
  if (!data) {
    return (
      <Layout title={'Loading'} description={'Loading'}>
        <div className="empty"><h1>Loading</h1></div>
      </Layout>);
  }

  return (
    <Layout
      title="categories"
      description="categories"
    >
      <CategoryList categories={data} />
    </Layout>
  );
}

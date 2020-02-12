// pages/categories/index.js

import React from 'react';
import useSWR from 'swr';

import fetcher from '../../utils/fetchData';
import Layout from '../../components/layout';
import CategoryList from '../../components/category';


const API_URL = 'http://dev.django.com/api/v1/categories/';


export default function Categories() {
  let { data, error } = useSWR(`${API_URL}`, fetcher);

  if (!data) { return <div>Loading...</div> }
  if (error) { return <div>error</div> }

  return (
    <Layout>
        <div className="center">
          <CategoryList categories={data} />
        </div>
    </Layout>
  );
}

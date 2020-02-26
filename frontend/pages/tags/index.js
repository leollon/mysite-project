// pages/tags/index.js

import React from 'react';
import useSWR from 'swr';

import fetcher from '../../lib/fetch';
import TagList from '../../components/tag';
import Layout from '../../components/layout';

const API_URL = 'http://dev.django.com/api/v1/tags';


export default function Tags() {
  let { data, error } = useSWR(`${API_URL}`, fetcher);

  if (!data) { return <div>Loading...</div>; }
  if (error) { return <div>Error</div>; }

  return (
    <Layout
      title='tags'
      description='tags'
    >
      <TagList tags={data.tags} count={data.count} />
    </Layout>
  )
}

// pages/tags/index.js

import React from 'react';
import useSWR from 'swr';

import Error from '../_error';
import fetcher from '../../lib/fetch';
import TagList from '../../components/Tag';
import Layout from '../../components/Layout';

const API_URL = 'http://dev.django.com/api/v1/tags';


export default function Tags() {
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
      title="tags"
      description="tags"
    >
      <TagList tags={data.tags} count={data.count} />
    </Layout>
  )
}

// pages/index.js

import useSWR from 'swr';
import { useRouter } from 'next/router';

import fetcher from '../utils/fetchData';
import Layout from './../components/Layout';
import ArticleList from '../components/Post';
import PageList from '../components/Pagination';

const API_URL = 'http://dev.django.com/api/v1/articles/'


export default function Index() {
    const { query } = useRouter();

    let { data, error } = useSWR(
        `${API_URL}${query.cur ? '?cur=' + query.cur : ''}`,
        fetcher
    );

    if (!data) { return <div>Loading...</div> };
    if (error) { return <div>error</div> };
    
    return (
        <Layout>
            <ArticleList articles={data.results} />
            <PageList links={data.links} />
        </Layout>
    );
};

// pages/tags/index.js

import useSWR from 'swr';

import fetcher from '../../utils/helpers';
import TagList from '../../components/Tag';
import Layout from '../../components/Layout';

const API_URL = 'http://dev.django.com/api/v1/tags/';


export default function Tags() {
    let { data, error } = useSWR(`${API_URL}`, fetcher);

    if (!data) { return <div>Loading...</div>; }
    if (error) { return <div>Error</div>; }

    return (
        <Layout>
            <TagList tags={data.tags} count={data.count} />
        </Layout>
    )
}
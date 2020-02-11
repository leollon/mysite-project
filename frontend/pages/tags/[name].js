// pages/tags/[name].js
import useSWR from 'swr';
import { useRouter } from 'next/router';

import fetcher from '../../utils/helpers';
import Layout from '../../components/Layout';
import ArticleList from '../../components/Post';
import PageList from '../../components/Pagination';

const API_URL = 'http://dev.django.com/api/v1/tags/';

export default TaggedArticles = () => {
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
};

import useSWR from 'swr';
import fetch from 'isomorphic-unfetch';
import Layout from './../components/Layout';
import ArticleList from '../components/Post';
import { useRouter } from 'next/router';
import PageList from '../components/Pagination';

const API_URL = 'http://dev.django.com/api/v1/articles/'

function checkStatus(response) {
    if (response.ok) {
        return response;
    } else {
        var error = new Error(response.statusText);
        error.response = response;
        return Promise.reject(error);
    }
};

async function fetcher(url) {
    return fetch(url)
        .then(checkStatus)
        .then(r => r.json());
};

export default function Index() {
    const { query } = useRouter()

    let { data, error } = useSWR(`${API_URL}${query.cur ? '?cur=' + query.cur : ''}`, fetcher)
    if (!data) { data = { results: [{ title: 'loading...', slug: 'slug', }] , links: {next: null, previous: null}, } };
    if (error) { data = { results: [{ title: "Ocurring errors.", slug: 'error1' }, { title: "Ocurring errors.", slug: 'error2' },] }};
    return (
        <Layout>
            <div className="center">
                <ArticleList articles={data.results} />
                <PageList links={data.links} />
            </div>
        </Layout>
    );
};

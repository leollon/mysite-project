import useSWR from 'swr';
import fetch from 'isomorphic-unfetch';
import { useRouter } from 'next/router';
import ArticleList from '../components/Post';

function checkStatus(response) {
    if (response.ok) {
        return response;
    } else {
        var error = new Error(response.statusText);
        error.response = response;
        return Promise.reject(error);
    }
};

let fetcher = url => {
    return fetch(url)
        .then(checkStatus)
        .then(r => r.json());
};

export default function Index() {

    const { query } = useRouter()
    const url = `http://dev.django.com/api/v1/articles/${query.cur ? '?cur=' + query.cur : ''}`;

    let { data, error } = useSWR(url, fetcher)

    if (error) { data = { results: [{ title: "Ocurring errors.", slug: 'error1' }, { title: "Ocurring errors.", slug: 'error2' },] }};
    if (!data) { data = { results: [{ title: 'hello world', slug: 'slug', }] } };

    return (
        <div className="center">
            <ArticleList articles={data.results} />
        </div>
    );
};

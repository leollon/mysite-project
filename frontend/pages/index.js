import useSWR from 'swr';
import { useRouter } from 'next/router';
// import Link from 'next/link';
import List from '../components/PostList';


let fetcher = url => {
    return fetch(url).then(r => r.json());
};


export default function Index() {

    const { query } = useRouter()
    const url = `http://dev.django.com/api/v1/articles/${query.cur ? '?cur=' + query.cur : ''}`;

    let { data, error } = useSWR(url, fetcher)

    if (error) { data = { results: [{ title: "Ocurring errors.", slug: 'error1' }, { title: "Ocurring errors.", slug: 'error2' },] }};
    if (!data) { data = { results: [{ title: 'hello world', slug: 'slug', }] } };

    return (
        <main className="center">
            <List articles={data.results} />
        </main>
    );
};

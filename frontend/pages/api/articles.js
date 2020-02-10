import useSWR from 'swr';
import fetch from 'isomorphic-unfetch';
import { useRouter } from 'next/router';


const api_url = 'http://dev.django.com/api/v1/articles/'

const fetcher = url => (
    fetch(url).then(r => r.json())
)

export default (req, res) => {

    const { query } = useRouter();

    const { data, error } = useSWR(
        `http://dev.django.com/api/v1/articles/${query.cur ? '?cur=' + query.cur : ''}`,
        fetcher
    );
    return res.status(200).json(data);
}
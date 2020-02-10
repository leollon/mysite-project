import Markdown from 'react-markdown';
import fetch from 'isomorphic-unfetch';
import Layout from '../../components/Layout';

const API_URL = 'http://web:8000/api/v1/articles/';

const Post = props => (
    <Layout>
        <h1>{props.article.title}</h1>
        <Markdown source={props.article.article_body} />
    </Layout>
);

Post.getInitialProps = async function (context) {
    const { slug } = context.query;
    const res = await fetch(`${API_URL}${slug}/`);
    const article = await res.json();

    return { article };
};

export default Post;

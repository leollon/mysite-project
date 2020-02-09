import Markdown from 'react-markdown';
import fetch from 'isomorphic-unfetch';
import Layout from '../../components/Layout';


const Post = props => (
    <Layout>
        <h1>{props.article.title}</h1>
        <Markdown source={props.article.article_body} />
    </Layout>
);

Post.getInitialProps = async function (context) {
    const { slug } = context.query;
    const res = await fetch(`http://dev.django.com/api/v1/articles/${slug}/`);
    const article = await res.json();

    console.log(`Fetched article: ${article.title}`);
    return { article };
};

export default Post;

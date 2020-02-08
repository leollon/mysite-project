import Link from 'next/link';
import Layout from './Layout';

export default function List(props) {
    console.log(props.articles);
    return (
        <Layout>
            <h1>My blog</h1>
            <ul>
                {props.articles.map(article => (
                    <li key={article.slug}>
                        <Link href="/article/[slug]" as={`/articles/${article.slug}`}>
                            <a>{article.title}</a>
                        </Link>
                    </li>
                ))}
            </ul>
        </Layout>
    );
};
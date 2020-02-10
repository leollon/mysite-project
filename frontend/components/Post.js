// components/Post.js

export default function ArticleList(props) {
    return (
        <>
            <h1>My blog</h1>
            <ul>
                {props.articles.map(article => (
                    <li key={article.title}>
                        <a href={`/articles/${article.slug}`}>{article.title}</a>
                    </li>
                    )
                )}
            </ul>
        </>
    );
};
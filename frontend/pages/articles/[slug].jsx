// pages/articles/[slug].js

import React from 'react';
import PropTypes from 'prop-types';

import Error from '../_error';
import fetcher from '../../lib/fetch';
import handler from '../../lib/errorHandler';
import Layout from '../../components/Layout';
import Comments from '../../components/Comment';
import SyntaxHighlight from '../../components/SyntaxHighlight';

const URL = process.env.apiHost + '/articles/';

const Post = (props) => {
    if (props.errorCode) {
        return <Error errorCode={props.errorCode} />;
    }
    return (
        <Layout title={props.article.title} description={props.article.title}>
            <article className="article-body">
                <SyntaxHighlight content={props.article.article_body} />

                <p className="text-muted empty">-- EOF --</p>
                <Comments
                    id={props.article.id}
                    slug={props.article.slug}
                    comments={props.comments}
                    statistics={props.article.comment_statistics}
                />
                <script src="/assets/js/blog.min.js" />
            </article>
        </Layout>
    );
};

Post.propTypes = {
    errorCode: PropTypes.any.isRequired,
    article: PropTypes.object.isRequired,
    comments: PropTypes.object.isRequired,
};

Post.getInitialProps = async function (context) {
    const query = context.query;
    const slug = query.slug;
    const cursor = query.cur ? '?cur=' + query.cur : '';
    let errorCode = false,
        article = {},
        comments = {};

    article = await fetcher(`${URL}${slug}`).catch((error) => {
        errorCode = handler(error);
    });

    if (!errorCode) {
        comments = await fetcher(
            `${URL}${article.slug}/comments${cursor}`
        ).catch((error) => {
            errorCode = handler(error);
        });
    }
    return { errorCode, article, comments };
};

export default Post;

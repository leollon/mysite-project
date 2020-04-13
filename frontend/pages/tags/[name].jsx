// pages/tags/[name].js

import React from 'react';
import PropTypes from 'prop-types';

import Error from '../_error';
import fetcher from '../../lib/fetch';
import handler from '../../lib/errorHandler';
import Layout from '../../components/Layout';
import ArticleList from '../../components/Post';
import PageList from '../../components/Pagination';

const URL = process.env.apiHost + '/tags/';

export default function taggedArticles({ articles, name, errorCode }) {
    if (errorCode) {
        return <Error errorCode={errorCode} />;
    }
    return (
        <Layout title={name} description={name}>
            <ArticleList articles={articles.results} />
            <PageList links={articles.links} />
        </Layout>
    );
}

taggedArticles.propTypes = {
    articles: PropTypes.object.isRequired,
    name: PropTypes.string.isRequired,
    errorCode: PropTypes.any.isRequired,
};

taggedArticles.getInitialProps = async function (context) {
    const { name, cur } = context.query;
    let errorCode = false;
    const articles = await fetcher(
        `${URL}${name}/articles/${cur ? '?cur=' + cur : ''}`
    ).catch((error) => {
        errorCode = handler(error);
    });
    return { errorCode, articles, name };
};

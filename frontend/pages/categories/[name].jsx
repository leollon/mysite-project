// pages/categories/[name].js

import React from 'react';
import PropTypes from 'prop-types';

import Error from '../_error';
import fetcher from '../../lib/fetch';
import handler from '../../lib/errorHandler';
import Layout from '../../components/Layout';
import ArticleList from '../../components/Post';
import Summary from '../../components/SubHeader';
import PageList from '../../components/Pagination';

const URL = process.env.apiHost + '/categories/';

export default function CategorizedArticles({ articles, name, errorCode }) {
    if (errorCode) {
        return <Error errorCode={errorCode} />;
    }

    return (
        <Layout title={name} description="categories">
            <Summary
                category_name={name}
                statistics={articles.article_statistics}
            />
            <ArticleList articles={articles.results} />
            <PageList links={articles.links} />
        </Layout>
    );
}

CategorizedArticles.propTypes = {
    articles: PropTypes.object.isRequired,
    name: PropTypes.string.isRequired,
    errorCode: PropTypes.any.isRequired,
};

CategorizedArticles.getInitialProps = async (context) => {
    let errorCode = false;
    const { name, cur } = context.query;
    const articles = await fetcher(
        `${URL}${name}/articles${cur ? '?cur=' + cur : ''}`
    ).catch((error) => {
        errorCode = handler(error);
    });
    return { errorCode, articles, name };
};

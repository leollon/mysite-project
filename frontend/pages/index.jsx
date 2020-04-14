// pages/index.js

import React from 'react';
import PropTypes from 'prop-types';

import Error from './_error';
import fetcher from '../lib/fetch';
import handler from '../lib/errorHandler';
import Layout from '../components/Layout';
import ArticleList from '../components/Post';
import PageList from '../components/Pagination';

const URL = process.env.apiHost + '/articles/';

export default function Index({ data, errorCode }) {
    if (errorCode) {
        return <Error errorCode={errorCode} />;
    }

    return (
        <Layout
            title="Leollon's web log"
            description="Leollon の web log. About Linux，c，c++，Python, Django, GoLang."
        >
            <ArticleList articles={data.results} />
            <PageList links={data.links} />
        </Layout>
    );
}

Index.propTypes = {
    data: PropTypes.object.isRequired,
    errorCode: PropTypes.any.isRequired,
};

Index.getInitialProps = async function (context) {
    const { cur } = context.query;
    let errorCode = false;
    const data = await fetcher(`${URL}${cur ? '?cur=' + cur : ''}`).catch(
        (error) => {
            errorCode = handler(error);
        }
    );
    return { data, errorCode };
};

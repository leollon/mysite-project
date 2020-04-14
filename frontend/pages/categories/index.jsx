// pages/categories/index.js

import React from 'react';
import PropTypes from 'prop-types';

import Error from '../_error';
import fetcher from '../../lib/fetch';
import handler from '../../lib/errorHandler';
import Layout from '../../components/Layout';
import CategoryList from '../../components/Category';

const URL = process.env.apiHost + '/categories/';

export default function Categories({ data, errorCode }) {
    if (errorCode) {
        return <Error errorCode={errorCode} />;
    }

    return (
        <Layout title="categories" description="categories">
            <CategoryList categories={data} />
        </Layout>
    );
}

Categories.propTypes = {
    data: PropTypes.array.isRequired,
    errorCode: PropTypes.any.isRequired,
};

Categories.getInitialProps = async function (context) {
    let errorCode = false;
    const data = await fetcher(`${URL}`).catch((error) => {
        errorCode = handler(error);
    });
    return { data, errorCode };
};

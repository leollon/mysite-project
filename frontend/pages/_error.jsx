// pages/_error.js

import React from 'react';

import PropTypes from 'prop-types';
import Layout from '../components/Layout';

function Error({ errorCode }) {
    return (
        <Layout title={errorCode} description={errorCode}>
            <div className="error404 empty">
                <h1>{errorCode}</h1>
                <img src="/static/img/404.webp" alt="error" />
            </div>
        </Layout>
    );
}

Error.propTypes = {
    errorCode: PropTypes.any.isRequired,
};

Error.getInitialProps = async function ({ res, err }) {
    const errorCode = res
        ? res.statusCode
        : err
        ? err.statusCode
        : '404 Not Found';
    return { errorCode: errorCode ? errorCode.toString() : errorCode };
};

export default Error;

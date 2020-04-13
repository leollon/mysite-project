// pages/tags/index.js

import React from 'react';
import PropTypes from 'prop-types';

import Error from '../_error';
import fetcher from '../../lib/fetch';
import handler from '../../lib/errorHandler';
import TagList from '../../components/Tag';
import Layout from '../../components/Layout';

const URL = process.env.apiHost + '/tags/';

export default function Tags({ data, errorCode }) {
    if (errorCode) {
        return <Error errorCode={errorCode} />;
    }

    return (
        <Layout title="tags" description="tags">
            <TagList tags={data.tags} count={data.count} />
        </Layout>
    );
}

Tags.propTypes = {
    data: PropTypes.object.isRequired,
    errorCode: PropTypes.any.isRequired,
};

Tags.getInitialProps = async function (context) {
    let errorCode = false;
    const data = await fetcher(`${URL}`).catch((error) => {
        errorCode = handler(error);
    });
    return { data, errorCode };
};

// pages/_error.js

import React from 'react';

import PropTypes from 'prop-types';
import Layout from '../components/Layout';

function Error({ errorCode }) {
  return (
    <Layout
      title={errorCode}
      description={errorCode}
    >
      <div className="error404 empty">
        <h1>{errorCode}</h1>
        <img src="/static/img/404.png" alt="400" />
      </div>
    </Layout>
  );
}

Error.propTypes = {
  errorCode: PropTypes.any.isRequired,
}


Error.getInitialProps = ({ res, err }) => {
  const errorCode = res ? res.statusCode.toString() : err ? err.statusCode.toString() : '404 Not Found';
  return { errorCode };
}

export default Error;

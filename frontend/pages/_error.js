// pages/_error.js

import Layout from '../components/layout';


function Error({ statusCode }) {
  return (
    <Layout
      title={statusCode.toString()}
      description={statusCode.toString()}
    >
      <div className="error404 empty">
        <h1>{statusCode}</h1>
        <img src="/static/img/404.png" alt="400" />
      </div>
    </Layout>
  );
}

Error.getInitialProps = ({ res, err }) => {
  const statusCode = res ? res.statusCode : err ? err.statusCode : 404;
  return { statusCode };
}

export default Error;



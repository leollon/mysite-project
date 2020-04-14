// components/Layout.jsx

import React, { useEffect } from 'react';
import PropTypes from 'prop-types';

import Header from './Header';

const Layout = function (props) {
    
    useEffect(() => {
        if (process.env.NODE_ENV === 'production') {
            window.dataLayer = window.dataLayer || [];
            function gtag() {
                dataLayer.push(arguments);
            }
            gtag('js', new Date());
            gtag('config', process.env.googleAnalysticsCode, {
                page_location: window.location.href,
                page_path: window.location.pathname,
                page_title: window.document.title,
            });
        }
    }, []);
    
    return (
        <>
            <Header title={props.title} description={props.description} />
            <div className="container-fluid" id="root">
                <div className="row">
                    <div className="col-lg-8 col-lg-offset-2 col-md-10 col-md-offset-1">
                        {props.children}
                    </div>
                </div>
            </div>
        </>
    );
};

Layout.propTypes = {
    children: PropTypes.node,
    title: PropTypes.string,
    description: PropTypes.string,
};

export default Layout;

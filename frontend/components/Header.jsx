// components/Header.jsx

import React from 'react';
import Head from 'next/head';
import PropTypes from 'prop-types';

const Header = (props) => (
    <div>
        <Head>
            <meta property="og:site_name" content="I'm Leollon" />
            <meta property="og:type" content="article" />
            <meta
                property="og:title"
                content={props.title ? props.title : "I'm 🤔"}
            />
            <meta property="og:url" content="" />
            <meta property="og:description" content={props.description} />
            <meta property="og:image" content="" />
            <meta name="twitter:creator" content="@lnr" />
            <meta name="twitter:site" content="@lnr" />
            <meta name="twitter:card" content="summary_large_image" />

            <title key="site-title">
                I&apos;m 🤔{props.title ? ' | ' + props.title : ''}
            </title>
        </Head>

        <nav className="navbar navbar-default navbar-custom navbar-fixed-top">
            <div className="container-fluid">
                <div className="navbar-header page-scroll">
                    <button
                        type="button"
                        className="navbar-toggle"
                        data-toggle="collapse"
                        data-target="#list-in-navbar-to-collapse-1"
                    >
                        <span className="sr-only">Toggle navigation</span>
                        Menu <i className="fa fa-bars" />
                    </button>
                    <a className="navbar-brand" href="/">
                        Home
                    </a>
                </div>

                <div
                    className="collapse navbar-collapse"
                    id="list-in-navbar-to-collapse-1"
                >
                    <ul className="nav navbar-nav navbar-right">
                        <li key="categories">
                            <a href="/categories">categories</a>
                        </li>
                        <li key="tags">
                            <a href="/tags">tags</a>
                        </li>
                        <li key="friends">
                            <a href="/friends">Friends</a>
                        </li>
                        <li key="about">
                            <a href="/about">about</a>
                        </li>
                    </ul>
                </div>
            </div>
        </nav>

        <header className="intro-header">
            <div className="container-fluid">
                <div className="row">
                    <div className="col-lg-8 col-lg-offset-2 col-md-10 col-md-offset-1">
                        <div className="site-heading">
                            <h1 key="head">{props.title ? props.title : ''}</h1>
                            <hr className="small" />
                            <span className="subheading">KISS</span>
                        </div>
                    </div>
                </div>
            </div>
        </header>
        {props.children}
    </div>
);

Header.propTypes = {
    title: PropTypes.string,
    description: PropTypes.string.isRequired,
    children: PropTypes.node,
};

export default Header;

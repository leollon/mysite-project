// components/header.js

import React from 'react';
import Head from 'next/head';
import Link from 'next/link';


const Header = (props) => (

  <>
    <Head>
      <meta property="og:site_name" content="I'm Leollon" />
      <meta property="og:type" content="article" />
      <meta property="og:title" content={props.title ? props.title : "leollon的小站🤔"} />
      <meta property="og:url" content="" />
      <meta property="og:description" content={props.description} />
      <meta property="og:image" content="" />
      <meta name="twitter:creator" content="@lnr" />
      <meta name="twitter:site" content="@lnr" />
      <meta name="twitter:card" content="summary_large_image" />
        
      <title key="site-title">{props.title ? props.title + ' | ' : ''}leollon的小站🤔</title>
    </Head>

    <nav className="navbar navbar-default navbar-custom navbar-fixed-top">
      <div className="container-fluid">
        <div className="navbar-header page-scroll">
          <button type="button" className="navbar-toggle" data-toggle="collapse" data-target="#list-in-navbar-to-collapse-1">
            <span className="sr-only">Toggle navigation</span>
            Menu <i className="fa fa-bars"></i>
          </button>
          <Link href="/">
            <a className="navbar-brand">Home</a>
          </Link>
        </div>

        <div className="collapse navbar-collapse" id="list-in-navbar-to-collapse-1">
          <ul className="nav navbar-nav navbar-right">
            <li>
                <Link href="/categories">
                  <a>categories</a>
                </Link>
            </li>
            <li>
              <Link href="/tags">
                <a>tags</a>
              </Link>
            </li>
              <li>
                <Link href="/about">
                  <a>about</a>
                </Link>
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
                <h1 key="head">{props.title ? props.title + ' | ' : ''}Tux</h1>
              <hr className="small" />
              <span className="subheading">KISS</span>
            </div>
          </div>
        </div>
      </div>
    </header>
    {props.children}
  </>
)

export default Header;
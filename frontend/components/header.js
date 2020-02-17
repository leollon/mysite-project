// components/header.js

import React from 'react';
import Head from 'next/head';
import Link from 'next/link';


const Header = (props) => (

  <div>
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
      <link href="/static/css/blog.css" rel="stylesheet" type="text/css" media="screen" />
        
      <title key="site-title">{props.title ? props.title + ' | ' : ''}leollon的小站🤔</title>
    </Head>
    <nav>
        <Link href="/">
          <a className="navigation">Home</a>
        </Link>
        <Link href="/categories">
          <a className="navigation">Categories</a>
        </Link>
        <Link href="/tags">
          <a className="navigation">Tags</a>
        </Link>
        <Link href="/about">
          <a className="navigation">AboutMe</a>
        </Link>
    </nav>
  </div>
)

export default Header;
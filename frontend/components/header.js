// components/header.js

import React from 'react';
import Head from 'next/head';
import Link from 'next/link';


const Header = (props) => (

  <div>
    <Head>
      <link href="/static/css/blog.css" rel="stylesheet" type="text/css" media="screen" />
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
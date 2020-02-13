// components/header.js

import React from 'react';
import Link from 'next/link';

const linkStyle = {
    marginRight: 15
};


const Header = () => (
  <div>
    <nav>
        <Link href="/">
          <a style={linkStyle}>Home</a>
        </Link>
        <Link href="/categories">
          <a style={linkStyle}>Categories</a>
        </Link>
        <Link href="/tags">
          <a style={linkStyle}>Tags</a>
        </Link>
        <Link href="/about">
          <a style={linkStyle}>AboutMe</a>
        </Link>
    </nav>
  </div>
)

export default Header;
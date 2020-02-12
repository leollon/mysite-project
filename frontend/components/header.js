// components/header.js

import React from 'react';
import Link from 'next/link';

const linkStyle = {
    marginRight: 15
};


const Header = () => (
  <div>
    <ul>
      <li key="home">
        <Link href="/">
          <a style={linkStyle}>Home</a>
        </Link>
      </li>
      <li key="home">
        <Link href="/categories">
          <a style={linkStyle}>Categories</a>
        </Link>
      </li>
      <li key="home">
        <Link href="/tags">
          <a style={linkStyle}>Tags</a>
        </Link>
      </li>
      <li key="about">
        <Link href="/about">
          <a style={linkStyle}>AboutMe</a>
        </Link>
      </li>
    </ul>
  </div>
)

export default Header;
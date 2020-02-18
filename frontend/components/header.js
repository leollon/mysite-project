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

    <nav class="navbar navbar-default navbar-custom navbar-fixed-top">
      <div class="container-fluid">
        <div class="navbar-header page-scroll">
          <button type="button" class="navbar-toggle" data-toggle="collapse" data-target="#list-in-navbar-to-collapse-1">
            <span class="sr-only">Toggle navigation</span>
            Menu <i class="fa fa-bars"></i>
          </button>
          <Link href="/">
            <a class="navbar-brand">Home</a>
          </Link>
        </div>

        <div class="collapse navbar-collapse" id="list-in-navbar-to-collapse-1">
          <ul class="nav navbar-nav navbar-right">
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

    <header class="intro-header">
      <div class="container-fluid">
        <div class="row">
          <div class="col-lg-8 col-lg-offset-2 col-md-10 col-md-offset-1">
            <div class="site-heading">
                <h1 key="head">{props.title ? props.title + ' | ' : ''}Tux</h1>
              <hr class="small" />
              <span class="subheading">KISS</span>
            </div>
          </div>
        </div>
      </div>
    </header>

    <div class="container-fluid">
      <div class="row">
        <div class="col-lg-8 col-lg-offset-2 col-md-10 col-md-offset-1">
          {props.children}
        </div>
      </div>
    </div>
  </>
)

export default Header;
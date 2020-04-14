// pages/_document.js

import React from 'react';
import Document, { Html, Head, Main, NextScript } from 'next/document';

class CustomDocument extends Document {
    static async getInitialProps(ctx) {
        const initialProps = await Document.getInitialProps(ctx);
        return { ...initialProps };
    }

    render() {
        return (
            <Html lang="en">
                <meta charSet="UTF-8" />
                <meta
                    name="viewport"
                    content="width=device-width, initial-scale=1, maximum-scale=1"
                />
                <meta httpEquiv="X-UA-Compatible" content="IE=edge" />
                <meta
                    name="keywords"
                    key="keywords"
                    content="Python,Django,c,c++,Linux,backend,后端"
                />
                <meta
                    name="google-site-verification"
                    content={process.env.googleVerificationCode}
                />

                <link rel="icon" type="image/x-icon" href="/favicon.ico" />
                <link
                    rel="shortcut icon"
                    type="image/x-icon"
                    href="/favicon.ico"
                />
                <link
                    rel="apple-touch-icon"
                    sizes="76x76"
                    href="/img/touch-icon-ipad.d5027c9927dc.png"
                />
                <link
                    rel="apple-touch-icon"
                    sizes="120x120"
                    href="/img/touch-icon-iphone-retina.007e7a910a86.png"
                />
                <link
                    rel="apple-touch-icon"
                    sizes="152x152"
                    href="/img/touch-icon-ipad-retina.87ac62f8dd0e.png"
                />
                <link
                    rel="alternate"
                    type="application/rss+xml"
                    title=""
                    href=""
                />
                <link rel="logo" type="image/svg" href="" />
                <link rel="preconnect" href="https://cdn.jsdelivr.net/" />

                <link
                    href="https://fonts.googleapis.com/css?family=Roboto&display=swap"
                    rel="stylesheet"
                />
                <link
                    href="https://fonts.googleapis.com/css?family=Source+Code+Pro&display=swap"
                    rel="stylesheet"
                />

                <link
                    href="https://cdn.staticfile.org/twitter-bootstrap/3.4.1/css/bootstrap.min.css"
                    rel="stylesheet"
                />
                <link
                    href="https://cdn.staticfile.org/font-awesome/4.7.0/css/font-awesome.min.css"
                    rel="stylesheet"
                    type="text/css"
                />
                <link
                    href="/assets/css/clean-blog.min.css"
                    rel="stylesheet"
                    type="text/css"
                    media="screen"
                />
                <script src="https://cdn.staticfile.org/jquery/3.4.1/jquery.min.js" />
                <script src="https://cdn.staticfile.org/twitter-bootstrap/3.4.1/js/bootstrap.min.js" />

                <script
                    async
                    src={
                        'https://www.googletagmanager.com/gtag/js?id=' +
                        process.env.googleAnalysticsCode
                    }
                />
                <title key="site-title">I&apos;m 🤔</title>

                <Head />
                <body>
                    <Main />

                    <hr />
                    <footer>
                        <div className="container">
                            <div className="row">
                                <div className="col-lg-8 col-lg-offset-2 col-md-10 col-md-offset-1">
                                    <ul className="list-inline text-center">
                                        <li key="github">
                                            <a
                                                href={
                                                    'https://github.com/' +
                                                    process.env.github
                                                }
                                            >
                                                <span className="fa-stack fa-lg">
                                                    <i className="fa fa-circle fa-stack-2x" />
                                                    <i className="fa fa-github fa-stack-1x fa-inverse" />
                                                </span>
                                            </a>
                                        </li>
                                        <li key="creativecommons">
                                            <a href="https://creativecommons.org/licenses/by-nc-sa/3.0/cn/">
                                                <span className="fa-stack fa-lg">
                                                    <i className="fa fa-circle fa-stack-2x" />
                                                    <i className="fa fa-creative-commons fa-stack-1x fa-inverse" />
                                                </span>
                                            </a>
                                        </li>
                                    </ul>
                                    <p
                                        className="blog-arch text-muted"
                                        id="online"
                                    ></p>
                                    <p className="copyright text-muted">
                                        Copyright &copy; Leo&apos;s blog 2017
                                    </p>
                                    <p className="blog-arch text-muted">
                                        Built with Django & Bootstrap
                                    </p>
                                </div>
                            </div>
                        </div>
                    </footer>
                    <NextScript />
                    <script src="/assets/js/clean-blog.min.js" />
                </body>
            </Html>
        );
    }
}

export default CustomDocument;

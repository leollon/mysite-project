// pages/_document.js

import Document, { Html, Head, Main, NextScript } from 'next/document'


class CustomDocument extends Document {
  static async getInitialProps(ctx) {
    const initialProps = await Document.getInitialProps(ctx)
    return { ...initialProps }
  }

  render() {
    return (
      <Html lang="en">
        <meta charset="UTF-8" />
        <meta name="viewport" content="width=device-width, initial-scale=1, maximum-scale=1" />
        <meta name="google-site-verification" content="" />
        
        <link rel="icon" type="image/x-icon" href="" />
        <link rel="apple-touch-icon" sizes="76x76" href="/static/img/touch-icon-ipad.d5027c9927dc.png" />
        <link rel="apple-touch-icon" sizes="120x120" href="/static/img/touch-icon-iphone-retina.007e7a910a86.png" />
        <link rel="apple-touch-icon" sizes="152x152" href="/static/img/touch-icon-ipad-retina.87ac62f8dd0e.png" />
        <link rel="alternate" type="application/rss+xml" title="" href="" />
        <link rel="logo" type="image/svg" href="" />
        <link rel="preconnect" href="https://cdn.jsdelivr.net/" />
        
        <link href="/static/css/blog.css" rel="stylesheet" type="text/css" media="screen" />
        
        <script async src="https://www.googletagmanager.com/gtag/js?id={GOOGLE ANALYTICS CODE}"></script>
        <title key="site-title">leollon的小站🤔</title>

        <Head />
        <body>
          <Main />
          <NextScript />
        </body>
      </Html>
    )
  }
}

export default CustomDocument;
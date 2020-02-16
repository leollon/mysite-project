// components/layout.js

import React from 'react';
import Header from './header';
import PropTypes from 'prop-types'


const Layout = function (props) {
  return (
    <div className="root" id="root">
      <Header />
      <div className="center">
        {props.children}
      </div>
    </div>
  )
}

Layout.propTypes = {
    children: PropTypes.node
}

export default Layout;
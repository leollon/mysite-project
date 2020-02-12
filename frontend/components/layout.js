// components/layout.js

import React from 'react';
import Header from './header';
import PropTypes from 'prop-types'

const layoutStyle = {
    margin: 20,
    padding: 20,
    border: '1px solid #DDD'
}


const Layout = function (props) {
  return (
    <div style={layoutStyle}>
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
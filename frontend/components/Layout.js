// components/Layout.js

import Header from './Header';

const layoutStyle = {
    margin: 20,
    padding: 20,
    border: '1px solid #DDD'
};


const Layout = function (props) {
    return (
        <div style={layoutStyle}>
            <Header />
            <div className="center">
                {props.children}
            </div>
        </div>
    )
};

export default Layout;
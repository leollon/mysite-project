// components/SubHeader.jsx

import React from 'react';
import PropTypes from 'prop-types';

export default function Summary(props) {
    return (
        <>
            {props.category_name && (
                <blockquote id="sub-header">
                    有<span className="badge">{props.statistics}</span>
                    篇文章属于
                    <strong>
                        <div className="label label-primary">
                            <span className="fa fa-folder-open">
                                {props.category_name}
                            </span>
                        </div>
                    </strong>
                    分类：
                </blockquote>
            )}
        </>
    );
}

Summary.propTypes = {
    statistics: PropTypes.number.isRequired,
    category_name: PropTypes.string.isRequired,
};

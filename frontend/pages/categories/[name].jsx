// pages/categories/[name].js

import React from 'react'
import PropTypes from 'prop-types'

import Error from '../_error'
import fetcher from '../../lib/fetch'
import Layout from '../../components/Layout'
import ArticleList from '../../components/Post'
import Summary from '../../components/SubHeader'
import PageList from '../../components/Pagination'

const API_URL = 'http://web:8000/api/v1/categories/'

export default function CategorizedArticles({ articles, name, errorCode }) {
    if (errorCode) {
        return <Error errorCode={errorCode} />
    }

    return (
        <Layout title={name} description="categories">
            <Summary
                category_name={name}
                statistics={articles.article_statistics}
            />
            <ArticleList articles={articles.results} />
            <PageList links={articles.links} />
        </Layout>
    )
}

CategorizedArticles.propTypes = {
    articles: PropTypes.object.isRequired,
    name: PropTypes.string.isRequired,
    errorCode: PropTypes.any.isRequired,
}

CategorizedArticles.getInitialProps = async (context) => {
    let errorCode = false
    const { name, cur } = context.query
    const articles = await fetcher(
        `${API_URL}${name}/articles${cur ? '?cur=' + cur : ''}`
    ).catch((error) => {
        if (error.name === 'FetchError') {
            errorCode = '500 Internal Server Error'
        } else if (error.name === 'AbortError') {
            errorCode = 'Request Cancelled'
        } else {
            errorCode = error.message
        }
    })
    return { errorCode, articles, name }
}

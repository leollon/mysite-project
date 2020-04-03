// pages/friends/index.js

import React from 'react';

import Layout from '../../components/Layout';
import allFriends from '../../data/friends.json';

export default function Friends() {
    return (
        <Layout title="friends" description="friends">
            <ul id="friends">
                {allFriends.map((friend) => (
                    <li className="friend" key={friend.name}>
                        <div className="friend-info">
                            <div className="friend-avatar">
                                <img
                                    className="avatar"
                                    src={friend.avatar}
                                    alt={friend.name}
                                />
                            </div>
                            <div className="friend-text">
                                <a href={friend.site}>{friend.name}</a>
                                <p className="text-muted" id="description">
                                    {friend.description}
                                </p>
                            </div>
                        </div>
                    </li>
                ))}
            </ul>
        </Layout>
    );
}

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
            <li key="about">
                <Link href="/about">
                <a style={linkStyle}>AboutMe</a>
                </Link>
            </li>
        </ul>
    </div>
);

export default Header;
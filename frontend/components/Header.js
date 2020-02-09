import Link from 'next/link';

const linkStyle = {
    marginRight: 15
};

const Header = () => (
    <div style={linkStyle}>
        <ul>
            <li key="home">
                <Link href="/">
                    <a>Hom3</a>
                </Link>
            </li>
            <li key="about">
                <Link href="/about">
                <a>AboutMe</a>
                </Link>
            </li>
        </ul>
    </div>
);

export default Header;
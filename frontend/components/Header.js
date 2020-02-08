import Link from 'next/link';

const linkStyle = {
    marginRight: 15
};

const Header = () => (
    <div>
        <Link href="/">
            <a>Hom3</a>
        </Link>
        <Link href="/about">
            <a>AboutMe</a>
        </Link>
    </div>
);

export default Header;
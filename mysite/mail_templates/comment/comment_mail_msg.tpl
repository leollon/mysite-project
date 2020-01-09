<!DOCTYPE html>
<html lang="en">
<head>
    <style>
        blockquote {
            margin: 0;
        }
        blockquote p {
            padding: 15px;
            background: #eee;
            border-radius: 5px;
        }
        blockquote p::before {
            content: '\201C';
        }

        blockquote p::after {
            content: '\201D';
        }
    </style>
</head>
<body>
    <p>Hi, Administrator</p>
    <pre><p>Having a new comment on article <a href="{{link}}">{{title}}</a>.</p></pre>
    <p>The article title is 《{{title}}》.</p>
    <p>{{username | capfirst}} said:</p>
    <blockquote>
        <p>{{comment}}</p>
        <footer>—{{username}}, <cite>{{title}}</cite></footer>
    </blockquote>
</body>
</html>
const gulp = require('gulp');
const rename = require('gulp-rename');
const terser = require('gulp-terser');
const cleanCSS = require('gulp-clean-css');
const imageMinify = require('gulp-imagemin');
const del = require('del');

const paths = {
    css: {
        orig: 'static/css/*.css',
        dest: 'public/css/',
    },
    js: {
        orig: ['static/js/*.js'],
        dest: 'public/js/',
    },
    img: {
        orig: 'static/img/*.*',
        dest: 'public/img/',
    },
};

function clean() {
    return del(['public/**']);
}

function jsMinify() {
    return gulp
        .src(paths.js.orig) // 1. js 文件目录
        .pipe(terser()) // 2. 压缩文件
        .pipe(
            rename({
                extname: '.min.js',
            })
        ) // 3. 重命名文件
        .pipe(gulp.dest(paths.js.dest)); // 4. 另存压缩后的文件
}

function cssMinify() {
    // 压缩css文件
    return gulp
        .src(paths.css.orig)
        .pipe(
            cleanCSS({
                level: 2,
            })
        )
        .pipe(
            rename({
                extname: '.min.css',
            })
        )
        .pipe(gulp.dest(paths.css.dest));
}

function imgMinify() {
    // 压缩图片
    return gulp
        .src(paths.img.orig)
        .pipe(
            imageMinify({
                progressive: true,
            })
        )
        .pipe(gulp.dest(paths.img.dest));
}

function auto() {
    gulp.watch('static/css/*.css', cssMinify);
    gulp.watch('static/js/*.js', jsMinify);
}

gulp.task(
    'compress',
    gulp.series(clean, gulp.parallel(cssMinify, jsMinify, imgMinify))
);
gulp.task(
    'default',
    gulp.series(clean, gulp.parallel(cssMinify, jsMinify, imgMinify), auto)
);

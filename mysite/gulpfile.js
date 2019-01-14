var gulp = require("gulp");
var rename = require("gulp-rename");
var uglify = require("gulp-uglify");
var cleanCSS = require("gulp-clean-css");
var imageMinify = require("gulp-imagemin");
var del = require("del");

var paths = {
    css: {
        orig: "static/css/*.css",
        dest: "assets/css/"
    },
    js: {
        orig: "static/js/*.js",
        dest: "assets/js/"
    },
    img: {
        orig: "static/images/*.*",
        dest: "assets/images/"
    }
};

function clean() {
    return del(["assets/**"]);
}

function jsMinify() {
    return gulp.src(paths.js.orig) // 1. js 文件目录
        .pipe(uglify()) // 2. 压缩文件
        .pipe(rename({
            extname: ".min.js"
        })) // 3. 重命名文件
        .pipe(gulp.dest(paths.js.dest)); // 4. 另存压缩后的文件
}

function cssMinify() {
    // 压缩css文件
    return gulp.src(paths.css.orig)
        .pipe(cleanCSS({
            format: "beautify",
            level: 2
        }))
        .pipe(rename({
            extname: ".min.css"
        }))
        .pipe(gulp.dest(paths.css.dest));
}

function imgMinifiy() {
    // 压缩图片
    return gulp.src(paths.img.orig)
        .pipe(imageMinify({
            progressive: true
        }))
        .pipe(gulp.dest(paths.img.dest))
}

function auto() {
    gulp.watch("static/css/*.css", cssMinify);
    gulp.watch("static/js/*.js", jsMinify);
}

exports.compress = gulp.series(clean, gulp.parallel(cssMinify, jsMinify, imgMinifiy));
exports.default = gulp.series(clean, gulp.parallel(cssMinify, jsMinify, imgMinifiy), auto);
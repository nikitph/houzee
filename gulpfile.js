var gulp = require('gulp'),
    minifyCSS = require('gulp-clean-css'),
    compass = require('gulp-compass'),
    concat = require('gulp-concat'),
    uglify = require('gulp-uglify'),
    livereload = require('gulp-livereload'),
    sourcemaps = require('gulp-sourcemaps');


gulp.task('css', function () {
    return gulp.src('static/_css/*.css')
        .pipe(sourcemaps.init())
        .pipe(concat('style.css'))
        .pipe(minifyCSS())
        .pipe(sourcemaps.write())
        .pipe(gulp.dest('static/css'))
        .pipe(livereload());
});

gulp.task('js', function () {
    //define scripts as array so we can prioritize them
    return gulp.src([
            'static/_js/*.js'
        ]
    )
        .pipe(concat('app.js'))
        .pipe(uglify())
        .pipe(gulp.dest('static/js'))
});

gulp.task('compass', function () {
    gulp.src('./static/scss/*.scss')
        .pipe(compass({
            css: './static/css',
            sass: './static/scss'
            //uncomment if you would like to include susy grids
            //require: ['susy']
        }))
        .pipe(gulp.dest('static/_css'));

    gulp.src('./static/scss/main/*.scss')
        .pipe(compass({
            css: './static/css',
            sass: './static/scss'
            //uncomment if you would like to include susy grids
            //require: ['susy']
        }))
        .pipe(gulp.dest('static/_css'));
});

gulp.task('default', function () {
    gulp.start('compass', 'css', 'js');
    livereload.listen();
    gulp.watch('gulpfile.js');
    gulp.watch('static/_css/*.css', ['css']);
    gulp.watch('static/_js/*.js', ['js']);
    gulp.watch('static/scss/components/*.scss', ['compass']);
    gulp.watch('static/scss/main/*.scss', ['compass']);
    gulp.watch('static/scss/*.scss', ['compass']);

});
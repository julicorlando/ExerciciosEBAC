// Importa os módulos necessários
const gulp = require('gulp');
const sass = require('gulp-sass')(require('sass'));
const imagemin = require('gulp-imagemin');
const uglify = require('gulp-uglify');

// Caminhos dos arquivos
const paths = {
  styles: {
    src: 'src/sass/**/*.scss',
    dest: 'dist/css'
  },
  scripts: {
    src: 'src/js/**/*.js',
    dest: 'dist/js'
  },
  images: {
    src: 'src/imagens/**/*',
    dest: 'dist/imagens'
  }
};

// 1️⃣ Compilar SASS em CSS e minificar
function compilarSass() {
  return gulp.src(paths.styles.src)
    .pipe(sass({ outputStyle: 'compressed' }).on('error', sass.logError))
    .pipe(gulp.dest(paths.styles.dest));
}

// 2️⃣ Comprimir imagens
function comprimirImagens() {
  return gulp.src(paths.images.src)
    .pipe(imagemin())
    .pipe(gulp.dest(paths.images.dest));
}

// 3️⃣ Minificar JavaScript
function minificarJS() {
  return gulp.src(paths.scripts.src)
    .pipe(uglify())
    .pipe(gulp.dest(paths.scripts.dest));
}

// 4️⃣ Tarefa que observa mudanças
function observarArquivos() {
  gulp.watch(paths.styles.src, compilarSass);
  gulp.watch(paths.scripts.src, minificarJS);
  gulp.watch(paths.images.src, comprimirImagens);
}

// Exportando as tarefas
exports.sass = compilarSass;
exports.images = comprimirImagens;
exports.js = minificarJS;
exports.observer = observarArquivos;

// Tarefa padrão
exports.default = gulp.series(compilarSass, comprimirImagens, minificarJS);

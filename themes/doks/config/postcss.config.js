const autoprefixer = require('autoprefixer');
const purgecss = require('@fullhuman/postcss-purgecss');
const whitelister = require('purgecss-whitelister');

module.exports = {
  plugins: [
    autoprefixer(),
    purgecss({
      content: [
        './themes/doks/layouts/**/*.html',
        './content/**/*.md',
      ],
      safelist: [
        'lazyloaded',
        'table',
        'thead',
        'tbody',
        'tr',
        'th',
        'td',
        'banner-message__item--active',
        ...whitelister([
          './themes/doks/assets/scss/components/_doks.scss',
          './themes/doks/assets/scss/components/_code.scss',
          './themes/doks/assets/scss/components/_search.scss',
          './themes/doks/assets/scss/common/_dark.scss',
          './node_modules/katex/dist/katex.css',
        ]),
      ],
    }),
  ],
};

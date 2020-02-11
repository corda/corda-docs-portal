# Hugo Assets

##  NOTE 

We are not currently using this.  We're deferring to `webpack` to build `sass` to `css` and to bundle and minify javascript in the theme

## tl;dr

The `assets` folder contains files accessible in Hugo templates via

```
{{ $thing := resources.Get "some/asset.ext" }}
```

via (built-in) Hugo pipelines, these asset files can be minified, fingerprinted and so on.

See:

* https://gohugo.io/hugo-pipes/introduction/#asset-directory


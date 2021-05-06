# Hugo Assets

The `assets` folder contains files accessible in Hugo templates via

```
{{ $thing := resources.Get "some/asset.ext" }}
```

via (built-in) Hugo pipelines, these asset files can be minified, fingerprinted and so on.

See:

* <https://gohugo.io/hugo-pipes/introduction/#asset-directory>

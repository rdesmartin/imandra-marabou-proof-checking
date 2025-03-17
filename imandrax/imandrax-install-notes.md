set *local* opam switch:
`eval $(opam env --switch=5.3.0 --set-switch)`

pin imandrax-api
- imandra-proof-system needs to be manually pinned

`opam pin imandra-kit git+https://github.com/imandra-ai/imandra-kit#main`

`opam pin imandra-proof-system git+https://github.com/imandra-ai/imandrax-api#main`


installing imandrax-api 
- pbrt_services needs to be manually installed

pin & install imandrax-api-ppx
`opam pin imandra-x-api-ppx git+https://github.com/imandra-ai/imandrax-api#main`

pin & install imandrax-api-prelude
`opam pin imandrax-api-prelude git+https://github.com/imandra-ai/imandrax-api#main`

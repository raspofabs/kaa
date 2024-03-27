# Kaa - the python tree sitter code analyser for C++

Primarily, this package is just to find a way to gather the static-path-count
of C++ code, but perhaps it will grow later.

## Installation

This is a poetry based package, so downloading the repo and running

```
pip install kaa
```

Should do the trick, and then you can use it:

```
kaa_spc <path_to_your_cpp_file>
```

## Roadmap

- Make this robust. To do so, run it against some bigger codebases. I already
  have access to some sizeable code, and have some examples to drive some new
  tests.
- Add nice rendering to show where the complexity it coming from.
- Add McCabe
- Huge refactor to use sub-functions?
- Rewrite it in Rust?

## Contributing

I'm doing this as a learning exercise as much as a usable tool, so contributing
fixes is appreciated, but goes against my goals.

For now, I would only want examples of code that is either calculated wrongly,
or raises an error during scanning. Feature contribution is not required, fork
instead.

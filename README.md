# pyreformat

`pyreformat` is a small script and vim function to convert Python function calls and definitions. It toggles between single and multi-line definitions.

It changes

    def foo(a, b='c', **d):

into

    def foo(
        a,
        b='c',
        **d,
    ):

and vice versa, plus the same action on function calls.

## Installation

Script:

    # Copy the script to your scripts directory
    $ cp pyreformat/__main__.py $HOME/bin
    $ chmod +x $HOME/bin/pyreformat

For convenient usage in vim, see https://github.com/jsvana/pyreformat.vim.

## Usage

In vim, simply press `<Leader>q` on a function definition or call.

To use this outside of vim:

    $ pyreformat -i <filename> <function_line_number>

then look at your beautifully formatted code.

## Motivation

I spend way too much time appeasing the 80 character linter and I don't want to do that anymore.

## License

[MIT](LICENSE)

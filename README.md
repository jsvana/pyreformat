# pyreformat

`pyreformat` is a small script and vim function to convert Python function calls and definitions. It toggles between single and multi-line definitions.

## Installation

Script:

    # Copy the script to your scripts directory
    $ cp pyreformat/__main__.py $HOME/bin
    $ chmod +x $HOME/bin/pyreformat

vim function:

    $ cat >> $HOME/.vim/vimrc
    if filereadable(expand(pyreformat/checkout/pyreformat.vim))
      source pyreformat/checkout/pyreformat.vim
    endif

## Usage

In vim, simply press `<Leader>q` on a function definition or call.

To use this outside of vim:

    $ pyreformat -i <filename> <function_line_number>

then look at your beautifully formatted code.

## Motivation

I spend way too much time appeasing the 80 character linter and I don't want to do that anymore.

## License

[MIT](LICENSE)

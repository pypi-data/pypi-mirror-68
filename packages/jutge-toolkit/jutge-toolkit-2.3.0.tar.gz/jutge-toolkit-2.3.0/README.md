# Toolkit to make problems for Jutge.org

![Logo](documentation/jutge-toolkit.png)


## Documentation

The `jutge-toolit` toolkit provides command line tools to
make all necessary files for problems in
[Jutge.org](https://jutge.org/).


## Installation

Install the toolkit with `pip3 install jutge-toolkit`. You can upgrade it to the latest version with `pip3 install --upgrade jutge-toolkit`. If you want to uninstall it, use `pip3 uninstall jutge-toolkit`.

**Note:** In order to use the toolkit, you need to have its external dependencies
installed: LaTeX and various compilers.


## Usage

There are three commands:

- `jutge-make-problem`: Makes all the necessary files to generate a common problem.

- `jutge-make-quiz`: Makes all the necessary files to generate a quiz problem.

- `jutge-compilers`: Outputs information on the available compilers.

For full details, please refer to the [common problem documentation](documentation/problems.md)
and to the [quiz problem documentation](documentation/quizzes.md).


## Credits

- [Jordi Petit](https://github.com/jordi-petit)
- [Cristina Raluca](https://github.com/ralucado)
- [Jordi Reig](https://github.com/jordireig)


## License

Apache License 2.0

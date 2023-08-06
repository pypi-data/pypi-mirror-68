# auto-gitignore

![](gitignore_demo.gif)

Create **gitignore** files right from your command line. Choose your templates faster than ever with **autocompletion**.

## Installation

auto-gitignore can be installed via `pipx`.

```py
pipx install auto-gitignore
```

You don't know pipx, yet? pipx is a tool to help you install and run end-user applications written in Python. In a way, it turns Python Package Index (PyPI) into a big app store for Python applications. You should definitely [check it out](https://pipxproject.github.io/pipx/).

## Usage

```py
$ gitignore
```
If you want to test the app before installation, the following command will run the app in a temporary environment:

```py
$ pipx run auto-gitignore
```
If a `.gitignore` file already exists in your current directory you can choose to append or overwrite.

## Credits

This app uses the [gitignore.io](https://gitignore.io/) API so credits go out to them.

Big thanks to creators of [pipx](https://pipxproject.github.io/pipx/) for turning PyPI in a big app store.
# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['rich']

package_data = \
{'': ['*']}

install_requires = \
['colorama>=0.4.0,<0.5.0',
 'commonmark>=0.9.0,<0.10.0',
 'pprintpp>=0.4.0,<0.5.0',
 'pygments>=2.6.0,<3.0.0',
 'typing-extensions>=3.7.4,<4.0.0']

extras_require = \
{':python_version >= "3.6" and python_version < "3.7"': ['dataclasses>=0.7,<0.8']}

setup_kwargs = {
    'name': 'rich',
    'version': '1.0.2',
    'description': 'Render rich text, tables, progress bars, syntax highlighting, markdown and more to the terminal',
    'long_description': '[![PyPI version](https://badge.fury.io/py/rich.svg)](https://badge.fury.io/py/rich)\n[![PyPI](https://img.shields.io/pypi/pyversions/rich.svg)](https://pypi.org/project/rich/)\n[![Downloads](https://pepy.tech/badge/rich/month)](https://pepy.tech/project/rich/month)\n[![Awesome](https://cdn.rawgit.com/sindresorhus/awesome/d7305f38d29fed78fa85652e3a63e154dd8e8829/media/badge.svg)](https://awesome-python.com/#command-line-interface-development)\n[![Twitter Follow](https://img.shields.io/twitter/follow/willmcgugan.svg?style=social)](https://twitter.com/willmcgugan)\n\n# Rich\n\nRich is a Python library for rendering _rich_ text and beautiful formatting to the terminal.\n\nThe [Rich API](https://rich.readthedocs.io/en/latest/) makes it easy to add colorful text (up to 16.7 million colors) with styles (bold, italic, underline etc.) to your script or application. Rich can also render pretty tables, progress bars, markdown, syntax highlighted source code, and tracebacks -- out of the box.\n\n![Features](https://github.com/willmcgugan/rich/raw/master/imgs/features.png)\n\n## Compatibility\n\nRich works with Linux, OSX, and Windows. True color / emoji works with new Windows Terminal, classic terminal is limited to 8 colors.\n\n## Installing\n\nInstall with `pip` or your favorite PyPi package manager.\n\n```\npip install rich\n```\n\n## Rich print function\n\nTo effortlessly add rich output to your application, you can import the [rich print](https://rich.readthedocs.io/en/latest/introduction.html#quick-start) method, which has the same signature as the builtin Python function. Try this:\n\n```python\nfrom rich import print\n\nprint("Hello, [bold magenta]World[/bold magenta]!", ":vampire:", locals())\n```\n\n![Hello World](https://github.com/willmcgugan/rich/raw/master/imgs/print.png)\n\n## Using the Console\n\nFor more control over rich terminal content, import and construct a [Console](https://rich.readthedocs.io/en/latest/reference/console.html#rich.console.Console) object.\n\n```python\nfrom rich.console import Console\n\nconsole = Console()\n```\n\nThe Console object has a `print` method which has an intentionally similar interface to the builtin `print` function. Here\'s an example of use:\n\n```python\nconsole.print("Hello", "World!")\n```\n\nAs you might expect, this will print `"Hello World!"` to the terminal. Note that unlike the builtin `print` function, Rich will word-wrap your text to fit within the terminal width.\n\nThere are a few ways of adding color and style to your output. You can set a style for the entire output by adding a `style` keyword argument. Here\'s an example:\n\n```python\nconsole.print("Hello", "World!", style="bold red")\n```\n\nThe output will be something like the following:\n\n![Hello World](https://github.com/willmcgugan/rich/raw/master/imgs/hello_world.png)\n\nThat\'s fine for styling a line of text at a time. For more finely grained styling, Rich renders a special markup which is similar in syntax to [bbcode](https://en.wikipedia.org/wiki/BBCode). Here\'s an example:\n\n```python\nconsole.print("Where there is a [bold cyan]Will[/bold cyan] there [u]is[/u] a [i]way[/i].")\n```\n\n![Console Markup](https://github.com/willmcgugan/rich/raw/master/imgs/where_there_is_a_will.png)\n\n### Console logging\n\nThe Console object has a `log()` method which has a similar interface to `print()`, but also renders a column for the current time and the file and line which made the call. By default Rich will do syntax highlighting for Python structures and for repr strings. If you log a collection (i.e. a dict or a list) Rich will pretty print it so that it fits in the available space. Here\'s an example of some of these features.\n\n```python\nfrom rich.console import Console\nconsole = Console()\n\ntest_data = [\n    {"jsonrpc": "2.0", "method": "sum", "params": [None, 1, 2, 4, False, True], "id": "1",},\n    {"jsonrpc": "2.0", "method": "notify_hello", "params": [7]},\n    {"jsonrpc": "2.0", "method": "subtract", "params": [42, 23], "id": "2"},\n]\n\ndef test_log():\n    enabled = False\n    context = {\n        "foo": "bar",\n    }\n    movies = ["Deadpool", "Rise of the Skywalker"]\n    console.log("Hello from", console, "!")\n    console.log(test_data, log_locals=True)\n\n\ntest_log()\n```\n\nThe above produces the following output:\n\n![Log](https://github.com/willmcgugan/rich/raw/master/imgs/log.png)\n\nNote the `log_locals` argument, which outputs a table containing the local variables where the log method was called.\n\nThe log method could be used for logging to the terminal for long running applications such as servers, but is also a very nice debugging aid.\n\n### Logging Handler\n\nYou can also use the builtin [Handler class](https://rich.readthedocs.io/en/latest/logging.html) to format and colorize output from Python\'s logging module. Here\'s an example of the output:\n\n![Logging](https://github.com/willmcgugan/rich/blob/master/imgs/logging.png)\n\n## Emoji\n\nTo insert an emoji in to console output place the name between two colons. Here\'s an example:\n\n```python\n>>> console.print(":smiley: :vampire: :pile_of_poo: :thumbs_up: :raccoon:")\n😃 🧛 💩 👍 🦝\n```\n\nPlease use this feature wisely.\n\n## Progress Bars\n\nRich can render multiple flicker-free [progress](https://rich.readthedocs.io/en/latest/progress.html) bars to track long-running tasks.\n\nFor basic usage, wrap any sequence in the `track` function and iterate over the result. Here\'s an example:\n\n```python\nfrom rich.progress import track\n\nfor step in track(range(100)):\n    do_step(step)\n```\n\nIt\'s not much harder to add multiple progress bars. Here\'s an example taken from the docs:\n\n![progress](https://github.com/willmcgugan/rich/raw/master/imgs/progress.gif)\n\nThe columns may be configured to show any details you want. Built-in columns include percentage complete, file size, file speed, and time remaining. Here\'s another example showing a download in progress::\n\n![progress](https://github.com/willmcgugan/rich/raw/master/imgs/downloader.gif)\n\nTo try this out yourself, see [examples/downloader.py](https://github.com/willmcgugan/rich/blob/master/examples/downloader.py) which can download multiple URLs simultaneously while displaying progress.\n\n## Markdown\n\nRich can render markdown and does a reasonable job of translating the formatting to the terminal.\n\nTo render markdown import the `Markdown` class and construct it with a string containing markdown code. Then print it to the console. Here\'s an example:\n\n```python\nfrom rich.console import Console\nfrom rich.markdown import Markdown\n\nconsole = Console()\nwith open("README.md") as readme:\n    markdown = Markdown(readme.read())\nconsole.print(markdown)\n```\n\nThis will produce output something like the following:\n\n![markdown](https://github.com/willmcgugan/rich/raw/master/imgs/markdown.png)\n\n## Syntax Highlighting\n\nRich uses the [pygments](https://pygments.org/) library to implement syntax highlighting. Usage is similar to rendering markdown; construct a `Syntax` object and print it to the console. Here\'s an example:\n\n```python\nfrom rich.console import Console\nfrom rich.syntax import Syntax\n\nmy_code = \'\'\'\ndef iter_first_last(values: Iterable[T]) -> Iterable[Tuple[bool, bool, T]]:\n    """Iterate and generate a tuple with a flag for first and last value."""\n    iter_values = iter(values)\n    try:\n        previous_value = next(iter_values)\n    except StopIteration:\n        return\n    first = True\n    for value in iter_values:\n        yield first, False, previous_value\n        first = False\n        previous_value = value\n    yield first, True, previous_value\n\'\'\'\nsyntax = Syntax(my_code, "python", theme="monokai", line_numbers=True)\nconsole = Console()\nconsole.print(syntax)\n```\n\nThis will produce the following output:\n\n![syntax](https://github.com/willmcgugan/rich/raw/master/imgs/syntax.png)\n\n## Tables\n\nRich can render flexible tables with unicode box characters. There is a large variety of formatting options for borders, styles, cell alignment etc. Here\'s a simple example:\n\n```python\nfrom rich.console import Console\nfrom rich.table import Column, Table\n\nconsole = Console()\n\ntable = Table(show_header=True, header_style="bold magenta")\ntable.add_column("Date", style="dim", width=12)\ntable.add_column("Title")\ntable.add_column("Production Budget", justify="right")\ntable.add_column("Box Office", justify="right")\ntable.add_row(\n    "Dev 20, 2019", "Star Wars: The Rise of Skywalker", "$275,000,0000", "$375,126,118"\n)\ntable.add_row(\n    "May 25, 2018",\n    "[red]Solo[/red]: A Star Wars Story",\n    "$275,000,0000",\n    "$393,151,347",\n)\ntable.add_row(\n    "Dec 15, 2017",\n    "Star Wars Ep. VIII: The Last Jedi",\n    "$262,000,000",\n    "[bold]$1,332,539,889[/bold]",\n)\n\nconsole.print(table)\n```\n\nThis produces the following output:\n\n![table](https://github.com/willmcgugan/rich/raw/master/imgs/table.png)\n\nNote that console markup is rendered in the same was as `print()` and `log()`. In fact, anything that is renderable by Rich may be included in the headers / rows (even other tables).\n\nThe `Table` class is smart enough to resize columns to fit the available width of the terminal, wrapping text as required. Here\'s the same example, with the terminal made smaller than the table above:\n\n![table2](https://github.com/willmcgugan/rich/raw/master/imgs/table2.png)\n\n## Tracebacks\n\nRich can render beautiful tracebacks which are easier to read and show more code than standard Python tracebacks. You can set Rich as the default traceback handler so all uncaught exceptions will be rendered by Rich.\n\nHere\'s what it looks like on OSX (similar on Linux):\n\n![traceback](https://github.com/willmcgugan/rich/raw/master/imgs/traceback.png)\n\nHere\'s what it looks like on Windows:\n\n![traceback_windows](https://github.com/willmcgugan/rich/raw/master/imgs/traceback_windows.png)\n\nSee the [rich traceback](https://rich.readthedocs.io/en/latest/traceback.html) documentation for the details.\n',
    'author': 'Will McGugan',
    'author_email': 'willmcgugan@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/willmcgugan/rich',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)

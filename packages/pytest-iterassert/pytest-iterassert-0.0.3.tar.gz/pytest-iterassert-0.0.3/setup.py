# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['iterassert']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'pytest-iterassert',
    'version': '0.0.3',
    'description': 'Nicer list and iterable assertion messages for pytest',
    'long_description': "[![License: MPL 2.0](https://img.shields.io/badge/License-MPL%202.0-brightgreen.svg)](https://opensource.org/licenses/MPL-2.0)\n[![Build](https://github.com/tobywf/pytest-iterassert/workflows/Build/badge.svg?branch=master&event=push)](https://github.com/tobywf/pytest-iterassert/actions)\n[![codecov](https://codecov.io/gh/tobywf/pytest-iterassert/branch/master/graph/badge.svg)](https://codecov.io/gh/tobywf/pytest-iterassert)\n[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)\n\n# pytest-iterassert\n\nHave you ever wanted to use `all` or `any` in a unit test, but found the assert\nmessage to be lacking? Do assertions on class attributes in collections almost\nmake you wish you were coding in Java (with a nice assertion framework)? Then\nthis is the [pytest](https://docs.pytest.org/en/latest/) helper for you!\n[pytest-iterassert](https://github.com/tobywf/pytest-iterassert) provides\n`all_match` and `any_match` to give you nice asserts.\n\n## Examples\n\nThe built-in [`any`](https://docs.python.org/3/library/functions.html#any) or\n[`all`](https://docs.python.org/3/library/functions.html#all) can cause a lot of\nsadness when tests fail:\n\n```plain\n    def test_generator_without_iterassert() -> None:\n>       assert all(i < 1 for i in range(3))\nE       assert False\nE        +  where False = all(<genexpr> at 0x10221a250>)\n```\n\n`all_match` and `any_match` make debugging easy by hoisting the comparison out,\nand printing meaningful debug:\n\n```plain\n    def test_generator_with_iterassert() -> None:\n>       assert all_match(range(3)) < 1\nE       assert all(0, 1, 2) < 1\nE        +  where all(0, 1, 2) = all_match(range(0, 3))\nE        +    where range(0, 3) = range(3)\n```\n\nHow about a more complex example? Asserting attributes of a class instance is\npretty common.\n\n``` plain\n    def test_attr_of_classes_without_iterassert() -> None:\n        foos = [Foo(1), Foo(2), Foo(3)]\n>       assert all(foo.bar < 3 for foo in foos)\nE       assert False\nE        +  where False = all(<genexpr> at 0x10597ca50>)\n```\n\n`iterassert` makes it easy to apply functions to the iterable, and will convince\npytest to show you the result of that function!\n\n``` plain\n    def test_attr_of_classes_with_iterassert_1() -> None:\n        foos = [Foo(1), Foo(2), Foo(3)]\n>       assert all_match(foos, get_bar) < 3\nE       assert all(9001, 9002, 9003) < 3\nE        +  where all(9001, 9002, 9003) = all_match([<Foo(1)>, <Foo(2)>, <Foo(3)>], get_bar)\n```\n\nIt's also possible to run more complex checks against all items, by doing the\nchecking inside a function:\n\n``` plain\n    def test_attr_of_classes_with_iterassert_2() -> None:\n        foos = [Foo(1), Foo(2), Foo(3)]\n>       assert all_match(foos, check_bar)\nE       assert all(False, False, False)\nE        +  where all(False, False, False) = all_match([<Foo(1)>, <Foo(2)>, <Foo(3)>], check_bar)\n```\n\nNote in this case, much like the buildin functions, `all_match` and `any_match`\ntake no operator or operand.\n\nAnd, if you need to incorporate more transformations, but would like to see the\nintermediary items, `capture` allows for this, too:\n\n``` plain\n    def test_attr_of_classes_with_iterassert_3() -> None:\n        foos = [Foo(1), Foo(2), Foo(3)]\n>       assert all_match(capture(foo.bar for foo in foos), check_val)\nE       assert all(False, False, False)\nE        +  where all(False, False, False) = all_match([9001, 9002, 9003], check_val)\nE        +    where [9001, 9002, 9003] = capture(<genexpr> at 0x1031220d0>)\n```\n\nEven the test summary says it all:\n\n``` plain\nFAILED example.py::test_generator_without_iterassert - assert False\nFAILED example.py::test_generator_with_iterassert - assert all(0, 1, 2) < 1\nFAILED example.py::test_attr_of_classes_without_iterassert - assert False\nFAILED example.py::test_attr_of_classes_with_iterassert_1 - assert all(9001, 9002, 9003) < 3\nFAILED example.py::test_attr_of_classes_with_iterassert_2 - assert all(False, False, False)\nFAILED example.py::test_attr_of_classes_with_iterassert_3 - assert all(False, False, False)\n```\n\n## Installation\n\n[pytest-iterassert is on\nPyPI](https://pypi.org/project/pytest-iterassert/), so you can simply install\nvia `pip install pytest-iterassert` (requires Python 3.6 or higher).\n\n(If you're really brave, you can also alias `all_match` and `any_match` to the\nbuiltin functions on import.)\n\n## Changelog\n\n### [0.0.3] - 2020-05-10\n\n* Add `capture`, and allow `all_match` and `any_match` to not take an\n  operator/operand, for checks inside the mapping function\n\n### [0.0.2] - 2020-05-07\n\n* Initial release\n\n## Development\n\nThis library uses [Poetry](https://python-poetry.org/) for managing\ndependencies. You just need to run `poetry install`, and it will create a\nvirtual environment with all developer dependencies installed.\n\nPlease run `poetry run ./lint` before submitting pull requests.\n\n## License\n\nThis library is licensed under the Mozilla Public License Version 2.0. For more\ninformation, see `LICENSE`.\n",
    'author': 'Toby Fleming',
    'author_email': 'tobywf@users.noreply.github.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/tobywf/pytest-iterassert',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)

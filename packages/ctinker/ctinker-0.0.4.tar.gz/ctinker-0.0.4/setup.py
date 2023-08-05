#!/usr/bin/env python
#   -*- coding: utf-8 -*-

from setuptools import setup
from setuptools.command.install import install as _install

class install(_install):
    def pre_install_script(self):
        pass

    def post_install_script(self):
        pass

    def run(self):
        self.pre_install_script()

        _install.run(self)

        self.post_install_script()

if __name__ == '__main__':
    setup(
        name = 'ctinker',
        version = '0.0.4',
        description = 'CTinker is a C project introspection and augmentation tool',
        long_description = '# CTinker - C/C++ Project Introspection and Augmentation Tool\n\n**C Tinker**, pronounced _see-tinker_ (or humorously "stinker", as suggested by \n[Chuck Ocheret](https://github.com/ocheret)) allows you to get in the middle of the build process of a \nmake/Ninja-style project and augment the compilation and linking as well as extract and redirect artifacts using \npolicies you can\'t implement otherwise even with LDFLAGS/CFLAGS magic.\n\n[![Gitter](https://img.shields.io/gitter/room/karellen/lobby?logo=gitter)](https://gitter.im/karellen/lobby)\n\n[![CTinker Version](https://img.shields.io/pypi/v/ctinker?logo=pypi)](https://pypi.org/project/ctinker/)\n[![CTinker Python Versions](https://img.shields.io/pypi/pyversions/ctinker?logo=pypi)](https://pypi.org/project/ctinker/)\n[![CTinker Downloads Per Day](https://img.shields.io/pypi/dd/ctinker?logo=pypi)](https://pypi.org/project/ctinker/)\n[![CTinker Downloads Per Week](https://img.shields.io/pypi/dw/ctinker?logo=pypi)](https://pypi.org/project/ctinker/)\n[![CTinker Downloads Per Month](https://img.shields.io/pypi/dm/ctinker?logo=pypi)](https://pypi.org/project/ctinker/)\n\n## Problem\n\nMore formally the problem **CTinker** solves can be stated as follows: \n\n> I need to get in the middle of a build process of a project I can know intimately but do not control\n> and that I have no intention of maintaining a fork/patches for, or for which I need to obtain runtime \n> dynamic control of the build process.\n\n## Solution\n\n### Overview\n\n`CTinker` is capable of getting in the middle of virtually any build process by: \n1. Starting in the `supervisor` mode.\n1. Creating a temporary directory full of toolkit-specific (e.g. for LLVM Clang it\'s `clang`, `ar` etc) \nsymlinks referring back to `CTinker` executable. \n1. Setting up environ and a local socket to communicate with the `workers`.\n1. Invoking the build process as specified by the user.\n1. Being invoked for each tool invocation in a `worker` mode (based on environmental variables),\n communicating with the `supervisor`, sending command-line arguments to the `supervisor` process and then\n invoking the tool itself.\n1. If specified, invoking `scripting` handlers before and after the build as a whole (in the `supervisor`) \nand before and after each intercepted tool invocation (in the `worker`). \n \n As a further illustration, if the original process invocation chain for a sample build is as follows:\n \n> make => clang => lld, => make => clang, => clang => lld\n \n then the same build instrumented with CTinker will produce the following process invocation chain:\n\n> ctinker => make => ctinker-clang => clang => ctinker-lld => lld, => make => ctinker-clang => clang, \n> => ctinker-clang => clang => ctinker-lld => lld\n\n### Scripting\n\nScripting is the most powerful part of `CTinker` that provides an ability to really change how build functions\nat runtime. It is implemented via a visitor pattern, invoking functions specified in the user-supplied script:\n\n```python\n\ndef ctinker_start(env: Dict[str, str], work_dir: Path):\n    """Invoked by CTinker `supervisor` prior to the main build process\n    \n    Changes to the `env` dictionary propagate to the main build process.\n    """\n    pass\n\ndef ctinker_finish(env: Dict[str, str], work_dir: Path, tool_calls: List[Tuple[Any]], return_code: int):\n    """Invoked by CTinker `supervisor` after the main build process exits\n\n    `tool_calls` is a `list` of `tuple`s of `(tool, tool_args, return_code, cwd, script_result)`, where `script_result`\n    is the value returned by `ctinker_after_tool`.\n    """\n    pass\n\n\ndef ctinker_before_tool(env: Dict[str, str], tool: str, tool_args: List[str], work_dir: Path, cwd: Path):\n    """Invoked by CTinker `worker` prior to the tool process\n    \n    Changes to the `env` dictionary propagate to the tool process.\n    Changes to the `tool_args` list propagate to the tool process.\n    """\n    pass\n\ndef ctinker_after_tool(env: Dict[str, str], tool: str, tool_args: List[str], work_dir: Path, cwd: Path, \n                       return_code: int) -> Any:\n    """Invoked by CTinker `worker` after the tool process exits\n    \n    Returned value, **if truthy**, will be stored and will appear \n    as the last entry in the `tool_calls` passed to `ctinker_finish`\n    """\n    pass\n```\n\nIt is guaranteed that `ctinker_start` - `ctinker_finish` and `ctinker_before_tool` - `ctinker_after_tool` pairs will \nbe executed in the same `supervisor` and `worker` processes _respectively_ and therefore you can pass values between \nthe start/finish and before/after functions (for example by a global or within the same instance of an object).\n\n## Help\n\n```bash\n$ ctinker --help\nusage: ctinker [-h] [-s SCRIPT] [-o OUT] [-f {text,pickle}] [-p PATHS]\n               [-w WORK_DIR] -t {clang} [-l [{clang,__default}]]\n               [-L LINKER_TOOL_OVERRIDE]\n               [--linker-flags-name LINKER_FLAGS_NAME]\n               ...\n\nCTinker project introspection and augmentation tool\n\npositional arguments:\n  command               build command to execute\n\noptional arguments:\n  -h, --help            show this help message and exit\n  -s SCRIPT, --script SCRIPT\n                        a Python script containing visitor-style hooks\n                        (default: None)\n  -o OUT, --out OUT     a path to a file where all tools, their arguments and\n                        exit codes will be recorded (default: None)\n  -f {text,pickle}, --format {text,pickle}\n                        the format of the output file (default: text)\n  -p PATHS, --path PATHS\n                        prepend a leading PATH entry to be inherited by the\n                        invoked command (default: None)\n  -w WORK_DIR, --work-dir WORK_DIR\n                        sets a work directory to be something other than\n                        current working directory (default: )\n  -t {clang}, --toolkit {clang}\n                        enable specific compilation interception modes\n                        (default: None)\n  -l [{clang,__default}], --linker-intercept [{clang,__default}]\n                        intercept linker with --linker-flags-name env var\n                        using the specified toolkit (default: None)\n  -L LINKER_TOOL_OVERRIDE, --linker-tool-override LINKER_TOOL_OVERRIDE\n                        specify linker tool name directly (may not work if no\n                        toolkit provides it) (default: None)\n  --linker-flags-name LINKER_FLAGS_NAME\n                        specify linker environmental variable (default:\n                        LDFLAGS)\n```\n\n## Example\n\nTBW\n\n## Troubleshooting\n\n1. Printing to `sys.stdout` from the `worker` is dangerous as the stdout is often interpreted by the invoking tool\nwhich can lead to a crash in the tool expecting certain data format. `print("debug!", file=sys.stderr)` is generally \nsafe.',
        long_description_content_type = 'text/markdown',
        classifiers = [
            'License :: OSI Approved :: Apache Software License',
            'Programming Language :: Python :: 3.6',
            'Programming Language :: Python :: 3.7',
            'Programming Language :: Python :: 3.8',
            'Operating System :: MacOS :: MacOS X',
            'Operating System :: POSIX',
            'Operating System :: POSIX :: Linux',
            'Programming Language :: C',
            'Programming Language :: C++',
            'Topic :: Software Development :: Build Tools',
            'Topic :: Software Development :: Compilers',
            'Topic :: Software Development :: Assemblers',
            'Topic :: Software Development :: Pre-processors',
            'Topic :: Utilities',
            'Intended Audience :: Developers',
            'Development Status :: 4 - Beta'
        ],
        keywords = 'C C++ build make ninja llvm clang flags intercept augment',

        author = 'Karellen, Inc.',
        author_email = 'supervisor@karellen.co',
        maintainer = 'Arcadiy Ivanov',
        maintainer_email = 'arcadiy@karellen.co',

        license = 'Apache License, Version 2.0',

        url = 'https://github.com/karellen/ctinker',
        project_urls = {
            'Bug Tracker': 'https://github.com/karellen/ctinker/issues',
            'Documentation': 'https://github.com/karellen/ctinker/',
            'Source Code': 'https://github.com/karellen/ctinker/'
        },

        scripts = ['scripts/ctinker'],
        packages = ['ctinker'],
        namespace_packages = [],
        py_modules = [],
        entry_points = {},
        data_files = [],
        package_data = {
            'ctinker': ['LICENSE']
        },
        install_requires = [],
        dependency_links = [],
        zip_safe = True,
        cmdclass = {'install': install},
        python_requires = '>=3.6',
        obsoletes = [],
    )

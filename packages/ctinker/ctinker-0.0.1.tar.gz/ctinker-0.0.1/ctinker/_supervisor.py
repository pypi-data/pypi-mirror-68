# -*- coding: utf-8 -*-
#
# (C) Copyright 2020 Karellen, Inc. (https://www.karellen.co/)
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#

import marshal
import pickle
import selectors
import signal
import socket
import sys
import tempfile
from os import environ, pathsep, symlink, fdopen
from pathlib import Path
from typing import Dict

from ctinker import (_CTINKER_LINKER_DEFAULT, CTINKER_WORK_DIR, CTINKER_SCRIPT,
                     CTINKER_SYS_PATH, CTINKER_PATH, CTINKER_SERVER, tool_executor)


class ToolkitDescriptor:
    toolkit_name = None

    def prepare_overlay_dir(self, ctinker_path, overlay_dir):
        pass

    def get_linker(self):
        pass


TOOLKITS_AVAILABLE: Dict[str, ToolkitDescriptor] = {}


class ClangModeDescriptor(ToolkitDescriptor):
    toolkit_name = "clang"

    FILES = ["addr2line", "ar", "bugpoint", "c++filt", "c-index-test", "clang", "clang++", "clang-10",
             "clang-apply-replacements", "clang-change-namespace", "clang-check", "clang-cl", "clang-cpp", "clangd",
             "clang-doc", "clang-extdef-mapping", "clang-format", "clang-import-test", "clang-include-fixer",
             "clang-move", "clang-offload-bundler", "clang-offload-wrapper", "clang-query", "clang-refactor",
             "clang-rename", "clang-reorder-fields", "clang-scan-deps", "clang-tidy", "diagtool", "dlltool", "dsymutil",
             "dwp", "find-all-symbols", "git-clang-format", "hmaptool", "ld64.lld", "ld.lld", "lipo", "llc", "lld",
             "lldb", "lldb-argdumper", "lldb-instr", "lldb-server", "lldb-vscode", "lld-link", "lli", "llvm-addr2line",
             "llvm-ar", "llvm-as", "llvm-bcanalyzer", "llvm-cat", "llvm-cfi-verify", "llvm-config", "llvm-cov",
             "llvm-c-test", "llvm-cvtres", "llvm-cxxdump", "llvm-cxxfilt", "llvm-cxxmap", "llvm-diff", "llvm-dis",
             "llvm-dlltool", "llvm-dwarfdump", "llvm-dwp", "llvm-elfabi", "llvm-exegesis", "llvm-extract", "llvm-ifs",
             "llvm-install-name-tool", "llvm-jitlink", "llvm-lib", "llvm-link", "llvm-lipo", "llvm-lto", "llvm-lto2",
             "llvm-mc", "llvm-mca", "llvm-modextract", "llvm-mt", "llvm-nm", "llvm-objcopy", "llvm-objdump",
             "llvm-opt-report", "llvm-pdbutil", "llvm-profdata", "llvm-ranlib", "llvm-rc", "llvm-readelf",
             "llvm-readobj", "llvm-reduce", "llvm-rtdyld", "llvm-size", "llvm-split", "llvm-stress", "llvm-strings",
             "llvm-strip", "llvm-symbolizer", "llvm-tblgen", "llvm-undname", "llvm-xray", "modularize", "nm",
             "obj2yaml", "objcopy", "objdump", "opt", "pp-trace", "ranlib", "readelf", "sancov", "sanstats",
             "scan-build", "scan-view", "size", "strings", "strip", "verify-uselistorder", "wasm-ld", "yaml2obj"]

    def __init__(self):
        pass

    def prepare_overlay_dir(self, ctinker_path, overlay_dir: Path):
        for f in self.FILES:
            link = overlay_dir / f
            if not link.exists():
                symlink(ctinker_path, link)

    def get_linker(self):
        if sys.platform == "linux":
            return "ld.lld"
        if sys.platform == "darwin":
            return "ld64.lld"
        if sys.platform == "win32":
            return "lld-link"


for cls in ToolkitDescriptor.__subclasses__():
    TOOLKITS_AVAILABLE[cls.toolkit_name] = cls


class NoneCM:
    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        pass

    def write(self, obj):
        pass


NONE_CM = NoneCM()


class CTinkerSupervisor:
    def __init__(self, *, toolkit_names, command, out, format, script, paths, work_dir: Path,
                 linker_intercept, linker_tool_override, linker_flags_name,
                 **_):
        self.toolkit_names = toolkit_names
        self.command = command
        self.out = Path(out) if out else None

        if format == "text":
            self.formatted_out = self.text_out
            self.out_mode = "wt"
            self.out_encoding = "utf-8"
        else:
            self.formatted_out = self.pickle_out
            self.out_mode = "wb"
            self.out_encoding = None

        self.script = Path(script).absolute() if script else None
        self.paths = paths
        self.work_dir = Path(work_dir).absolute()
        self.linker_intercept = linker_intercept
        self.linker_tool_override = linker_tool_override
        self.linker_flags_name = linker_flags_name

        self.overlay_dir = None
        self.toolkits = {k: TOOLKITS_AVAILABLE[k]() for k in toolkit_names}

        if linker_intercept == _CTINKER_LINKER_DEFAULT and len(self.toolkit_names) > 1:
            raise RuntimeError("Multiple toolkits specified along with a 'default' linker intercept."
                               "You need to specify a linker intercept toolkit.")

        if linker_intercept and linker_intercept != _CTINKER_LINKER_DEFAULT and linker_intercept not in self.toolkits:
            raise RuntimeError("Specified linker intercept toolkit %r has not been enabled" % linker_intercept)

        self.tool_calls = []

    def text_out(self, f_out, obj):
        f_out.write(repr(obj))
        f_out.write("\n")

    def pickle_out(self, f_out, obj):
        pickle.Pickler(f_out).dump(obj)

    def run(self):
        child_env = dict(**environ)
        path_env = child_env.get("PATH", "")
        if self.paths:
            for path in reversed(self.paths):
                path_env = str(Path(path).absolute()) + pathsep + path_env

        server_addr = tempfile.mktemp()
        child_env[CTINKER_SERVER] = server_addr

        with tempfile.TemporaryDirectory() as self.overlay_dir:
            self.overlay_dir = Path(self.overlay_dir)

            self.prepare_overlay_bin()
            self.work_dir.mkdir(parents=True, exist_ok=True)

            child_env[CTINKER_PATH] = str(self.overlay_dir)
            child_env["PATH"] = str(self.overlay_dir) + pathsep + path_env
            child_env[CTINKER_SYS_PATH] = pathsep.join(sys.path)
            child_env[CTINKER_WORK_DIR] = str(self.work_dir)

            if self.linker_intercept:
                linker = self.linker_tool_override or (self.toolkits[self.linker_intercept]
                                                       if self.linker_intercept != _CTINKER_LINKER_DEFAULT
                                                       else next(iter(self.toolkits.values()))).get_linker()
                child_env[self.linker_flags_name] = "-fuse-ld=" + str(self.overlay_dir / linker)

            script_names = {}

            ctinker_start = None
            ctinker_finish = None
            if self.script:
                script_path = self.script.absolute()
                script_pyc_path = self.overlay_dir / "__ctinker_script.pyc"
                with open(str(script_path), "rb") as script_f:
                    script_source = script_f.read()
                co = compile(script_source, str(script_path), mode="exec")

                exec(co, script_names, script_names)
                ctinker_start = script_names.get("ctinker_start")
                ctinker_finish = script_names.get("ctinker_finish")

                with open(script_pyc_path, "wb") as script_pyc_f:
                    marshal.dump(co, script_pyc_f)

                child_env[CTINKER_SCRIPT] = script_pyc_path

            if ctinker_start:
                ctinker_start(child_env, self.work_dir)

            formatted_out = self.formatted_out

            with open(self.out, self.out_mode, encoding=self.out_encoding) if self.out else NONE_CM as f_out:
                with socket.socket(socket.AF_UNIX) as s_sock:
                    s_sock.bind(server_addr)
                    s_sock.listen()

                    with selectors.DefaultSelector() as sel:
                        wake_w, wake_r = socket.socketpair()
                        with wake_w, wake_r:
                            def read(conn: socket.socket, mask: int):
                                with conn:
                                    s_file = fdopen(conn.fileno(), "rb", buffering=0)
                                    try:
                                        obj = pickle.Unpickler(s_file).load()
                                        # False obj means skip
                                        if obj:
                                            self.tool_calls.append(obj)
                                            formatted_out(f_out, obj)
                                    finally:
                                        sel.unregister(conn)

                            def accept(sock: socket.socket, mask: int):
                                conn, client_addr = sock.accept()
                                sel.register(conn, selectors.EVENT_READ, read)

                            def sel_close(sock: socket.socket, mask: int):
                                sel.unregister(sock)
                                sel.close()

                            sel.register(s_sock, selectors.EVENT_READ, accept)
                            sel.register(wake_r, selectors.EVENT_READ, sel_close)

                            def child_died(signum, frame):
                                signal.signal(signal.SIGCHLD, signal.SIG_DFL)
                                wake_w.close()

                            signal.signal(signal.SIGCHLD, child_died)

                            with tool_executor(self.command, child_env) as child_p:
                                while True:
                                    if not sel.get_map():
                                        break
                                    events = sel.select()
                                    for key, mask in events:
                                        callback = key.data
                                        callback(key.fileobj, mask)

                                return_code = child_p.poll()

                                if ctinker_finish:
                                    ctinker_finish(child_env, self.work_dir, self.tool_calls, return_code)

                                return return_code

    def prepare_overlay_bin(self):
        for name, toolkit in self.toolkits.items():
            toolkit.prepare_overlay_dir(sys.argv[0], self.overlay_dir)


def main_supervisor():
    import argparse

    parser = argparse.ArgumentParser(description="CTinker project introspection and augmentation tool",
                                     formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument("-s", "--script",
                        help="a Python script containing visitor-style hooks")
    parser.add_argument("-o", "--out",
                        help="a path to a file where all tools, their arguments and exit codes will be recorded")
    parser.add_argument("-f", "--format", choices=["text", "pickle"], default="text",
                        help="the format of the output file")
    parser.add_argument("-p", "--path", action="append", dest="paths",
                        help="prepend a leading PATH entry to be inherited by the invoked command")
    parser.add_argument("-w", "--work-dir", default="",
                        help="sets a work directory to be something other than current working directory")
    parser.add_argument("-t", "--toolkit", choices=list(TOOLKITS_AVAILABLE.keys()),
                        action="append",
                        dest="toolkit_names",
                        required=True, help="enable specific compilation interception modes")
    parser.add_argument("-l", "--linker-intercept", choices=list(TOOLKITS_AVAILABLE.keys()) + [_CTINKER_LINKER_DEFAULT],
                        const=_CTINKER_LINKER_DEFAULT,
                        default=None,
                        nargs="?",
                        help="intercept linker with --linker-flags-name env var using the specified toolkit")
    parser.add_argument("-L", "--linker-tool-override",
                        help="specify linker tool name directly (may not work if no toolkit provides it)")
    parser.add_argument("--linker-flags-name",
                        default="LDFLAGS",
                        help="specify linker environmental variable")

    parser.add_argument("command", nargs=argparse.REMAINDER, help="build command to execute")

    result = parser.parse_args()
    if not result.command:
        parser.error("build command must be specified")
    return CTinkerSupervisor(**vars(result), ).run()

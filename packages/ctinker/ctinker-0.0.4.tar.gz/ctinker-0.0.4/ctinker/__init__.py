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
import shutil
import socket
import subprocess
import sys
from os import environ, pathsep, fdopen
from pathlib import Path

environ = environ
CTINKER_SERVER = "__CTINKER_SERVER"
CTINKER_PATH = "__CTINKER_PATH"
CTINKER_SYS_PATH = "__CTINKER_SYS_PATH"
CTINKER_SCRIPT = "__CTINKER_SCRIPT"
CTINKER_WORK_DIR = "__CTINKER_WORK_DIR"
CTINKER_OFF = "__CTINKER_OFF"

_CTINKER_LINKER_DEFAULT = "__default"


def find_tool(tool, env):
    """Part of the public API"""

    path = env["PATH"]
    paths = path.split(pathsep)
    ctinker_path = env[CTINKER_PATH]

    # We need PATH without our shim for real tool execution
    idx = paths.index(ctinker_path)
    del paths[idx]
    tool_path_env = pathsep.join(paths)

    return shutil.which(tool, path=tool_path_env)


def tool_executor(command, env):
    """Part of the public API"""
    return subprocess.Popen(command, env=env, bufsize=0)


class CTinkerWorker:
    def __init__(self, server_addr):
        self.server_addr = server_addr

    def run(self):
        script_names = {}
        before_tool = None
        after_tool = None

        if CTINKER_SCRIPT in environ and not environ.get(CTINKER_OFF):
            script = environ[CTINKER_SCRIPT]
            with open(script, "rb") as co_f:
                co_bytes = co_f.read()

            co = marshal.loads(co_bytes)
            exec(co, script_names, script_names)
            before_tool = script_names.get("ctinker_before_tool")
            after_tool = script_names.get("ctinker_after_tool")

        cwd = Path.cwd()
        work_dir = Path(environ["__CTINKER_WORK_DIR"])

        argv = sys.argv
        tool = Path(argv[0]).name
        tool_args = sys.argv[1:]

        env = dict(environ.items())
        if before_tool:
            before_tool(env, tool, tool_args, work_dir, cwd)

        tool_path = find_tool(tool, env)

        tool_cmd = [tool_path] + tool_args

        with tool_executor(tool_cmd, env) as p:
            with socket.socket(socket.AF_UNIX) as sock:
                sock.connect(self.server_addr)
                s_file = fdopen(sock.fileno(), "wb", buffering=0)
                pickler = pickle.Pickler(s_file, pickle.HIGHEST_PROTOCOL)
                p.wait()
                return_code = p.returncode

                script_result = None
                if after_tool:
                    script_result = after_tool(env, tool, tool_args, work_dir, cwd, return_code)

                if not environ.get(CTINKER_OFF):
                    pickler.dump((tool, tool_args, return_code, cwd, script_result))
                else:
                    # False obj means skip
                    pickler.dump(())
                s_file.flush()
                sock.recv(1)
                return return_code


def main():
    server_addr = environ.get(CTINKER_SERVER)
    if server_addr:
        return main_worker(server_addr)
    else:
        from ctinker._supervisor import main_supervisor
        return main_supervisor()


def main_worker(sock_path):
    return CTinkerWorker(sock_path).run()

"""
MIT License
Copyright (c) 2020 williamfzc
Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:
The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.
THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
"""
from minadb import ADBDevice
from loguru import logger
import requests
import typing

__PROJECT_NAME__ = r"cort_client"
__AUTHOR__ = r"williamfzc"
__AUTHOR_EMAIL__ = r"fengzc@vip.qq.com"
__LICENSE__ = r"MIT"
__VERSION__ = r"0.1.0"


class CortJob(object):
    def __init__(
        self,
        product_name: str,
        user_name: str,
        cli: "CortClient",
        *_,
        **__,
    ):
        self.product_name = product_name
        self.user_name = user_name

        # from cli
        self.device = cli.device
        self.serial_no = cli.device.serial_no
        self.host = cli.host
        self.port = cli.port

        # build this job
        self.package_name = self.get_package_name()
        self.version_name = self.get_version_name()
        self.hash_name = self.get_hash_name()
        logger.info(
            f"job generated: {self.product_name} / {self.package_name} / {self.version_name} / {self.hash_name}"
        )

    def get_package_name(self) -> str:
        raise NotImplementedError

    def get_version_name(self) -> str:
        raise NotImplementedError

    def get_hash_name(self) -> str:
        raise NotImplementedError

    def start(self):
        command = [
            "am",
            "instrument",
            "-w",
            "-r",
            # required
            "-e",
            "coverage",
            "true",
            "-e",
            "debug",
            "false",
            "-e",
            "class",
            f"{self.package_name}.CortInstrumentedTest",
            # optional
            # product name
            "-e",
            "productName",
            self.product_name,
            # package name
            "-e",
            "packageName",
            self.package_name,
            # version name
            "-e",
            "versionName",
            self.version_name,
            # hash name
            "-e",
            "hashName",
            self.hash_name,
            # user name
            "-e",
            "userName",
            self.user_name,
            # serial no
            "-e",
            "serialNo",
            self.serial_no,
            # host
            "-e",
            "host",
            self.host,
            # port
            "-e",
            "port",
            str(self.port),
            # step (period)
            "-e",
            "step",
            # todo: now locked
            str(5000),
            # runner
            f"{self.package_name}.test/{self.package_name}.CortTestRunner",
        ]
        logger.debug(f"job start with command: {command}")
        self.device.shell(command)
        # todo: test will never stop by default. need a cleanup here


class CortClient(object):
    def __init__(self, host: str, port: int, serial_no):
        # server
        self.host = host
        self.port = port
        self.base_url = f"http://{self.host}:{self.port}"
        self.artifact_url = f"{self.base_url}/api/v1/artifact"
        # local
        self.device: ADBDevice = ADBDevice(serial_no)

    def heartbeat(self) -> bool:
        try:
            return requests.get(f"{self.base_url}/").ok
        except requests.exceptions.BaseHTTPError:
            return False

    def register_device(self, serial_no: str):
        self.device = ADBDevice(serial_no)

    def new_job(
        self,
        job_kls: typing.Type[CortJob],
        product_name: str,
        user_name: str,
        *args,
        **kwargs,
    ) -> CortJob:
        return job_kls(product_name, user_name, self, *args, **kwargs)

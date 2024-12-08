from subprocess import Popen
import logging


def open_application(parametrized_cmd: list[str], **kwargs):
    cmd = [x.format(**kwargs) for x in parametrized_cmd]
    logging.debug(f"executing: {cmd}")
    process = Popen(cmd)
    return process

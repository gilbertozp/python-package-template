"""
BSD 3-Clause License

Copyright (c) 2017, Gilberto Pastorello
All rights reserved.

Redistribution and use in source and binary forms, with or without
modification, are permitted provided that the following conditions are met:

* Redistributions of source code must retain the above copyright notice, this
  list of conditions and the following disclaimer.

* Redistributions in binary form must reproduce the above copyright notice,
  this list of conditions and the following disclaimer in the documentation
  and/or other materials provided with the distribution.

* Neither the name of the copyright holder nor the names of its
  contributors may be used to endorse or promote products derived from
  this software without specific prior written permission.

THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE
FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL
DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR
SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER
CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY,
OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.

Template with basic functionality for new Python projects: module

@author: Gilberto Pastorello
@contact: gzpastorello@lbl.gov
@date: 2017-07-12
"""
import sys
import logging
import warnings

from packagetemplate import TemplateModuleError, log_config, log_trace

log = logging.getLogger(__name__)


def f():
    """
    Leaf (bottom) function
    """
    log.info("Ran function f")


def err():
    """
    Exception generating function (middle);
    using custom exception TemplateModuleError
    """
    f()
    log.info("Ran function err")
    raise TemplateModuleError('Called function err')


def main():
    """
    Main (top) execution function
    """
    err()


if __name__ == '__main__':

    # configure logging facilities (stderr and/or file)
    log_config(std=True)

    warnings.warn('This is a test warning', Warning)

    # save traceback from exception to log before
    # printing out traceback and exiting
    try:
        # call main function
        main()
    except Exception as e:
        # N.B.: careful when catching Exception class,
        #       this can mask virtually any error in Python
        msg = log_trace(exception=e, level=logging.CRITICAL, log=log)
        sys.exit(msg)

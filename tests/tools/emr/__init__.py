# Copyright 2009-2012 Yelp
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
import sys
from io import BytesIO

from mrjob.emr import EMRJobRunner
from mrjob.py2 import PY2
from mrjob.py2 import StringIO

from tests.py2 import mock_stdout_or_stderr
from tests.py2 import patch
from tests.mockboto import MockBotoTestCase


class ToolTestCase(MockBotoTestCase):

    def monkey_patch_argv(self, *args):
        p = patch('sys.argv', [sys.argv[0]] + list(args))
        self.addCleanup(p.stop)
        p.start()

    def monkey_patch_stdout(self):
        p = patch('sys.stdout', mock_stdout_or_stderr())
        self.addCleanup(p.stop)
        p.start()

    def monkey_patch_stderr(self):
        p = patch('sys.stderr', mock_stdout_or_stderr())
        self.addCleanup(p.stop)
        p.start()

    def make_job_flow(self, **kwargs):
        self.add_mock_s3_data({'walrus': {}})
        kwargs.update(dict(
            conf_paths=[],
            s3_scratch_uri='s3://walrus/',
            s3_sync_wait_time=0))
        with EMRJobRunner(**kwargs) as runner:
            return runner.make_persistent_job_flow()

import logging
import unittest

import cutest

logging.basicConfig(
    format="%(asctime)s %(levelname)-7s %(threadName)s: %(message)s",
    level=logging.INFO
)


class SmokeTest(unittest.TestCase):

    def test_sample_module(self):
        from test import sample
        test_output = cutest.default_output_stream()
        runner = cutest.SerialRunner(test_output, verbosity=1)
        sample.cu.initialize()
        runner.run_model(sample.cu)

    def test_sample_suite(self):
        from test import sample
        test_output = cutest.default_output_stream()
        runner = cutest.SerialRunner(test_output, verbosity=1)
        sample.my_suite.initialize()
        runner.run_suite(sample.my_suite)

    def test_sample_tests(self):
        from test import sample
        test_output = cutest.default_output_stream()
        runner = cutest.SerialRunner(test_output, verbosity=1)
        runner.run_tests(sample.test_1.calls)

    @unittest.skip
    def test_skip(self):
        pass

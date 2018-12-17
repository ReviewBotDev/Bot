# coding=utf8
from django.test import TestCase

from blitz.bw_env.bw_script import BWAccountScript, BWScriptBase
from blitz.external_deps import SSHCallResult


class BWAccountScriptTestCase(TestCase):
    def test_run_on_sereral_baseapps_and_check_ids(self):
        BWScriptBase._SCRIPT_BASE_TEMPLATE = BWScriptBase.PAYLOAD_PLACEHOLDER
        BWAccountScript._SCRIPT_ACCOUNT_TEMPLATE = BWScriptBase.PAYLOAD_PLACEHOLDER

        script = BWAccountScript("%(dbid_list)s %(process_id)s", [1, 2, 3])
        self.assertEqual(script.data('baseapp01'), '[1, 2, 3] baseapp01')

        result1 = SSHCallResult()
        result1.output = """
            Test output start
            {} >[1, 3]<
            """.format(BWAccountScript.MISSED_ENTITY_MARKER)
        self.assertFalse(script.process_exe_result(result1))

        self.assertEqual(script.data('baseapp02'), '[1, 3] baseapp02')
        result2 = SSHCallResult()
        result2.output = """
            Test output start
            """
        self.assertTrue(script.process_exe_result(result2))
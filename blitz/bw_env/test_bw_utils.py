# coding=utf8
import os

from django.test import TestCase

from blitz.bw_env import bw_utils

class BWUtilsTestCase(TestCase):
    def test_getbaseapps_1(self):
        text = u"""
	baseapp01       on by1-wotblitz-42  0% cpu  28% mem  pid:12909 version:2.9.3
        """
        baseapps = bw_utils.get_processes(text, 'baseapp')

        self.assertEqual(baseapps, ['baseapp01'])

    def test_getbaseapps_2(self):
        text = """
	baseapp01       on by1-wotblitz-42  0% cpu  28% mem  pid:12909 version:2.9.3
	baseapp02       on by1-wotblitz-42  0% cpu  28% mem  pid:12909 version:2.9.3
        """
        baseapps = bw_utils.get_processes(text, 'baseapp')

        self.assertEqual(baseapps, ['baseapp01', 'baseapp02'])

    def test_getDataByMarker_0(self):
        data = bw_utils.get_data_by_marker('[MISSED ENTITY]', '12312 sad\n[MISSED ENTITY] >[1, 2, 3]<\nasdf sdf')

        self.assertEqual(data, [1, 2, 3])

    def test_getDataByMarker_1(self):
        data = bw_utils.get_data_by_marker('[MISSED ENTITY]', '12312 sad\n[MISSED E1NTITY] >[1, 2, 3]<\nasdf sdf')
        self.assertEqual(data, None)

    def test_getBwScriptPath_Ok(self):
        path = bw_utils.get_bw_script('server_command_template/bw_base_template.py')

        self.assertTrue(os.path.exists(path))
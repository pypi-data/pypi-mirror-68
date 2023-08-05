#!/usr/bin/python
# -*- coding: utf-8 -*-
"""File used to unit test the pacifica archive interface."""
from os.path import sep
import unittest
import mock
from pacifica.archiveinterface.__main__ import cmd, main
from .common_setup_test import SetupTearDown


class TestAIAdminCmd(unittest.TestCase, SetupTearDown):
    """Test the Posix backend archive."""

    @mock.patch('os.unlink')
    @mock.patch('os.chmod')
    def test_admin_cmd(self, mock_chmod, mock_unlink):
        """Test admin command."""
        temp_fd = open('{sep}tmp{sep}1234'.format(sep=sep), 'w')
        temp_fd.close()
        del temp_fd
        mock_unlink.return_value = 0
        mock_chmod.return_value = 0
        res = cmd(['delete', '1234'])
        mock_unlink.assert_called_with('{sep}tmp{sep}1234'.format(sep=sep))
        mock_chmod.assert_called_with('{sep}tmp{sep}1234'.format(sep=sep), 0o200)
        self.assertEqual(res, 0)

    def test_main(self):
        """Test that main works."""
        hit_exception = False
        try:
            main('--stop-after-a-moment')
        # pylint: disable=broad-except
        except Exception:
            hit_exception = True
        self.assertFalse(hit_exception)

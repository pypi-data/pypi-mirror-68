#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Tests for the git helper."""

import unittest

from l2tscaffolder.helpers import git


class GitHelperTest(unittest.TestCase):
  """Tests the git helper"""

  def testInitialize(self):
    """Tests that the helper can be initialized."""
    helper = git.GitHelper(
        'https://github.com/log2timeline/l2tdevtools.git')
    self.assertIsNotNone(helper)


if __name__ == '__main__':
  unittest.main()

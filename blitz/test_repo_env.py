from django.test import TestCase
from mock import patch

from blitz import repo_env

class RemoEnvTestCase(TestCase):
    GIT_LS_REMOTE_DATA = """
    bdccaa2779abadd79b6dc3761be472cb70d6d829	HEAD
    22b3bc9146bf0d16d4466c8ff4dbfd88625080ce	refs/heads/back_to_school
    d54e04e779d60da9c2067441c182b4073a7b16b2	refs/heads/daily_bonus_real
    fc69e00ef11fffea82ff8c1111f9573ff13d99fc	refs/heads/rareAchievements
    bdccaa2779abadd79b6dc3761be472cb70d6d829	refs/heads/trunk
    04783aff0fbedf2ef618168e14f1c5b46f52aef5	refs/pull-requests/129/from
    32161b320d53639c5aa28676c6009e2280d7d491	refs/pull-requests/129/merge
    d332b37d52a9beb03cf86dd83a44d9a6feb87c59	refs/pull-requests/167/from
    cba4fe02e38ed1e17ed7842d8064357cc0545e61	refs/pull-requests/167/merge
    df7f36816a550a197469c01d5175a487ed8efcb8	refs/tags/3.10.0
    b1e29464828607486ac89ca0917dd0b43c053f40	refs/tags/3.10.0^{}
    ba43e76bfa52c186cb288b945a73078622cdbb5e	refs/tags/3.9.0.5
    da110b6fea3f7fce506725944e12801aed6ccad2	refs/tags/3.9.0.5^{}
    b12ed468b0cbe2bddc3d9a651b1474ba8f0e966c	refs/tags/4.0.0.1
    65d90c2ae0281218d7dd5ff3214250794a0fdcf4	refs/tags/4.0.0.1^{}
    """

    @patch('blitz.repo_env._executeCommand')
    def test_doGetBranches(self, mock):
        mock.return_value = self.GIT_LS_REMOTE_DATA
        branches, pullReqs, tags = repo_env._doGetBranches('')
        self.assertEqual(branches, ['trunk', 'master', 'back_to_school', 'daily_bonus_real', 'rareAchievements'])
        self.assertEqual(pullReqs, [167, 129])
        self.assertEqual(tags, ['4.0.0.1', '3.10.0', '3.9.0.5'])

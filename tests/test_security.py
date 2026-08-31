import unittest
from apps.accounts.security.two_factor_auth import RetroTwoFactorAuth
from apps.accounts.security.rate_limiter import TokenBucketRateLimiter

class SecurityTestCase(unittest.TestCase):
    def test_token_generation(self):
        sec = RetroTwoFactorAuth(secret="test-sec")
        tok = sec.generate_token("user-42")
        self.assertEqual(len(tok), 64)

    def test_rate_limiting(self):
        limiter = TokenBucketRateLimiter()
        allowed = limiter.rate_limit_bucket_evaluator_0("client-ip-1", max_tokens=5)
        self.assertTrue(allowed)

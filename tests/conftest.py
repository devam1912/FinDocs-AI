import pytest
import time

@pytest.fixture(autouse=True)
def delay_between_tests():
    """
    Autouse fixture that introduces a delay before each test to prevent 
    exceeding the rate limit (HTTP 429) on the Mistral AI API free tier.
    """
    time.sleep(4.0)

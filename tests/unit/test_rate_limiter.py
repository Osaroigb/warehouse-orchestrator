import time
import pytest
from unittest.mock import MagicMock
from app.utils.rate_limiting import RateLimiter
from app.utils.errors import RateLimitExceededError


@pytest.fixture
def mock_request():
    mock = MagicMock()
    mock.client.host = "127.0.0.1"
    return mock


@pytest.mark.asyncio
async def test_first_request_passes(mock_request):
    limiter = RateLimiter(limit=2, reset_time=60)
    assert limiter.requests == {}
    assert await limiter.__call__(mock_request) is None


@pytest.mark.asyncio
async def test_request_within_limit(mock_request):
    limiter = RateLimiter(limit=2, reset_time=60)
    now = time.time()
    limiter.requests[mock_request.client.host] = {'count': 1, 'time': now}
    assert await limiter.__call__(mock_request) is None


@pytest.mark.asyncio
async def test_rate_limit_exceeded_raises(mock_request):
    limiter = RateLimiter(limit=2, reset_time=60)
    now = time.time()
    limiter.requests[mock_request.client.host] = {'count': 2, 'time': now}
    with pytest.raises(RateLimitExceededError):
        await limiter.__call__(mock_request)


@pytest.mark.asyncio
async def test_rate_limit_reset_after_window(mock_request):
    limiter = RateLimiter(limit=2, reset_time=1)
    past_time = time.time() - 2
    limiter.requests[mock_request.client.host] = {'count': 2, 'time': past_time}
    assert await limiter.__call__(mock_request) is None
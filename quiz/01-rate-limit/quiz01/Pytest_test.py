import pyperf
from core.views import RateLimitAPI
setup = "from core.views import RateLimitAPI"
runner = pyperf.Runner()
runner.timeit(name="Get test",
              stmt="RateLimitAPI.get",
              setup=setup)
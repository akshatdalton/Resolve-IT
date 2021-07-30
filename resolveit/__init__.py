from resolveit.app import ResolveIT
from resolveit.settings import do_suppress_animation

do_suppress_animation()

# Expose `ResolveIT` as the context manager.
debug = ResolveIT

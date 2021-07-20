import os
import sys

RESOLVEIT_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "../")
sys.path.append(RESOLVEIT_PATH)

from src.resolveit import ResolveIT

# Expose `ResolveIT` as the context manager.
debug = ResolveIT

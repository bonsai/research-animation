"""Initialize the DISNEY-QUOTES corpus DB (schema + seed data)."""

import os
import sys

here = os.path.dirname(os.path.abspath(__file__))
corpus_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(corpus_dir, 'corpus'))

from seed import main as seed_main

if __name__ == '__main__':
    seed_main()

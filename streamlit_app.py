import sys
import os

# Force add root to path
root = os.path.dirname(os.path.abspath(__file__))
if root not in sys.path:
    sys.path.insert(0, root)

# Now run the actual app
exec(open(os.path.join(root, "app.py")).read())
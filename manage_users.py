"""List or delete registered people.
python manage_users.py list
python manage_users.py delete "Ali"
"""
import sys
from collections import Counter

from utils import load_db, save_db

faces, names = load_db()
if faces is None:
    raise SystemExit("No registered people.")

cmd = sys.argv[1] if len(sys.argv) > 1 else "list"
if cmd == "list":
    for n, c in Counter(names).items():
        print(f"{n}: {c} samples")
elif cmd == "delete" and len(sys.argv) > 2:
    target = sys.argv[2]
    keep = [i for i, n in enumerate(names) if n != target]
    if len(keep) == len(names):
        raise SystemExit(f"'{target}' not found.")
    save_db([faces[i] for i in keep], [names[i] for i in keep])
    print(f"Deleted '{target}'.")
else:
    print(__doc__)

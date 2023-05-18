import sys, os
import asyncio

sys.path.append(os.path.abspath(os.path.dirname(__file__)))

from app import app, initialize


if __name__ == "__main__":
    # Change to False to ignore any breakpoints/pdb traces, etc.
    asyncio.get_event_loop().run_until_complete(initialize())
    app.run(debug=True)

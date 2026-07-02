#!/usr/bin/env python3
"""
🎯 PROBLEM 15: Async Function
================================

TODO: Create an async function 'fetch_data' that:
- Simulates a delay using asyncio.sleep(1)
- Returns "data fetched"

Then call it using asyncio.run()

Remember:
- async def → defines async function
- await → waits for async operation
- asyncio.run() → runs async code

Expected output:
    Fetching...
    data fetched
"""

import asyncio


# Your code here:
async def fetch_data():
    print("..fetching")
    await asyncio.sleep(3)
    return "data fetched"


data = asyncio.run(fetch_data())

print(data)

import asyncio

from icon_governance.db import init_db

def test_init_db():
    asyncio.run(init_db())

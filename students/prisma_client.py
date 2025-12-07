from prisma import Prisma
from contextlib import asynccontextmanager

# Legacy global (unused by views after refactor); kept to avoid import errors
db = Prisma()


@asynccontextmanager
async def prisma_session():
	client = Prisma()
	await client.connect()
	try:
		yield client
	finally:
		try:
			await client.disconnect()
		except Exception:
			pass

import asyncio

from hyper_crawler.core import execute_from_command_line


async def main():
    await execute_from_command_line()


loop = asyncio.get_event_loop()
loop.run_until_complete(main())
loop.run_until_complete(asyncio.sleep(1))
loop.close()

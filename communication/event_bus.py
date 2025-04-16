#!/usr/bin/env python3
"""
Event Bus Module

Connects asynchronously to the local NATS server for inter-module messaging.
Subscribes to the 'updates' topic and publishes a test message.
Logs all activity to ${PROJECT_BASE_DIR}/logs/event_bus.log.
"""
import asyncio, logging
from pathlib import Path
from nats.aio.client import Client as NATS
logging.basicConfig(
  level=logging.INFO,
  format="%(asctime)s - %(levelname)s - %(message)s",
  filename=str(Path(__file__).parent.parent / "logs/event_bus.log"),
  filemode="a"
)
async def run(loop):
    nc = NATS()
    try:
        await nc.connect("localhost:4222", loop=loop)
        logging.info("Connected to NATS at localhost:4222")
    except Exception as e:
        logging.error(f"NATS connection error: {e}")
        return
    async def handler(msg):
        subject = msg.subject
        data = msg.data.decode()
        logging.info(f"Received on '{subject}': {data}")
        print(f"Message on '{subject}': {data}")
    await nc.subscribe("updates", cb=handler)
    await asyncio.sleep(2)
    await nc.publish("updates", b"Hello from Event Bus!")
    logging.info("Published test message on 'updates'")
    while True:
        await asyncio.sleep(1)
if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    try:
        loop.run_until_complete(run(loop))
    except Exception as e:
        logging.error(f"Event bus error: {e}")
    finally:
        loop.close()

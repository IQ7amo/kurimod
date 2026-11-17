import asyncio
import unittest
from types import SimpleNamespace

import pyrogram.dispatcher

from kurimod.listen.client import ListenerAwareQueue


class DispatcherCompatibilityTests(unittest.TestCase):
    def test_handler_worker_accepts_kurigram_no_argument_call(self):
        dispatcher = object.__new__(pyrogram.dispatcher.Dispatcher)
        dispatcher.updates_queue = asyncio.Queue()
        dispatcher.updates_queue.put_nowait(None)

        dispatcher.handler_worker()

    def test_loop_state_rebuild_preserves_listener_aware_queue(self):
        dispatcher = object.__new__(pyrogram.dispatcher.Dispatcher)
        dispatcher.client = SimpleNamespace(loop=None)
        dispatcher.updates_queue = asyncio.Queue()

        dispatcher._rebuild_loop_bound_state()

        self.assertIsInstance(dispatcher.updates_queue, ListenerAwareQueue)


class ListenerAwareQueueCompatibilityTests(unittest.IsolatedAsyncioTestCase):
    async def test_pump_uses_running_loop_without_client_loop_attribute(self):
        queue = ListenerAwareQueue(SimpleNamespace(), asyncio.Queue())
        queue.input_queue.put_nowait(None)

        queue.ensure_pump()
        await queue.pump_task

        self.assertIsNone(await queue.get())
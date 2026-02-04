"""
Event Bus - Event-driven communication system
"""

from typing import Callable, Dict, List, Any
from collections import defaultdict
from asyncio import create_task
import asyncio


class Event:
    """Event object"""

    def __init__(self, type: str, data: Dict[str, Any] = None):
        self.type = type
        self.data = data or {}
        self.timestamp = None

    def __repr__(self):
        return f"Event(type={self.type}, data={self.data})"


class EventBus:
    """Event bus for pub/sub communication"""

    def __init__(self):
        self._listeners: Dict[str, List[Callable]] = defaultdict(list)
        self._async_listeners: Dict[str, List[Callable]] = defaultdict(list)

    def subscribe(self, event_type: str, callback: Callable):
        """Subscribe to synchronous event"""
        self._listeners[event_type].append(callback)

    def subscribe_async(self, event_type: str, callback: Callable):
        """Subscribe to asynchronous event"""
        self._async_listeners[event_type].append(callback)

    def unsubscribe(self, event_type: str, callback: Callable):
        """Unsubscribe from event"""
        if callback in self._listeners[event_type]:
            self._listeners[event_type].remove(callback)

    def publish(self, event: Event):
        """Publish event to synchronous subscribers"""
        for callback in self._listeners[event.type]:
            try:
                callback(event)
            except Exception as e:
                print(f"Error in event handler: {e}")

    def publish_sync(self, event: Event):
        """Publish event synchronously (alias for publish)"""
        self.publish(event)

    async def publish_async(self, event: Event):
        """Publish event to asynchronous subscribers"""
        tasks = []

        for callback in self._async_listeners[event.type]:
            task = create_task(callback(event))
            tasks.append(task)

        if tasks:
            await asyncio.gather(*tasks, return_exceptions=True)

    async def publish(self, event: Event):
        """Publish event to both sync and async subscribers"""
        # First notify sync subscribers
        for callback in self._listeners[event.type]:
            try:
                callback(event)
            except Exception as e:
                print(f"Error in sync event handler: {e}")

        # Then notify async subscribers
        await self.publish_async(event)

    def clear(self):
        """Clear all subscribers"""
        self._listeners.clear()
        self._async_listeners.clear()

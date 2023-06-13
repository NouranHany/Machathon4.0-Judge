"""
Module containing the CollisionManager class to manage the collision events from
multiple checkpoints in CoppeliaSim
"""
import time
import asyncio
import threading
from typing import Callable

# pylint: disable=import-error
import websockets


class ConnectionFailedException(Exception):
    """
    Exception raised when the connection to CoppeliaSim fails
    Usually this means that CoppeliaSim is not running
    """


class ConnectionClosedException(Exception):
    """
    Exception raised when the connection to CoppeliaSim is closed
    """


class WebSocketManager:
    """
    Class used to manage a web socket connection to a checkpoint in CoppeliaSim

    Parameters
    ----------
    host: str, default="localhost"
        Host address of the CoppeliaSim websocket server for this checkpoint
    port: int, default=9000
        Port number of the CoppeliaSim websocket server for this checkpoint
    """

    def __init__(self, host="localhost", port=9000):
        self.address = f"ws://{host}:{port}"
        self.thread = None

    async def await_collision(self, callback: Callable) -> None:
        """
        An async function that waits for a collision event from CoppeliaSim

        Parameters
        ----------
        callback : Callable
            A function to be called when a collision event is received

        Raises
        ------
        Exception
            Couldn't connect to CoppeliaSim, make sure it is opened
        Exception
            Connection to CoppeliaSim closed
        """
        try:
            async with websockets.connect(self.address) as websocket:
                await websocket.recv()
                callback()
        except ConnectionRefusedError as exp:
            raise ConnectionFailedException(
                "Couldn't connect to CoppeliaSim, make sure it is opened"
            ) from exp
        except websockets.exceptions.ConnectionClosedError as exp:
            raise ConnectionClosedException("Connection to CoppeliaSim closed") from exp

    def run_async_in_thread(
        self, loop: asyncio.AbstractEventLoop, callback: Callable
    ) -> None:
        """
        Runs the await_collision function in a new thread

        Parameters
        ----------
        loop : AbstractEventLoop
            The event loop to run the await_collision function in
        callback : Callable
            A function to be called when a collision event is received
        """
        asyncio.set_event_loop(loop)
        loop.run_until_complete(self.await_collision(callback))

    def set_callback(self, callback: Callable) -> None:
        """
        Sets the callback function to be called when a collision event is received
        Creates a thread and starts listening for collision events

        Parameters
        ----------
        callback : Callable
            A function to be called when a collision event is received
        """
        new_loop = asyncio.new_event_loop()
        self.thread = threading.Thread(
            target=self.run_async_in_thread, args=(new_loop, callback)
        )
        self.thread.daemon = True
        self.thread.start()

    def close(self) -> None:
        """
        Closes the web socket connection by joining the thread
        """
        self.thread._stop()  # pylint: disable=protected-access


class CollisionManager:
    """
    Class used to manage the collision events from multiple checkpoints in CoppeliaSim
    """

    def __init__(self):
        self.ckpt_managers = [WebSocketManager(port=9000), WebSocketManager(port=9001)]

        self.ckpts_collided = [False, False]

        self.ckpt_managers[0].set_callback(lambda: self.ckpt_callback(0))
        self.ckpt_managers[1].set_callback(lambda: self.ckpt_callback(1))

    def ckpt_callback(self, ckpt_id: int) -> None:
        """
        Callback function to be called when a collision event is received from a checkpoint

        Parameters
        ----------
        ckpt_id : int
            The id of the checkpoint that received the collision event
        """
        self.ckpts_collided[ckpt_id] = True
        self.ckpt_managers[ckpt_id] = WebSocketManager(port=9000 + ckpt_id)

        # Sleep to ensure the judge has time to read the collision event
        time.sleep(0.1)

        # Reset the checkpoint websocket manager
        self.ckpts_collided[ckpt_id] = False
        self.ckpt_managers[ckpt_id].set_callback(lambda: self.ckpt_callback(ckpt_id))

    def is_collision(self, ckpt_id: int) -> bool:
        """
        Checks if a collision event has been received from any checkpoint

        Parameters
        ----------
        checkpoint_id : int
            Id of the checkpoint to detect collision with
        Returns
        -------
        boolean
            whether collision occurs or not
        """
        return self.ckpts_collided[ckpt_id]

    def close(self) -> None:
        """
        Closes the web socket connections by joining the threads
        """
        for manager in self.ckpt_managers:
            try:
                manager.close()
            except:  # pylint: disable=bare-except
                pass

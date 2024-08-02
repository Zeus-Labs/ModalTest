import asyncio
import grpc
import grpc.aio
import streaming_pb2
import streaming_pb2_grpc
import time
import json
from loguru import logger
import sys

logger.remove(0)
logger.add(sys.stderr, level="DEBUG")

class StreamingClient:
    def __init__(self, host="localhost", port=50051, retry_delay_seconds=0.25):
        self._host = host
        self._port = port
        self._channel = None
        self._stub = None
        self._retry_delay_seconds = retry_delay_seconds

    async def connect(self):
        logger.debug("begin connect")


        while True:
            logger.debug("Setting up channel and stub")
            self._channel = grpc.aio.insecure_channel(
                f"{self._host}:{self._port}",
            )
            self._stub = streaming_pb2_grpc.StreamingServiceStub(self._channel)
            logger.debug("Finished setting up channel and stub")

            try:
                await asyncio.wait_for(self._channel.channel_ready(), timeout=self._retry_delay_seconds)
                logger.debug("gRPC connection established successfully.")
                break
            except asyncio.TimeoutError:
                logger.debug(f"Connection timed out after {self._retry_delay_seconds} seconds")
            except grpc.aio.AioRpcError as e:
                logger.error(f"Failed to establish connection: {e}")
                raise

            logger.debug("Closing channel.")
            if self._channel:
                await self._channel.close()
            logger.debug("Finished closing channel.")


    async def stream_audio_video(self):
        if not self._stub:
            logger.debug("Client not connected. Please connect first.")
            return

        async def request_iterator():
            while True:
                dummy_audio_data = b'dummy_audio_data'
                yield streaming_pb2.AudioRequest(audio_data=dummy_audio_data)
                await asyncio.sleep(1)

        try:
            async for response in self._stub.StreamAudioVideo(request_iterator()):
                logger.debug(f"Received video data of length: {len(response.video_data)}")
        except grpc.aio.AioRpcError as e:
            logger.debug(f"RPC error: {e}")

    async def close(self):
        if self._channel:
            await self._channel.close()
            logger.debug("gRPC channel closed.")

async def main():
    client = StreamingClient(retry_delay_seconds=0.5)  # Retry every 0.5 seconds
    try:
        await client.connect()
        await client.stream_audio_video()
    except Exception as e:
        logger.error(f"An error occurred: {e}")
    finally:
        await client.close()

if __name__ == '__main__':
    asyncio.run(main())
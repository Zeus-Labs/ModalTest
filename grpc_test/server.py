print("Inside server.py")
from loguru import logger
import sys
logger.remove(0)
logger.add(sys.stderr, level="DEBUG")
logger.debug("server logger set up")

import asyncio
import grpc
import streaming_pb2
import streaming_pb2_grpc

class StreamingServiceServicer(streaming_pb2_grpc.StreamingServiceServicer):
    def __init__(self):
        super().__init__()

    async def StreamAudioVideo(self, request_iterator, context):
        async for request in request_iterator:
            # Process the incoming audio request (not implemented in this example)
            logger.debug("Received audio data of length:", len(request.audio_data))
            dummy_video_data = b'dummy_video_data'
            yield streaming_pb2.VideoResponse(video_data=dummy_video_data)

async def serve():
    server = grpc.aio.server()
    streaming_pb2_grpc.add_StreamingServiceServicer_to_server(
        StreamingServiceServicer(), server)
    server.add_insecure_port("[::]:50051")
    await server.start()
    logger.debug('Server started. Listening on port 50051.')
    await server.wait_for_termination()

if __name__ == '__main__':
    asyncio.run(serve())
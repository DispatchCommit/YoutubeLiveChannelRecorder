import atexit
from ..log import verbose
from ..encoder import Encoder


class SharableHandler:
    def get(self, variable_name):
        try:
            return getattr(self, variable_name)
        except AttributeError:
            return None

    def set(self, variable_name, value):
        return setattr(self, variable_name, value)


class ChannelInfo_template(SharableHandler):
    """
    Holds as a template for other platforms. (ONLY JUST ADDED FOR TWITCH SUPPORT)

    # Channel Data
    :type channel_id: str, None
    :type channel_name: str

    # STREAM DATA
    # :type video_id: str, None
    :type title: str
    :type StreamInfo: dict, None

    # SERVER VARIABLES
    :type stop_heartbeat: bool

    # USED FOR RECORDING.
    :type EncoderClass: Encoder

    # Server-type Variables
    :type live_streaming, bool

    # USED FOR UPLOADING.
    :type video_location: str

    """

    # USED FOR SERVER
    crashed_traceback = None
    live_streaming = None

    # Channel Data
    channel_id = None
    channel_name = None

    # VIDEO DATA
    title = None
    StreamInfo = None  # DICT THAT HOLDS STREAM URLS

    # USED FOR UPLOADING
    video_location = None

    # SERVER VARIABLES
    stop_heartbeat = False

    # USED FOR RECORDING
    EncoderClass = Encoder()

    # USED FOR UPLOADING TO HOLD MORE THAN ONE RECORDING.
    video_list = {}

    def __init__(self, channel_id, SharedVariables=None, cachedDataHandler=None, queue_holder=None):
        self.channel_id = channel_id
        self.SharedVariables = SharedVariables
        self.cachedDataHandler = cachedDataHandler
        self.queue_holder = queue_holder

    def registerCloseEvent(self):
        atexit.register(self.stop_recording)

    # USED FOR THE CLOSE EVENT AND STUFF.
    def stop_recording(self):
        if self.EncoderClass is not None:
            self.EncoderClass.stop_recording()
        self.stop_heartbeat = True

    def loadVideoData(self):
        pass

    def updateVideoData(self):
        pass

    def start_heartbeat_loop(self):
        pass

    def add_youtube_queue(self):
        """

        To add videos to be uploaded in the YouTube Queue.

        """
        if len(self.video_list) != 0:
            if self.queue_holder:
                verbose("Adding streams to youtube upload queue.")
                self.queue_holder.addQueue(self.video_list)
                self.video_list.clear()

    def is_live(self):
        pass

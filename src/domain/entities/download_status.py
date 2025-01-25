from enum import Enum
from dataclasses import dataclass
from datetime import datetime


class DownloadState(Enum):
    PENDING = "pending"
    DOWNLOADING = "downloading"
    PROCESSING = "processing"
    COMPLETED = "completed"
    ERROR = "error"


@dataclass
class DownloadStatus:
    id: str
    state: DownloadState
    progress: float = 0.0  # 0 a 100
    error_message: str = ""
    start_time: datetime = None
    end_time: datetime = None

    def __post_init__(self):
        if self.start_time is None:
            self.start_time = datetime.now()

    def complete(self):
        self.state = DownloadState.COMPLETED
        self.progress = 100.0
        self.end_time = datetime.now()

    def fail(self, error_message: str):
        self.state = DownloadState.ERROR
        self.error_message = error_message
        self.end_time = datetime.now()

    def update_progress(self, progress: float):
        self.progress = min(max(progress, 0.0), 100.0)

    @property
    def duration(self) -> float:
        """Retorna la duración en segundos"""
        if self.end_time and self.start_time:
            return (self.end_time - self.start_time).total_seconds()
        return 0.0
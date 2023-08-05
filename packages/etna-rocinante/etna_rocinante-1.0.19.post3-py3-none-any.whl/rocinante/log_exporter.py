import io
import json
import logging
from typing import Any, Dict


class LogExporter:
    """
    Class recording job logs and exporting them through RabbitMQ
    """

    def __init__(self):
        self._buffer = io.StringIO()
        self.log_handler = logging.StreamHandler(self._buffer)

    def _clear_buffer(self):
        self._buffer.truncate(0)
        self._buffer.seek(0)

    def start_recording(self):
        """
        Start recording logged data for an upcoming export
        """
        self._clear_buffer()

    def send(
            self,
            channel,
            *,
            info: Dict[str, Any],
            retries_count: int,
            status: str = None,
            message: str = None
    ):
        """
        Send the recorded data

        :param channel:             the RabbitMQ channel to use to send logs
        :param info:                the job information
        :param retries_count:       the number of times the job was retried
        :param status:              the status of the job
        :param message:             the message describing the result of the job
        """
        result = {
            "module_id": info['module_id'],
            "activity_id": info['activity_id'],
            "task_name": info["stage"],
            "group_id": info['group_id'],
            "leader_login": info['leader'],
            "request_date": info['request_date'],
            "status": status or "success",
            "retries": retries_count,
            "feedback": message or "",
            "logs": ""
        }

        self.log_handler.flush()
        result["logs"] = self._buffer.getvalue()
        self._clear_buffer()
        channel.basic_publish(
            exchange='moulinette',
            routing_key='moulinette_result.log',
            body=json.dumps(result)
        )

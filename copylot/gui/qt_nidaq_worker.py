from PyQt5.QtCore import QRunnable, pyqtSlot

from copylot.gui.qt_worker_signals import WorkerSignals
from copylot.hardware.alternative_control import NIdaq


class NIDaqWorker(QRunnable):
    def __init__(self, program_type, view, channel, parameters, *args, **kwargs):
        super(NIDaqWorker, self).__init__()

        self.program_type = program_type
        self.view = view
        self.channel = channel
        self.parameters = parameters
        self.args = args
        self.kwargs = kwargs
        self.signals = WorkerSignals()

        self.daq_card = NIdaq(self, **parameters)
        self.thread_running = True

    @pyqtSlot()
    def run(self):
        try:
            self.signals.running.emit()
            # self.fn(self, *self.args, **self.kwargs)
            if self.program_type == "live":
                self.daq_card.select_view(self.view)
                self.daq_card.select_channel_remove_stripes(self.channel)
            elif self.program_type == "timelapse":
                self.daq_card.acquire_stacks(channels=self.channel, view=self.view)

        finally:
            self.signals.finished.emit()

    def stop(self):
        self.daq_card.stop_now = True
        # self.thread_running = False

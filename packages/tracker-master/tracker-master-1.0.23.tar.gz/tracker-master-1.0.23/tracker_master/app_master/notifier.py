import logging
import threading
from socket import timeout

from pyzabbix.sender import ZabbixSender, ZabbixMetric

from tracker_master import config as CFG
from tracker_master.app_master.master import TrackerMaster
from tracker_master.model.app_model import Message, MonitoringName
from tracker_master.zbx_client import Fields


class MessageListener:

    def receive_message(self, msg_list):
        pass


class ZabbixNotifier(MessageListener):

    def __init__(self, tracker_master):
        assert isinstance(tracker_master, TrackerMaster)
        self.host_name = tracker_master.get_master().get_uniq_master_name()
        assert isinstance(tracker_master, TrackerMaster)
        self.tracker_master = tracker_master
        self.logger = logging.getLogger(ZabbixNotifier.__name__)

    def receive_message(self, msg_list):
        zbx_metrics_batch = []
        for msg in msg_list:
            assert isinstance(msg, Message)
            slave = self.tracker_master.get_master().get_slave(msg.hw_id)
            device_name = Fields.ZBX_SLAVE_NAME_PREF + str(slave.zbx_slave_number)
            msg_key_name = device_name + '.' + msg.type.name.lower()
            charge_key_name = device_name + '.' + MonitoringName.CHARGE.value
            zbx_metrics_batch.append(ZabbixMetric(self.host_name, msg_key_name, 1))
            zbx_metrics_batch.append(ZabbixMetric(self.host_name, charge_key_name, msg.charge))

        sending_thread = ZabbixSenderThread(zbx_metrics_batch)
        self.logger.debug('Active threads %s' % threading.active_count()) # todo move to separate Thread
        sending_thread.start()


class ZabbixSenderThread(threading.Thread):

    def __init__(self, batch):
        threading.Thread.__init__(self)
        self.logger = logging.getLogger(ZabbixSenderThread.__name__)
        self.batch = batch
        self.sender = ZabbixSender(CFG.zbx_sender_url())

    def run(self) -> None:
        try:
            self.logger.debug('Send %s metrics to Zabbix' % len(self.batch))
            resp = self.sender.send(self.batch)
            self.logger.debug('Response: %s' % resp)
        except timeout:
            self.logger.error('Lost connection with Zabbix server')
            self.logger.error('Lost %s messages: %s' % (len(self.batch), self.batch))
            # todo WARN now just lost the data
            pass
        except Exception as ex:
            if 'gaierror' in ex.args[0]:
                self.logger.warning('Lost connection with Network')
            else:
                self.logger.error(ex)
            self.logger.error('Lost %s messages: %s' % (len(self.batch), self.batch))




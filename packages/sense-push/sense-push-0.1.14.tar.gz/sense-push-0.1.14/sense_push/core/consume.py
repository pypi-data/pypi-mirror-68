import sense_core as sd
from sense_push.common import *


class SensePushConsumer(object):

    def __init__(self, handler, table=None, retry_times=0, check_log_receive=None):
        super(SensePushConsumer, self).__init__()
        self.table = table
        self.handler = handler
        self.retry_times = retry_times
        self.check_log_receive = check_log_receive

    @sd.try_catch_exception
    def consume_queue(self, label=None, config_info=None, queue=None):
        sd.log_info("start consume_queue {}".format(queue))
        consumer = sd.RabbitConsumer2(topic=queue, label=label, config_info=config_info, retry_times=self.retry_times)
        consumer.consume_loop(self.handle_message)

    def handle_message(self, message):
        message2 = sd.load_json(message)
        if not message2:
            sd.log_error("invalid message for {}".format(message))
            return
        table = message2.get('table')
        if self.table and self.table != table:
            return
        if not self.check_log_receive or self.check_log_receive(table):
            sd.log_info("start _handle_message0 {0}".format(message))
        action = message2.get('action')
        database = message2.get('db')
        data = message2.get('data')
        if action == PUSH_ACTION_INSERT:
            self.insert(database=database, table=table, data=data)
        elif action == PUSH_ACTION_UPDATE:
            after = data.get('after')
            if after:
                data = after
            self.update(database=database, table=table, data=data)
        elif action == PUSH_ACTION_DELETE:
            self.delete(database=database, table=table, data=data)
        else:
            self.handle_custom(database=database, table=table, data=data, action=action)

    def insert(self, database, table, data):
        self.handler.insert(database, table, data)

    def update(self, database, table, data):
        self.handler.update(database, table, data)

    def delete(self, database, table, data):
        self.handler.delete(database, table, data)

    def handle_custom(self, database, table, data, action):
        self.handler.handle_custom(database, table, data, action)

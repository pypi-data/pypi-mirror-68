from sense_push.common import *


class DumbPushDataHandler(object):

    def insert(self, database, table, data):
        self.callback_handle(PUSH_ACTION_INSERT, database, table, data)

    def update(self, database, table, data):
        self.callback_handle(PUSH_ACTION_UPDATE, database, table, data)

    def delete(self, database, table, data):
        self.callback_handle(PUSH_ACTION_DELETE, database, table, data)

    def handle_custom(self, database, table, data, action):
        self.callback_handle(action, database, table, data)

    def callback_handle(self, action, database, table, data):
        pass

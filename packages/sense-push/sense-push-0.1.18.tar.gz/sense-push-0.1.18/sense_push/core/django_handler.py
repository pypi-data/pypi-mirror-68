import sense_core as sd
from django.db.utils import IntegrityError
from sense_push.common import *
from django.db import connections


class DjangoPushDataHandler(object):

    def __init__(self, model_map=None, models=None):
        if model_map:
            self.model_map = self._convert_model_map(model_map)
        else:
            self.model_map = self._build_model_map(models)
        self.model_field_map = dict()

    def add_model_config(self, model, primary=None, fields=None, exclude_fields=None, table=None):
        if not primary:
            primary = ['id']
        config = {
            'model': model,
            'primary': primary,
        }
        if fields:
            config['fields'] = fields
        if exclude_fields:
            config['exclude_fields'] = exclude_fields
        if not table:
            table = model._meta.db_table
        self.model_map[table] = config

    def _build_model_map(self, models):
        result = dict()
        for model in models:
            result[model._meta.db_table] = {
                'model': model,
                'primary': ['id'],
            }
        return result

    def _convert_model_map(self, model_map):
        result = dict()
        for k, v in model_map.items():
            if type(v) != dict:
                result[k] = {
                    'model': v,
                }
            else:
                result[k] = v
            primary = v.get('primary')
            if not primary:
                v['primary'] = ['id']
        if sd.is_debug():
            sd.log_info("model_map={}".format(result))
        return result

    def get_model_key(self, database, table):
        return "{0}_{1}".format(database, table)

    def get_model_fields(self, model):
        fields = self.model_field_map.get(model)
        if fields:
            return fields
        fields = set([field.name for field in model._meta.get_fields()])
        self.model_field_map[model] = fields
        return fields

    def _get_model(self, database, table):
        key = self.get_model_key(database, table)
        model = self.model_map.get(key)
        if model:
            return model
        return self.model_map.get(table)

    def insert(self, database, table, data):
        self._insert0(database, table, data, "insert")
        self.callback_handle(PUSH_ACTION_INSERT, database, table, data)

    def before_update(self, database, table, data):
        return True

    def _insert0(self, database, table, data, action):
        data2 = None
        try:
            model_item = self._get_model(database, table)
            if not model_item:
                sd.log_info("skip table {}".format(table))
                return
            if not self.before_update(database, table, data):
                return
            model = model_item['model']
            fields = model_item.get('fields')
            if not fields:
                fields = self.get_model_fields(model)
            else:
                fields = set(fields)
            exclude_fields = model_item.get('exclude_fields')
            if exclude_fields:
                for field in exclude_fields:
                    fields.discard(field)
            data2 = self._build_update_data(data, model_item, fields)
            if not data2:
                return
            model.objects.update_or_create(**data2)
            sd.log_info(
                action + " data table={0} data={1}".format(table, self.build_primary_keys(data, model_item['primary'])))
        except IntegrityError as ex:
            sd.log_warn("IntegrityError for table={0} data2={1} msg={2}".format(table, data2, str(ex)))
        except Exception as ex:
            self.close_model_connection()
            sd.log_exception(ex)
            sd.log_error("execption for table={0} data2={1} action={2}".format(table, data2, action))
            sd.sleep(1)
            raise ex

    def update(self, database, table, data):
        after = data.get('after')
        if after and type(after) == dict:
            data = after
        self._insert0(database, table, data, "update")
        self.callback_handle(PUSH_ACTION_UPDATE, database, table, data)

    def _build_update_data(self, data, model_item, fields):
        data2 = dict(data)
        res = self.build_primary_keys(data2, model_item['primary'])
        if not res:
            sd.log_error("build_primary_keys failed for data={0} primary={1}".format(data, model_item['primary']))
            return None
        data2 = self.build_field_keys(data2, fields)
        res = self.build_update_params(res, data2)
        return res

    def build_update_params(self, res, data):
        res['defaults'] = data
        return res

    def build_field_keys(self, data, fields):
        res = {}
        for key, val in data.items():
            if key not in fields:
                continue
            res[key] = val
        return res

    def build_primary_keys(self, data, primary_keys):
        res = {}
        for key in primary_keys:
            val = data.get(key)
            if val is None:
                return None
            res[key] = val
        return res

    def before_delete(self, database, table, data):
        return True

    def delete(self, database, table, data):
        try:
            model_item = self._get_model(database, table)
            if not model_item:
                return
            if not self.before_delete(database, table, data):
                return
            model = model_item['model']
            data2 = dict(data)
            res = self.build_primary_keys(data2, model_item['primary'])
            if not res:
                sd.log_error("build_primary_keys failed for data={0} primary={1}".format(data, model_item['primary']))
                return
            model.objects.filter(**res).delete()
            sd.log_info("delete table={0} primary={1}".format(table, model_item['primary']))
            self.callback_handle(PUSH_ACTION_DELETE, database, table, data)
        except Exception as ex:
            self.close_model_connection()
            sd.log_exception(ex)
            sd.log_error("delete error table={} data={}".format(table, data))
            sd.sleep(1)

    def callback_handle(self, action, database, table, data):
        pass

    def handle_custom(self, database, table, data, action):
        self.callback_handle(action, database, table, data)

    @sd.try_catch_exception
    def close_model_connection(self):
        connections.close_all()

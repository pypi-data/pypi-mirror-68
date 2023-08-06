import six
import time

from threading import Thread
from sys import stdout

DK_ACTIVE_SERVING_WATCHER_SLEEP_TIME = 5


class DKActiveServingWatcherSingleton(object):
    __shared_state = {}
    watcher = None
    keep_running = True
    sleep_time = DK_ACTIVE_SERVING_WATCHER_SLEEP_TIME

    def __init__(self):
        self.__dict__ = self.__shared_state
        if self.watcher is None:
            self.watcher = DKActiveServingWatcher()

    def start_watcher(self):
        self.keep_running = True
        return self.watcher.start_watcher()

    def wait_until_watcher_complete(self):
        self.watcher.wait_until_watcher_complete()

    def get_watcher(self):
        return self.watcher

    def get_sleep_time(self):
        return self.sleep_time

    def set_sleep_time(self, st):
        self.sleep_time = st

    def set_api(self, api):
        self.watcher.set_api(api)

    def set_formatter(self, formatter):
        self.watcher.set_formatter(formatter)

    def set_kitchen(self, kitchen_name):
        self.watcher.set_kitchen(kitchen_name)

    def should_run(self):
        return self.keep_running

    def stop_watcher(self):
        self.keep_running = False

    def print_serving_summary(self, serving):
        self.watcher.print_serving_summary(serving)


# Only one watcher runs  ... run and done.
def make_watcher_thread(watcher, *args):
    if watcher is None or isinstance(watcher, DKActiveServingWatcher) is False:
        print('make_watcher_thread bad watcher')
        return
    # print 'Starting watcher make thread'
    while DKActiveServingWatcherSingleton().should_run() is True:
        # print ' calling watcher.watch()'
        watcher.watch()
        time.sleep(DKActiveServingWatcherSingleton().get_sleep_time())
    # print 'Ending watcher make thread 2'


class DKActiveServingWatcher(object):
    _time = 'last-update-time'

    def __init__(self, api=None, kn=None, fmt=None):
        self.run_thread = None
        self._api = api
        self._kitchen_name = kn
        self._formatter = fmt

    def get_run_thread(self):
        return self.run_thread

    def set_formatter(self, formatter):
        self._formatter = formatter

    def set_api(self, api):
        self._api = api

    def set_kitchen(self, kitchen_name):
        self._kitchen_name = kitchen_name

    def start_watcher(self):
        if self._api is None or self._kitchen_name is None:
            print(
                'DKActiveServingWatcher: start_making_watcher failed requires api and kitchen name'
            )
            return False
        try:
            self.run_thread = Thread(
                target=make_watcher_thread, args=(self, 1), name='DKActiveServingWatcher'
            )
            self.run_thread.start()
        except Exception as e:
            print(f'DKActiveServingWatcher: start_making_watcher exception {e}')
            return False
        return True

    def wait_until_watcher_complete(self):
        try:
            self.run_thread.join()
        except Exception as e:
            print(f'DKActiveServingWatcher: wait_until_watcher_complete exception {e}')
            return False

    def watch(self):
        cache = DKActiveServingCache().get_cache()
        print('watching ...')
        rc = self._api.orderrun_detail(self._kitchen_name, {'summary': True})
        if rc.ok() and rc.get_payload() is not None:
            payload = rc.get_payload()['servings']
            for serving in payload:
                if isinstance(serving, dict) is True and 'summary' in serving:
                    if 'current' not in cache:
                        cache['current'] = serving['summary']
                    else:
                        cache['previous'] = cache['current']
                        cache['current'] = serving['summary']
                        DKActiveServingWatcher._print_changes(self, cache, False)

    @staticmethod
    def print_serving_summary(serving):
        temp_cache = dict()
        temp_cache['current'] = serving
        temp_cache['previous'] = serving
        DKActiveServingWatcher._print_changes(temp_cache, True)

    @staticmethod
    def _print_changes(watcher, cache, trace=False):
        found_change = False
        # print top level changes
        if 'current' in cache and 'previous' in cache:
            found_change = DKActiveServingWatcher._print_serving_summary(watcher, cache, trace)
        if found_change is False:
            stdout.write(' . \r')
            stdout.flush()
        return found_change

    @staticmethod
    def _print_serving_summary(watcher, cache, trace=False):
        cur = cache['current']
        pre = cache['previous']
        nodes = list()
        found_change = False
        for item, val in six.iteritems(cur):
            if isinstance(val, dict):
                nodes.append(item)
            else:
                fmt_watcher = watcher._format_item(item, val)
                output = f"{cur['name']}({cur['hid'][:5]}..) {item}:  {fmt_watcher}"
                if cur[item] != pre[item] and item != 'hid':
                    print(output)
                    found_change = True
                else:
                    if trace is True:
                        print(f'Trace: {output}')
        for node_name in nodes:
            pre_val = pre[node_name] if node_name in pre else None
            if DKActiveServingWatcher._print_node_changes(watcher, cur['name'], cur['hid'][:5],
                                                          cur[node_name], pre_val, node_name,
                                                          trace) is True:
                found_change = True

        return found_change

    # node_name,
    #   data_source/data_sink/actions
    #       file_name
    #           keys
    #               key_name
    #                   status
    #           tests
    #               applies-to-keys
    #               results
    #               status
    #           status
    #           timing
    #           type
    #   status
    #   timing
    #   type
    @staticmethod
    def _print_node_changes(watcher, rname, hid, cur, pre, item_print_string, trace=False):
        found_change = False
        if isinstance(cur, dict) and isinstance(pre, dict):
            for item, val in six.iteritems(cur):
                new_item_print_string = f'{item_print_string}: {item}'
                if isinstance(val, dict):
                    cur_item = cur[item] if item in cur else None
                    pre_item = pre[item] if item in pre else None
                    if DKActiveServingWatcher._print_node_changes(watcher, rname, hid, cur_item,
                                                                  pre_item, new_item_print_string,
                                                                  trace) is True:
                        found_change = True
                else:
                    fmt_watcher = watcher._format_item(item, cur[item])
                    output = f'{rname}({hid}..) {item_print_string}: {item}:  {fmt_watcher}'
                    if item in cur and item in pre and cur[item] != pre[item]:
                        print(output)
                        found_change = True
                    else:
                        if trace is True:
                            print(f'Trace: {output}')
        else:
            if pre and cur:
                print(f'cur and pre are incorrect ({cur}) ({pre})')
            else:
                found_change = True
        return found_change

    def _format_item(self, item, value):
        if not self._formatter or not isinstance(value, int):
            return value

        if item in ['end-time', 'start-time']:
            return self._formatter.format_timestamp(value)
        elif item == 'total-recipe-time':
            return self._formatter.format_timing(value)

        return value


class DKActiveServingCache(object):
    __shared_state = {}
    _cache = dict()
    _time = 'last-update-time'

    def __init__(self):
        self.__dict__ = self.__shared_state

    def __repr__(self):
        return self.__shared_state

    def __str__(self):
        return self.__repr__()

    def get_cache(self):
        return self._cache

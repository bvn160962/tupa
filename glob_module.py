import util_module as util


# Глобальные переменные
#

# Список сессий
all_sessions = []


def add_session(sess):
    # global all_sessions
    if sess not in all_sessions:
        util.log_tmp(f'add_session: {sess}')
        all_sessions.append(sess)


def get_sessions():
    # global sessions
    return all_sessions

# Счетчик текущих сессий
session_count = 0


def inc_session_count():
    global session_count
    session_count += 1
    # util.log_tmp(f'session_count+: {session_count}')


def dec_session_count():
    global session_count
    session_count -= 1
    # util.log_tmp(f'session_count-: {session_count}')


def get_session_count():
    global session_count
    # util.log_tmp(f'session_count: {session_count}')
    return session_count


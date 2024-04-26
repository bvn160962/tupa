import datetime
import hashlib
import os
import logging

import app
import pg_module
import settings

logger = None


# Для работы с паролями
#
def get_hash(s):
    sha256_hash = hashlib.new('sha256')
    sha256_hash.update(s.encode())
    return sha256_hash.hexdigest()


# Доступность модулей для различных ролей
#
def is_module_available(module):
    role = app.get_c_prop(settings.C_USER_ROLE)

    if module == settings.M_TIMESHEETS:
        return True

    if module == settings.M_USERS:
        return role == settings.R_ADMIN

    if module == settings.M_PROJECTS:
        return role == settings.R_ADMIN or role == settings.R_MANAGER

    if module == settings.M_APPROVEMENT:
        return role == settings.R_ADMIN or role == settings.R_MANAGER

    return False


# Логирование
#
def logger_init():
    # Создать лог папку если ее нет
    #
    if not os.path.isdir(settings.LOG_DIR):
        os.makedirs(settings.LOG_DIR)

    global logger
    if logger is None:
        logger = logging.getLogger(__name__)
        logger.setLevel(level=settings.LOG_FILE_LEVEL)

        file_handler = logging.FileHandler(settings.LOG_FILE_NAME, mode=settings.LOG_FILE_MODE)
        formatter = logging.Formatter(settings.LOG_FILE_FORMAT)
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)
        print(f'logger: {logger}')



def log_info(msg):
    print(f'--{msg}')
    logger.info(msg)


def log_debug(msg):
    print(f'++{msg}')
    logger.debug(msg)


def log_error(msg):
    print(f'**{msg}')
    logger.error(msg)


def log_tmp(msg):
    print(f'=={msg}')
    logger.debug(msg)


def update():
    clear_timesheet()
    app.set_c_prop(settings.C_WEEK, get_week())
    app.print_cache()

    pg_module.DB_CONNECT = None


def clear_timesheet():
    app.set_c_prop(settings.C_TIMESHEET_ID, '')
    app.set_c_prop(settings.C_DATE, '')
    app.set_c_prop(settings.C_TSH_BTN_VALUE, '')
    app.set_c_prop(settings.C_PROJECT_ID, '')


# Вспомогательные функции
#
def get_week():
    return get_week_by_date(datetime.datetime.now())


def get_date():
    return datetime.datetime.now().date()


def get_week_by_date(date):

    year, i_week, day = date.isocalendar()
    s_week = f'{i_week:0{2}}'  # 1 -> 01, 12 -> 12
    out = str(year) + '-W' + s_week

    # log_debug(f'{year}, {week}, {w}, {out}')
    return out


def date_to_day(date):
    s_date = str(date).split('-')
    return f'{s_date[2]}.{s_date[1]}'


def list_dates_in_week(week=None):
    s_date = datetime.datetime.strptime(week + '-1', "%Y-W%W-%w").date()
    date_str = s_date.isocalendar()

    out = []
    for i in range(1, 8):
        date = datetime.datetime.fromisocalendar(year=date_str[0], week=date_str[1], day=i).date()
        # o_date = date_to_day(date)
        # out.append(o_date)
        out.append(str(date))

    # log_debug(f'out: {out}')
    return out


# Начальная и конечная даты в неделе
#
def get_dates_by_week(week):

    s_date = datetime.datetime.strptime(week + '-1', "%Y-W%W-%w").date()
    date_str = s_date.isocalendar()
    e_date = datetime.datetime.fromisocalendar(year=date_str[0], week=date_str[1], day=7).date()

    return s_date, e_date


def is_project_in_week(week, prj_range):
    week_range = get_dates_by_week(week)
    s_edge = False
    e_edge = False

    # Нижняя граница проекта
    if prj_range[0] is None:
        s_edge = True
    else:
        if prj_range[0] <= week_range[1]:
            s_edge = True

    # Верхняя граница проекта
    if prj_range[1] is None:
        e_edge = True
    else:
        if prj_range[1] >= week_range[0]:
            e_edge = True

    return s_edge and e_edge


def shift_week(week='', next=True):
    s = week.split('-')
    if next:
        i = int(s[1][1:]) + 1
    else:
        i = int(s[1][1:]) - 1

    year = s[0]
    last_week = datetime.date(int(year), 12, 28).isocalendar().week

    if i == 0:
        i = 1
    if i > last_week:
        i = last_week

    shifted_week = f'{year}-W{i:0{2}}'
    return shifted_week
    # return s[0] + '-W' + str(i)


logger_init()


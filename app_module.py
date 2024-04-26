from flask import redirect, url_for

import app
import pg_module
import util_module as util
import settings
import ui_module
import data_module

# COMMON BLOCK
#
# def get_client_ip(request):
#     # Get client ip
#     ip = request.environ.get('REMOTE_ADDR')
#
#     if ip == '':
#         isNginx = request.headers.get('T-Nginx')
#         if isNginx is None:
#             util.log_error('Host is ""')
#         else:
#             # Определяем хост для nginx установки
#             # util.log_debug(f'headers: {request.headers}')
#             ip_addrs = request.headers.get('X-Real-Ip')
#             if ip_addrs is None:
#                 util.log_error('Host is None')
#             else:
#                 ips = ip_addrs.split(',')
#                 if len(ips) == 0:
#                     util.log_error(f'Bad Host: {ip_addrs}')
#                 else:
#                     ip = ips[0]
#
#     # if ip == '':
#     #     util.log_error(f'IP Address is not determine')
#     # else:
#     #     util.log_debug(f'IP Address is {ip}')
#
#     return ip


def init_module(request):
    # Определить ip адрес
    # ip = get_client_ip(request)

    # Get form values
    values = request.form
    util.log_debug(f'FORM={values}')

    # Check DB connection
    html_test_db = pg_module.test_connection()

    return values, html_test_db


def check_password(values):
    err_msg = 'Неправильно введен логин или пароль!'
    # util.set_user_name(ip, '')
    app.set_c_prop(settings.C_USER_NAME, '')

    usr_name = ''
    usr_pwd = ''
    for v in values:
        if v == settings.LOGIN_USERNAME:
            usr_name = values[v]
        if v == settings.LOGIN_PASSWORD:
            usr_pwd = values[v]

    if usr_name != '':
        user = data_module.get_user_by_name_list(usr_name)
        if len(user) == 0:  # Нет такого пользователя!!!
            pass
            # Сбросить кэш
            # util.clear_user_cache(host)
        else:
            pwd_db = user[2]  # из базы данных
            pwd_in = util.get_hash(usr_pwd)  # хэш введенного пароля

            # util.log_debug(f'{pwd_in}={pwd_db}')
            if pwd_in == pwd_db:
                err_msg = ''

                app.set_c_prop(settings.C_USER_ID, user[0])
                app.set_c_prop(settings.C_USER_NAME, usr_name)
                app.set_c_prop(settings.C_USER_ROLE, user[1])

    # util.print_cache()
    return err_msg


def logoff(module):
    # util.log_debug(f'Logoff')
    app.clear_cache()

    return redirect(url_for(settings.M_LOGIN, module=module))


# TIMESHEETS BLOCK
#
def timesheets_select(value=''):
    # util.log_debug(f'Нажата кнопка в Таблице: {value}')

    # Разбор значения value (prj_id#tsh_id#date)
    #
    s = value.split(settings.SPLITTER)
    if s is None:
        raise Exception('Ошибка при парсинге values: None')

    if len(s) != 3:
        raise Exception(f'Ошибка при парсинге values: len={len(s)}')

    # Set cache
    #
    app.set_c_prop(settings.C_PROJECT_ID, s[0])
    app.set_c_prop(settings.C_TIMESHEET_ID, s[1])
    app.set_c_prop(settings.C_DATE, s[2])
    app.set_c_prop(settings.C_TSH_BTN_VALUE, value)

    return ui_module.create_timesheet_html()


def week_select(values=None):
    util.clear_timesheet()
    week = values[ui_module.INPUT_WEEK_NAME]
    app.set_c_prop(settings.C_WEEK, week)


def current_week():
    util.clear_timesheet()
    app.set_c_prop(settings.C_WEEK, util.get_week())
    return ui_module.create_timesheet_html()


def next_week():
    util.clear_timesheet()
    week = app.get_c_prop(settings.C_WEEK)
    app.set_c_prop(settings.C_WEEK, util.shift_week(week, True))
    return ui_module.create_timesheet_html()


def prev_week():
    util.clear_timesheet()
    week = app.get_c_prop(settings.C_WEEK)
    app.set_c_prop(settings.C_WEEK, util.shift_week(week, False))
    return ui_module.create_timesheet_html()


def timesheets_update():
    try:
        # util.log_debug(f'Нажата кнопка Update Timesheets')
        util.update()
        return ui_module.create_timesheet_html()

    except Exception as ex:
        return ui_module.create_info_html(settings.INFO_TYPE_ERROR, f'{ex}', settings.M_TIMESHEETS)


def timesheets_save(values=None):
    try:
        # util.log_info(f'Нажата кнопка Save: {values}')

        html = ''
        tsh_id = app.get_c_prop(settings.C_TIMESHEET_ID)
        # Прочитать значения из формы (values = request.form)
        #
        prj_id, inp_hours, inp_note, inp_status, current_date, comment = '', '', '', '', '', ''
        for value in values:
            if value == ui_module.SELECT_PROJECT_NAME:
                prj_id = values[value]
            if value == ui_module.INPUT_HOURS_NAME:
                inp_hours = values[value]
            if value == ui_module.INPUT_NOTE_NAME:
                inp_note = values[value]
            if value == ui_module.SELECT_STATUS_NAME:
                inp_status = values[value]
            if value == ui_module.DATE_NAME:
                current_date = values[value]
            if value == ui_module.INPUT_COMMENT_NAME:
                comment = values[value]

        if tsh_id == '':
            # Новая запись timeshhets (Insert)
            #
            if prj_id == '' or current_date == '' or inp_hours == '':
                msg = f'Не задано одно из обязательных значений атрибутов (prj_id={prj_id}, date={current_date}, hours={inp_hours}) при попытке создать новую запись!'
                util.log_debug(msg)
                html = ui_module.create_info_html(settings.INFO_TYPE_WARNING, msg, module=settings.M_TIMESHEETS)
            else:
                data_module.insert_entry(
                    user_id=app.get_c_prop(settings.C_USER_ID),
                    prj_id=prj_id,
                    data={
                        settings.F_TSH_DATE: current_date,
                        settings.F_TSH_HOURS: inp_hours,
                        settings.F_TSH_NOTE: inp_note,
                        settings.F_TSH_STATUS: inp_status,
                        settings.F_TSH_COMMENT: comment
                    }
                )
        else:
            # Существующая запись timeshhets (Update)
            #
            data_module.update_entry(
                tsh_id=tsh_id,
                data={
                    settings.F_TSH_HOURS: inp_hours,
                    settings.F_TSH_NOTE: inp_note,
                    settings.F_TSH_STATUS: inp_status,
                    settings.F_TSH_COMMENT: comment
                }
            )

        return html

    except Exception as ex:
        return ui_module.create_info_html(settings.INFO_TYPE_ERROR, f'{ex}', settings.M_TIMESHEETS)


def timesheets_delete():
    try:
        tsh_id = app.get_c_prop(settings.C_TIMESHEET_ID)
        util.log_debug(f'pressed_delete_button: Delete entry: tsh_id={tsh_id}')

        if tsh_id != '':
            data_module.delete_entry(tsh_id=tsh_id)
            app.set_c_prop(settings.C_TIMESHEET_ID, '')  # убрать tsh_id из кэша
        else:
            raise Exception('Попытка удалить запись с пустым tsh_id')


    except Exception as ex:
        return ui_module.create_info_html(settings.INFO_TYPE_ERROR, f'{ex}', settings.M_TIMESHEETS)


# GET
#
def timesheets_get():
    return ui_module.create_timesheet_html()

# POST
#
def timesheets_post(values):
    html = ''

    for value in values:
        # util.log_error(f'values={values}')

        # Нажата кнопка LOGOFF
        #
        if value == settings.LOGOFF_BUTTON:
            # тестирование метода!!!
            # data_module.get_entries_for_approval(102)
            html = logoff(settings.M_TIMESHEETS)

        # Нажата кнопка REFRESH
        #
        if value == settings.UPDATE_BUTTON:
            html = timesheets_update()

        # Нажата одна из кнопок в таблице
        #
        if value == settings.TABLE_BUTTON:
            html = timesheets_select(value=values[value])

        # Нажата кнопка SAVE Entry
        #
        if value == settings.SAVE_BUTTON:
            html_e = timesheets_save(values=values)
            if html_e != '':
                return html_e
            html = ui_module.create_timesheet_html()

        # Нажата кнопка DELETE YES
        #
        if value == settings.DELETE_BUTTON_YES:
            timesheets_delete()
            html = ui_module.create_timesheet_html()

        # Нажата кнопка DELETE NO
        #
        if value == settings.DELETE_BUTTON_NO:
            html = ui_module.create_timesheet_html()

        # Нажата кнопка DELETE Entry
        #
        if value == settings.DELETE_BUTTON:
            # Show confirmation dialog
            html = ui_module.create_delete_confirm_html(app.get_c_prop(settings.C_TIMESHEET_ID), settings.M_TIMESHEETS)

        # Нажата кнопка WEEK
        #
        if value == settings.WEEK_BUTTON_SELECT:
            week_select(values=values)
            html = ui_module.create_timesheet_html()

        # Нажата кнопка NEW Entry
        #
        if value == settings.NEW_BUTTON:
            app.set_c_prop(settings.C_TIMESHEET_ID, '')
            html = ui_module.create_timesheet_html()

        # Нажата кнопка CURRENT WEEK
        #
        if value == settings.WEEK_BUTTON_CURRENT:
            html = current_week()

        # Нажата кнопка NEXT WEEK
        #
        if value == settings.WEEK_BUTTON_NEXT:
            html = next_week()

        # Нажата кнопка PREV WEEK
        #
        if value == settings.WEEK_BUTTON_PREV:
            html = prev_week()

    # util.log_debug(f'timesheets.POST: Не задан обработчик кнопки {value}')
    return html


# PROJECTS BLOCK
#
def projects_delete(prj_id):
    try:
        util.log_debug(f'Delete Project: prj_id={prj_id}')
        data_module.delete_project(prj_id)
        return ui_module.create_projects_html(())
    except Exception as ex:
        return ui_module.create_info_html(settings.INFO_TYPE_ERROR, f'{ex}', settings.M_PROJECTS)


def projects_not_delete(prj_id):
    props = data_module.get_project_by_id_list(prj_id)
    m_props = (str(props[0]), str(props[1]), str(props[2]), str(props[3]), str(props[4]), str(props[5]))

    return ui_module.create_projects_html(m_props)


def projects_update():
    try:
        # util.log_debug(f'Нажата кнопка Update Projects')
        util.update()
        return ui_module.create_projects_html()

    except Exception as ex:
        return ui_module.create_info_html(settings.INFO_TYPE_ERROR, f'{ex}', settings.M_PROJECTS)


def projects_select(prj_id):
    try:
        # util.log_debug(f'Нажата кнопка Select Project id={prj_id}')
        prj_props = data_module.get_project_by_id_list(prj_id)
        # util.log_debug(f'props: {prj_props}')

        return ui_module.create_projects_html(prj_props)
    except Exception as ex:
        return ui_module.create_info_html(settings.INFO_TYPE_ERROR, f'{ex}', settings.M_PROJECTS)


def projects_save(prj_id, props):
    try:
        # util.log_debug(f'Нажата кнопка Save Project for prj_id={prj_id}, props={props}')

        # Сформировать список свойств проекта
        #
        p_name, p_manager_id, p_s_date, p_e_date, p_org = '', '', '', '', ''
        team_list = []
        for p in props:
            if p == settings.F_PRJ_NAME:
                p_name = props[p]
            if p == settings.F_PRJ_ORG:
                p_org = props[p]
            if p == settings.F_PRJ_MANAGER_ID:  # Не передается, если список значений disabled
                p_manager_id = props[p]
            if p == settings.F_PRJ_START_DATE:
                p_s_date = props[p]
            if p == settings.F_PRJ_END_DATE:
                p_e_date = props[p]
            # Команда проекта
            if props[p] == 'on':
                team_list.append(p)

        # util.log_debug(f'team_list={len(team_list)}')
        if p_manager_id == '':  # Список ролей disabled
            p_manager_id = app.get_c_prop(settings.C_USER_ID)

        prj_props = (prj_id, p_manager_id, p_name, p_s_date, p_e_date, p_org)
        prj_props_db = (prj_id, p_manager_id, p_name, None if p_s_date == '' else p_s_date, None if p_e_date == '' else p_e_date, p_org)
        # util.log_debug(f'prj_props={prj_props}')
        # util.log_debug(f'prj_props_db={prj_props_db}')

        # Проверка переданных атрибутов
        if p_name == '':
            msg = 'Не заполнено одно из обязательных атрибутов:  Наименование проекта!'
            return ui_module.create_info_html(settings.INFO_TYPE_ERROR, msg, settings.M_PROJECTS)

        if prj_id == '':  # Создать нового пользователя
            util.log_debug('Insert')
            data_module.insert_project(prj_props_db, team_list)
        else:  # Обновить существующего пользователя
            util.log_debug('Update')
            data_module.update_project(prj_props_db, team_list)

        return ui_module.create_projects_html(())

    except Exception as ex:
        return ui_module.create_info_html(settings.INFO_TYPE_ERROR, f'{ex}', settings.M_PROJECTS)


def projects_new_button():
    # util.log_debug(f'Нажата кнопка New Project')
    return ui_module.create_projects_html((), True)


def projects_ref_button(prj_id):
    prj = data_module.get_project_by_id_list(prj_id)
    prj_name = prj[2]
    # util.log_debug(f'Нажата кнопка Project Reference: {prj_id}; {prj_name}')

    e_list = data_module.where_project_refs(prj_id)
    if len(e_list) == 0:
        return ui_module.create_info_html(settings.INFO_TYPE_INFORMATION, f'Нет записей учета отработанного времени на проекте "{prj_name}".', settings.M_PROJECTS)
    else:
        title = f'Записи из учета отработанного времени на проекте "{prj_name}"'
        e_list.insert(0, ('Дата', 'Статус', 'Комментарий', 'Исполнитель'))  # Заголовок таблицы
        return ui_module.create_info_html(settings.INFO_TYPE_INFORMATION, e_list, settings.M_PROJECTS, title)


# GET
#
def projects_get():
    return ui_module.create_projects_html(())


# POST
#
def projects_post(values):
    html = ''
    for value in values:
        # util.log_debug(f'projects_post: value={value}')

        # Нажата кнопка LOGOFF
        #
        if value == settings.LOGOFF_BUTTON:
            return logoff(settings.M_PROJECTS)

        # Нажата кнопка REFRESH
        #
        if value == settings.UPDATE_BUTTON:
            return projects_update()

        # Нажата кнопка SELECT
        #
        if value == settings.TABLE_BUTTON:
            return projects_select(values[value])

        # Нажата кнопка SAVE
        #
        if value == settings.SAVE_BUTTON:
            return projects_save(values[value], values)

        # Нажата кнопка NEW
        #
        if value == settings.NEW_BUTTON:
            return projects_new_button()

        # Нажата кнопка REFERENCE
        #
        if value == settings.REF_BUTTON:
            return projects_ref_button(values[value])

        # Нажата кнопка HIDEINFO
        #
        if value == settings.HIDEINFO_BUTTON:
            return ui_module.create_projects_html()

        # Нажата кнопка DELETE
        #
        if value == settings.DELETE_BUTTON:
            # Show confirmation dialog
            html = ui_module.create_delete_confirm_html(values[value], settings.M_PROJECTS)

        # Отклонение DELETE NO
        #
        if value == settings.DELETE_BUTTON_NO:
            return projects_not_delete(values[value])

        # Подтверждение DELETE YES
        #
        if value == settings.DELETE_BUTTON_YES:
            return projects_delete(values[value])

    return html


# USERS BLOCK
#
def users_update():
    try:
        # util.log_debug(f'Нажата кнопка Update Users')
        util.update()
        return ui_module.create_users_html()

    except Exception as ex:
        return ui_module.create_info_html(settings.INFO_TYPE_ERROR, f'{ex}', settings.M_USERS)


def users_select(usr_id):
    try:
        # util.log_debug(f'Нажата кнопка Select User for user_id={usr_id}')
        usr_props = data_module.get_user_by_id_list(usr_id)
        # util.log_debug(f'props: {usr_props}')

        return ui_module.create_users_html(usr_props)

    except Exception as ex:
        return ui_module.create_info_html(settings.INFO_TYPE_ERROR, f'{ex}', settings.M_USERS)


def users_save(usr_id, props):
    try:
        util.log_debug(f'Нажата кнопка Save User for user_id={usr_id}, props={props}')

        # Сформировать список свойств
        #
        u_name, u_role, u_pwd, u_mail, u_info = '', '', '', '', ''
        for p in props:
            if p == settings.F_USR_NAME:
                u_name = props[p]
            if p == settings.F_USR_ROLE:
                u_role = props[p]
            if p == settings.F_USR_PASSWORD:
                u_pwd = props[p]
                # u_pwd = util.get_hash(props[p])
            if p == settings.F_USR_MAIL:
                u_mail = props[p]
            if p == settings.F_USR_INFO:
                u_info = props[p]

        if usr_id == '':  # Создать нового пользователя
            # util.log_debug('Insert')
            # Проверка атрибутов
            if u_name == '' or u_pwd == '':
                msg = 'Не заполнен один из обязательных атрибутов: Имя или Пароль пользователя!'
                return ui_module.create_info_html(settings.INFO_TYPE_ERROR, msg, settings.M_USERS)
            usr_props = (usr_id, u_name, u_role, util.get_hash(u_pwd), u_mail, u_info)
            data_module.insert_user(usr_props)
        else:  # Обновить существующего пользователя
            # util.log_debug('Update')
            # Проверка атрибутов
            if u_name == '':
                msg = 'Атрибут Имя пользователя должен быть заполнен!'
                return ui_module.create_info_html(settings.INFO_TYPE_ERROR, msg, settings.M_USERS)
            if u_pwd != '':
                u_pwd = util.get_hash(u_pwd)
            usr_props = (usr_id, u_name, u_role, u_pwd, u_mail, u_info)
            data_module.update_user(usr_props)

        return ui_module.create_users_html(())
        # return ui_module.create_users_html(host, usr_props)

    except Exception as ex:
        return ui_module.create_info_html(settings.INFO_TYPE_ERROR, f'{ex}', settings.M_USERS)


def users_new():
    # util.log_debug(f'Нажата кнопка New User')

    return ui_module.create_users_html((), True)


def users_delete(usr_id):
    try:
        util.log_debug(f'Нажата кнопка Delete User: usr_id={usr_id}')
        data_module.delete_user(usr_id)
        return ui_module.create_users_html('')

    except Exception as ex:
        return ui_module.create_info_html(settings.INFO_TYPE_ERROR, f'{ex}', settings.M_USERS)


def users_ref_button(usr_id):
    usr = data_module.get_user_by_id_list(usr_id)
    usr_name = usr[1]
    # util.log_debug(f'Нажата кнопка Project Reference: {usr_id}; {usr_name}')

    title = f'Ссылки на пользователя "{usr_name}"'

    obj_list = data_module.where_user_refs(usr_id)

    if len(obj_list) == 0:
        return ui_module.create_info_html(settings.INFO_TYPE_INFORMATION, f'На пользователя "{usr_name}" ссылок нет.', settings.M_USERS)
    else:
        title = f'Ссылки на пользователя "{usr_name}"'
        obj_list.insert(0, ('Проект', 'Куда ссылается', 'Участие',))  # Заголовок таблицы
        return ui_module.create_info_html(settings.INFO_TYPE_INFORMATION, obj_list, settings.M_USERS, title)


# GET
#
def users_get():
    return ui_module.create_users_html()

# POST
#
def users_post(values):
    html = ''
    for value in values:
        # util.log_debug(f'users_post: value={value}')

        # Нажата кнопка LOGOFF
        #
        if value == settings.LOGOFF_BUTTON:
            return logoff(settings.M_USERS)

        # Нажата кнопка REFRESH
        #
        if value == settings.UPDATE_BUTTON:
            return users_update()

        # Нажата кнопка SELECT
        #
        if value == settings.TABLE_BUTTON:
            return users_select(values[value])

        # Нажата кнопка SAVE
        #
        if value == settings.SAVE_BUTTON:
            return users_save(values[value], values)

        # Нажата кнопка NEW
        #
        if value == settings.NEW_BUTTON:
            return users_new()

        # Нажата кнопка REFERENCE
        #
        if value == settings.REF_BUTTON:
            return users_ref_button(values[value])

        # Нажата кнопка HIDEINFO
        #
        if value == settings.HIDEINFO_BUTTON:
            return ui_module.create_users_html()

        # Нажата кнопка DELETE
        #
        if value == settings.DELETE_BUTTON:
            # Show confirmation dialog
            return ui_module.create_delete_confirm_html(values[value], settings.M_USERS)

        # Отклонение DELETE NO
        #
        if value == settings.DELETE_BUTTON_NO:
            return ui_module.create_users_html()

        # Подтверждение DELETE YES
        #
        if value == settings.DELETE_BUTTON_YES:
            return users_delete(values[value])

    return html


# APPROVE BLOCK
#
# Отработка списка на согласование
def agreed(values):
    msg = ''
    tsh_id_list = []
    for key in values:
        if key == 'feedback':
            msg = values[key]
        elif values[key] == 'on':
            tsh_id_list.append(int(key))
    data_module.update_status(tuple(tsh_id_list), True, msg)
    return ui_module.create_approvement_html()


# Отработка списка на отклонение
def rejected(values):
    msg = ''
    tsh_id_list = []
    for key in values:
        if key == 'feedback':
            msg = values[key]
        elif values[key] == 'on':
            tsh_id_list.append(int(key))
    data_module.update_status(tuple(tsh_id_list), False, msg)
    return ui_module.create_approvement_html()


def approvement_update():
    try:
        # util.log_debug(f'Нажата кнопка Update Approvement')
        util.update()
        return ui_module.create_approvement_html()

    except Exception as ex:
        return ui_module.create_info_html(settings.INFO_TYPE_ERROR, f'{ex}', settings.M_APPROVEMENT)

# GET
#
def approvement_get():
    return ui_module.create_approvement_html()

def approvement_post(values):
    html = ''
    for value in values:
        # util.log_debug(f'approvement_post: value={value}')

        # Нажата кнопка LOGOFF
        #
        if value == settings.LOGOFF_BUTTON:
            return logoff(settings.M_APPROVEMENT)

        # Нажата кнопка REFRESH
        #
        if value == settings.UPDATE_BUTTON:
            return approvement_update()

        # Нажата кнопка СОГЛАСОВАТЬ
        #
        if value == settings.AGREE_BUTTON:
            return agreed(values)

        # Нажата кнопка ОТКЛОНИТЬ
        #
        if value == settings.REJECT_BUTTON:
            return rejected(values)

        # Нажата кнопка ВЫДЕЛИТЬ ВСЁ/УБРАТЬ ВСЁ
        #
        if value == settings.ALL_FLAG_BUTTON:
            util.log_info(f'значение кнопки реверс: {type(values[value])}')
            return ui_module.create_approvement_html(values[value])

    return html


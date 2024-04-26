from flask import render_template
from xml.etree import ElementTree as et

import app
import data_module
import settings
import util_module as util

DATE_NAME = 'current_date'
INPUT_WEEK_NAME = 'inp_week'
INPUT_HOURS_NAME = 'inp_hours'
INPUT_NOTE_NAME = 'inp_note'
INPUT_COMMENT_NAME = 'inp_comment'
SELECT_STATUS_NAME = 'selected_status'
SELECT_PROJECT_NAME = 'selected_project'


class BaseHTML:

    def __init__(self, title, module):
        # util.log_debug(f'BaseHTML: New(title={title})')
        self.__html = et.Element('html', {'lang': 'ru'})

        # HEAD
        self.__head = et.SubElement(self.__html, 'head')
        et.SubElement(self.__head, 'link', {"rel": "stylesheet", "type": "text/css", "href": 'static/css/common.css'})
        et.SubElement(self.__head, 'link', {"rel": "stylesheet", "type": "text/css", "href": 'static/css/buttons.css'})
        et.SubElement(self.__head, 'link', {"rel": "stylesheet", "type": "text/css", "href": 'static/css/inputs.css'})
        et.SubElement(self.__head, 'link', {"rel": "stylesheet", "type": "text/css", "href": 'static/css/tables.css'})
        # et.SubElement(self.__head, 'link', {'rel': 'icon', 'type': 'image/x-icon', 'href': 'static/img/edit.png'})

        et.SubElement(self.__head, 'link', {"rel": "stylesheet", "href": 'https://cdnjs.cloudflare.com/ajax/libs/font-awesome/4.7.0/css/font-awesome.min.css'})
        et.SubElement(self.__head, 'link', {"rel": "stylesheet", "href": 'https://fonts.googleapis.com/css2?family=Material+Symbols+Outlined'})
        # et.SubElement(self.__head, 'meta', attrib={"name": "viewport", "content": "min-width=870px, initial-scale=1"})

        t_title = et.SubElement(self.__head, 'title')
        t_title.text = title

        # BODY
        self.__body = et.SubElement(self.__html, 'body', {'style': 'min-height: 400px;'})  # После этой высоты появляется прокрутка

        # FORM
        self.__form = et.SubElement(self.__body, 'form', attrib={'name': 'form', 'method': 'POST'})

        p = et.SubElement(self.__form, 'p class="p_gray"')
        # MODULE
        m = et.SubElement(p, 'a style="margin:10px; font-weight: 200;"')

        # INFO
        if  module == '':
            m.text = ''
        else:
            m.text = module[settings.M_NAME] + ': ' + f'{str(app.get_c_prop(settings.C_USER_NAME))} ({str(app.get_c_prop(settings.C_USER_ROLE))})'

        # LOGOFF button
        btn = et.SubElement(p,
                            'button class="material-symbols-outlined right btn-t-cell" title="Завершить работу"',
                            {
                                'style': 'padding-inline: 0px; margin-left: 0; margin-right: 0; padding-left: 1px',
                                'name': settings.LOGOFF_BUTTON,
                            })
        btn.text = 'logout'
        # log_off = et.SubElement(p,
        #                         'button title="Завершить работу"',
        #                         attrib={
        #                             'type': 'submit',
        #                             'name': settings.LOGOFF_BUTTON,
        #                             'class': 'right btn-icon'
        #                         })
        # i = et.SubElement(log_off, 'i', {'class': 'fa fa-user-circle-o fa-lg'})  # fa-user-o
        # i.text = '\n'  # !!!Обязательно!!! Иначе, создает одиночный тэг <i .... />, вместо парного <i> ... </i>

        # DEBUG button
        btn = et.SubElement(p,
                            'button class="material-symbols-outlined right btn-t-cell" title="Состояние текущей сессии"',
                            {
                                'style': 'padding-inline: 0px; margin-left: 0; margin-right: 0; padding-left: 1px',
                                'name': settings.DEBUG_BUTTON,
                            })
        btn.text = 'pest_control'

        # REFRESH button
        btn = et.SubElement(p,
                            'button class="material-symbols-outlined right btn-t-cell" title="Обновить"',
                            {
                                'style': 'padding-inline: 0px; margin-left: 0; margin-right: 0; padding-left: 1px',
                                'name': settings.UPDATE_BUTTON,
                            })
        btn.text = 'sync'
        # log_off = et.SubElement(p,
        #                         'button title="Обновить"',
        #                         attrib={
        #                             'type': 'submit',
        #                             'name': settings.UPDATE_BUTTON,
        #                             'class': 'right btn-icon'
        #                         })
        # i = et.SubElement(log_off, 'i', {'class': 'fa fa-refresh fa-lg'})
        # i.text = '\n'

        # Добавляем навигацию по сайту
        #
        if util.is_module_available(settings.M_APPROVEMENT):
            b = et.SubElement(p,
                              f'a title="{settings.MODULES[settings.M_APPROVEMENT][settings.M_TITLE]}"',
                              attrib={'href': settings.MODULES[settings.M_APPROVEMENT][settings.M_URL], 'class': 'right btn-head'})
            b.text = settings.MODULES[settings.M_APPROVEMENT][settings.M_NAME]

        if util.is_module_available(settings.M_USERS):
            b = et.SubElement(p,
                              f'a title="{settings.MODULES[settings.M_USERS][settings.M_TITLE]}"',
                              attrib={'href': settings.MODULES[settings.M_USERS][settings.M_URL], 'class': 'right btn-head'})
            b.text = settings.MODULES[settings.M_USERS][settings.M_NAME]

        if util.is_module_available(settings.M_PROJECTS):
            b = et.SubElement(p,
                              f'a title="{settings.MODULES[settings.M_PROJECTS][settings.M_TITLE]}"',
                              attrib={'href': settings.MODULES[settings.M_PROJECTS][settings.M_URL], 'class': 'right btn-head'})
            b.text = settings.MODULES[settings.M_PROJECTS][settings.M_NAME]

        if util.is_module_available( settings.M_TIMESHEETS):
            b = et.SubElement(p,
                              f'a title="{settings.MODULES[settings.M_TIMESHEETS][settings.M_TITLE]}"',
                              attrib={'href': settings.MODULES[settings.M_TIMESHEETS][settings.M_URL], 'class': 'right btn-head'})
            b.text = settings.MODULES[settings.M_TIMESHEETS][settings.M_NAME]


    def get_html(self):
        # util.log_debug(f'===={self.__html}')
        # util.log_debug(f'====get_html:{et.tostring(self.__html)}')

        return et.tostring(self.__html).decode()

    def get_body(self):
        return self.__body

    def get_head(self):
        return self.__head

    def get_form(self):
        return self.__form


def is_available_html(module):
    if not util.is_module_available(module):
        html_is_available = create_info_html(
            i_type=settings.INFO_TYPE_WARNING,
            module=module,
            msg=f'Модуль "{settings.MODULES[module][settings.M_TITLE]}" недоступен для роли "{app.get_c_prop(settings.C_USER_ROLE)}"!',
            url=settings.MODULES[settings.M_TIMESHEETS][settings.M_URL]  # Ссылка на модуль Timesheets
        )
    else:
        html_is_available = ''
    return html_is_available


def _create_html_static():
    html = render_template('test.html')
    return html


def get_row_color(row):
    if row % 2 == 0:
        color = '#E5E5E5'
    else:
        color = '#FFFFFF'

    return color


def add_table_buttons(col, btn_id):
    btn = et.SubElement(col,
                        'button class="material-symbols-outlined btn-t-cell" title="Ссылки"',
                        {
                            'style': 'padding-inline: 0px; margin-left: 0; margin-right: 0; padding-left: 1px',  # padding-left - добавлен для корректного отображения на ipad
                            'name': settings.REF_BUTTON,
                            'value': btn_id,
                        })
    btn.text = 'quick_reference_all'

    btn = et.SubElement(col,
                        'button class="material-symbols-outlined btn-t-cell" title="Удалить"',
                        {
                            'style': 'padding-inline: 0px; margin-left: 0; margin-right: 0; padding-left: 1px',
                            'name': settings.DELETE_BUTTON,
                            'value': btn_id,
                        })
    btn.text = 'delete'

    btn = et.SubElement(col,
                        'button class="material-symbols-outlined btn-t-cell" title="Редактировать"',
                        {
                            'style': 'padding-inline: 0px; margin-left: 0; margin-right: 0; padding-left: 1px',
                            'name': settings.TABLE_BUTTON,
                            'value': btn_id,
                        })
    btn.text = 'draft_orders'


def add_buttons(col, btn_id):

    btn = et.SubElement(col,
                        'button class="material-symbols-outlined btn-t-cell" title="Сохранить"',
                        {
                            'style': 'padding-inline: 0px; margin-left: 0; margin-right: 0;',
                            'name': settings.SAVE_BUTTON,
                            'value': btn_id,
                        })
    btn.text = 'save'

    btn = et.SubElement(col,
                        'button class="material-symbols-outlined btn-t-cell" title="Скрыть атрибуты"',
                        {
                            'style': 'padding-inline: 0px; margin-left: 0; margin-right: 0;',
                            'name': settings.HIDEINFO_BUTTON,
                            'value': btn_id,
                        })
    btn.text = 'stat_minus_2'


def craete_login_html(err_msg, module=''):
    util.log_debug(f'craete_login_html: ...')
    html = et.Element('html', attrib={'lang': 'ru'})

    # HEAD
    head = et.SubElement(html, 'head')
    et.SubElement(head, 'meta', {'charset': 'UTF-8'})
    et.SubElement(head, 'meta', {'name': 'viewport', 'content': 'width=device-width, initial-scale=1'})
    et.SubElement(head, 'link', {'rel': 'stylesheet', 'href': '/static/css/common.css'})
    # et.SubElement(head, 'link', {'rel': 'icon', 'href': '/static/img/4388342.png', 'type': 'image/x-icon'})
    # et.SubElement(head, 'link', {'rel': 'icon', 'href': '/static/img/timesheets.png', 'type': 'image/x-icon'})
    t = et.SubElement(head, 'title')
    t.text = 'Регистрация'

    # BODY
    body = et.SubElement(html, 'body')

    # FORM
    form = et.SubElement(body, 'form', attrib={'name': 'login', 'method': 'POST', 'class': 'center_frame'})
    et.SubElement(form, 'img', {'src': '/static/img/timesheets.png', 'class': 'fit-picture'})

    et.SubElement(form, settings.TAG_INPUT, {'style': 'margin: 5px;', 'type': 'text', 'name': settings.LOGIN_USERNAME, 'placeholder': 'логин'})
    et.SubElement(form, settings.TAG_INPUT, {'style': 'margin: 3px;', 'type': 'password', 'name': settings.LOGIN_PASSWORD, 'placeholder': 'пароль'})

    p = et.SubElement(form, 'p')
    msg = et.SubElement(p, 'a', {'style': 'color: red;'})
    if err_msg == '':
        msg.text = '\n'
    else:
        msg.text = err_msg

    btn = et.SubElement(form, 'button',
                        {
                            'style': 'margin: 10px;',
                            'type': 'submit',
                            'name': settings.LOGIN_BUTTON,
                            'value': module,
                            'class': 'sub_button'})
    btn.text = 'ВОЙТИ'

    return et.tostring(html).decode()


def create_info_html(i_type='', msg=(), module='', title='', url=''):
    # util.log_debug(f'size: {len(msg)}')

    if msg == '':
        msg = 'Информация'

    if i_type == '':
        i_type = settings.INFO_TYPE_INFORMATION

    if module == '':
        mdl = ''
        url_ = ''
    else:
        mdl = settings.MODULES[module]
        if url != '':
            url_ = url
        else:
            url_ = mdl[settings.M_URL]

    base_html = BaseHTML(i_type, mdl)
    p = base_html.get_form()


    # Ссылка для возврата
    if url_ != '':
        ret_url = et.SubElement(p,
                                'a class="material-symbols-outlined" title="Возврат..."',
                                {
                                    'href': url_,
                                    'type': 'submit',
                                    'style': 'text-decoration-color: transparent; color: #008B8B; padding: 10px;'})
        ret_url.text = 'text_select_jump_to_beginning'


    # MESSAGE
    h = et.SubElement(p, 'H3', {'style': 'display: inline-block; margin: 0px'})
    if title == '':
        h.text = i_type + ':'
    else:
        h.text = title + ':'

    et.SubElement(p, 'br')
    et.SubElement(p, 'br')

    if isinstance(msg, str):  # div
        # util.log_debug(f'type: строка')
        div = et.SubElement(p, 'div')
        div.text = msg
    else:
        if isinstance(msg, tuple) or isinstance(msg, list):
            if isinstance(msg[0], str):  # divs
                # util.log_debug(f'type: массив строк ({len(msg)})')
                for m in msg:
                    div = et.SubElement(p, 'div')
                    div.text = m
            if isinstance(msg[0], tuple) or isinstance(msg[0], list):  # table
                # util.log_debug(f'type: таблица из строк ({len(msg)}x{len(msg[0])})')
                table = et.SubElement(p, 'table')
                row_num = 0
                for r in msg:
                    # util.log_debug(f'row: {r}')
                    row = et.SubElement(table, 'tr')
                    for c in r:
                        if row_num == 0:  # Заголовок таблицы
                            td = 'td align=center'
                            style = 'border-bottom: 2px solid gray; border-top: 2px solid gray; padding-left: 10px; background-color: #C0C0C0; font-weight: bold;'
                        else:
                            td = 'td align=left'
                            style = 'border-bottom: 1px solid gray; min-width: 100px; max-width: 300px; padding-left: 10px; padding-top: 10px;'
                        col = et.SubElement(row, td, {'style': style})
                        a = et.SubElement(col, 'a')
                        a.text = c
                    row_num += 1

    return base_html.get_html()


def create_delete_confirm_html(obj_id, module):

    # FORM
    #
    base_html = BaseHTML('Подтверждение', settings.MODULES[module])
    form = base_html.get_form()

    # INFO AREA
    #
    p_msg = et.SubElement(form, 'p')

    msg = 'Вы действительно хотите удалить запись?\n'

    values = None
    rows = 10
    cols = 60
    if module == settings.M_TIMESHEETS:
        values = data_module.get_timesheet_dict(obj_id)
        msg = 'Вы действительно хотите удалить запись?\n'
        msg += f'   - Дата: {values[settings.F_TSH_DATE]}\n'
        msg += f'   - Часы: {values[settings.F_TSH_HOURS]}\n'
        msg += f'   - Статус: {values[settings.F_TSH_STATUS]}\n'
        msg += f'   - Замечание: {values[settings.F_TSH_NOTE]}\n'
        msg += f'   - Комментарий: {values[settings.F_TSH_COMMENT]}\n'
        rows = 7

    if module == settings.M_USERS:
        refs = data_module.where_user_refs(obj_id)
        values = data_module.get_user_by_id_list(obj_id)
        msg = 'Вы действительно хотите удалить пользователя?\n'
        msg += f'   - Имя: {values[1]}\n'
        msg += f'   - Роль: {values[2]}\n'
        if len(refs) > 0:
            msg += '--------------------------------------\n'
            msg += f'На пользователя существуют ссылки - {str(len(refs))}\n'
            msg += f'Нажмите "Ссылки" - для подробностей\n'
            msg += '--------------------------------------\n'
            rows = 8
        else:
            rows = 4

    if module == settings.M_PROJECTS:
        refs = data_module.where_project_refs(obj_id)
        values = data_module.get_project_by_id_list(obj_id)
        msg = 'Вы действительно хотите удалить проект?\n'
        msg += f'   - Имя: {values[2]}\n'
        msg += f'   - Начало: {values[3]}\n'
        msg += f'   - Окончание: {values[4]}\n'
        if len(refs) > 0:
            msg += '------------------------------------------------------\n'
            msg += f'На проект существуют ссылки - {str(len(refs))}\n'
            msg += f'Нажмите "Ссылки" - для получения детальной информации\n'
            msg += '------------------------------------------------------\n'
            rows = 9
        else:
            rows = 5

    text = et.SubElement(p_msg, f'textarea cols="{cols}" rows="{rows}" readonly')  # style="background-color:LightGray"
    text.text = msg

    # CONFIRM AREA
    #
    p_confirm = et.SubElement(form, 'p')

    btn_yes = et.SubElement(p_confirm, 'button',
                            attrib={
                                'type': 'submit',
                                'name': settings.DELETE_BUTTON_YES,
                                'value': obj_id,
                                'style': 'margin-left:100px; width: 60px;'
                            })  #   style="margin-left:150px;"
    btn_yes.text = 'Да'

    btn_no = et.SubElement(p_confirm,
                           'button',
                           {'type': 'submit', 'name': settings.DELETE_BUTTON_NO, 'value': obj_id, 'style': 'width: 60px;'})
    btn_no.text = 'Нет'

    return base_html.get_html()


# TIMESHEETS
#
def add_timesheets_info(form=None, tsh_entry=None):

    tsh_id = app.get_c_prop(settings.C_TIMESHEET_ID)
    week = app.get_c_prop(settings.C_WEEK)

    # parsing attributes
    #
    hours = ''
    note = ''
    status = ''
    date = ''
    comment = ''
    if tsh_entry is not None:
        hours = tsh_entry.get(settings.F_TSH_HOURS)
        note = tsh_entry.get(settings.F_TSH_NOTE)
        status = tsh_entry.get(settings.F_TSH_STATUS)
        date = str(tsh_entry.get(settings.F_TSH_DATE))
        comment = str(tsh_entry.get(settings.F_TSH_COMMENT))

    p = et.SubElement(form, 'p')

    # TABLE
    table = et.SubElement(p, 'table')

    # WEEK ROW
    #
    row = et.SubElement(table, 'tr')
    col = et.SubElement(row, 'td colspan="5" align="center"')  # Объединенная ячейка

    # Кнопка Текущая неделя
    btn = et.SubElement(col, 'button title="Текущая неделя" class="btn-icon"', attrib={'type': 'submit', 'name': settings.WEEK_BUTTON_CURRENT})
    i = et.SubElement(btn, 'i class="fa fa-calendar fa-lg" aria-hidden="true"')
    i.text = '\n'

    # Кнопка Назад
    btn = et.SubElement(col, 'button title="Предыдущая неделя" class="btn-icon"', attrib={'type': 'submit', 'name': settings.WEEK_BUTTON_PREV})
    i = et.SubElement(btn, 'i class="fa fa-arrow-circle-o-left fa-lg" aria-hidden="true"')
    i.text = '\n'

    # Кнопка Вперед
    btn = et.SubElement(col, 'button title="Следующая неделя" class="btn-icon"', attrib={'type': 'submit', 'name': settings.WEEK_BUTTON_NEXT})
    i = et.SubElement(btn, 'i class="fa fa-arrow-circle-o-right fa-lg" aria-hidden="true"')
    i.text = '\n'

    # Календарь
    # util.log_debug(f'week html={week}; {type(week)}')
    et.SubElement(col, settings.TAG_INPUT, attrib={'type': 'week', 'name': INPUT_WEEK_NAME, 'value': week, 'style': 'border-radius: 10px; margin: 0px 0px 5px 5px;'})

    # Кнопка Применить
    btn = et.SubElement(col, 'button title="Выбрать неделю" class="btn-icon"', attrib={'type': 'submit', 'name': settings.WEEK_BUTTON_SELECT})
    i = et.SubElement(btn, 'i class="fa fa-arrow-circle-o-down fa-lg" aria-hidden="true"')
    i.text = '\n'

    # HEADERS ROW
    #
    row = et.SubElement(table, 'tr', {'style': 'border: 2px solid green'})
    col = et.SubElement(row, settings.TAG_TD_CENTER)
    lab = et.SubElement(col, settings.TAG_A_HEAD)
    lab.text = 'Дата:'

    col = et.SubElement(row, settings.TAG_TD_CENTER)
    lab = et.SubElement(col, settings.TAG_A_HEAD)
    lab.text = 'Проект:'

    col = et.SubElement(row, settings.TAG_TD_CENTER)
    lab = et.SubElement(col, settings.TAG_A_HEAD)
    lab.text = 'Часы:'

    col = et.SubElement(row, settings.TAG_TD_CENTER)
    lab = et.SubElement(col, settings.TAG_A_HEAD + ' title="Дополнительная информация"')
    lab.text = 'Описание:'

    col = et.SubElement(row, settings.TAG_TD_CENTER)
    lab = et.SubElement(col, settings.TAG_A_HEAD + ' title="Комментарий согласования с руководителем"')
    lab.text = 'Комментарий:'

    col = et.SubElement(row, settings.TAG_TD_CENTER)
    lab = et.SubElement(col, settings.TAG_A_HEAD)
    lab.text = 'Статус:'

    # FIELDS ROW
    #
    row = et.SubElement(table, 'tr')
    # ДАТА
    col = et.SubElement(row, 'td')
    et.SubElement(col, settings.TAG_INPUT, attrib={'type': 'date', 'name': DATE_NAME, 'value': date})

    # ПРОЕКТЫ
    col = et.SubElement(row, 'td')
    prj_id = app.get_c_prop(settings.C_PROJECT_ID)  # текущий проект из кэш
    prj_dict = data_module.get_all_projects_dict(app.get_c_prop(settings.C_USER_ID))
    p_list = et.SubElement(col, 'select', {'name': SELECT_PROJECT_NAME, 'style': 'min-width: 150px'})

    if prj_dict is None:
        raise Exception(f'Список проектов не сформирован. Возможно, нет подключения к базе данных!')

    for value in prj_dict:
        p_dict = prj_dict[value]
        # util.log_debug(f'=={value}={p_dict}')
        if value == prj_id:
            opt = et.SubElement(p_list, 'option selected', attrib={'value': value})
        else:
            opt = et.SubElement(p_list, 'option', attrib={'value': value})
        opt.text = p_dict[settings.F_PRJ_NAME]

    # ЧАСЫ
    col = et.SubElement(row, 'td')
    et.SubElement(col, settings.TAG_INPUT + ' size="3"', attrib={'type': 'text', 'name': INPUT_HOURS_NAME, 'value': hours})

    # ЗАМЕТКИ
    col = et.SubElement(row, 'td')
    et.SubElement(col, settings.TAG_INPUT + ' size="20"', attrib={'type': 'text', 'name': INPUT_NOTE_NAME, 'value': note, 'title': note})

    # КОММЕНТАРИЙ
    col = et.SubElement(row, 'td')
    et.SubElement(col, settings.TAG_INPUT + ' size="20"', attrib={'type': 'text', 'name': INPUT_COMMENT_NAME, 'value': comment, 'title': comment})

    # СТАТУСЫ
    col = et.SubElement(row, 'td')
    select_status = et.SubElement(col, 'select style="max-width:150px;"', attrib={'name': SELECT_STATUS_NAME})
    valid_statuses = settings.get_valid_statuses(status)
    for value in valid_statuses:
        if value == status:
            opt = et.SubElement(select_status, 'option selected', attrib={'value': value})
        else:
            opt = et.SubElement(select_status, 'option', attrib={'value': value})
        opt.text = valid_statuses[value]

    # TABLE & BUTTONS ROW
    #
    row_1 = et.SubElement(table, 'tr')
    col_table = et.SubElement(row_1, 'td colspan=5 rowspan=3 align=center', {'style': 'border: 2px solid'})  # Объединенная ячейка для таблицы
    col_btns = et.SubElement(row_1, 'td', {'align': 'center', 'valign': 'top', 'width': '50'})
    # Кнопка СОХРАНИТЬ
    btn_save = et.SubElement(col_btns, 'button', attrib={'type': 'submit', 'name': settings.SAVE_BUTTON, 'value': 'submit'})
    btn_save.text = 'сохранить'

    # Кнопка УДАЛИТЬ
    if tsh_id == '':
        b_tag_name = 'button disabled'
    else:
        b_tag_name = 'button'
    btn_delete = et.SubElement(col_btns, b_tag_name, attrib={'type': 'submit', 'name': settings.DELETE_BUTTON, 'value': 'delete'})
    btn_delete.text = 'удалить'

    # TABLE AREA
    #
    time_sheets_data = data_module.get_data(user_id=app.get_c_prop(settings.C_USER_ID), week=week)
    add_timesheet_table(time_sheets_data, col_table)


def add_timesheet_table(data, column):

    prj_col_width = '330px'
    date_col_width = '50px'
    c_btn_value = app.get_c_prop(settings.C_TSH_BTN_VALUE)

    curr_tsh_id = app.get_c_prop(settings.C_TIMESHEET_ID)
    table_tsh = et.SubElement(column, 'table', {'style': 'width: 100%; border-spacing: 0px 0px;'})

    # HEAD ROW (project + dates)
    #
    dates_node = et.SubElement(table_tsh, 'tr')
    dates_col_node = et.SubElement(dates_node, settings.TAG_TD_BTN_HEADER, {'style': f'width: {prj_col_width};'})
    dates_col_node.text = 'Проекты'

    days = util.list_dates_in_week(week=app.get_c_prop(settings.C_WEEK))
    for day in days:
        dates_cell_node = et.SubElement(dates_node, settings.TAG_TD_BTN_HEADER, {'style': f'width: {date_col_width};'})
        btn_day = et.SubElement(dates_cell_node, 'a', attrib={'type': 'submit', 'name': 'btn_' + day, 'value': day})
        btn_day.text = util.date_to_day(day)

    # TABLE ROWS (project + hours)
    #
    if data is not None:
        row = 0
        for prj_id in data:
            # projects
            #
            row += 1
            days = data[prj_id][settings.FLD_TSH_DICT]
            col = 0
            row_node = et.SubElement(table_tsh, 'tr', {'style': f'background-color: {get_row_color(row)}; padding: none;'})
            project_ceil = et.SubElement(row_node, 'td', {'style': f'width: {prj_col_width};'})
            project_ceil.text = data[prj_id][settings.F_PRJ_NAME]
            for day in days:
                col += 1
                time_sheets = days[day]
                # util.log_debug(f'time_sheets: {day}={time_sheets}')
                for tsh_id in time_sheets:
                    btn_tag = settings.TAG_BUTTON_TABLE
                    tag_td = settings.TAG_TD_CENTER
                    day_node = et.SubElement(row_node, tag_td, {'style': f'width: {date_col_width};'})
                    if tsh_id == settings.EMPTY_ID_KEY:
                        # new timesheet button
                        btn_value = prj_id + settings.SPLITTER + settings.SPLITTER + day
                        hours = '0'
                    else:
                        # existing timesheet button
                        btn_value = prj_id + settings.SPLITTER + tsh_id + settings.SPLITTER
                        hours = time_sheets[tsh_id][settings.F_TSH_HOURS]
                        note = time_sheets[tsh_id][settings.F_TSH_NOTE]

                        # Раскрасить по статусам
                        status = time_sheets[tsh_id][settings.F_TSH_STATUS]
                        title = f' title="Описание: {note}"'
                        if status == settings.EDIT_STATUS:
                            btn_tag = settings.TAG_BUTTON_TABLE_EDIT + title

                        if status == settings.IN_APPROVE_STATUS:
                            btn_tag = settings.TAG_BUTTON_TABLE_IN_APPROVE + title

                        if status == settings.APPROVED_STATUS:
                            btn_tag = settings.TAG_BUTTON_TABLE_APPROVED + title

                        if status == settings.REJECTED_STATUS:
                            btn_tag = settings.TAG_BUTTON_TABLE_REJECTED + title

                    if btn_value == c_btn_value: # Выбранная ячейка
                        btn_node = et.SubElement(day_node, btn_tag,
                                                 attrib={
                                                     'type': 'submit',
                                                     'name': settings.TABLE_BUTTON,
                                                     'value': btn_value,
                                                     'style': 'border: 3px solid blue;'})
                    else:
                        btn_node = et.SubElement(day_node, btn_tag,
                                                 attrib={
                                                     'type': 'submit',
                                                     'name': settings.TABLE_BUTTON,
                                                     'value': btn_value})

                    # util.log_tmp(f'btn_value: {btn_value}; btn_cache: {c_btn_value}')
                    btn_node.text = hours

    else:  # Показать доступные проекты с пустыми кнопками
        if settings.SHOW_EMPTY_WEEK:
            prj_dict = data_module.get_all_projects_dict(app.get_c_prop(settings.C_USER_ID))
            row = 0
            for prj_id in prj_dict:
                row += 1
                prj_data = prj_dict[prj_id]
                prj_name = prj_data[settings.F_PRJ_NAME]

                row_node = et.SubElement(table_tsh, 'tr', {'style': f'background-color: {get_row_color(row)}; padding: none;'})
                project_ceil = et.SubElement(row_node, 'td', {'style': f'width: {prj_col_width};'})
                project_ceil.text = prj_name
                # util.log_debug(f'add_timesheet_table_area: {prj_id}={prj_name}')
                for day in days:
                    day_node = et.SubElement(row_node, 'td', {'style': f'width: {date_col_width};'})
                    btn_value = prj_id + settings.SPLITTER + settings.SPLITTER + day
                    # btn_node = et.SubElement(day_node, settings.TAG_BUTTON_TABLE, attrib={'type': 'submit', 'name': settings.TABLE_BUTTON, 'value': btn_value})
                    if btn_value == c_btn_value:  # Выбранная ячейка
                        btn_node = et.SubElement(day_node,
                                                 settings.TAG_BUTTON_TABLE,
                                                 attrib={
                                                     'type': 'submit',
                                                     'name': settings.TABLE_BUTTON,
                                                     'value': btn_value,
                                                     'style': 'border: 3px solid blue;'})
                    else:
                        btn_node = et.SubElement(day_node,
                                                 settings.TAG_BUTTON_TABLE,
                                                 attrib={
                                                     'type': 'submit',
                                                     'name': settings.TABLE_BUTTON,
                                                     'value': btn_value})
                    btn_node.text = '0'


def create_timesheet_html():
    util.log_debug(f'create_timesheet_html')
    # week = util.get_current_week(host)

    tsh_id = app.get_c_prop(settings.C_TIMESHEET_ID)
    tsh_date = app.get_c_prop(settings.C_DATE)

    if tsh_id == '':  # пустая кнопка на дату
        tsh_entry = {
                settings.F_TSH_HOURS: '',
                settings.F_TSH_NOTE: '',
                settings.F_TSH_COMMENT: '',
                settings.F_TSH_STATUS: settings.EDIT_STATUS,
                settings.F_TSH_DATE: tsh_date
            }

    else:  # кнопка на дату с данными
        tsh_entry = data_module.get_entry(tsh_id=tsh_id)
        if tsh_entry is None:
            msg = f'create_timesheet_html: Запись tsh_id="{tsh_id}" не найдена в базе данных'
            html_i = create_info_html(module=settings.M_TIMESHEETS, i_type=settings.INFO_TYPE_ERROR, msg=msg)
            return html_i


    # HTML
    #
    base_html = BaseHTML('TimeSheets', settings.MODULES[settings.M_TIMESHEETS])
    form = base_html.get_form()

    # INFO AREA
    #
    # util.log_debug(f'tsh_entry: {tsh_entry}')
    if tsh_id != '' and tsh_entry is None:  # Зачитать и отобразить INFO запись если tsh_id есть в кэше
        tsh_entry = data_module.get_entry(tsh_id=tsh_id)

    add_timesheets_info(form=form, tsh_entry=tsh_entry)

    # util.log_debug(f'str_html: {base_html.get_html()}')

    return base_html.get_html()


# USERS
#
def add_user_info(table, fields):

    u_id = fields[0][5]
    u_role = fields[2][5]

    row = 0
    for f in fields:
        if f[0] != 'ID':  # Пропустить атрибут ID
            # util.log_debug(f'row={row}')
            edt_row = et.SubElement(table, 'tr')

            # Название атрибута
            col_1 = et.SubElement(edt_row, 'td', {'style': 'min-width: 250px;', 'align': 'right'})
            if f[4] == 'ir' or f[4] == 'p':  # Обязательные атрибуты
                fld = et.SubElement(col_1, settings.TAG_A_HEAD_REQ)
            else:
                fld = et.SubElement(col_1, settings.TAG_A_HEAD)
            fld.text = f[0]

            # if row > 3:  # 2 ячейки в одну для длинных полей)
            #     col_2 = et.SubElement(edt_row, 'td colspan=3', {'style': 'padding-left: 5px'})
            # else:  # одна ячейка
            #     col_2 = et.SubElement(edt_row, 'td', {'style': 'width: 300px; padding-left: 5px'})  # Определяет общую ширину таблицы!
            col_2 = et.SubElement(edt_row, 'td', {'style': 'width: 300; padding-left: 5px; border: 0px solid blue;'})

            if f[4] == 'i' or f[4] == 'ir':  # Input
                et.SubElement(col_2, f'{settings.TAG_INPUT} size={f[1]} class=input-bottom-border',
                                  {'type': 'text', 'name': f[3], 'value': f[5]})

            if f[4] == 'p':  # Password
                et.SubElement(col_2, f'{settings.TAG_INPUT} size={f[1]} class=input-bottom-border',
                                  {'type': 'password', 'name': f[3], 'value': ''})

            if f[4] == 'r':  # Roles List
                p_list = et.SubElement(col_2, 'select class=input-bottom-border', attrib={'name': settings.F_USR_ROLE})
                for k in settings.R_LIST:
                    if u_role == k:
                        opt = et.SubElement(p_list, 'option selected', attrib={'value': k})
                    else:
                        opt = et.SubElement(p_list, 'option', attrib={'value': k})
                    opt.text = settings.R_LIST[k]

            if row == 0:
                # Ячейка с кнопками
                col_3 = et.SubElement(edt_row,
                                         'td rowspan=5 class=td-buttons',
                                         {'align': 'left', 'valign': 'top', 'width': '40'})
                add_buttons(col_3, u_id)

                # Пустая, объединенная ячейка для выравнивания общей ширины
                col_4 = et.SubElement(edt_row,
                                         'td rowspan=5 class=td-buttons',
                                         {'align': 'left', 'valign': 'middle', 'width': '100%', 'style': 'border: 0px solid blue;'})

            row += 1


def add_user_table(table, fields):
    x = '0px'
    # Объединенная ячейка для таблицы пользователей
    row = et.SubElement(table, 'tr')
    col = et.SubElement(row, 'td colspan=4 align=left', {'style': f'border: {x} solid black;'})  # Объединенная ячейка

    # Таблица пользователей
    table_usr = et.SubElement(col, 'table', {'style': 'width: 100%; border-spacing: 0px 0px;'})
    t_head = et.SubElement(table_usr, 'thead', {'style': 'display: table; width: 100%;'})
    # t_body = et.SubElement(table_usr, 'tbody', {'style': 'display: block; width: 100%; max-height: 100px; overflow: auto;'})

    # Заголовок таблицы пользователей
    hd_row = et.SubElement(t_head, 'tr')
    for f in fields:
        if f[4] != 'p':
            if f[0] != 'ID':
                col = et.SubElement(hd_row,
                                    'td align=left class="td-header td-header-borders"',
                                    {'style': f'width: {f[2]}; border: {x} solid red;'})
                col.text = f[0]
            else:  # Кнопка NEW вместо ID
                col = et.SubElement(hd_row,
                                    'td align=left class="td-header td-header-borders"',
                                    {'style': f'min-width: {f[2]}; border: {x} solid red;'})
                btn = et.SubElement(col,
                                    'button class="material-symbols-outlined btn-t-cell" title="Создать нового пользователя"',
                                    {
                                        'style': 'padding-inline: 0px; margin: 0; margin-left: 5',
                                        'name': settings.NEW_BUTTON,
                                    })
                btn.text = 'person_add'

    # Список пользователей из БД (тело таблицы пользователей)
    users = data_module.get_all_users_dict()
    # util.log_debug(f'create_users_html: users={users}')

    n_row = 1
    for user in users:
        row = et.SubElement(t_head, 'tr', {'style': f'background-color: {get_row_color(n_row)}; padding: none;'})
        for f in fields:
            if f[4] == 'p':
                continue
            if f[0] != 'ID':
                col = et.SubElement(row, 'td class=td-table-border',
                                    {'style': f'width: {f[2]}; border: {x} solid green;'})
                col.text = users[user][f[3]]
            else:  # Кнопки в строке таблицы
                col = et.SubElement(row, 'td align=left class=td-table-border',
                                    {'style': f'min-width: {f[2]}; border: {x} solid red;'})
                add_table_buttons(col, users[user][f[3]])

        n_row += 1


def create_users_html(user_props=(), show_info=False):
    # util.log_debug('create_users_html...')

    u_id = '' if len(user_props) == 0 or user_props[0] is None else str(user_props[0])
    u_name = '' if len(user_props) == 0 or user_props[1] is None else str(user_props[1])
    u_role = '' if len(user_props) == 0 or user_props[2] is None else str(user_props[2])
    u_pwd = '' if len(user_props) == 0 or user_props[3] is None else str(user_props[3])
    u_mail = '' if len(user_props) == 0 or user_props[4] is None else str(user_props[4])
    u_info = '' if len(user_props) == 0 or user_props[5] is None else str(user_props[5])

    fields = (
        ('ID', 10, 80, settings.F_USR_ID, 'i', u_id),
        ('Имя', 60, 100*3, settings.F_USR_NAME, 'ir', u_name),
        ('Роль', 60, 150*3, settings.F_USR_ROLE, 'r', u_role),
        ('Пароль', 35, 100*3, settings.F_USR_PASSWORD, 'p', u_pwd),
        ('Электронный адрес', 60, 150*3, settings.F_USR_MAIL, 'i', u_mail),
        ('Дополнительная информация', 60, 500*3, settings.F_USR_INFO, 'i', u_info),
    )

    # HTML
    #
    base_html = BaseHTML('Users', settings.MODULES[settings.M_USERS])
    form = base_html.get_form()
    p = et.SubElement(form, 'p')

    # Общая таблица
    table = et.SubElement(p, 'table', {'style': 'width: 100%; border: 0px solid blue;'})

    # Поля редактирования
    if len(user_props) > 0 or show_info:
        add_user_info(table, fields)

    # Таблица пользователей
    add_user_table(table, fields)

    # util.log_debug(f'html={base_html.get_html()}')
    return base_html.get_html()

# PROJECTS
#
def add_project_info(table, fields):

    p_id = fields[0][5]
    # get managers
    users = data_module.get_all_users_dict(True)  # Поиск Managers
    # util.log_debug(f'add_project_info: managers={users}')
    if len(users) == 0:
        raise Exception(f'В базе данных нет пользователей с ролью {settings.R_MANAGER}.\nВозможно, база данных недоступна!')

    row = 0
    for f in fields:
        if f[0] != 'ID':  # Пропустить атрибут ID
            edt_row = et.SubElement(table, 'tr')

            # Название атрибута
            col_1 = et.SubElement(edt_row, 'td', {'style': 'width: 150px;', 'align': 'right'})
            if f[4] == 'ir' or f[4] == 'm':  # Обязательные атрибуты
                fld = et.SubElement(col_1, settings.TAG_A_HEAD_REQ)
            else:
                fld = et.SubElement(col_1, settings.TAG_A_HEAD)
            fld.text = f[0]

            col_2 = et.SubElement(edt_row, 'td', {'style': 'width: 200px; padding-left: 5px;'})
            # Значение атрибута
            if f[4] == 'i' or f[4] == 'ir':  # Input
                et.SubElement(col_2,
                              f'{settings.TAG_INPUT} size={f[1]} class=input-bottom-border',
                              {'type': 'text', 'name': f[3], 'value': f[5]})

            if f[4] == 'm':  # Managers list
                if p_id == '':  # Смена руководителя доступна только для существующих проектов!?
                    select = 'select disabled class=input-bottom-border'
                else:
                    select = 'select class=input-bottom-border'
                m_list = et.SubElement(col_2, select, attrib={'name': f[3], 'style': 'min-width:200px;'})
                for u in users:
                    u_id = users[u][settings.F_USR_ID]
                    u_name = users[u][settings.F_USR_NAME]
                    # util.log_debug(f'=={f[5]}={u_id}:{u_name}')
                    if f[5] == u_id:
                        opt = et.SubElement(m_list, 'option selected', attrib={'value': u_id})
                    else:
                        opt = et.SubElement(m_list, 'option', attrib={'value': u_id})
                    opt.text = u_name

            if f[4] == 'd':  # Date
                et.SubElement(col_2, settings.TAG_INPUT, attrib={'type': 'date', 'name': f[3], 'value': f[5], 'style': 'min-width:150px;'})

            # Объединенные ячейки
            if row == 0:
                # Ячейка с командой проекта
                col_3 = et.SubElement(edt_row,
                                         'td rowspan=5 class=td-buttons',
                                         {'align': 'left', 'valign': 'top', 'width': '300'})
                add_project_team(col_3, p_id)

                # Ячейка с кнопками
                col_4 = et.SubElement(edt_row,
                                         'td rowspan=5 class=td-buttons',
                                         {'align': 'left', 'valign': 'top', 'width': '40'})
                add_buttons(col_4, p_id)

                # Пустая, объединенная ячейка для выравнивания общей ширины
                col_4 = et.SubElement(edt_row,
                                      'td rowspan=5 class=td-buttons',
                                      {'align': 'left', 'valign': 'middle', 'width': 'auto',
                                       'style': 'border: 0px solid red;'})

            row += 1


def add_project_team(col, prj_id):
    # util.log_debug(f'add_project_team: {col}, {prj_id}')
    table = et.SubElement(col, 'table', {'style': 'width: 100%; border: 0px solid blue;'})
    t_head = et.SubElement(table, 'thead', {'style': 'display: table; width: 100%'})
    t_body = et.SubElement(table, 'tbody', {'style': 'display: block; height: 110px; overflow: auto; width: 100%'})

    # Заголовок таблицы
    #
    r = et.SubElement(t_head, 'tr')
    c = et.SubElement(r, 'td align="center" class="td-header td-header-borders"', {'style': 'width: 100%; border: 0px solid red;'})
    a = et.SubElement(c, 'a')
    a.text = 'Исполнители'

    # Участники (Пользователи)
    #
    users = data_module.get_all_users_dict()  # список всех пользователей
    if prj_id != '':  # команда проекта
        team = data_module.get_project_team_list(prj_id)
    else:
        team = ()
    for u in users:
        # util.log_debug(f'u={u}:{users[u][settings.F_USR_NAME]}:{users[u][settings.F_USR_ROLE]}')
        r = et.SubElement(t_body, 'tr')

        # Checkbox
        c = et.SubElement(r, 'td align="left"', {'style': 'border: 0px solid red;'})
        # util.log_debug(f'u={u} in team={team}')
        if str(u) in team:
            tag_cb = 'input type=checkbox checked'
        else:
            tag_cb = 'input type=checkbox'
        cb = et.SubElement(c, tag_cb, {'name': u, 'style': 'height: 15px'})
        # cb.text = users[u][settings.F_USR_NAME]

        # Text
        c = et.SubElement(r, 'td align="left"', {'style': 'border: 0px solid blue;'})
        a = et.SubElement(c, 'a')
        a.text = f'{users[u][settings.F_USR_NAME]} ({users[u][settings.F_USR_ROLE]})'


def add_project_table(table, fields):
    x = '0px'
    brd = 'border: 0px solid gray;'
    row = et.SubElement(table, 'tr')

    # Объединенная ячейка для таблицы проектов
    col = et.SubElement(row, 'td colspan=5 align=left', {'style': brd})

    # Таблица проектов
    table_prj = et.SubElement(col, 'table', {'style': 'width: 100%; border-spacing: 0px 0px;'})
    t_head = et.SubElement(table_prj, 'thead', {'style': 'display: table; width: 100%'})
    # t_body = et.SubElement(table_prj, 'tbody', {'style': 'display: block; max-height: 300px; overflow: auto; width: 100%'})

    # Заголовок таблицы проектов
    hd_row = et.SubElement(t_head, 'tr', {'style': 'width: 100%'})
    for f in fields:
        if f[4] == 'm':  # Пропустить колонку список пользователей
            continue
        if f[0] != 'ID':
            col_h = et.SubElement(hd_row,
                                  'td align=left class="td-header td-header-borders"',
                                  {'style': f'width: {f[2]}; border: {x} solid blue'})
            fld = et.SubElement(col_h, 'a')
            fld.text = f[0]
        else:
            col = et.SubElement(hd_row,
                                'td align=left class="td-header td-header-borders"',
                                {'style': f'width: {f[2]}; border: {x} solid blue'})
            btn = et.SubElement(col,
                                'button class="material-symbols-outlined btn-t-cell" title="Создать новый проект"',
                                {
                                    'style': 'padding-inline: 0px; margin: 0; margin-left: 5',
                                    'name': settings.NEW_BUTTON,
                                })
            btn.text = 'add_chart'

    # Список проектов из БД (тело таблицы)
    projects = data_module.get_all_projects_dict(app.get_c_prop(settings.C_USER_ID), False)
    # util.log_debug(f'add_project_table: projects={projects}')

    n_row = 1
    for p in projects:
        row = et.SubElement(t_head, 'tr', {'style': f'background-color: {get_row_color(n_row)}; padding: none;'})
        for f in fields:
            if f[4] == 'm':  # Пропустить колонку список пользователей
                continue
            if f[0] != 'ID':
                if f[4] != 'p':
                    col = et.SubElement(row, 'td class=td-table-border', {'style': f'width: {f[2]}; border: {x} solid blue'})
                    col.text = projects[p][f[3]]
            else:  # Кнопки в строке таблицы
                col = et.SubElement(row, 'td class=td-table-border', {'style': f'min-width: {f[2]}; border: {x} solid blue'})
                add_table_buttons(col, p)

        n_row += 1


def create_projects_html(prj_props=(), show_info=False):
    # util.log_debug('create_projects_html...')
    try:
        p_id = '' if len(prj_props) == 0 or prj_props[0] is None else str(prj_props[0])
        p_mgr_id = str(app.get_c_prop(settings.C_USER_ID)) if len(prj_props) == 0 or prj_props[1] is None else str(prj_props[1])
        p_name = '' if len(prj_props) == 0 or prj_props[2] is None else str(prj_props[2])
        p_s_date = '' if len(prj_props) == 0 or prj_props[3] is None else str(prj_props[3])
        p_e_date = '' if len(prj_props) == 0 or prj_props[4] is None else str(prj_props[4])
        p_org = '' if len(prj_props) == 0 or prj_props[5] is None else str(prj_props[5])

        fields = (
            ('ID', 10, 80, settings.F_PRJ_ID, 'i', p_id),
            ('Название', 50, 550*3, settings.F_PRJ_NAME, 'ir', p_name),
            ('Организация', 50, 400*3, settings.F_PRJ_ORG, 'i', p_org),
            ('Руководитель', 50, 200*3, settings.F_PRJ_MANAGER_ID, 'm', p_mgr_id),
            ('Начало', 40, 90*3, settings.F_PRJ_START_DATE, 'd', p_s_date),
            ('Окончание', 40, 40*3, settings.F_PRJ_END_DATE, 'd', p_e_date),
        )

        # HTML
        #
        base_html = BaseHTML('Projects', settings.MODULES[settings.M_PROJECTS])
        form = base_html.get_form()
        p = et.SubElement(form, 'p')

        # Общая таблица
        table = et.SubElement(p, 'table', {'style': 'width: 100%; border: 0px solid blue;'})

        # Поля редактирования
        if len(prj_props) > 0 or show_info:
            add_project_info(table, fields)

        # Таблица проектов
        add_project_table(table, fields)

        return base_html.get_html()

    except Exception as ex:
        return create_info_html(module=settings.M_PROJECTS, i_type=settings.INFO_TYPE_ERROR, msg=f'{ex}')






# Для тестирования создания html
#
def t_html():
    html = et.Element('html', attrib={'lang': 'ru'})
    head = et.SubElement(html, 'head')
    et.SubElement(head, 'link', attrib={"rel": "stylesheet", "type": "text/css", "href": 'static/css/common.css'})
    et.SubElement(head, 'link', attrib={"rel": "stylesheet", "href": 'https://cdnjs.cloudflare.com/ajax/libs/font-awesome/4.7.0/css/font-awesome.min.css'})
    et.SubElement(head, 'link', {"rel": "stylesheet", "href": 'https://fonts.googleapis.com/css2?family=Material+Symbols+Outlined'})

    t_title = et.SubElement(head, 'title')
    t_title.text = 'x'

    body = et.SubElement(html, 'body')
    form = et.SubElement(body, 'form', attrib={'name': 'form', 'method': 'POST'})
    p = et.SubElement(form, 'p')

    btn_2 = et.SubElement(p, 'button class="material-symbols-outlined"', {'style': 'width: 25px; height: 25px; padding-inline: 0px; border: 0px'})
    btn_2.text = 'draft_orders'
    et.SubElement(p, 'br')
    btn_1 = et.SubElement(p, 'button', {'style': 'background-image: url("static/img/edit.png"); width: 24px; height: 24px;'})
    btn_1.text = '\n'

    s_html = et.tostring(html).decode()
    # util.log_debug(f'=={s_html}')

    return s_html
## APPROVEMENT
#

def add_approvement_info(table):
    row1 = et.SubElement(table, 'tr')

    col1 = et.SubElement(row1, 'td', {'style': 'border: 0px solid red'})
    note = et.SubElement(col1, 'textarea', {'name': 'feedback', 'placeholder': 'замечание', 'class': 'feedback'})
    note.text = '\n'

    col2 = et.SubElement(row1, 'td', {'style': 'border: 0px solid green; max-width: 105px'})
    agree_btn = et.SubElement(col2, 'button', {'type': 'submit', 'name': 'agree_btn', 'class': 'btn-left-width'})
    agree_btn.text = 'Согласовать'
    del_btn = et.SubElement(col2, 'button', {'type': 'submit', 'name': 'del_btn', 'class': 'btn-left-width'})
    del_btn.text = 'Отклонить'

    et.SubElement(row1, 'td', {'style': 'border: 0px solid black; width: 100%'})


def add_approvement_table(table, entries, is_clear):
    row = et.SubElement(table, 'tr', {'style': 'width: 100%'})
    col = et.SubElement(row, 'td colspan=3 align=left', {'style': 'border: 0px solid grey;'})  # Объединенная ячейка

    # Таблица согласований
    # Заголовок таблицы
    table_app = et.SubElement(col, 'table', {'style': 'width: 100%; border-spacing: 0px 0px;'})
    t_head = et.SubElement(table_app, 'thead class="td-header"', {'style': 'display: table; width: 100%'})
    # t_body = et.SubElement(table_app, 'tbody', {'style': 'display: block; max-height: 300px; overflow: auto; width: 100%'})

    hd_row = et.SubElement(t_head, 'tr')
    col_h = et.SubElement(hd_row, 'td align="left" class="td-header td-header-borders"',
                          {'style': 'max-width: 30; border: 0px solid blue'})
    if is_clear == '1':
        btn = et.SubElement(col_h,
                            'button class="material-symbols-outlined btn-t-cell" title="Выделить всё"',
                            {
                                'style': 'padding-inline: 0px; margin: 0; margin-left: 0',
                                'name': settings.ALL_FLAG_BUTTON, 'value': '0'
                            })
        btn.text = 'check_box'
    else:
        btn = et.SubElement(col_h,
                            'button class="material-symbols-outlined btn-t-cell" title="Очистить всё"',
                            {
                                'style': 'padding-inline: 0px; margin: 0; margin-left: 0',
                                'name': settings.ALL_FLAG_BUTTON, 'value': '1'
                            })
        btn.text = 'check_box_outline_blank'

    col_h = et.SubElement(hd_row, 'td align="left" class="td-header td-header-borders"',
                          {'style': 'width: 80; border: 0px solid blue;'})
    fld = et.SubElement(col_h, 'a')
    fld.text = 'Имя'

    col_h = et.SubElement(hd_row, 'td align="left" class="td-header td-header-borders"',
                          {'style': 'width: 80; border: 0px solid blue;'})
    fld = et.SubElement(col_h, 'a')
    fld.text = 'Дата'

    col_h = et.SubElement(hd_row, 'td align="left" class="td-header td-header-borders"',
                          {'style': 'width: 300; border: 0px solid blue;'})
    fld = et.SubElement(col_h, 'a')
    fld.text = 'Проект'

    col_h = et.SubElement(hd_row, 'td align="left" class="td-header td-header-borders"',
                          {'style': 'width: 50; border: 0px solid blue;'})
    fld = et.SubElement(col_h, 'a')
    fld.text = 'Часы'

    col_h = et.SubElement(hd_row, 'td align="left" class="td-header td-header-borders"',
                          {'style': 'width: 300; border: 0px solid blue;'})
    fld = et.SubElement(col_h, 'a')
    fld.text = 'Описание'

    col_h = et.SubElement(hd_row, 'td align="left" class="td-header td-header-borders"',
                          {'style': 'width: 300; border: 0px solid blue;'})
    fld = et.SubElement(col_h, 'a')
    fld.text = 'Комментарий'

    # Тело таблицы
    if entries is None:
        row = et.SubElement(t_head, 'tr', {'style': f'background-color: #FFFFFF;font-weight: normal'})
        col = et.SubElement(row, 'td colspan=7 align=center')
        col.text = 'Нет доступных записей'

    else:
        n_row = 1
        for s in entries:
            row = et.SubElement(t_head, 'tr', {'style': f'background-color: {get_row_color(n_row)}; padding: none;'
                                                        f'font-weight: normal'})

            if is_clear == '1':
                col = et.SubElement(row, 'td align=left', {'style': 'max-width: 30'})
                et.SubElement(col, 'input', {'type': 'checkbox', 'name': f'{s}'})
            else:
                col = et.SubElement(row, 'td align=left', {'style': 'min-width: 30; max-width: 30'})
                et.SubElement(col, 'input checked', {'type': 'checkbox', 'name': f'{s}'})

            col = et.SubElement(row, 'td align=left', {'style': f'width:80'})
            col.text = entries[s][settings.F_USR_NAME]
            col = et.SubElement(row, 'td align=left', {'style': 'width:80'})
            col.text = entries[s][settings.F_TSH_DATE]
            col = et.SubElement(row, 'td align=left', {'style': 'width:300'})
            col.text = entries[s][settings.F_PRJ_NAME]
            col = et.SubElement(row, 'td align=left', {'style': 'width:50'})
            col.text = entries[s][settings.F_TSH_HOURS]
            col = et.SubElement(row, 'td align=left', {'style': 'width:300'})
            col.text = entries[s][settings.F_TSH_NOTE]
            col = et.SubElement(row, 'td align=left', {'style': 'width:300'})
            col.text = entries[s][settings.F_TSH_COMMENT]

            n_row += 1

def create_approvement_html(is_clear='1'):
    # отлавливаем форму
    entries = data_module.get_entries_for_approval(app.get_c_prop(settings.C_USER_ID))
    # util.log_info(f'entries: {entries}')

    # HTML
    #
    base_html = BaseHTML('Approvement', settings.MODULES[settings.M_APPROVEMENT])
    form = base_html.get_form()
    p = et.SubElement(form, 'p')

    # Общая таблица
    table = et.SubElement(p, 'table', {'style': 'border: 0px solid blue;'})

    # Поля редактирования
    add_approvement_info(table)

    # Таблица на согласование
    add_approvement_table(table, entries, is_clear)

    # рендеринг html
    #

    return base_html.get_html()


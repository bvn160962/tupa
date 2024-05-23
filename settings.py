import logging
import sys

# Для отладки - вход без регистрации
DBG_DO_LOGIN = False
DBG_USER_ID = 102
DBG_USER_NAME = 'user'
DBG_USER_ROLE = 'Administrator'

SHOW_EMPTY_WEEK = False

# Показывать диалог подтверждения удаления в виде модального окна
USE_MODAL_CONFIRMATION_DIALOG = True
CONFIRMATION_DIALOG_ID = 'confirm_dialog_id'

# Показывать сообщение в виде модального окна
USE_MESSAGE_DIALOG = True
MESSAGE_DIALOG_ID = 'message_dialog_id'
OK_BUTTON_ID = 'message_dialog_ok_btn_id'

# Имя ключа куки для передачи сообщения
COOKIE_SHOW_MESSAGE = 'showMessage'

CLIENT_OS_SUPPORTED = ('Windows', 'iPad', 'iPhone')

IS_WINDOWS = (sys.platform == 'win32')
if IS_WINDOWS:
    LOG_DIR = 'c:\\tsh_home\\logs\\'
else:
    LOG_DIR = '/var/log/timesheets/'

LOG_FILE_NAME = LOG_DIR + 'app_server.log'
LOG_FILE_MODE = 'w'  # 'a' - append, 'w' - rewrite
LOG_FILE_LEVEL = logging.DEBUG

LOG_FILE_FORMAT = '%(asctime)s %(levelname)s: %(message)s'
# LOG_FILE_FORMAT = '%(asctime)s %(funcName)s, line %(lineno)s: %(message)s'

# SESSION
S_PERMANENT = False
S_LIFETIME_IN_MINUTES = 15

# Список ролей
#
R_ADMIN = 'Administrator'
R_MANAGER = 'Manager'
R_USER = 'User'
R_LIST = {
    R_ADMIN: 'Администратор',
    R_MANAGER: 'Руководитель проектов',
    R_USER: 'Исполнитель',
}

# Регистрация модулей
#
M_TIMESHEETS = 'timesheets'
M_APPROVEMENT = 'approvement'
M_USERS = 'users'
M_PROJECTS = 'projects'
M_LOGIN = 'login'

M_NAME = 'name'
M_URL = 'url'
M_TITLE = 'title'

API_TIMESHEETS_BY_USER = '/api/timesheets/<user_name>'

MODULES = {
    M_TIMESHEETS: {M_NAME: 'Табель', M_URL: '/timesheets', M_TITLE: 'Учет отработанного времени'},
    M_APPROVEMENT: {M_NAME: 'Согласование', M_URL: '/approvement', M_TITLE: 'Согласование отработанного времени'},
    M_USERS: {M_NAME: 'Пользователи', M_URL: '/users', M_TITLE: 'Управление пользователями'},
    M_PROJECTS: {M_NAME: 'Проекты', M_URL: '/projects', M_TITLE: 'Управление проектами'},
    M_LOGIN: {M_NAME: 'Регистрация', M_URL: '/login/<module>', M_TITLE: 'Регистрация'}
}

# Стили для тэгов
#
ENTER_DISABLE = 'onkeydown="if(event.keyCode==13){return false;}"'  # Предотвращение нажатия Enter на Input
TAG_INPUT = 'input ' + ENTER_DISABLE

TAG_BUTTON_TABLE = 'button class="btn-t"'  # Кнопка в таблице timesheets
TAG_BUTTON_TABLE_EDIT = 'button class="btn-t btn-t-edit"'  # Кнопка в таблице timesheets статус Edit
TAG_BUTTON_TABLE_IN_APPROVE = 'button class="btn-t btn-t-in_approve"'  # Кнопка в таблице timesheets статус In-Approve
TAG_BUTTON_TABLE_APPROVED = 'button class="btn-t btn-t-approved"'  # Кнопка в таблице timesheets статус Approved
TAG_BUTTON_TABLE_REJECTED = 'button class="btn-t btn-t-rejected"'  # Кнопка в таблице timesheets статус Rejected

TAG_TD_CENTER = 'td align=center'  # Ячейка под заголовки: атрибутов в timesheets info и кнопки в таблице timesheets
TAG_A_HEAD = 'a class="a-head"'  # Названия атрибутов в timesheets info
TAG_A_HEAD_REQ = 'a class="a-head required"'  # Названия обязатедьного атрибутов в timesheets info

TAG_TD_SELECTED = 'td align=center class=td-selected'  # Ячейка под нажатую кнопку в таблице timesheets
TAG_TD_BTN_HEADER = 'td align="center" class=td-header'  # Ячейка под заголовки в таблице timesheets
TAG_A_HEADER_P = 'a class=a-prj-head'  # Заголовок "Проекты" в таблице timesheets

# Типы информационных сообщений
#
INFO_TYPE_INFORMATION = 'Информация'
INFO_TYPE_WARNING = 'Предупреждение'
INFO_TYPE_ERROR = 'Ошибка'

# Переменные кэша
#
C_USER_ID = 'c_user_id'
C_USER_NAME = 'c_user_name'
C_USER_ROLE = 'c_user_role'
C_PROJECT_ID = 'c_project_id'
C_TIMESHEET_ID = 'c_timesheet_id'
C_DATE = 'c_date'
C_WEEK = 'c_week'
C_TSH_BTN_VALUE = 'c_tsh_btn_value'
C_CLIENT_OS_TYPE = 'c_client_os_type'

# Name для кнопок
#
TABLE_BUTTON = 'table_cell_btn'
SAVE_BUTTON = 'save_btn'
NEW_BUTTON = 'new_btn'
REF_BUTTON = 'reference_btn'
DELETE_BUTTON = 'delete_btn'
DELETE_BUTTON_ID = 'delete_btn_id'
DELETE_BUTTON_YES = 'delete_btn_yes'
DELETE_BUTTON_YES_ID = 'delete_btn_yes_id'
DELETE_BUTTON_NO = 'delete_btn_no'
DELETE_BUTTON_NO_ID = 'delete_btn_no_id'
WEEK_BUTTON_SELECT = 'week_btn'
WEEK_BUTTON_NEXT = 'next_week_btn'
WEEK_BUTTON_PREV = 'prev_week_btn'
WEEK_BUTTON_CURRENT = 'current_week_btn'
UPDATE_BUTTON = 'update_btn'
LOGOFF_BUTTON = 'logoff_btn'
HIDEINFO_BUTTON = 'hideinfo_btn'
DEBUG_BUTTON = 'debug_btn'

# Name для login диалога
#
LOGIN_BUTTON = 'login_btn'
LOGIN_USERNAME = 'user_name'
LOGIN_PASSWORD = 'user_password'

# Атрибуты таблицы <Projects>
#
F_PRJ_ID = 'prj_id'
F_PRJ_MANAGER_ID = 'prj_manager_id'
F_PRJ_NAME = 'prj_name'
F_PRJ_ORG = 'prj_organization'
F_PRJ_START_DATE = 'prj_start_date'
F_PRJ_END_DATE = 'prj_end_date'
F_PRJ_ALL = f'{F_PRJ_MANAGER_ID}, {F_PRJ_NAME}, {F_PRJ_START_DATE}, {F_PRJ_END_DATE}, {F_PRJ_ORG}'
F_PRJ_ALL_ID = f'{F_PRJ_ID}, {F_PRJ_ALL}'
F_PTM_PRJ_ID = 'ptm_project_id'
F_PTM_USR_ID = 'ptm_user_id'


#  Атрибуты таблицы <Timesheets>
#
F_TSH_ID = 'tsh_id'
F_TSH_USER_ID = 'tsh_user_id'
F_TSH_PRJ_ID = 'tsh_project_id'
F_TSH_HOURS = 'tsh_hours'
F_TSH_NOTE = 'tsh_note'
F_TSH_COMMENT = 'tsh_comment'
F_TSH_STATUS = 'tsh_status'
F_TSH_DATE = 'tsh_date'
F_TSH_ALL = f'{F_TSH_USER_ID}, {F_TSH_PRJ_ID}, {F_TSH_HOURS}, {F_TSH_STATUS}, {F_TSH_NOTE}, {F_TSH_DATE}, {F_TSH_COMMENT}'
F_TSH_ALL_ID = f'{F_TSH_ID}, {F_TSH_ALL}'

# Атрибуты таблицы <Users>
#
F_USR_ID = 'usr_id'
F_USR_NAME = 'usr_name'
F_USR_ROLE = 'usr_role'
F_USR_PASSWORD = 'usr_password'
F_USR_MAIL = 'usr_mail'
F_USR_INFO = 'usr_info'
F_USR_ALL = f'{F_USR_NAME}, {F_USR_ROLE}, {F_USR_PASSWORD}, {F_USR_MAIL}, {F_USR_INFO}'
F_USR_ALL_ID = f'{F_USR_ID}, {F_USR_ALL}'

# Атрибуты таблицы <ts_parameters>
#
F_PRM_NAME = 'prm_name'
F_PRM_VALUE = 'prm_value'
PRM_LOGIN_COUNT = 'login_count'

# Название словаря свойств Timesheet Entry
FLD_TSH_DICT = 'data'

# Признак незаполненного timesheet на дату и проект (пустая кнопка в таблице Timesheets)
EMPTY_ID_KEY = '-'

# Разделитель на кнопке в таблице Timesheets между prj_id, tsh_id и date
SPLITTER = '#'

# Статусы для Timesheets
#
EDIT_STATUS = 'edit'
IN_APPROVE_STATUS = 'in_approve'
APPROVED_STATUS = 'approved'
REJECTED_STATUS = 'rejected'
LIST_OF_STATUSES = {
    EDIT_STATUS: 'Редактируется',
    IN_APPROVE_STATUS: 'На согласовании',
}

# Доступный список статусов для статуса выбранного Timesheet
#
def get_valid_statuses(status=None):
    if status is None:
        return LIST_OF_STATUSES

    if status == '':
        return LIST_OF_STATUSES

    if status == EDIT_STATUS:
        return LIST_OF_STATUSES

    if status == IN_APPROVE_STATUS:
        return {IN_APPROVE_STATUS: 'На согласовании'}

    if status == APPROVED_STATUS:
        return {APPROVED_STATUS: 'Согласован'}

    if status == REJECTED_STATUS:
        return {
            EDIT_STATUS: 'Редактируется',
            REJECTED_STATUS: 'Отклонен',
        }

    return LIST_OF_STATUSES

# модуль Approval
AGREE_BUTTON = 'agree_btn'
REJECT_BUTTON = 'del_btn'
ALL_FLAG_BUTTON = 'all_flag_btn'


# -*- coding: utf-8 -*-
import logging

from django.core.exceptions import ValidationError
from django.db import models
from documents import retrospection
from rbuilder.models import TreeTextValue

import conf
from base.models import DocumentForeignKey
from base.utils import dictionary_to_choises
from docums.models import Doc, ISOGD_DOC_STATUSES, ISOGD_DOC_GIVEN
from processes.reference_book import CARD_TYPES
from smev3.models import Smev3Journal
from ws.adapters.minstroy.reference_book import SEND_TO_GS_STATUS, TURN, SEND_TO_ISOGD_STATUS
from ws.adapters.rldd2.reference_book import PGU_STATUS_COMPONENT_CREATOR, PGU_STATUS_DIRECTION
from ws.enumerates import RR_DISTRICT_TYPES, RR_APARTMENT_TYPES, RR_HOUSE_TYPES, RR_BUILD_TYPES, \
    RR_CORP_TYPES, RR_ALL_DOC_TYPES, RR_GROUND_UNIT_TYPES, RR_REALTY_UNIT_TYPES, RR_GKN_REALTY_UNIT_TYPES
from ws.signals import guag_message_accepted_ws, guag_message_accepted, document_accepted_ws, \
    document_accepted_from_vis_guag_gs

logger = logging.getLogger(__name__)

"""Модели приложения для работы с Веб-сервисами"""

AUTO_ERRORS_LIMIT = getattr(conf, u'AUTO_ERRORS_LIMIT', 20)
RLDD_ERRORS_LIMIT = getattr(conf, u'RLDD_ERRORS_LIMIT', 4)
AUTO_WAIT_DAYS = getattr(conf, u'AUTO_WAIT_DAYS', 14)

# Необходимые константы
INNER, OUTER = 1, 2
SERVICE_DIRECTIONS = (
    (INNER, u'Внутренний сервис (наш)'),
    (OUTER, u'Внешний сервис'),
)
"""
Напрвление сервиса:
    - 1 - Внутренний сервис (наш)
    - 2 - Внешний сервис
"""
ASYNC_TYPE, SYNC_TYPE = 1, 2
SERVICE_TYPES = (
    (ASYNC_TYPE, u'Асинхронный сервис'),
    (SYNC_TYPE, u'Синхронный сервис'),
)
"""
Типы сервисов:
    - 1 - Асинхронный сервис
    - 2 - Синхронный сервис
"""
REQUEST_STATES = (
    (1, u'Создано задание'),
    (2, u'Заявка подана'),
    (3, u'Заявка обрабатывается'),
    (4, u'Информация по заявке доступна'),  # не используется
    (5, u'Получен ответ'),
    (6, u'Ошибка'),
)
"""
Статусы запросов:
    - 1 - Создано задание
    - 2 - Заявка подана
    - 3 - Заявка обрабатывается
    - 4 - Информация по заявке доступна
    - 5 - Получен ответ
    - 6 - Ошибка
"""
REQUEST_STATES_DICT = dict(REQUEST_STATES)

REQUESTACCEPTED = u'Заявка принята'
REQUEST_DENIED = u'Заявка отклонена'
ERROR_STATE = u'Ошибка'

RLDD2_RECEIP_REQUEST_STATE = (
    (REQUESTACCEPTED, u'Заявка принята'),
    (REQUEST_DENIED, u'Заявка отклонена'),
    (ERROR_STATE, u'Ошибка'),
)

QUEUED = 1
QUEUED_FORM = 2
PROCESS = 11
READY_TO_ATTACH = 21
COMPLETED = 22
EMPTY = 4
REJECTED = 90
OVERDUED = 92
TASK_WAIT_OVERDUED = 93
ERROR = 99
RECEIVE_ERROR = 91
AUTO_REQUEST_STATES = (
    (QUEUED, u'Запрос ожидает создания'),
    (QUEUED_FORM, u'Запрос ожидает создания пользователем'),
    (PROCESS, u'Запрос ожидает обработки поставщиком данных '
              u'(результат будет получен автоматически, дополнительных действий не требуется)'),
    (READY_TO_ATTACH, u'Запрос успешно обработан, ожидается результирующее задание для выгрузки результата'),
    (COMPLETED, u'Запрос успешно обработан'),
    (EMPTY, u'Данные отсутствуют'),
    (OVERDUED, u'Превышено время ожидания ответа от поставщика данных, результат не будет получен автоматически'),
    (TASK_WAIT_OVERDUED, u'Запрос успешно обработан, однако превышено время ожидания результирующего задания '
                         u'для выгрузки результата'),
    (ERROR, u'Ошибка создания запроса'),
    (RECEIVE_ERROR, u'Ошибка получения/разбора ответа'),
    (REJECTED, u'Заявка отклонена'),
)

ROOM = u'ROOM'
EXTRA = u'EXTRA'
GROUND = u'GROUND'
BUILDING = u'BUILDING'

ROSREESTR_OBJECT_TYPES = (
    (ROOM, u'помещение'),
    (EXTRA, u'строение'),
    (GROUND, u'земельный участок'),
    (BUILDING, u'здание')
)

INN = u'inn'
OGRN = u'ogrn'
FNS_PARAM_TYPES = (
    (INN, u'ИНН'),
    (OGRN, u'ОГРН')
)

ADDRESS = u'ADDRESS'
CADASTRAL_NO = u'CADASTRAL_NO'
COND_CADASTRAL_NO = u'COND_CADASTRAL_NO'

ROSREESTR_IDENT_TYPES = (
    (ADDRESS, u'Запрос по адресу объекта'),
    (CADASTRAL_NO, u'Запрос по кадастровому номеру'),
    (COND_CADASTRAL_NO, u'Запрос по условному кадастровому номеру')
)

REQUEST_DIRECTIONS = (
    (INNER, u'Запрос к внешнему сервису'),
    (OUTER, u'Запрос к нашему сервису'),
)
"""
Направления запросов:
    - 1 - Запрос к внешнему сервису
    - 2 - Запрос в нашему сервису
"""

CREATED = u'created'
READY_TO_CREATE = u'turn'
DOC_WAIT = u'doc_wait'
SIGN_WAIT = u'sign_wait'
RECEIVED = u'finished'
OVERDUE = u'overdue'
READY_TO_RECREATE = u'recreate_ready'

RLDD2_REQUEST_STATES = (
    (CREATED, u'Заявка создана, ожидание обработки'),
    (READY_TO_RECREATE, u'Заявка готова к повторной отправке'),
    (READY_TO_CREATE, u'Заявка готова к созданию'),
    (SIGN_WAIT, u'Результат услуги получен, ожидание ЭЦП'),
    (DOC_WAIT, u'Заявка обработана, ожидание результа услуги'),
    (OVERDUE, u'Результат услуги получен, время ожидания документа/ЭЦП истекло, в случае отсутствия результирующего '
              u'документа и/или ЭЦП обратитесь в ТП'),
    (RECEIVED, u'Результат услуги получен, ЭЦП получена')
)

FNS_CODES = (
    (101, u'Запрашиваемые сведения не найдены'),
    (102, u'Запрос принят в обработку'),
    (103, u'Ответ не готов'),
    (104,
     u'Сведения в отношении юридического лица/индивидуального предпринимателя не могут быть предоставлены в '
     u'электронном виде'),
    (105, u'Ошибка форматно-логического контроля, либо ЭЦП не прошла проверку'),
    (106, u'Отсутствует запрос с указанным идентификатором запроса и видом запрошенных сведений от данного органа '),
    # (107, u'Обмен сведениями с обратившимся государственным органом не согласован'),
    # (108, u'Не уникальный идентификатор запроса (ранее был получен запрос с таким идентификатором)'),
    (107, u'Обмен сведениями с обратившимся государственным органом не согласован'),
    (108, u'Не уникальный идентификатор запроса (ранее был получен запрос с таким идентификатором)'),

    (701, u'Сведения о лицензиате не найдены в ЕГРИП'),
    (702, u'Неизвестный вид деятельности, на которы'),
    (703, u'Отсутствуют ранее переданные сведения с указанным идентификатором документа'),
    (704, u'Лицензиат прекратил деятельность; сведения не подлежат внесению в реестр'),
    (706, u'Ошибка форматно-логического контроля'),
)
"""
Коды Федеральной Налоговой службы:
    - 101 - Запрашиваемые сведенья не найдены
    - 102 - Запрос принят в обработку
    - 103 - Ответ не готов
    - 104 - Сведения в отношении юридического лица/индивидуального предпринимателя
    не могут быть представлены в электронном виде
    - 105 - Ошибка форматно-логического контроля, либо ЭЦП не прошла проверку
    - 106 - Обмен сведениями с обратившимся государственным органом на согласован
    - 107 - Не уникальный идентификатор запроса (ранее был получен запрос с таким же идентификатором)
"""

RUS_REG_CODES = (
    (201, u'Создана'),
    (202, u'На проверке'),
    (203, u'Проверка не пройдена'),
    (204, u'В работе'),
    (205, u'Завершена отказом'),
    (206, u'Сведения отсутствуют'),
    (207, u'Приостановлена'),
    (208, u'Отказ в обработке'),
    (209, u'Приостановление снято'),
    (210, u'Запрос не рассматривается'),
    (211, u'ГКУ приостановлен'),
    (212, u'ГКУ проведен'),
    (213, u'Отказ в ГКУ'),
    (214, u'Сведения отсутствуют в ГКН '),
    (215, u'Заявка зарегистрирована'),
    (216, u'Ввод и обработка сведений'),
    (217, u'Решение передано на утверждение'),
    (218, u'Сведения подготовлены'),
    (219, u'Отказано в предоставлении сведений'),
    (220, u'Аварийное завершение заявки'),
    (221, u'Запрос не получен'),
    (222, u'Запрос принят, ожидается подтверждение внесения платы'),
    (223, u'Запрос принят в обработку'),
    (224, u'Обработка запроса завершена'),
    (225, u'Ответ направлен заявителю'),
    (226, u'Заявление не получено'),
    (227, u'Заявление принято в обработку'),
    (228, u'Обработка заявления приостановлена'),
    (229, u'Обработка заявления завершена'),
    (230, u'Документы направлены заявителю'),
)
"""
Код для Росреестра:
    - 201 - Создана
    - 202 - На проверке
    - 203 - Проверка не пройдена
    - 204 - В работе
    - 205 - Завершена отказом
    - 206 - Сведения отсутствуют
    - 207 - Приостановлена
    - 208 - Отказ в обработке
    - 209 - Приостановление снято
    - 210 - Запрос не рассматривается
    - 211 - ГКУ приостановлен
    - 212 - ГКУ проведен
    - 213 - Отказ в ГКУ
    - 214 - Сведения отсутствуют в ГКН
    - 215 - Заявка зарегистрирована
    - 216 - Ввод и обработка сведений
    - 217 - Решение передано на утверждение
    - 218 - Сведения подготовлены
    - 219 - Отказано в предоставлении сведений
    - 220 - Аварийное завершение заявки
    - 221 - Запрос не получен
    - 222 - Запрос принят, ожидается подтверждение внесения платы
    - 223 - Запрос принят в обработку
    - 224 - Обработка запроса завершена
    - 225 - Ответ направлен заявителю
    - 226 - Заявление не получено
    - 227 - Заявление принято в обработку
    - 228 - Обработка заявления приостановлена
    - 229 - Обработка заявления завершена
    - 230 - Документы направлены заявителю
"""

FNS_DEBT_CODES = (
    (404, u'Не найдены сведения об организации'),
    (401, u'Ошибка форматно-логического контроля'),
    (402, u'СКП выдан УЦ, не входящим в сеть доверия ФНС России, или срок действия СКП истек, или СКП отозван'),
    (403, u'Неверный OID в СКП'),
    (405, u'Не совпадают реквизиты запроса и СКП'),
    (406, u'Организация снята с учета'),
    (407, u'В работе'),
    (408, u'Недопустимое значение даты'),
    (409, u'Неверный контрольный разряд ИНН'),
    (410, u'Несовпадение сигнатур цифровой подписи'),
    (411, u'В работе'),
)

"""
Коды для задолженностей ФНС
        404 - Не найдены сведения об организации"
        401 - ошибка форматно-логического контроля(не используется)
        402 - СКП выдан УЦ, не входящим в сеть доверия ФНС России, или срок действия СКП истек, или СКП отозван"
        403 - неверный OID в СКП "
        405 - не совпадают реквизиты запроса и СКП "
        406 - Организация снята с учета"
        407 - Ответ не готов"
        408 - Недопустимое значение даты"
        409 - Неверный контрольный разряд ИНН"
        410 - Несовпадение сигнатур цифровой подписи"
        411 - Запрос принят в обработку
"""

ROSPOTREB_SEZ_CODES = (
    (601, u'Ошибка в параметре serialnumb'),
    (602, u'Ошибка в параметре numb'),
    (603, u'Отсутствуют какие-либо параметры запроса (пустой запрос)'),
    (604, u'Ошибка в ИНН'),
    (605, u'Ошибка в ОГРН'),
    (607, u'У системы, сформировавшей запрос, отсутствует доступ к ЭС')
)
"""
Коды РосПотребНадзор
        601 - ошибка в параметре serialnumb
        602 - ошибка в параметре numb
        603 - отсутствуют какие либо параметры запроса (пустой запрос)
        604 - ошибка в ИНН
        605 - ошибка в ОГРН
        607 - У системы, сформировавшей запрос, отсутствует доступ к ЭС
"""

ROS_ZDRAV_CERTS_CODES = (
    (301, u'Регистрационное заявление, по запрашиваемым сведениям не найдено'),
    (302, u'Сигнатура ЭП не соответствует методическим рекомендациям'),
    (303, u'СКП выдан УЦ, не входящим в сеть доверия или срок действия СКП истек, или СКП отозван'),
    (304, u'Отсутствует обязательное поле no_reg'),
    (305, u'Отсутствует обязательное поле dt_reg'),
    (306, u'Формат поля не date'),
    (307, u'Версия запроса отличается от действующей версии сервиса')
)

"""
Коды РосЗдравНадзор Сертификаты
        301 - Регистрационное заявление, по запрашиваемым сведениям не найдено
        302 - Сигнатура ЭП не соответствует методическим рекомендациям
        303 - СКП выдан УЦ, не входящим в сеть доверия или срок действия СКП истек, или СКП отозван
        304 - Отсутствует обязательное поле no_reg
        305 - Отсутствует обязательное поле dt_reg
        306 - Формат поля не date
        307 - Версия запроса отличается от действующей версии сервиса
"""

ROS_ZDRAV_LIC_CODES = (
    (501, u'Запрашиваемые сведения не найдены в реестре лицензий'),
    (502, u'В запросе отсутствует обязательное поле INN'),
    (503, u'В запросе отсутствует обязательное поле OGRN'),
    (504, u'В запросе указан неверный формат поля INN'),
    (505, u'В запросе указан неверный формат поля OGRN'),
    (506, u'Неверный тип запроса'),
    (507, u'Отсутствует блок Message'),
    (508, u'Неверное значение поля Message/Recipient'),
    (509, u'Неверное значение поля Message/Sender'),
    (510, u'Отсутствует блок MessageData'),
    (511, u'Отсутствует блок MessageData/AppData'),
    (512, u'Отсутствует блок MessageData/AppData/Request'),
    (513, u'Несовпадение сигнатур цифровой подписи'),
    (514, u'СКП выдан УЦ, не входящим в сеть доверия или срок действия СКП истек, или СКП отозван')
)

"""
Росздравнадзор лицензии
        501 - Запрашиваемые сведения не найдены реестре лицензий
        502 - В запросе отсутствует обязательное поле INN
        503 - В запросе отсутствует обязательное поле OGRN
        504 - В запросе указан неверный формат поля INN
        505 - В запросе указан неверный формат поля OGRN
        506 - Неверный тип запроса
        507 - Отсутствует блок Message
        508 - Неверное значение поля Message/Recipient
        509 - Неверное значение поля Message/Sender
        510 - Отсутствует блок MessageData
        511 - Отсутствует блок MessageData/AppData
        512 - Отсутствует блок MessageData/AppData/Request
        513 - Несовпадение сигнатур цифровой подписи
        514 - СКП выдан УЦ, не входящим в сеть доверия или срок действия СКП истек, или СКП отозван

"""

ACCEPT = 2  # Выполнен
EMPTY = 4  # Нет данных
IN_WORK = 22  # В работе
WRONG_INPUT = 44  # Нет данных
PAPER = 53  # нет данных в электронном виде, обратитесь в ФНС
EXTERNAL_ERROR = 99  # Внешняя ошибка (ошибка СМЭВ)
INTERNAL_ERROR = 98  # Внутренняя ошибка (ошибка сервиса)
TRYLATER_ERROR = 299  # Внутренняя ошибка (ошибка сервиса)

GENERAL_CODES = (
    (ACCEPT, u'Выполнен'),
    (IN_WORK, u'В работе'),
    (EMPTY, u'Запрашиваемые сведения не найдены'),
    (PAPER, u'Сведения не могут быть предоставлены в электронном виде.'
            u' Для получения выписки в бумажном виде необходимо обратиться в регистрирующий орган'),
    (WRONG_INPUT, u'Некорректно введены исходные данные запроса'),
    (EXTERNAL_ERROR, u'Внешняя ошибка (ошибка СМЭВ)'),
    (INTERNAL_ERROR, u'Внутренняя ошибка'),
    (TRYLATER_ERROR, u'Сервис недоступен. Повторите попытку'),
)

POSITIVE_CODES = [ACCEPT, EMPTY, WRONG_INPUT, PAPER]
GET_ARCHIVE = 0
GET_DATA = 1
SEND_DATA = 5
PAYMENT_CHECK = 6
ACKNOWLEDGE_PAYMENT = 7
ACKNOWLEDGE_WO_PAYMENT = 8
CREATE_ACCRUAL = 9
NULLIFY_ACCRUAL = 10
API_POST_REQUEST = 11
GET_DOC = 12
PING = 2
SEND_CODES = [GET_DATA, SEND_DATA]
PING_CODES = [PING]
# from ATTEMPT_TYPES


# Коды ошибок сервиса отправки сведений в Росздравнадзор
RZN_S_LIC_FLC_ERROR = 301
RZN_S_LIC_ERRORS = (
    (RZN_S_LIC_FLC_ERROR, u'Ошибка форматно-логического контроля'),
)

PGU_CODES = (
    (1001, u'Выполнен'),
    (1002, u'Не выполнен'),
)

ATTEMPT_TYPES = (
    (GET_ARCHIVE, u'Запрос на подготовку данных'),
    (API_POST_REQUEST, u'Входящий запрос на подготовку данных (API)'),
    (GET_DATA, u'Запрос на получение сведений'),
    (GET_DOC, u'Запрос на получение документа'),
    (PING, u'Запрос на получение результата'),
    (SEND_DATA, u'Запрос на отправку сведений'),
    (PAYMENT_CHECK, u'Запрос сведений об оплате услуги'),
    (ACKNOWLEDGE_PAYMENT, u'Запрос на квитирование платежа'),
    (ACKNOWLEDGE_WO_PAYMENT, u'Запрос на квитирование без платежа'),
    (CREATE_ACCRUAL, u'Запрос на создание начисления'),
    (NULLIFY_ACCRUAL, u'Запрос на аннулирование начисления'),
)
"""
Тип запроса:
    - 1 - Запрос на получение сведений
    - 2 - Запрос на получение результата
    - 3 - Запрос сведений по оплате госпошлины
"""
# Перенесено из MЧС, иначе custom.forms не работает
FOIVS = {
    'fns_request': 1,
}
"""
Старое назначение запроса
"""

FOIV_DEST = (
    (1, u'ФНС'),
    (101, u'ФНС (автозапрос)'),
    (21, u'Росреестр'),
    (201, u'Росреестр (автозапрос)'),
    (30, u'Росздравнадзор'),
    (4, u'Министерство культуры'),
    (5, u'МВД'),
    (60, u'МВД (проверка паспорта)'),
    (6, u'МЧС'),
    (7, u'Роспотребнадзор'),
    (8, u'ФСКН'),
    (31, u'ГИС ГМП'),
    # (32, u'ГИС ГМП (период)'),
    (33, u'ИС УНП'),
    (40, u'АИС ГЖИ'),
    (41, u'ВИС ГУАГ'),
    (42, u'АИС ГС (ППТ и ГПЗУ)'),
    (43, u'ВИС ГУАГ (комментарии)'),
    (44, u'АИС ГС (МинСтрой)'),
    (45, u'АИС ГС (КУРТ)'),

    (50, u'ИСОГД (загрузка документа с ЭЦП)'),
    (51, u'ИСОГД (получение временного номера)'),
    (52, u'ИСОГД (получение постоянного номера/получение номера РЛДД)'),
    (53, u'РЛДД (получение информации для документации ИСОГД)'),

    (54, u'ИСОГД (загрузка документа без ЭЦП)'),

    (55, u'АИС ГС (результаты)'),

    (60, u'АИС ТАксомотор'),

    (70, u'Минприроды'),

    (77, u'РЛДД (отправка статуса)'),
    (78, u'РЛДД (создание заявки)'),
    (79, u'РЛДД (загрузка документов)')

)
"""
Назначение запроса
"""

FNS_DEC_PR = (
    (1, u'предоставление лицензии'),
    (2, u'переоформление (продление срока действия)'),
    (3, u'приостановление действия лицензии'),
    (4, u'возобновление действия лицензии'),
    (5, u'аннулирование лицензии'),
    (6, u'признание лицензии утратившей силу'),
    (7, u'ограничение действия лицензии (снятие ограничения)'),
    (8, u'отзыв лицензии')
)
"""
Вид принятого решения в отношении лицензии
"""

FNS_LIC_PR = (
    (1, u'лицензия выдана (возобновлена) на данный вид деятельности'),
    (2, u'действие лицензии приостановлено на данный вид деятельности'),
    (3, u'лицензия прекращает действие на данный вид деятельности'),
    (4, u'новый вид деятельности')
)
"""
Признак действия для лицензии
"""

FNS_APL_PR = (
    (1, u'лицензия выдана (возобновлена) на данный адрес места осуществления лицензируемого вида деятельности'),
    (2, u'действие лицензии приостановлено по данному адресу места осуществления лицензируемого вида деятельности'),
    (3, u'лицензия прекращает действие по данному адресу места осуществления лицензируемого вида деятельности'),
    (4, u'новый адрес места осуществления лицензируемого вида деятельности')
)
"""
Признак действия для лицензии
"""

TASK_STATES = ((1, u'Готово к отправке'), (2, u'Данные подготовлены к отправке'), (3, u'В работе'), (5, u'Выполнено'))

"""
Задача по обработке одного полного запроса к данных к ведомству
"""


class DataServiceRequestTask(models.Model):
    """
    Процесс, из которого выполняется обращение к ОИВ за данными
    """
    process = models.ForeignKey('licprocesses.Process', db_index=True)
    """
    L{Процесс.<licprocesses.models.Process>}
    """
    status = models.IntegerField(u'Статус заявки',
                                 choices=REQUEST_STATES, blank=True,
                                 null=True, editable=False, db_index=True)
    """
    Статус заявки
    """
    ticket_id = models.CharField(u'Идентификатор принятой заявки', max_length=25, null=True, blank=True)
    """ Идентификатор принятой заявки
    """
    dest_foiv = models.IntegerField(u'Куда направляется запрос',
                                    choices=FOIV_DEST, blank=True, null=True,
                                    editable=False, db_index=True)
    """
    Куда направляется запрос
    """
    # обязательно для запроса в РР
    task = models.ForeignKey('licprocesses.Task', null=True, db_index=True)
    """
    L{Конкретное задание.<licprocesses.models.Task>}
    """
    address = models.ForeignKey('licenses.ActivityPlace', null=True, db_index=True)
    """
    L{Модель для мест осуществления деятельности.<licenses.models.ActivityPlace>}
    """
    kad_num = models.CharField(u'Код кадастрового номера (ЕГРП)', max_length=50, blank=True, null=True)
    """
    Код кадастрового номера (запрос ЕГРП)
    """
    cond_kad_num = models.CharField(u'Код условного кадастрового номера (ЕГРП)', max_length=50, blank=True, null=True)
    """
    Код кадастрового номера (запрос ЕГРП)
    """
    method = models.CharField(u'', max_length=10, blank=True, null=True)

    license = models.ForeignKey('licenses.License', db_index=True, null=True, blank=True)

    @property
    def request_status_text(self):
        return dict(TASK_STATES).get(self.status, '')

    @property
    def foiv_text(self):
        return dict(FOIV_DEST).get(self.dest_foiv, '')


class ServiceState(models.Model):
    """
    Статусы обращения к сервисам
    """
    errorcode = models.IntegerField(u'Код статуса', unique=True, db_index=True)
    """
    Код статуса. 0-99 глобальные, >99 локальные для каждого сервиса
    """

    smev_code = models.CharField(u'Код ошибки в СМЭВ', max_length=255,
                                 blank=True, null=True)
    """
    Код ошибки в СМЭВ
    """

    text = models.TextField(u'Сообщение об ошибке', null=True)
    """
    Краткое описание ошибки. Выводится на форму.
    """

    slug = models.CharField(u'Код статуса', max_length=50, db_index=True, blank=True, null=True)
    """
    Системный код статуса
    """

    action = models.TextField(u'Действия специалиста в случае возникновения ошибки',
                              blank=True, null=True)
    """
    Действия специалиста в случае возникновения ошибки
    """

    desc = models.TextField(u'Подробное описание статуса',
                            blank=True, null=True)
    """
    Подробное описание
    """

    reason = models.TextField(u'Причины возникновения ошибки',
                              blank=True, null=True)
    """
    Причины возникновения ошибки
    """

    need_out = models.BooleanField(u'Необходимость выгрузки статуса в файл', blank=True, default=False)
    """
    Если отмечено, то выгружаем статус на форму запроса
    """

    class Meta:
        verbose_name = u'Статусы веб-сервисов'
        """
        Отображение наименования экземпляра класса в админке
        """
        verbose_name_plural = u'Статусы веб-сервисов'
        """
        Отображение наименования модели в админке
        """
        db_table = 'ws_servicestatus'


class DataServiceRequest(models.Model):
    """
    Один запрос к одному конкретному сервису
    """
    data_request_task = models.ForeignKey(DataServiceRequestTask, db_index=True)
    """
    L{Процесс, из которого осуществляется обращение к ОВИ за данными.<DataServiceRequestTask>}
    """
    process = models.ForeignKey('licprocesses.Process', db_index=True, blank=True, null=True)
    """
    L{Процесс.<licprocesses.models.Process>}
    Процесс, из которого выполняется обращение к ОИВ за данными
    Вместо data_request_task
    """
    dest_foiv = models.IntegerField(u'Куда направляется запрос',
                                    choices=FOIV_DEST, blank=True, null=True,
                                    editable=False)
    """
    Куда направляется запрос
    """
    sid = models.CharField(u'SID сервиса', null=True, blank=True, max_length=50)
    """
    SID сервиса, куда направляется запрос
    """
    send_time = models.DateTimeField(u'Время отправки запроса', editable=False,
                                     null=True)
    """
    Время отправки запроса
    """
    receive_time = models.DateTimeField(u'Время получения ответа', editable=False,
                                        null=True)
    """
    Время получения ответа
    """
    result_code = models.IntegerField(u'Код возврата', blank=True, null=True,
                                      editable=False, db_index=True)
    """
    Код возврата
    """
    request_type = models.IntegerField(u'Тип запроса',
                                       choices=ATTEMPT_TYPES, blank=True, null=False,
                                       editable=False, db_index=True)
    """
    Тип запроса
    """
    request_text = models.TextField(u'Текст запроса', null=True)
    """
    Текст запроса
    """
    receive_text = models.TextField(u'Текст ответа', null=True)
    """
    Текст ответа
    """
    result_text = models.TextField(u'Текст ответа', null=True)

    state = models.ForeignKey(ServiceState, db_index=True)

    client = models.ForeignKey('clients.Client', db_index=True, blank=True, null=True)

    from chtd_forms.fake_upload import fake_upload

    request_text_journal = fake_upload(models.FileField)(u'Текст запроса/ответа. Ссылка на файл',
                                                         max_length=255, upload_to='secure-files/smev/%Y_%m_%d/',
                                                         blank=True, null=True)
    receive_text_journal = fake_upload(models.FileField)(u'Текст запроса/ответа. Ссылка на файл',
                                                         max_length=255, upload_to='secure-files/smev/%Y_%m_%d/',
                                                         blank=True, null=True)

    archive = fake_upload(models.FileField)(u'Архив вложения запроса. Ссылка на файл',
                                            max_length=500,
                                            upload_to='secure-files/smev/%Y_%m_%d/',
                                            blank=True, null=True)

    def check_file_permission(self, user, field_name):
        """ Проверка прав для загрузки документа пользователем """

        return True

    @property
    def request_status_text(self):
        """
        @return: возвращает статус запроса в виде строки
        @rtype: string
        """

        return dict(
            GENERAL_CODES + FNS_CODES + RUS_REG_CODES + FNS_DEBT_CODES + ROS_ZDRAV_CERTS_CODES + ROS_ZDRAV_LIC_CODES
            + ROSPOTREB_SEZ_CODES).get(self.result_code)

    @property
    def final_request_status_text(self):
        try:
            if self.id == DataServiceRequest.objects \
                    .filter(data_request_task=self.data_request_task) \
                    .order_by('id') \
                    .reverse()[0].id:
                return 'Выполнена'
            else:
                return 'В работе'
        except IndexError:
            return 'Выполнена'

    @property
    def form_result_text(self):
        if self.result_code < 0:
            return u'Внутренняя ошибка'
        if self.result_code > 2:
            return dict(GENERAL_CODES).get(self.result_code)
        else:
            if self.data_request_task.status == 5:
                return self.final_request_status_text
            else:
                return self.data_request_task.request_status_text

    def form_result_text_sync(self):
        if self.result_code > 2:
            return dict(GENERAL_CODES).get(self.result_code)
        else:
            return self.data_request_task.request_status_text

    @property
    def form_error_text(self):
        import json

        if self.receive_text:
            try:
                return json.loads(self.receive_text).get('status', '').get('message', None)
            except Exception as e:
                logger.error(e)
                return None
        else:
            return None

    @property
    def foiv_text(self):
        return dict(FOIV_DEST).get(self.dest_foiv, '')


"""
Входные данные для сервиса ФНС.
"""


class FnsRequestData(models.Model):
    """
    Результаты запроса регистрации заявки на получение сведений
    """
    data_service_request = models.ForeignKey(DataServiceRequest, null=True, db_index=True)
    task = models.ForeignKey('licprocesses.Task', null=True, db_index=True)
    requestid = models.CharField(u'ID запроса', max_length=255, null=True, blank=True)
    request_type = models.CharField(u'Тип запроса', max_length=255, null=True, blank=True)
    inn = models.CharField(u'ИНН', max_length=12, null=True, blank=True)
    ogrn = models.CharField(u'ОГРН', max_length=20, null=True, blank=True)
    client = models.ForeignKey('clients.Client', db_index=True, blank=True, null=True)

    class Meta:
        db_table = 'ws_fnsrequestdata'


"""
Входные данные для автозапросов сервиса ФНС.
"""


class AutoFnsRequestData(models.Model):
    """
    Запрос в ФНС, выполняемый в фоновом режиме
    """
    smev3 = models.ForeignKey(Smev3Journal, db_index=True, blank=True, null=True)
    param = models.CharField(u'Параметр запроса', max_length=20, null=True, blank=True)
    param_type = models.CharField(u'Параметр запроса', max_length=100, choices=FNS_PARAM_TYPES, null=True, blank=True)
    type = models.IntegerField(u'Тип запроса', null=True, blank=True)
    status = models.IntegerField(u'Статус заявки', choices=AUTO_REQUEST_STATES, blank=True, null=True)
    result_doc = models.ForeignKey(Doc, blank=True, null=True)
    process = models.ForeignKey('licprocesses.Process')
    error_attempts = models.IntegerField(u'Количество ошибочных попыток', default=0)
    error_comment = models.TextField(u'Комментарий к ошибке', null=True, blank=True)

    @property
    def request_status_text(self):
        return dict(AUTO_REQUEST_STATES).get(self.status, '')

    class Meta:
        db_table = 'ws_auto_fnsrequestdata'


class AutoFnsRequestHistory(models.Model):
    """
    История запросов в ФНС, выполняемых в фоновом режиме
    """
    auto_fns_request_data = models.ForeignKey(AutoFnsRequestData, null=True, blank=True)
    service_request = models.OneToOneField(DataServiceRequest, blank=True, null=True)

    class Meta:
        db_table = 'ws_auto_fnsrequestdata_history'


class AutoEgrpRequestResult(models.Model):
    """
    Набор данных из ЕГРП, выполняемых в фоновом режиме
    """
    auto_egrp_request_data = models.ForeignKey(u'AutoEgrpRequestData', null=True, blank=True)
    result_doc = models.ForeignKey(Doc, blank=True, null=True)

    class Meta:
        db_table = 'ws_auto_egrprequestdata_result'


class AutoEgrpRequestData(models.Model):
    """
    Запрос данных из ЕГРП, выполняемый в фоновом режиме
    """
    queue_date = models.DateTimeField(u'Постановка в очередь', blank=True, null=True)
    request_doc = models.ForeignKey('docums.DocFile', verbose_name=u'Результирующий документ', null=True, blank=True)
    request_id = models.CharField(u'ID запроса', max_length=255, null=True, blank=True)
    request_type = models.CharField(u'Тип запроса', max_length=255, null=True, blank=True)
    client = models.ForeignKey('clients.Client', db_index=True, blank=True, null=True)
    status = models.IntegerField(u'Статус заявки', choices=AUTO_REQUEST_STATES, blank=True, null=True)
    process = models.ForeignKey('licprocesses.Process')
    receiver_task = models.ForeignKey('licprocesses.Task', blank=True, null=True)
    identificator = models.CharField(u'Идентификатор объекта', max_length=255, blank=True, null=True)
    identification_method = models.CharField(u'Метод идентификатора объекта', choices=ROSREESTR_IDENT_TYPES,
                                             max_length=255, blank=True, null=True)
    custom_request_param = models.TextField(u'Значение параметра (с формы)', default='')
    custom_request_param_selected = models.BooleanField(u'Ручной ввод параметра (с формы)', default=False)
    object_type = models.CharField(u'Тип объекта', choices=ROSREESTR_OBJECT_TYPES, max_length=255, blank=False,
                                   null=False)
    error_attempts = models.IntegerField(u'Количество ошибочных попыток', default=0)
    error_comment = models.TextField(u'Комментарий к ошибке', null=True, blank=True)

    @property
    def request_status_text(self):
        return dict(AUTO_REQUEST_STATES).get(self.status, '')

    @property
    def identification_method_text(self):
        return dict(ROSREESTR_IDENT_TYPES).get(self.identification_method, '')

    @property
    def object_type_text(self):
        return dict(ROSREESTR_OBJECT_TYPES).get(self.object_type, '')

    @property
    def get_results(self):
        return AutoEgrpRequestResult.objects.filter(auto_egrp_request_data=self)

    class Meta:
        db_table = 'ws_auto_egrprequestdata'


class AutoEgrpRequestHistory(models.Model):
    """
    История запросов данных из ЕГРП, выполняемых в фоновом режиме
    """
    auto_egrp_request_data = models.ForeignKey(AutoEgrpRequestData, null=True, blank=True)
    service_request = models.OneToOneField(DataServiceRequest, blank=True, null=True)

    class Meta:
        db_table = 'ws_auto_egrprequestdata_history'


"""
Входные данные для сервиса РЗН.
"""


class RusZdravLicRequestData(models.Model):
    """
    Результаты запроса регистрации заявки на получение сведений
    """
    task = models.ForeignKey('licprocesses.Task', null=True, db_index=True)
    answer = models.ForeignKey(DataServiceRequest, null=True, db_index=True)
    inn = models.CharField(u'ИНН', max_length=12, null=True, blank=True)
    ogrn = models.CharField(u'ОГРН', max_length=20, null=True, blank=True)
    licno = models.CharField(u'Номер лицензии', max_length=20, null=True, blank=True)


class TreasuryServiceRequestData(models.Model):
    """
    Входные/выходные данные для сервиса Казначейства
    """
    data_service_request = models.ForeignKey(DataServiceRequest, db_index=True)
    """
    L{Ссылка на запрос, для которго предназначены данные.<DataServiceRequest>}
    """

    task = models.ForeignKey('licprocesses.Task', db_index=True)

    # """Входные параметры"""
    start_date = models.DateTimeField(u'Начало периода', editable=False,
                                      null=True)
    """
    Начало периода
    """
    finish_date = models.DateTimeField(u'Окончание периода', editable=False,
                                       null=True)
    """
    Окончание периода
    """
    payer_id = models.CharField(u'Уникальный идентификатор плательщика',
                                max_length=25, null=True)
    """
    Уникальный идентификатор плательщика. Максимальная длина - 25
    """

    inn = models.CharField(u'ИНН', max_length=13, null=True)
    inn_filter = models.CharField(u'ИНН', max_length=13, null=True)
    kpp = models.CharField(u'КПП', max_length=9, null=True)

    # """Выходные параметры"""
    narrative = models.CharField(u'Назначение платежа', max_length=255, null=True)
    """
    Назначение платежа. Максимальная длина - 255
    """
    ammount = models.BigIntegerField(u'Сумма оплаты по платежу в копейках',
                                     null=True)
    """
    Сумма оплаты по платежу в копейках.
    """
    payment_date = models.DateTimeField(u'Дата платежа', editable=False,
                                        null=True)
    """
    Дата платежа.
    """
    supplier_bill_id = models.CharField(u'Уникальный идентификатор начисления',
                                        null=True, max_length=20)
    """
    Уникальный идентификатор начисления. Максимальная длина - 20
    """
    application_id = models.CharField(u'Уникальный идентификатор заявки',
                                      null=True, max_length=20)
    """
    Уникальный идентификатор заявки. Максимальная длина - 20
    """
    ufk_name = models.CharField(u'Наименование УФК, проведшего платёж',
                                null=True, max_length=100)
    """
    Наименование УФК, проведшего платеж. Максимальная длина - 100
    """
    ufk_tofk = models.CharField(u'Код ТОФК УФК, проведшего платёж',
                                null=True, max_length=255)
    """
    Код ТОФК УФК, проведшего платеж. Максимальная длина - 255
    """
    bank_name = models.CharField(u'Наименование банка',
                                 null=True, max_length=100)
    """
    Наименование банка. Максимальная длина - 100
    """
    bank_correspondent_account = models.CharField(u'Корреспондентский счёт банка в ЦБ (РКЦ)',
                                                  null=True, max_length=20)
    """
    Корреспондентский счет банка в ЦБ (РКЦ). Максимальная длина - 20
    """
    bank_bik = models.CharField(u'БИК банка',
                                null=True, max_length=9)
    """
    БИК банка. Максимальная длина - 9
    """
    bank_swift = models.CharField(u'SWIFT банка',
                                  null=True, max_length=12)
    """
    SWIFT банка. Максимальная длина - 12
    """
    bank_address = models.CharField(u'Адрес банка',
                                    null=True, max_length=255)
    """
    Адрес банка. Максимальная длина - 255
    """
    bank_contacts = models.CharField(u'Контакты банка',
                                     null=True, max_length=1000)
    """
    Контакты банка. Максимальная длина - 1000
    """
    payer_status = models.CharField(u'Статус плательщика (ФЛ)',
                                    null=True, max_length=2)
    """
    Статус плательщика (ФЛ). Максимальная длина - 2
    """
    payment_type = models.CharField(u'Тип платежа',
                                    null=True, max_length=1)
    """
    Тип платежа. Максимальная длина - 1
    """
    payment_purpose = models.CharField(u'Основание платежа',
                                       null=True, max_length=2)
    """
    Основание платежа. Максимальная длина - 2
    """
    tax_period = models.CharField(u'Налоговый период',
                                  null=True, max_length=10)
    """
    Налоговый период. Максимальная длина - 10
    """
    tax_doc_number = models.CharField(u'Показатель номера документа',
                                      null=True, max_length=20)
    """
    Показатель номера документа. Максимальная длина - 20
    """
    tax_doc_date = models.CharField(u'Показатель даты документа',
                                    null=True, max_length=10)
    """
    Показатель даты документа. Максимальная длина - 10
    """
    answer = models.TextField(u'Ответ в XML',
                              null=True)
    request_id = models.CharField(u'Показатель номера документа',
                                  null=True, max_length=255)


class treasury_quittance(models.Model):
    balance = models.CharField(u'Баланс', max_length=255, null=True)
    bik = models.CharField(u'БИК', max_length=255, null=True)
    billstatus = models.CharField(u'Статус', max_length=255, null=True)
    creationdate = models.DateTimeField(u'Дата', null=True)
    payeridentifier = models.CharField(u'payeridentifier', max_length=255, null=True)
    supplierbillid = models.CharField(u'supplierbillid', max_length=255, null=True)
    treasury_service_request = models.ForeignKey(TreasuryServiceRequestData, db_index=True)


class RusRegServiceRequestData(models.Model):
    """
    Входные/выходные данные для сервиса Росреестра
    """
    data_service_request = models.ForeignKey(DataServiceRequest, db_index=True)  # 1:1
    """
    L{Запрос, для которого предназначены данные.<DataServiceRequest>}
    """
    # """Входные параметры"""
    okato = models.CharField(u'Уникальный идентификатор плательщика', max_length=25, null=True)
    """
    Уникальный идентификатор плательщика. Максимальная длина - 25
    """
    # """Выходные параметры"""
    # Выписка
    add_info = models.CharField(u'Дополнительная информация', max_length=4000, null=True)
    """
    Дополнительная информация. Максимальная длина - 4000
    """
    desc_recipient = models.CharField(u'Описание получателя информации', max_length=4000, null=True)
    """
    Описание получателя информации. Максимальная длина - 4000
    """
    date_extract = models.DateField(u'Дата выписки', null=True)
    """
    Дата выписки
    """
    num_extract = models.CharField(u'Номер выписки', max_length=50, null=True)
    """
    Номер выписки. Максимальная длина - 50
    """
    num_doc_req = models.CharField(u'Номер запроса', max_length=50, null=True)
    """
    Номер запроса. Максимальная длина - 50
    """
    date_doc_req = models.DateField(u'Дата запроса', null=True)
    """
    Дата запроса.
    """
    num_office = models.CharField(u'Исходящий номер учреждения', max_length=50, null=True)
    """
    Исходящий номер учереждения. Максимальная длина - 50
    """
    date_office = models.DateField(u'Исходящая дата учреждения', null=True)
    """
    Исходящая дата учереждения.
    """
    registrator = models.CharField(u'Регистратор, подписавший выписку', max_length=100)
    """
    Регистратор, подписавший выписку. Максимальная длина - 100
    """


class RusRegServiceTaskSelectedData(models.Model):
    task = models.ForeignKey('licprocesses.Task', db_index=True)
    address = models.ForeignKey('licenses.ActivityPlace', null=True, db_index=True)
    ap_param = models.CharField(u'Код кадастрового номера (ЕГРП)', max_length=50, blank=True, null=True)
    method = models.CharField(u'', max_length=10, blank=True, null=True)


# Не удалять!
class PguRequest(models.Model):
    """
    Служебный класс для сервисов ПГУ.
    """
    date = models.DateTimeField(null=True)
    """
    Дата
    """
    pgu_id = models.CharField(max_length=255, null=False)
    """
    идентификатор заявки с ПГУ. Максимальная длина - 255
    """
    message_id = models.CharField(max_length=255, null=True)
    """
    идентификатор сообщения, проставляемый СМЭВ
    """
    service_orgcode = models.CharField(max_length=255, null=True)
    """

    """
    reestr_id = models.CharField(max_length=255, null=True)
    """
    Номер реестра. Максимальная длина - 255
    """
    service_id = models.CharField(max_length=255, null=True)
    """
    Номер сервиса. Максимальная длина - 255
    """
    process_ref = DocumentForeignKey('licprocesses.Process', db_index=True)
    """
    L{Процесс.<licprocesses.models.Process>}
    """
    mfc_order_num = models.CharField(max_length=255, null=True)
    """
    Номер заявки из МФЦ, выдаваемый пользователю на бланке. Максимальная длина - 255
    """


class PguEventRequestsHistory(models.Model):
    """
    История запросов отправки статусов в РЛДД, выполняемых в фоновом режиме
    """
    pgu_event = models.ForeignKey('PguEvent', related_name='event_history', null=True, blank=True)
    claim = models.ForeignKey('RLDD2ClaimInfo', related_name='claim_history', null=True, blank=True)
    service_request = models.OneToOneField(DataServiceRequest, blank=True, null=True)

    class Meta:
        db_table = 'ws_pguevent_requests_history'


class PguEvent(models.Model):
    """
    Модель для хранения событий изменения статуса запроса с ПГУ
    """

    """
    Дорустимые Коды статуса заявки для ПГУ
    """

    task = models.ForeignKey('licprocesses.Task', db_index=True)

    request = models.ForeignKey(PguRequest, db_index=True)

    tech_code = models.IntegerField(u'Код статуса заявки для ПГУ')

    lod_request = models.CharField(u'UUID запроса в РЛДД', null=False, blank=False, max_length=255)
    """
    UUID запроса в РЛДД
    """

    comment = models.CharField(
        u'Комментарий к статусу',
        max_length=4000,
        null=True)

    performed = models.NullBooleanField(
        u'Статус отправки',
        default=False)
    """ False - готов к отправке
        True  - отправлен
        None  - не требует обработки (например, обнаружена ошибка)  
    """

    pgu_service_code = models.CharField(
        u'Код услуги на ПГУ',
        max_length=50
    )
    """
    Код услуги на ПГУ
    """

    attempts = models.IntegerField(
        u'Число попыток',
        null=False,
        default=0
    )

    component_creator = models.IntegerField(
        u'Система создатель',
        null=False,
        blank=False,
        default=0,
        choices=PGU_STATUS_COMPONENT_CREATOR
    )

    direction = models.IntegerField(
        u'Направление статуса',
        null=False,
        blank=False,
        default=0,
        choices=PGU_STATUS_DIRECTION
    )

    status_uuid = models.CharField(
        u'Код статуса из внешней системы',
        null=False,
        blank=False,
        default='',
        max_length=255
    )

    created_date = models.DateTimeField(
        u'Дата отправки получения статуса',
        null=False,
        blank=False,
        auto_now_add=True
    )
    error_comment = models.TextField(u'Комментарий к ошибке', null=True, blank=True)
    additional_info = models.TextField(u'additionally', null=True, blank=True)

    @property
    def get_event_attempts(self):
        return self.event_history.all().order_by('-id')

    def check_self_errors(self):
        """ Вернёт ошибку, если есть проблемы проверки"""
        error = ''
        comment = ''
        try:
            # проверяем ретроспекцию Задания
            comment = u'Проверка Задания: '
            type(self.task).at(retrospection.now()).get(document_id=self.task.document_id)
            # проверяем ретроспекцию Процесса
            comment = u'Проверка Процесса: '
            process = self.task.get_process()
            type(process).at(retrospection.now()).get(document_id=process.document_id)
            # проверяем ещё что-то
            pass
        except Exception as e:
            logger.error(e)
            error = '{}{}'.format(comment, e)
        return error


class PguEventDocs(models.Model):
    """
    Документы передаваемые с задания сервису
    """
    pgu_event = models.ForeignKey(
        PguEvent,
        verbose_name=u'Событие, к которому привязан документ',
        null=False)

    name = models.CharField(
        verbose_name=u'Имя документа',
        max_length=255)

    file_name = models.CharField(
        verbose_name=u'Файл документа',
        max_length=255)

    signature_file_name = models.CharField(
        verbose_name=u'Файл подписи документа',
        default=None,
        blank=True,
        null=True,
        max_length=255)

    slug = models.SlugField(
        u'Код вида документа',
        db_index=True)


def service_request_task_post_delete_handler(sender, instance, **kwargs):
    """
    Удаляет данные о запросах
    @kwparam sender: источник
    @kwparam instance: L{Процесс, из которого осуществляется обращение к ОВИ за данными.<DataServiceRequestTask>}
    @kwparam **kwargs: kwargs
    """
    for service_request in DataServiceRequest.objects.filter(data_request_task=instance):
        service_request.delete()


REQUEST_KINDS = (
    (1, u'Межведомственное взаимодействие'),
    (2, u'Запрос с ПГУ'),
    (3, u'Запрос выписки из реестра лицензий'),
    (4, u'Запрос из МФЦ'),
    (5, u'Отправка статуса'),
    (6, u'Межведомственное взаимодействие'),
    (7, u'Отправка/прием данных'),
)
"""
Виды запросов:
    - 1 - Межведомственное взаимодействие
    - 2 - Запрос с ПГУ
    - 3 - Запрос выписки из реестра лицензий
"""

REQUEST_NAMES = (
    (1, u'Запрос сведений из ЕГРЮЛ/ЕГРИП'),
    (2, u'Запрос на проверку в Росреестр.ЕГРП'),
    (3, u'Запрос в Казначейство'),
    (4, u'Запрос на оказание услуги'),
    (5, u'Отмена заявки на оказание услуги'),
    (6, u'Запрос справочника'),
    (7, u'Запрос выписки из реестра'),
    (8, u'Запрос выписки из реестра'),
    (9, u'Отправка статуса по электронной заявке'),
    (10, u'Запрос в РосЗдрав лицензия'),
    (11, u'Запрос в РосЗдрав сертификат'),
    (12, u'Запрос в роспотребнадзор'),
    (13, u'Запрос в ФСКН по судимостям'),
    (14, u'Запрос в ФСКН по помещениям'),
    (15, u'Запрос сведений о задолженности'),
    (16, u'Предоставление лицензий в ФНС'),
    (17, u'Запрос в минкульт'),
    (18, u'Отправка сведений о рег. ТС'),
    (19, u'Запрос в МЧС'),
    (20, u'Запрос в МВД'),
    (21, u'Запрос из АИС Таксомотор'),
    (22, u'Запрос мест деятельности')
)
"""
Наименование запроса:
    - 1 - Запрос сведений из ЕГРЮЛ/ЕГРИП
    - 2 - Запрос на проверку в Росреестр.ЕГРП
    - 4 - Запрос на оказание услуг
    - 5 - Отмена заявки на оказание услуг
    - 6 - Запрос справочника
    - 7 - Запрос выписки из реестра лицензий для ИП
    - 8 - Запрос выписки из реестра лицензий для ЮЛ
"""

REQUEST_LINKS = (
    (1, (1, 2)),
    (2, (4, 5, 6)),
    (3, (7, 8)),
)
"""
Запросы
"""


class Fns_DebtInfo(models.Model):
    # ulname = models.CharField(u'Статус', max_length=255) #DEPRECATED
    debtflag = models.BooleanField(u'Наличие задолженности', default=False)
    innul = models.CharField(u'ИНН', max_length=255)
    ifns = models.TextField(u'Список кодов ФНС')
    # ogrn = models.CharField(u'ОГРН', max_length=255) #DEPRECATED
    # processingcode = models.IntegerField(u'Код обрабоки') #DEPRECATED
    # requestguid = models.CharField(u'ID запроса', max_length=255) #DEPRECATED
    requestid = models.CharField(u'ID запроса', max_length=255)
    # status = models.CharField(u'Статус', max_length=255) #DEPRECATED
    todate = models.DateField(u'Дата запроса')
    # date_request = models.CharField(u'Дата для запроса', max_length=20) #DEPRECATED
    # data_service_request = models.ForeignKey(DataServiceRequest, db_index=True
    # ) #DEPRECATED
    task = models.ForeignKey('licprocesses.Task', null=True, db_index=True)

    class Meta:
        db_table = 'ws_fns_debtinfo'


class fskn_spaceinfo(models.Model):
    status = models.CharField(u'', max_length=255)
    dataservicerequest = models.ForeignKey(DataServiceRequest, db_index=True)
    legalfullname = models.CharField(u'Полное наименование ЮЛ', max_length=255)
    territory_fskn = models.CharField(u'Территориальный орган ФСКН России выдавший заключение', max_length=255)
    number_conclusion = models.CharField(u'Номер заключения', max_length=255)
    date_conclusion = models.DateField(u'Дата выдачи заключения')
    originidref = models.CharField(u'', max_length=255)
    reqidref = models.CharField(u'', max_length=255)
    casenumber = models.CharField(u'', max_length=255)

    class Meta:
        db_table = 'ws_fskn_spaceinfo'


class fskn_convictioninfo(models.Model):
    status = models.CharField(u'', max_length=255)
    dataservicerequest = models.ForeignKey(DataServiceRequest, db_index=True)
    legalfullname = models.CharField(u'Полное наименование ЮЛ', max_length=255)
    territory_fskn = models.CharField(u'Территориальный орган ФСКН России выдавший заключение', max_length=255)
    number_conclusion = models.CharField(u'Номер заключения', max_length=255)
    date_conclusion = models.DateField(u'Дата выдачи заключения')
    originidref = models.CharField(u'', max_length=255)
    reqidref = models.CharField(u'', max_length=255)
    casenumber = models.CharField(u'', max_length=255)

    class Meta:
        db_table = 'ws_fskn_convictioninfo'


class TreasuryPayment(models.Model):
    kaznachdata = models.ForeignKey(TreasuryServiceRequestData, db_index=True)
    payment_sum = models.IntegerField(u'', blank=True, null=True)
    paydate = models.DateTimeField(u'', null=True, blank=True)
    numpp = models.CharField(u'', max_length=255)
    bankname = models.CharField(u'', max_length=255)
    account = models.CharField(u'', max_length=255)

    class Meta:
        db_table = 'ws_treasury_payment'


class SentDocsInfo(models.Model):
    result = models.BooleanField(u'Статус отправки', default=False)
    order_uuid = models.CharField(u'Идентификатор заявки на ПГУ при подаче лично', max_length=255)
    pgu_service_code = models.CharField(u'Код услуги на ПГУ', max_length=50)
    pgu_depart_code = models.CharField(u'Код департамента на ПГУ', max_length=50)

    person_params = models.TextField(u'Параметры для создания персоны в РЛДД в формате JSON', blank=False, null=False)
    '''
    Возможные параметры
    {
        "personEMail" : "x@y.ru",
        "userId : "123",
        "personSNILS : "123-456-789-00",
        "personINN : "5012345678"
    }
    '''

    person_id = models.CharField(u'Идентификатор персоны в РЛДД', max_length=255)

    class Meta:
        db_table = 'ws_rest_send_docs_info'


class SentDocs(models.Model):
    result_text = models.CharField(u'Текст ответа', max_length=255, null=True)
    result = models.BooleanField(u'Статус отправки', default=False)
    doc_file = models.ForeignKey('docums.DocFile', db_index=True)
    info = models.ForeignKey(SentDocsInfo, db_index=True)

    class Meta:
        db_table = 'ws_rest_send_docs'


class RLDD2ClaimInfo(models.Model):
    is_docs_created = models.BooleanField(u'Статус отправки документов, связанных с заявкой, в РЛДД2', default=False)
    is_claim_created = models.BooleanField(u'Статус отправки документов, связанных с заявкой, в РЛДД2', default=False)
    created = models.DateTimeField(u'Дата создания заявки', null=True, blank=True)
    pgu_service_code = models.CharField(u'Код услуги на ПГУ', max_length=50)
    pgu_passport_service_code = models.CharField(u'Паспортный код услуги на ПГУ', max_length=50)
    pgu_dept_code = models.CharField(u'Код департамента на ПГУ', max_length=50)
    claim_id = models.CharField(u'Идентификатор, присвоенный заявке в РЛДД2', max_length=50)
    additional_params = models.TextField(u'Дополнительные параметры заявки (json)', null=True, blank=True)
    request = models.ForeignKey('licenses.LicenseRequest', db_index=True)
    error_comment = models.TextField(u'Комментарий к ошибке', null=True, blank=True)
    existing_claim_id = models.CharField(u'Идентификатор, присвоенный заявке ПГУ', max_length=50)

    class Meta:
        db_table = 'ws_rldd2_claim_info'


class RLDD2Document(models.Model):
    content = models.TextField(u'Относительное имя файла документа', blank=False, null=False)
    is_doc_created = models.BooleanField(u'Статус отправки документа в РЛДД2', default=False)
    info = models.ForeignKey(RLDD2ClaimInfo, db_index=True)
    doc_id = models.TextField(u'ID документа в РЛДД2', blank=True, null=True)

    class Meta:
        db_table = 'ws_rldd2_document'


class PguStatus(models.Model):
    """
    Статус исполнения услуги на ПГУ
    """
    code = models.IntegerField(verbose_name=u'Код статуса')
    name = models.CharField(verbose_name=u'Наименование статуса', max_length=255)
    description = models.TextField(u'Расшифровка статуса', blank=True, null=True)

    class Meta:
        verbose_name = u'Статус'
        """
        Отображение наименования экземпляра класса в админке
        """
        verbose_name_plural = u'Статусы'
        """
        Отображение наименования модели в админке
        """

    def __unicode__(self):
        """
        @return: Возвращает наименование статуса
        @rtype: string
        """
        return u'{0} - {1}'.format(self.code, self.name)


'''
Входные/выходные данные для сервиса Роспотреба (SID0003402).
'''


class RusPotrebSezRequestData(models.Model):
    """
    Результаты запроса регистрации заявки на получение сведений
    """
    task = models.ForeignKey('licprocesses.Task', null=True, db_index=True)

    ogrn = models.CharField(u'ОГРН', max_length=255, null=True, blank=True)
    inn = models.CharField(u'ИНН', max_length=255, null=True, blank=True)
    serialnumb = models.CharField(u'Типографский номер бланка', max_length=255, null=True)
    numb = models.CharField(u'Номер СЭЗ М', max_length=255, null=True)
    firmget_full = models.CharField(u'Полное наименование фирмы-заявителя', max_length=255, null=True)
    firmget_short = models.CharField(u'Краткое наименование фирмы-заявителя', max_length=255, null=True)
    firmget = models.CharField(u'Часть наименования фирмы-заявителя', max_length=255, null=True)
    mode = models.CharField(u'Режим поиска', max_length=255, null=True)
    is_pril = models.CharField(u'Передавать приложение или нет', max_length=255, null=True)


'''
Компания - производитель изделий (Росздрав)
'''


class rzdrav_company(models.Model):
    address = models.CharField(u'Адрес организации', max_length=255, null=True)
    label = models.CharField(u'Наименование', max_length=255, null=True)
    inn = models.CharField(u'ИНН организации', max_length=255, null=True)


'''
Входные/выходные данные для сервиса Росздрава.
'''


class rzdrav_medizdinfo(models.Model):
    '''Ссылка на запрос, для которого предназначены данные'''
    data_service_request = models.ForeignKey(DataServiceRequest, db_index=True)
    '''
    Входные параметры
    '''
    noreg = models.CharField(u'Номер регистрационного удостоверения', max_length=255, null=True)
    dtreg = models.DateField(u'Дата выдачи', null=True)

    """
    Выходные параметры
    """
    application = models.TextField(u'Информация', blank=True, null=True)
    description = models.CharField(u'Описание изделия', max_length=255, null=True)
    classid = models.IntegerField(u'Класс безопасности изделия', null=True)
    classlabel = models.CharField(u'Описание класса изделия', max_length=255, null=True)
    expirationdate = models.DateField(u'Дата истечения', null=True)
    okpcode = models.CharField(u'Код по ОКП', max_length=255, null=True)
    okplabel = models.CharField(u'Описание кода по ОКП', max_length=255, null=True)
    recipient = models.CharField(u'Кому выдано ', max_length=255, null=True)
    org = models.ForeignKey(rzdrav_company,
                            verbose_name=u'Организация - производитель',
                            blank=True, null=True, db_index=True)


class fns_license_info(models.Model):
    authority = models.ForeignKey(TreeTextValue, db_index=True)
    currentdecision = models.IntegerField(u'', blank=True, null=True)
    currentlic = models.IntegerField(u'', blank=True, null=True)
    process = models.IntegerField(u'', blank=True, null=True)
    license = models.IntegerField(u'', blank=True, null=True)
    dataservicerequest = models.IntegerField(u'', blank=True, null=True)
    iddoc = models.CharField(u'ID запроса', max_length=255)
    slvd_code = models.CharField(u'СЛВД', max_length=255)
    actcode = models.CharField(u'', max_length=255)
    actname = models.CharField(u'', max_length=255)
    clientinn = models.CharField(u'', max_length=255)
    clientname = models.CharField(u'', max_length=255)
    clientfam = models.CharField(u'', max_length=255)
    clientim = models.CharField(u'', max_length=255)
    clientotch = models.CharField(u'', max_length=255)
    clientogrn = models.CharField(u'', max_length=255)
    licseries = models.CharField(u'', max_length=255)
    licenseno = models.CharField(u'', max_length=255)
    actpr = models.CharField(u'', max_length=255)
    dectype = models.CharField(u'', max_length=255)
    decdate = models.DateField(u'')
    decdatefrom = models.DateField(u'')
    decdatetill = models.DateField(u'')
    licvalidfrom = models.DateField(u'')
    licvalidtill = models.DateField(u'')

    class Meta:
        db_table = 'ws_fns_license_info'


class fns_license_info_ap(models.Model):
    actpr = models.CharField(u'', max_length=255)
    fulladdress = models.TextField(u'')
    license_info = models.ForeignKey(fns_license_info, db_index=True)


class EmergencyRequestData(models.Model):
    """
    Введенные данные для запроса в МЧС
    """
    inn = models.CharField(verbose_name=u'ИНН', max_length=255, null=True, blank=True)
    ogrn = models.CharField(verbose_name=u'ОГРН', max_length=255, null=True, blank=True)
    task = models.ForeignKey('licprocesses.Task', db_index=True)
    applicantshortname = models.TextField(verbose_name=u'Краткое наименование заявителя', null=True, blank=True)
    current_place_id = models.IntegerField(null=True, blank=True)


class EmergencyRequestDataActivityPlace(models.Model):
    """
    Введенные данные для запроса по ap
    """
    tip_no = models.CharField(verbose_name=u'ОГРН', max_length=255, null=True, blank=True)
    zak_no = models.CharField(verbose_name=u'ОГРН', max_length=255, null=True, blank=True)
    zip = models.CharField(verbose_name=u'Индекс', max_length=255, null=True, blank=True)
    region = models.CharField(verbose_name=u'Регион', max_length=255, null=True, blank=True)
    district = models.CharField(verbose_name=u'Район', max_length=255, null=True, blank=True)
    city = models.CharField(verbose_name=u'Город', max_length=255, null=True, blank=True)
    street = models.CharField(verbose_name=u'Улица', max_length=255, null=True, blank=True)
    house = models.CharField(verbose_name=u'Дом', max_length=255, null=True, blank=True)
    flat = models.CharField(verbose_name=u'Квартира/Офис', max_length=255, null=True, blank=True)
    obj_zip = models.CharField(verbose_name=u'Индекс МД', max_length=255, null=True, blank=True)
    obj_region = models.CharField(verbose_name=u'Регион МД', max_length=255, null=True, blank=True)
    obj_district = models.CharField(verbose_name=u'Район МД', max_length=255, null=True, blank=True)
    obj_city = models.CharField(verbose_name=u'Город МД', max_length=255, null=True, blank=True)
    obj_street = models.CharField(verbose_name=u'Улица МД', max_length=255, null=True, blank=True)
    obj_house = models.CharField(verbose_name=u'Дом МД', max_length=255, null=True, blank=True)
    obj_flat = models.CharField(verbose_name=u'Квартира/Офис МД', max_length=255, null=True, blank=True)
    ap = models.ForeignKey('licenses.ActivityPlace', db_index=True)
    applicantregisteredadress = models.CharField(verbose_name=u'Юридический адрес заявителя', max_length=255,
                                                 null=True, blank=True)
    request_id = models.CharField(verbose_name=u'id запроса, возвращаемый адаптером', max_length=255,
                                  null=True, blank=True)
    request_data = models.ForeignKey(EmergencyRequestData, db_index=True)
    service_answer = models.ForeignKey(DataServiceRequest, blank=True,
                                       null=True, db_index=True)


class RusRegPersonDocumentType(models.Model):
    """ Справочник "Виды документов, удостоверяющих личность физического лица"
    """

    name = models.CharField(
        verbose_name=u'Наименование',
        max_length=1000,
        blank=False,
        null=False)
    """
    Наименование
    """

    code = models.CharField(
        verbose_name=u'Код',
        max_length=50,
        blank=False,
        null=False)
    """
    Код
    """

    lod_doc_type = models.IntegerField(u'Вид документа, удостоверяющего личность (соотношение справочнику в ЛОД)',
                                       choices=dictionary_to_choises(CARD_TYPES), default=1)
    """
    Тип документа, удостоверяющего личность (соотношение справочнику в ЛОД)
    """

    def __unicode__(self):
        """
        @return: возвращает код + название
        @rtype: string
        """
        return self.name

    class Meta:
        verbose_name = u'Документ'
        """
        Отображение наименования экземпляра класса в админке
        """
        verbose_name_plural = u'Справочник "Виды документов, удостоверяющих личность физического лица"'
        """
        Отображение наименования модели в админке
        """


class RusReg3Level(models.Model):
    """Справочник "3-й уровень - административно-территориальное образование (АТО) районного подчинения"
    """

    name = models.CharField(
        verbose_name=u'Наименование',
        max_length=255,
        blank=False,
        null=False)
    """
    Наименование
    """

    code = models.CharField(
        verbose_name=u'Код',
        max_length=50,
        blank=False,
        null=False)
    """
    Код
    """

    def __unicode__(self):
        """
        @return: возвращает код + название
        @rtype: string
        """
        return self.name

    class Meta:
        verbose_name = u'АТО'
        """
        Отображение наименования экземпляра класса в админке
        """
        verbose_name_plural = u'Справочник "3-й уровень - АТО районного подчинения"'
        """
        Отображение наименования модели в админке
        """


class RusReg4Level(models.Model):
    """ Справочник "4-й уровень - тип населенного пункта"
    """

    name = models.CharField(
        verbose_name=u'Наименование',
        max_length=255,
        blank=False,
        null=False)
    """
    Наименование
    """

    code = models.CharField(
        verbose_name=u'Код',
        max_length=50,
        blank=False,
        null=False)
    """
    Код
    """

    def __unicode__(self):
        """
        @return: возвращает код + название
        @rtype: string
        """
        return self.name

    class Meta:
        verbose_name = u'тип населенного пункта'
        """
        Отображение наименования экземпляра класса в админке
        """
        verbose_name_plural = u'Справочник "4-й уровень - тип населенного пункта"'
        """
        Отображение наименования модели в админке
        """


class RusReg5Level(models.Model):
    """Справочник "5-й уровень - геоним (улицы городов, поселков городского типа и сельских населенных пунктов)"
    """

    name = models.CharField(
        verbose_name=u'Наименование',
        max_length=255,
        blank=False,
        null=False)
    """
    Наименование
    """

    code = models.CharField(
        verbose_name=u'Код',
        max_length=50,
        blank=False,
        null=False)
    """
    Код
    """

    def __unicode__(self):
        """
        @return: возвращает код + название
        @rtype: string
        """
        return self.name

    class Meta:
        verbose_name = u'геоним'
        """
        Отображение наименования экземпляра класса в админке
        """
        verbose_name_plural = u'Справочник "5-й уровень - геоним"'
        """
        Отображение наименования модели в админке
        """


class RusRegRegion(models.Model):
    """ Справочник регионов РР
    """

    name = models.CharField(
        verbose_name=u'Наименование региона',
        max_length=255,
        blank=False,
        null=False)
    """
    Наименование
    """

    kladr_name = models.CharField(
        verbose_name=u'Наименование региона по КЛАДР',
        max_length=255,
        blank=False,
        null=False)
    """
    Наименование по КЛАДР
    """

    code = models.CharField(
        verbose_name=u'Код региона',
        max_length=10,
        blank=False,
        null=False)
    """
    Код региона
    """

    def __unicode__(self):
        """
        @return: возвращает код региона + название
        @rtype: string
        """
        return self.name

    class Meta:
        verbose_name = u'Регион РР'
        """
        Отображение наименования экземпляра класса в админке
        """
        verbose_name_plural = u'Справочник регионов РР'
        """
        Отображение наименования модели в админке
        """


class RusRegRightsDocRequest(models.Model):
    """ Данные запроса в ЕГРП по правоустанавливающим документам
    """
    task = models.ForeignKey('licprocesses.Task', null=True, db_index=True)
    doc_type = models.CharField(choices=RR_ALL_DOC_TYPES, max_length=255, null=True, db_index=True)
    doc_name = models.CharField(u'Наименование документа', max_length=255, null=True)
    doc_series = models.CharField(u'Серия документа', max_length=45, null=True)
    doc_numb = models.CharField(u'Номер документа', max_length=45, null=True)
    doc_date = models.DateField(u'Дата выдачи документа', null=True)
    request_type = models.IntegerField(u'Тип запроса', null=True)


class RusRegRightsDocGround(models.Model):
    """ Данные запроса в ЕГРП по правоустанавливающим документам - информация о Земельный участок
    """
    request = models.ForeignKey(RusRegRightsDocRequest, db_index=True)
    name = models.CharField(u'Наименование', max_length=500)
    kad_num = models.CharField(u'Кадастровый номер участка', max_length=40)
    square = models.CharField(u'Площадь', max_length=30, null=True)
    unit = models.CharField(choices=RR_GROUND_UNIT_TYPES, max_length=255, null=True, db_index=True)
    post_index = models.CharField(u'Почтовый миндекс', max_length=6, null=True)
    region = models.ForeignKey(RusRegRegion, null=True, db_index=True)
    district = models.CharField(u'Район', max_length=255, null=True)
    district_type = models.CharField(choices=RR_DISTRICT_TYPES, max_length=255, null=True, db_index=True)
    city_type = models.ForeignKey(RusReg4Level, null=True, db_index=True)
    city = models.CharField(u'Населенный пункт', max_length=255, null=True)
    street_type = models.ForeignKey(RusReg5Level, null=True, db_index=True)
    street = models.CharField(u'Улица', max_length=255, null=True)
    additional = models.CharField(u'Дополнение', max_length=4000, null=True)


class RusRegRightsDocRealtyObject(models.Model):
    """ Данные запроса в ЕГРП по правоустанавливающим документам - информация о Объект недвижимости
    """
    request = models.ForeignKey(RusRegRightsDocRequest, db_index=True)
    type = models.CharField(choices=RR_REALTY_UNIT_TYPES, max_length=255, null=True, db_index=True)
    name = models.CharField(u'Наименование', max_length=500)
    kad_num = models.CharField(u'Кадастровый номер', max_length=40)
    cond_kad_num = models.CharField(u'Кадастровый номер', max_length=40)
    square = models.CharField(u'Площадь', max_length=30, null=True)
    unit = models.CharField(choices=RR_GROUND_UNIT_TYPES, max_length=255, null=True, db_index=True)
    post_index = models.CharField(u'Почтовый миндекс', max_length=6, null=True)
    region = models.ForeignKey(RusRegRegion, null=True, db_index=True)
    district = models.CharField(u'Район', max_length=255, null=True)
    district_type = models.CharField(choices=RR_DISTRICT_TYPES, max_length=255, null=True, db_index=True)
    city_type = models.ForeignKey(RusReg4Level, null=True, db_index=True)
    city = models.CharField(u'Населенный пункт', max_length=255, null=True)
    street_type = models.ForeignKey(RusReg5Level, null=True, db_index=True)
    street = models.CharField(u'Улица', max_length=255, null=True)
    house_type = models.CharField(choices=RR_HOUSE_TYPES, max_length=255, null=True, db_index=True)
    house = models.CharField(u'Дом', max_length=255, null=True)
    corp_type = models.CharField(choices=RR_CORP_TYPES, max_length=255, null=True, db_index=True)
    corp = models.CharField(u'Корпус', max_length=255, null=True)
    building_type = models.CharField(choices=RR_BUILD_TYPES, max_length=255, null=True, db_index=True)
    building = models.CharField(u'Строение', max_length=255, null=True)
    apartment_type = models.CharField(choices=RR_APARTMENT_TYPES, max_length=255, null=True, db_index=True)
    apartment = models.CharField(u'Квартира', max_length=255, null=True)
    additional = models.CharField(u'Дополнение', max_length=4000, null=True)
    letter = models.CharField(u'Литера', max_length=500, blank=True, null=True)
    inventory_number = models.CharField(u'Инвентаризационный номер', max_length=100, blank=True, null=True)


class RusRegKadastrPassportRequest(models.Model):
    """ Данные запроса в ЕГРП по кадастровому паспорту объекта недвижимости
    """
    task = models.ForeignKey('licprocesses.Task', null=True, db_index=True)
    obj_type = models.CharField(choices=RR_GKN_REALTY_UNIT_TYPES, max_length=255, null=True, db_index=True)
    obj = models.PositiveIntegerField(null=True)
    req_type = models.CharField(u'Тип запроса (объект/сооружение) служебное поле', max_length=50, blank=True, null=True)
    # REALTY/CONSTRUCTION


class RusRegKadastrPassportRealtyObjectData(models.Model):
    request = models.ForeignKey(RusRegKadastrPassportRequest, db_index=True)
    obj = models.PositiveIntegerField(null=True)
    kad_num = models.CharField(u'Кадастровый номер', max_length=100)
    post_index = models.CharField(u'Почтовый миндекс', max_length=6, null=True)
    region = models.ForeignKey(RusRegRegion, null=True, db_index=True)
    district = models.CharField(u'Район', max_length=255, null=True)
    district_type = models.CharField(choices=RR_DISTRICT_TYPES, max_length=255, null=True, db_index=True)
    city_type = models.ForeignKey(RusReg4Level, null=True, db_index=True)
    city = models.CharField(u'Населенный пункт', max_length=255, null=True)
    street_type = models.ForeignKey(RusReg5Level, null=True, db_index=True)
    street = models.CharField(u'Улица', max_length=255, null=True)
    house_type = models.CharField(choices=RR_HOUSE_TYPES, max_length=255, null=True, db_index=True)
    house = models.CharField(u'Дом', max_length=255, null=True)
    corp_type = models.CharField(choices=RR_CORP_TYPES, max_length=255, null=True, db_index=True)
    corp = models.CharField(u'Корпус', max_length=255, null=True)
    building_type = models.CharField(choices=RR_BUILD_TYPES, max_length=255, null=True, db_index=True)
    building = models.CharField(u'Строение', max_length=255, null=True)
    apartment_type = models.CharField(choices=RR_APARTMENT_TYPES, max_length=255, null=True, db_index=True)
    apartment = models.CharField(u'Квартира', max_length=255, null=True)
    additional = models.CharField(u'Дополнение', max_length=1000, null=True)


class RusRegGKNExtractRequest(models.Model):
    """ Запрос кадастрового плана территории
    """
    arc_doc = models.ForeignKey('docums.DocFile', null=True)
    task = models.ForeignKey('licprocesses.Task', null=True, db_index=True)
    obj_type = models.CharField(choices=RR_GKN_REALTY_UNIT_TYPES, max_length=255, null=True, db_index=True)
    obj = models.PositiveIntegerField(null=True)
    chapter = models.CharField(u'Необходимые разделы выписки', max_length=100)


class RusRegGKNExtractObjectData(models.Model):
    request = models.ForeignKey(RusRegGKNExtractRequest, db_index=True)
    obj = models.PositiveIntegerField(null=True)
    kad_num = models.CharField(u'Кадастровый номер', max_length=100)
    post_index = models.CharField(u'Почтовый миндекс', max_length=6, null=True)
    region = models.ForeignKey(RusRegRegion, null=True, db_index=True)
    district = models.CharField(u'Район', max_length=255, null=True)
    district_type = models.CharField(choices=RR_DISTRICT_TYPES, max_length=255, null=True, db_index=True)
    city_type = models.ForeignKey(RusReg4Level, null=True, db_index=True)
    city = models.CharField(u'Населенный пункт', max_length=255, null=True)
    street_type = models.ForeignKey(RusReg5Level, null=True, db_index=True)
    street = models.CharField(u'Улица', max_length=255, null=True)
    house_type = models.CharField(choices=RR_HOUSE_TYPES, max_length=255, null=True, db_index=True)
    house = models.CharField(u'Дом', max_length=255, null=True)
    corp_type = models.CharField(choices=RR_CORP_TYPES, max_length=255, null=True, db_index=True)
    corp = models.CharField(u'Корпус', max_length=255, null=True)
    building_type = models.CharField(choices=RR_BUILD_TYPES, max_length=255, null=True, db_index=True)
    building = models.CharField(u'Строение', max_length=255, null=True)
    apartment_type = models.CharField(choices=RR_APARTMENT_TYPES, max_length=255, null=True, db_index=True)
    apartment = models.CharField(u'Квартира', max_length=255, null=True)
    additional = models.CharField(u'Дополнение', max_length=1000, null=True)


class RusRegKadastrPlanRequest(models.Model):
    """ Запрос кадастрового паспорта территории
    """
    task = models.ForeignKey('licprocesses.Task', null=True, db_index=True)
    obj = models.PositiveIntegerField(null=True)
    kad_num = models.CharField(u'Кадастровый номер', max_length=40)
    obj_kad_num = models.CharField(u'Кадастровый номер', max_length=100)
    orientirs = models.CharField(u'Ориентиры территории', max_length=4000, null=True)


class RequestDocument(models.Model):
    """
    Связь документов с заявкой (ВИС ГУАГ)
    """
    from processes.minstroy.models import ApprovalsDocument

    request = models.ForeignKey('licenses.LicenseRequest', verbose_name=u'Заявка', db_index=True)
    doc = models.ForeignKey('docums.Doc', verbose_name=u'Документ', db_index=True)
    approvals_doc = models.ForeignKey(ApprovalsDocument, verbose_name=u'Согласование документа', db_index=True,
                                      null=True)


class RequestSignedDocumentLink(models.Model):
    """
    Связь ГПЗУ с заявкой (ВИС ГУАГ)
    """
    request = models.ForeignKey('licenses.LicenseRequest', verbose_name=u'Заявка', db_index=True)
    doc = models.ForeignKey('docums.Doc', verbose_name=u'Документ', db_index=True)


class RequestDocumentGS(models.Model):
    """
    Связь документов с заявкой (АИС ГС) (устарело)
    """

    request = models.ForeignKey('licenses.LicenseRequest', verbose_name=u'Заявка', db_index=True)
    doc = models.ForeignKey('docums.Doc', verbose_name=u'Документ', db_index=True)


class GSRequestData(models.Model):
    """
    Данные, полученные из АИС ГС
    """

    from ws.services.minstroy.minstroy_integration_gs_views import CLAIM_STATUS, MEETING_KINDS

    request = models.ForeignKey('licenses.LicenseRequest', verbose_name=u'Заявка', db_index=True)
    report_text = models.TextField(u'Текст мнения главы', null=True, blank=True)
    user_name = models.CharField(u'Имя пользователя, добавившего мнение', max_length=255, null=True, blank=True)
    decision_mvk = models.TextField(u'Решение МВК', null=True, blank=True)
    decision_gs = models.TextField(u'Решение ГС', null=True, blank=True)
    claim_status = models.IntegerField(u'Статус по заявлению',
                                       choices=dictionary_to_choises(CLAIM_STATUS),
                                       null=True, blank=True,
                                       # default=1,
                                       db_index=True)
    meeting_date = models.DateField(u'Дата заседания с решением по вопросу', null=True, blank=True)
    meeting_number = models.CharField(u'Номер заседания с решением по вопросу', max_length=255, null=True, blank=True)
    meeting_type = models.IntegerField(u'Тип заседания',
                                       choices=dictionary_to_choises(MEETING_KINDS),
                                       null=True, blank=True,
                                       # default=1,
                                       db_index=True)


class GSDocument(models.Model):
    """
    Связь документов с заявкой (АИС ГС)
    """

    request_data = models.ForeignKey(GSRequestData, verbose_name=u'Даннные из АИС ГС', db_index=True)
    doc = models.ForeignKey('docums.Doc', verbose_name=u'Документ', db_index=True)


class ConcentratorEvent(models.Model):
    task = models.ForeignKey('licprocesses.Task', db_index=True)

    external_id = models.CharField(verbose_name=u'Идентификатор заявления в Концентраторе', max_length=255, null=True,
                                   blank=True)

    epgu_id = models.CharField(verbose_name=u'Идентификатор заявления на портале ЕПГУ', max_length=255, null=True,
                               blank=True)

    from_epgu = models.BooleanField(verbose_name=u'Направление изменения статуса заявления в Концентраторе',
                                    default=False)

    performed = models.BooleanField(verbose_name=u'Статус отправки', default=False)

    applicant_firstname = models.CharField(verbose_name=u'Имя Заявителя', max_length=150, blank=True, null=True)

    applicant_lastname = models.CharField(verbose_name=u'Фамилия Заявителя', max_length=150, blank=True, null=True)

    applicant_middlename = models.CharField(verbose_name=u'Отчество Заявителя', max_length=150, blank=True, null=True)

    state = models.CharField(verbose_name=u'Статус заявления', max_length=255)

    details = models.TextField(verbose_name=u'Детализация стауса', blank=True, null=True)

    attempts = models.IntegerField(u'Число попыток', null=False, default=0)

    def clean(self):
        if not (self.external_id or self.epgu_id):
            raise ValidationError(u"Идентификатор заявления должен быть указан.")


class ExternalStatus(models.Model):
    code = models.IntegerField(verbose_name=u'Код статуса', primary_key=True)
    name = models.CharField(verbose_name=u'Наименование статуса', max_length=255)
    description = models.TextField(u'Расшифровка статуса', blank=True, null=True)

    class Meta:
        verbose_name = u'Статус для концентратора'
        """
        Отображение наименования экземпляра класса в админке
        """
        verbose_name_plural = u'Статусы для концентратора'
        """
        Отображение наименования модели в админке
        """

    def __unicode__(self):
        """
        @return: Возвращает наименование статуса
        @rtype: string
        """
        return self.name


class FMSPassportData(models.Model):
    """
    Данные о проверяемом паспорте в ФМС
    """

    series = models.CharField(u'Серия паспорта', max_length=10, null=True, blank=True)
    no = models.CharField(u'Номер паспорта', max_length=10, null=True, blank=True)
    issue_date = models.DateField(u'Дата выдачи паспорта', null=True, blank=True)
    surname = models.CharField(u'Фамилия', max_length=100, null=True, blank=True)
    name = models.CharField(u'Имя', max_length=100, null=True, blank=True)
    patronymic = models.CharField(u'Отчество', max_length=100, null=True, blank=True)

    result = models.TextField(u'Результат запроса в ФМС', null=True, blank=True)

    task_id = models.IntegerField(verbose_name=u'Идентификатор задания', primary_key=True, db_index=True)


class SendToGSQueue(models.Model):
    task = models.ForeignKey('licprocesses.Task', blank=True, null=True, db_index=True)

    status = models.CharField(choices=dictionary_to_choises(SEND_TO_GS_STATUS), default=TURN,
                              verbose_name=u'Состояние отправки запроса в ГС', max_length=128)

    additionally = models.TextField(
        u'Дополнение',
        blank=True, null=True)

    number_of_attempts_send = models.IntegerField(u'Счетчик', default=0, blank=False, null=False)

    def get_status_name(self):
        return SEND_TO_GS_STATUS.get(self.status)


class SendToISOGDQueue(models.Model):
    task = models.ForeignKey('licprocesses.Task', blank=True, null=True, db_index=True)

    status = models.CharField(choices=dictionary_to_choises(SEND_TO_ISOGD_STATUS), default=TURN,
                              verbose_name=u'Состояние отправки запроса в ИСОГД', max_length=128)

    additionally = models.TextField(u'Дополнение', blank=True, null=True)

    number_of_attempts_send = models.IntegerField(u'Счетчик', default=0, blank=False, null=False)

    def get_status_name(self):
        return SEND_TO_ISOGD_STATUS.get(self.status)


class RLDD2ClaimQueue(models.Model):
    task = models.ForeignKey('licprocesses.Task', verbose_name=u'Задание', db_index=True)
    is_created = models.BooleanField(u'Создана ли заявка в РЛДД2', default=False)
    is_ready_to_create = models.BooleanField(u'Готова ли заявка к созданию в РЛДД2', default=True)
    sign_wait_deadline = models.DateTimeField(u'Время ожидания подписи')
    state = models.CharField(u'Статус обработки заявки', choices=RLDD2_REQUEST_STATES, max_length=128)
    rldd_code = models.CharField(u'Код РЛДД2 заявки', max_length=4)

    def get_status_name(self):
        return dict(RLDD2_REQUEST_STATES).get(self.state) or u'-'

    def get_documents(self):
        return RLDD2ClaimQueueDocs.objects.filter(queue=self)


class RLDD2ClaimQueueRLDDId(models.Model):
    queue = models.ForeignKey(RLDD2ClaimQueue)
    claim_id = models.CharField(u'ID в РЛДД', max_length=128)
    custom_claim_id = models.CharField(u'ID МКУ', max_length=128)


class RLDD2ClaimQueueDocs(models.Model):
    not_accepted_by_user = models.NullBooleanField(u'Отказано пользователем', null=True, blank=True)
    result_doc_uuid = models.CharField(u'GUID результирующего документа в РЛДД', max_length=128)
    queue = models.ForeignKey(RLDD2ClaimQueue)
    result_doc = models.ForeignKey('docums.Doc', verbose_name=u'Результирующий документ', db_index=True)
    is_signed = models.BooleanField(u'Подписан ли документ', default=False)


class RLDD2ReceiptApplications(models.Model):

    class RLDD2ReceiptApplicationsManager(models.Manager):
        def get_queryset(self):
            from base.middleware import get_current_user
            from accounts.permissions import Permissions
            from licprocesses.models import PGUProcessType

            user = get_current_user()
            if user and user.is_authenticated() and not user.is_superuser:
                kind_list = Permissions().activities_kinds().values('id')
                srgu_list = PGUProcessType.objects.filter(
                    process_type__license_kind__id__in=kind_list).values('srguServiceId')
                return super(RLDD2ReceiptApplications.RLDD2ReceiptApplicationsManager, self).get_queryset().filter(
                    srguServiceId__in=srgu_list
                )
            return super(RLDD2ReceiptApplications.RLDD2ReceiptApplicationsManager, self).get_queryset()

    request = models.ForeignKey('licenses.LicenseRequest', verbose_name=u'Созданная заявка', db_index=True,
                                null=True)
    process_ref = DocumentForeignKey('licprocesses.Process', db_index=True, null=True)
    srguServiceId = models.CharField(u'srguServiceId', max_length=128, null=True)
    date_receipt = models.DateTimeField(u'Дата приема')
    claim_id = models.CharField(u'ID в РЛДД', max_length=128)
    custom_claim_id = models.CharField(u'ID МКУ', max_length=128, null=True)
    status = models.CharField(u'Статус обработки заявки', choices=RLDD2_RECEIP_REQUEST_STATE, max_length=128)
    comment = models.TextField(u'Комментарии к заявке', blank=True, null=True)

    objects = RLDD2ReceiptApplicationsManager()

    def get_process(self):
        from licprocesses.models import Process
        return Process.at(retrospection.now()).get(document_id=self.process_ref)

    def get_rgu_process_names(self):
        from licprocesses.models import PGUProcessType
        return u','.join(PGUProcessType.objects.filter(srguServiceId=self.srguServiceId).values_list('name', flat=True))


class ISOGDDocInfo(models.Model):
    isogd_queue = models.ForeignKey(SendToISOGDQueue, db_index=True, null=True, blank=True)
    result_doc = models.ForeignKey('docums.DocFile', verbose_name=u'Результирующий документ', db_index=True)
    ap_data = models.OneToOneField(
        'licenses.ActivityPlace',
        verbose_name=u'Информация по ПА',
        db_index=True, blank=True, null=True)
    uploading_number_isogd = models.CharField(u'Загрузочный номер ИСОГД', max_length=255, blank=True, null=True)

    sign_uploading_number_isogd = models.CharField(
        u'Загрузочный номер ИСОГД для ЭЦП',
        max_length=255, blank=True, null=True)
    temporary_number_isogd = models.CharField(u'Временный номер ИСОГД', max_length=255, blank=True, null=True)
    constant_number_isogd = models.CharField(u'Постоянный номер ИСОГД', max_length=255, blank=True, null=True)
    isogd_status = models.IntegerField(u'Статус документа ИСОГД', choices=ISOGD_DOC_STATUSES, default=ISOGD_DOC_GIVEN)


class EgrpCryptoReuestData(models.Model):
    request_doc = models.ForeignKey('docums.DocFile', verbose_name=u'Результирующий документ', null=True, blank=True,
                                    db_index=True)
    request_id = models.CharField(u'ID запроса', max_length=255, null=True, blank=True)
    request_type = models.CharField(u'Тип запроса', max_length=255, null=True, blank=True)
    status = models.IntegerField(u'Статус заявки', choices=AUTO_REQUEST_STATES, blank=True, null=True)
    task = models.ForeignKey('licprocesses.Task')
    identificator = models.CharField(u'Идентификатор объекта', max_length=255, blank=True, null=True)
    identification_method = models.CharField(u'Метод идентификатора объекта', max_length=255, blank=True, null=True)

    @property
    def request_status_text(self):
        """
        @return: возвращает статус запроса в виде строки
        @rtype: string
        """

        return dict(AUTO_REQUEST_STATES).get(self.status)


class EgrpCryptoHistory(models.Model):
    """
    История запросов в ЕГРП, выполняемых с криптошлюзом
    """
    request_data = models.ForeignKey(EgrpCryptoReuestData, null=True, blank=True)
    service_request = models.OneToOneField(DataServiceRequest, blank=True, null=True)

    class Meta:
        db_table = 'ws_crypto_egrprequestdata_history'


RLDD2_INFO_STATES = (
    (QUEUED, u'Запрос поставлен в очередь'),
    (COMPLETED, u'Запрос успешно обработан'),
    (ERROR, u'Ошибка создания запроса'),
)


class RLDD2InfoRequestQueue(models.Model):
    """
    Элементы очереди на запрос информации из РЛДД
    """
    completed = models.BooleanField(u'Опрошен ли РЛДД2', default=False)
    state = models.CharField(u'Статус обработки заявки',
                             choices=RLDD2_INFO_STATES,
                             default=QUEUED,
                             max_length=128)
    type = models.CharField(u'Тип опроса РЛДД', default=u'MINSTROY_ESIA', max_length=128)
    # на случай разных типов запросов в РЛДД2, по умолчанию "Запрос информации о данных ЕСИА для РС/РВ"
    attempts = models.IntegerField(u'Счетчик опроса РЛДД', default=0)
    process = models.ForeignKey('licprocesses.Process', blank=True, null=True)
    rldd_response = models.ForeignKey('docums.DocFile', verbose_name=u'Результат запроса', null=True, blank=True,
                                      db_index=True)
    queue_time = models.DateTimeField(u'Время постановки задания', null=True)
    receipt_time = models.DateTimeField(u'Время получения данных', null=True)

    @property
    def request_status_text(self):
        """
        @return: возвращает статус запроса в виде строки
        @rtype: string
        """

        return dict(RLDD2_INFO_STATES).get(int(self.state))


class UserProfileCryptoVersion(models.Model):
    """
    Лог версий Криптошлюза на машине пользователя
    """
    from accounts.models import Profile

    user_profile = models.ForeignKey(Profile, null=True, blank=True)
    version = models.CharField(u'Версия Криптошлюза', max_length=50, null=True)
    datetime = models.DateTimeField(u'Время получения данных', null=True)

    class Meta:
        db_table = 'ws_userprofile_cryptoversion'


document_accepted_ws.connect(document_accepted_from_vis_guag_gs, sender=None, dispatch_uid='93923635498346876275')
guag_message_accepted_ws.connect(guag_message_accepted, sender=None, dispatch_uid='0923554092354496642')

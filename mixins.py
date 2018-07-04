# coding: utf-8
import logging

from core_utils.utils import EmptyQuerySet
from documents import retrospection

from base.decorators import try_it_more
from processes.minstroy.utils import get_received_doc_info, journal_seq_counter_num
from processes.minstroy.utils import get_seq_counter, increment_seq_counter_num

logger = logging.getLogger(__name__)


class MixinTask(object):

    @property
    def case_land(self):
        """
        Возвращает дело о земельном участке
        :return: processes.minstroy.CaseLand
        """
        process = self.get_process()

        from processes.minstroy.models import CaseLand
        while process.parent_process is not None:
            process = process.parent_process

        try:
            return CaseLand.at(retrospection.now()).get(
                process_ref=process.document_id)
        except CaseLand.DoesNotExist or CaseLand.MultipleObjectsReturned:
            return None

    @staticmethod
    def case_land_go_faster_filter(filter={}, param=EmptyQuerySet()):
        """
        статик метод для быстрого поиска, получился большой из-за того что надо было выгребсти подпроцессы
        filter если поиск по модели конечный,т.е. искомое поле находится в этой модели
        param промужуточная модель для поиска, конечное поле в другой модели
        """
        from licprocesses.models import Process, Task
        if param:
            param_list = param.values_list('process_ref', flat=True)
            c_l_process = Process.at(retrospection.now()).filter(document_id__in=param_list)
            task = Task.at(retrospection.now()).filter(process__in=c_l_process.values_list('document_id', flat=True))
            parent_process = Process.at(retrospection.now()).filter(parent_task__in=task.values_list('document_id',
                                                                                                     flat=True))
            c_l_list_process = list(param_list)
            c_l_list_process.extend(list(parent_process.values_list('document_id', flat=True)))
            return {'process__in': c_l_list_process}
        from processes.minstroy.models import CaseLand

        case_land_list = CaseLand.at(retrospection.now()).filter(**filter).values_list('process_ref', flat=True)
        c_l_process = Process.at(retrospection.now()).filter(document_id__in=case_land_list)
        task = Task.at(retrospection.now()).filter(process__in=c_l_process.values_list('document_id', flat=True))
        parent_process = Process.at(retrospection.now()).filter(parent_task__in=task.values_list('document_id',
                                                                                                 flat=True))
        c_l_list_process = list(case_land_list)
        c_l_list_process.extend(list(parent_process.values_list('document_id', flat=True)))
        return {'process__in': c_l_list_process}

    @staticmethod
    def case_land_result_type_registry():
        """ x """
        from processes.minstroy.models import CaseLand
        pass
        return CaseLand

    @staticmethod
    def case_land_result_type():
        """ x """
        from processes.minstroy.models import CaseLand
        return CaseLand

    @property
    def who_send_case(self):
        """
        Возвращает запись журнала о отправленных
        :return: processes.minstroy.WhoSendCase
        """

        from processes.minstroy.models import WhoSendCase
        return WhoSendCase.objects.get(
            process_ref=self.process)

    @property
    def send_2_mfc(self):
        """
        Возвращает запись журнала об отправленных документа в МФЦ
        :return: processes.minstroy.Send2MFCRegistry
        """

        from processes.minstroy.models import Send2MFCRegistry
        return Send2MFCRegistry.objects.get(
            process_ref=self.process)

    @property
    def to_accept_task(self):
        from django.utils.safestring import mark_safe
        return mark_safe(
            '<input type="button" onclick="to_accept_task(' + str(self.document_id) + ')" value="Принять">')

    @property
    def name_with_docs_received_status(self):
        """ Возвращает наименование задания + иконки статуса о поступлении документов из вне (ГУАГ, ГС...)

        @type self: licprocesses.models.Task
        @return:
        @rtype: basestring
        """
        from django.contrib.staticfiles.templatetags.staticfiles import static
        from django.utils.safestring import mark_safe

        def _groupby_date(docs):
            out = []
            prev_date = None
            for doc in docs:
                _date = doc['registered_date'].strftime("%d.%m.%Y %H:%M")
                if _date != prev_date and prev_date is not None:
                    out.append((prev_date, local_out))
                    prev_date = _date
                    local_out = []
                if prev_date is None:
                    prev_date = _date
                    local_out = []
                local_out.append(doc)
            if docs:
                out.append((_date, local_out))

            return out

        def _get_received_docs(task, rel_name_):
            """ возвращает поступившие из вне документы для задания

            @type task: licprocesses.models.Task
            @param rel_name_: имя обратной связи для Doc
            @type rel_name_: str
            @return: events = []
            @rtype: list
            """

            event_ = ''
            rel_map = {'requestdocument': (u'А', u'ВИС ГУАГ', 'guag_docs'),
                       'gsdocument__request_data': (u'Г', u'АИС ГС', 'gs_docs')}
            short_from_ = rel_map[rel_name_][0]
            doc_from = rel_map[rel_name_][1]
            icon_name_ = rel_map[rel_name_][2]

            # import random
            # if not random.choice([0, 1, 2]):
            #     return short_from_, icon_name_, event_

            date_docs = get_received_doc_info(task.document_id, rel_name_, order_by='-doc__registered')
            if date_docs:
                """ согласно постановки: если первая дата в списке свежее,
                 чем дата просмотра задания - выбираем только свежие события, иначе все """
                if task.owner_seen and task.owner_seen < date_docs[0]['registered_date']:
                    icon_name_ = 'new_' + icon_name_
                    date_docs = [d for d in date_docs if task.owner_seen < date_docs[0]['registered_date']]
                elif not task.owner_seen:
                    icon_name_ = 'new_' + icon_name_

                date_docs = _groupby_date(date_docs)
                events_ = []

                for date_, docs_ in date_docs:
                    events_.append(
                        u'{date} - {where_from} {state}:\n'
                        u'{docs}'.format(
                            date=date_,
                            where_from=doc_from,
                            docs=u'\n'.join([u'  - %s' % d['name'] for d in docs_]),
                            state='(%s)' % docs_[0]['state'] if docs_[0]['state'] else ''
                        )
                    )

                event_ = u'\n\n'.join(events_)

            return short_from_, icon_name_, event_

        out = self.__unicode__()
        if self.request and self.task_type.slug in ('rppt_information_analysis',
                                                    'uppt_information_analysis',
                                                    'gpzu_information_analysis'):

            cells_with_icon = []
            for rel_name in ('requestdocument',
                             'gsdocument__request_data'):
                short_from, icon_name, event = _get_received_docs(self, rel_name)
                if event:
                    img_src = static("minstroy/img/{0}.png".format(icon_name))
                    img_html_code = (u''
                                     # u'<td>'
                                     u'<td style="border: 0;">'
                                     u'<img src="{img_src}" title="{events}">'
                                     # u'{short}'
                                     u'</td>').format(img_src=img_src, events=event, short=short_from)
                    cells_with_icon.append(img_html_code)

            if cells_with_icon:
                trs = (u'<tr>'
                       u'{cell}'
                       u'<td style="border: 0;"  rowspan="{rowspan}">{href_text}</td>'
                       u'</tr>').format(rowspan=len(cells_with_icon), href_text=out, cell=cells_with_icon[0])

                for cell in cells_with_icon[1:]:
                    trs += u'<tr>{0}</tr>'.format(cell)

                html_table = (
                    u'<table><tbody>'
                    u'{trs}'
                    u'</tbody></table>'
                ).format(cells=''.join(cells_with_icon), trs=trs)

                out = mark_safe(html_table)

        return out


class MixinProcess(object):
    """
    Примесь к процессам (Process)
    """

    @property
    def case_land(self):
        """
        Возвращает дело о земельном участке
        @return: processes.minstroy.models.minstroy.CaseLand
        """

        from processes.minstroy.models import CaseLand
        process = self

        while process.parent_process is not None:
            process = process.parent_process
        try:
            # После запуска ГПЗУ до завершения подачи документов дело
            # о змеле еще не создано
            return CaseLand.at(retrospection.now()).get(
                process_ref=process.document_id)
        except CaseLand.DoesNotExist:
            return None

    @staticmethod
    def case_land_result_type():
        from processes.minstroy.models import CaseLand
        return CaseLand

    @property
    def finished_state(self):
        return u'Закрытая' if self.finished else u'Открытая'

    @staticmethod
    def finished_state_result_type():
        return ((0, u'---------'), (1, u'Открытая'), (2, u'Закрытая'))

    @staticmethod
    def finished_state_go_faster_filter(value):
        from licprocesses.models import Process
        if value:
            param = value.values()[0]
        else:
            param = True
        if param == u'0':
            return {'document_id__in': Process.at(retrospection.now()).values_list('document_id', flat=True)}
        elif param in (u'1', u'2'):
            return {'document_id__in': Process.at(retrospection.now()).filter(
                finished__isnull=param == u'1').values_list('document_id', flat=True)}
        else:
            return {'document_id__in': Process.at(retrospection.now()).values_list('document_id', flat=True)}

    @property
    def pause_info(self):
        """
        Возвращает дело о приостановлении
        @return: processes.minstroy.models.minstroy.ProcessPauseInfo
        """
        process = self

        from processes.minstroy.models import ProcessPauseInfo
        return ProcessPauseInfo.at(retrospection.now()).get(
            process_ref=process.document_id)

    def get_info_about_lands(self):
        from processes.minstroy.models import InfoAboutLand
        from processes.minstroy.models import CaseLand
        try:
            return InfoAboutLand.objects.filter(case_ref=self.case_land.document_id)
        except CaseLand.DoesNotExist:
            return InfoAboutLand.objects.none()

    def get_cases_gpzu(self):
        from processes.minstroy.models import CaseGpzu
        return CaseGpzu.at(retrospection.now()).filter(document_id=self.case_land.gpzu.document_id)


class MixinLicenseRequest(object):
    """
    Примесь к заявкам (LicenseRequest)
    """
    from processes.minstroy.reference_book import REQ_NUM_COUNTER

    @try_it_more(max_attempts=3)
    def generate_request_number(self, seq_slug=REQ_NUM_COUNTER, suffix=u'', suffix_end=u''):
        """ Присвоение входящего номера заявке.

        :param seq_slug: слаг нумератора
        :param suffix: суффикс для жилья/нежилья на КУРТ
        :type self: licenses.models.LicenseRequest
        """
        from processes.minstroy.models.minstroy import RequestNumbers
        from processes.minstroy.reference_book import REQ_NUM_PREFIXES

        cnt = None
        qs = RequestNumbers.objects.filter(object_id=self.id)
        if not qs.exists():
            cnt = get_seq_counter(seq_slug)
        elif not self.no:
            try:
                cnt = qs.order_by('-assignation_date')[0].counter_type
            except Exception as e:
                logger.exception(e)

        if cnt:
            req_num = u'%s%s%s-%sВХ/%s%s' % (
                REQ_NUM_PREFIXES.get(int(self.way_to_apply)),
                str(cnt.counter).rjust(5, '0'),
                suffix,
                str(cnt.year)[2:],
                self.process_type_link.req_num_code,
                suffix_end
            )
            self.no = req_num
            self.save()

            journal_seq_counter_num(self.id, cnt)
            increment_seq_counter_num(seq_slug)

    @property
    def case_land(self):
        """
        Возвращает дело о земельном участке
        :return: processes.minstroy.CaseLand
        """

        from processes.minstroy.models import CaseLand
        try:
            process = self.get_process()
            if process:
                return CaseLand.at(retrospection.now()).get(
                    process_ref=process.document_id)
            else:
                return None
        except CaseLand.DoesNotExist or CaseLand.MultipleObjectsReturned:
            return None

    @staticmethod
    def case_land_result_type_registry():
        from processes.minstroy.models import CaseLand
        return CaseLand

    @staticmethod
    def case_land_result_type():
        from processes.minstroy.models import CaseLand
        return CaseLand

    def get_custom_order_id_history(self):
        from ws.models import RLDD2ClaimQueueRLDDId, RLDD2ClaimQueue
        queues = RLDD2ClaimQueue.objects.filter(task__owner_process__request=self)
        history_ids = [x.custom_claim_id for x in RLDD2ClaimQueueRLDDId.objects.filter(queue__in=queues)]
        customer_order_ids = [self.custom_order_id] if self.custom_order_id else list()
        return '; '.join(customer_order_ids+history_ids)

    @property
    def get_custom_order_id_history_registry(self):
        from ws.models import RLDD2ClaimQueueRLDDId, RLDD2ClaimQueue
        queues = RLDD2ClaimQueue.objects.filter(task__owner_process__request=self)
        history_ids = [x.custom_claim_id for x in RLDD2ClaimQueueRLDDId.objects.filter(queue__in=queues)]
        customer_order_ids = [self.custom_order_id] if self.custom_order_id else list()
        return '; '.join(customer_order_ids+history_ids)

    @staticmethod
    def get_custom_order_id_history_registry_go_faster_filter(value):
        from ws.models import RLDD2ClaimQueueRLDDId
        from licenses.models import LicenseRequest
        param = u''
        if value:
            param = value.values()[0]
        request = RLDD2ClaimQueueRLDDId.objects.filter(custom_claim_id__icontains=param).values_list('queue__task__owner_process__request', flat=True)
        request_1 = LicenseRequest.objects.filter(custom_order_id__icontains=param).values_list('id', flat=True)
        return {'id__in': request | request_1 if request_1 and request else request or request_1}

    @property
    def get_process_registry(self):
        from licprocesses.models import Process
        try:
            return Process.at(retrospection.now()).filter(request_id=self.id)[0]
        except IndexError:
            pass

    @staticmethod
    def get_process_registry_go_faster_filter(filter=None, param=EmptyQuerySet()):
        """
        статик метод для быстрого поиска, получился большой из-за того что надо было выгребсти подпроцессы
        filter если поиск по модели конечный,т.е. искомое поле находится в этой модели
        param промужуточная модель для поиска, конечное поле в другой модели
        """
        from licprocesses.models import Process
        if filter is None:
            filter = {}
        if param:
            param_list = param.values_list('id', flat=True)
            process = Process.at(retrospection.now()).filter(request_id__in=param_list)
            return {'id__in': process.values_list('id', flat=True)}

        return {'id__in': Process.at(retrospection.now()).filter(**filter).values_list('request_id', flat=True)}

    @staticmethod
    def case_land_go_faster_filter(filter={}, param=EmptyQuerySet()):
        """
        статик метод для быстрого поиска, получился большой из-за того что надо было выгребсти подпроцессы
        filter если поиск по модели конечный,т.е. искомое поле находится в этой модели
        param промужуточная модель для поиска, конечное поле в другой модели
        """
        from licprocesses.models import Process
        from licenses.models import LicenseRequest
        if param:
            param_list = param.values_list('process_ref', flat=True)
            c_l_process = Process.at(retrospection.now()).filter(document_id__in=param_list)
            l_r = LicenseRequest.objects.filter(id__in=c_l_process.values_list('request', flat=True))
            return {'id__in': l_r.values_list('id', flat=True)}
        from processes.minstroy.models import CaseLand
        case_land_list = CaseLand.at(retrospection.now()).filter(**filter).values_list('process_ref', flat=True)
        c_l_process = Process.at(retrospection.now()).filter(document_id__in=case_land_list)
        l_r = LicenseRequest.objects.filter(id__in=c_l_process.values_list('request', flat=True))
        return {'id__in': l_r.values_list('id', flat=True)}

    def requestdocuments_for_tmpl(self, rel, reverse_it=False):
        """ Группирует документы по дате поступления из ВИС ГУАГ

        @param rel: related name for RequestDocument or RequestDocumentGS or ...
        @type self: licenses.models.LicenseRequest
        @keyword reverse_it: обратный порядок
        @return: [date1, [Doc1, Doc2,...], date2, [Doc3, Doc4,...]]
        """

        # FIXME костыль ! сделан для показа. разобраться с groupby() и переделать
        reverse = {True: '-', False: ''}[reverse_it]
        out = []
        prev_date = None
        rel_manager = getattr(self, rel)
        for r_d in rel_manager.all().order_by('{0}doc__registered'.format(reverse)):
            _date = r_d.doc.registered.strftime("%d.%m.%Y %H:%M") if r_d.doc.registered else u'нет данных'
            if _date != prev_date and prev_date is not None:
                out.append((prev_date, local_out))
                prev_date = _date
                local_out = []
            if prev_date is None:
                prev_date = _date
                local_out = []
            local_out.append(r_d)
        if rel_manager.all():
            out.append((_date, local_out))

        # FIXME разобраться с groupby
        # from itertools import groupby
        # docs = list(self.requestdocument_set.all().order_by('doc__registered'))
        # out = groupby(docs, key=lambda x: x.doc.registered.strftime("%d.%m.%Y %H:%M"))

        return out

    @property
    def visguag_requestdocuments_for_tmpl(self):
        return self.requestdocuments_for_tmpl('requestdocument_set')

    @property
    def aisgs_requestdocuments_for_tmpl(self):
        return self.requestdocuments_for_tmpl('gsdocument__request_data')

    @property
    def visguag_status_history(self):
        from django.core.urlresolvers import reverse
        from ws.models import DataServiceRequest

        qs = DataServiceRequest.objects \
            .filter(data_request_task__ticket_id=self.id,
                    data_request_task__dest_foiv=41) \
            .order_by('-receive_time') \
            .values_list('receive_time', 'state__slug')

        res_list = []
        for d_s_r in qs:
            if d_s_r[1] == 'success':
                color = 'green'
            else:
                color = 'red'
            out = """<p href="#" title="{title}" style="color:{color}"> {value} </p>""" \
                .format(color=color,
                        value=d_s_r[0].strftime('%d.%m.%Y'),
                        title=d_s_r[0].strftime('%d.%m.%Y %H:%M:%S'))
            res_list.append(out)

        if self.case_land and len(res_list):
            out = '<ul><li>' + '</li><li>'.join(res_list) + '</li></ul>'
            href = '{0}{1}'.format(reverse('smev_service_requests'),
                                   u'?filter=Поиск&appeal_number=%s' % self.case_land.registration_number)
            out = '<a target="_blank" href="{0}">{1}</a>'.format(href, out)
        else:
            out = ''

        return out

    @property
    def visguag_status_history_filter(self):
        from ws.models import DataServiceRequest

        qs = DataServiceRequest.objects \
            .filter(data_request_task__ticket_id=self.id,
                    data_request_task__dest_foiv=41,
                    state__slug='success') \
            .order_by('-receive_time') \
            .values_list('receive_time', flat=True)

        return qs[0] if qs else None

    @property
    def days_of_delay_filter(self):
        return self.get_process().due

    @staticmethod
    def days_of_delay_filter_go_faster_filter(value):
        """
        Метод для быстрого поиска
        """
        from licenses.models import LicenseRequest
        from licprocesses.models import Process
        from licprocesses.utils import get_process_due_date_with_holiday
        import datetime
        if value.values()[0].isdigit():
            date_now = datetime.datetime.now().date()
            date = get_process_due_date_with_holiday(datetime.datetime.now().date(), int(value.values()[0]))
            date = datetime.datetime.combine(date, datetime.time(23, 59, 59, 999999))
            return {
                'id__in': LicenseRequest.objects
                    .filter(id__in=Process.at(retrospection.now())
                            .filter(due__lte=date, due__gte=date_now, finished__isnull=True)
                            .values_list('request', flat=True))
                    .values_list('id', flat=True)}
        else:
            return {'id__in': []}

    @property
    def type_residential_and_classification_construction_site_minst(self):
        return ' / '.join([i for i in [self.type_residential_construction_site,
                                       self.classification_constructio_site,
                                       self.category_object_bulding,
                                       self.infrastructure] if i])

    @property
    def classification_minstroy_project_offices_list(self):
        """
        метод для создания фильтров в реестре миснтроя
        """
        from models import MinstroyProjectOffice
        return list(MinstroyProjectOffice.objects.all().values_list('description', flat=True))


class MixinDoc(object):
    """
    Примесь к документам (Doc)
    """

    @try_it_more(max_attempts=3)
    def _generate_number(self, counter_type_slug, number_string, number_long=5, **number_kwargs):
        from processes.minstroy.models.minstroy import RequestNumbers

        if not RequestNumbers.objects\
                .filter(object_id=self.id, counter_type__slug=counter_type_slug)\
                .exists():
            cnt = get_seq_counter(counter_type_slug)
            number_kwargs.update({
                'cnt': str(cnt.counter).rjust(number_long, '0'),
                'year': str(cnt.year)[2:]
            })
            self.reg_no = number_string.format(**number_kwargs)
            self.save()

            journal_seq_counter_num(self.id, cnt)
            increment_seq_counter_num(counter_type_slug)

    def generate_deny_out_number(self, process_type_code):
        """ Присвоение исходящего номера при отказе ГПЗУ"""
        from processes.minstroy.reference_book import DOC_DENY_OUT_NUM
        self._generate_number(
            DOC_DENY_OUT_NUM.get(process_type_code),
            u'{cnt}-{year}ИСХ/{code}',
            code=process_type_code,
            number_long=4
        )

    def generate_deny_out_number_ppt(self, process_type_code):
        """ Присвоение исходящего номера при отказе ППТ"""
        from processes.minstroy.reference_book import DOC_DENY_OUT_NUM
        self._generate_number(
            DOC_DENY_OUT_NUM.get(process_type_code),
            u'{cnt}-{year}ИСХ/{process}',
            process=process_type_code,
            number_long=4
        )

    def generate_approve_out_number(self, process_type_code, municipal_code, req_num_code_full):
        """ Присвоение исходящего номера при + ГПЗУ"""
        from processes.minstroy.reference_book import DOC_APPROVE_OUT_NUM

        self._generate_number(
            DOC_APPROVE_OUT_NUM.get(req_num_code_full),
            u'{process}{municipal}/{cnt}-{year}',
            process=process_type_code,
            municipal=municipal_code,
            number_long=4
        )

    def generate_approve_out_number_ppt(self, process_type_code, municipal_code, req_num_code_full):
        """ Присвоение исходящего номера при + ППТ"""
        from processes.minstroy.reference_book import DOC_APPROVE_OUT_NUM

        self._generate_number(
            DOC_APPROVE_OUT_NUM.get(req_num_code_full),
            u'{process}{municipal}/{cnt}-{year}',
            process=process_type_code,
            municipal=municipal_code,
            number_long=4
        )

    def generate_deny_out_registration_number(self, req_num_code_full):
        """ Присвоение исходящего номера при отказе в регистрации документов"""
        from processes.minstroy.reference_book import DOC_DENY_OUT_REGISTRATION_NUM
        self._generate_number(
            DOC_DENY_OUT_REGISTRATION_NUM.get(req_num_code_full),
            u'{cnt}-{year}ИСХ/{process}',
            process=req_num_code_full,
            number_long=4
        )

    def generate_deny_out_number_curt(self, seq_slug, format_string, suffix, process_type_code, suffix_end=u''):
        """ Присвоение исходящего номера при отказе КУРТ"""
        self._generate_number(
            counter_type_slug=seq_slug,
            number_string=format_string,
            suffix=suffix,
            code=process_type_code,
            number_long=5
        )

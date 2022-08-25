from app import app, db, utils
from app.models import MonHoc, HocSinh, Diem, LopHoc, Users, NoiQuy
from flask_admin.contrib.sqla import ModelView
from flask_admin import BaseView, expose, Admin, AdminIndexView
from flask_login import logout_user, current_user
from flask import redirect, request

class AdminAuthenticatedView(ModelView):
    def is_accessible(self):
        return current_user.is_authenticated and current_user.username == 'admin'

class SubjectView(AdminAuthenticatedView):
    column_display_pk = True
    can_view_details = True
    edit_modal = True
    details_modal = True
    column_filters = ['ten_mon_hoc']
    column_searchable_list = ['ma_mon_hoc', 'ten_mon_hoc']

    column_labels = {
        'ma_mon_hoc': 'Mã môn học',
        'ten_mon_hoc': 'Tên môn học',
    }
    form_excluded_columns = ['diem']

class StudentView(AdminAuthenticatedView):
    can_view_details = True
    edit_modal = True
    details_modal = True
    column_filters = ['ten_hoc_sinh']
    column_searchable_list = ['ten_hoc_sinh']

    column_labels = {
        'ten_hoc_sinh': 'Họ tên',
        'ngay_sinh': 'Ngày sinh',
        'gioi_tinh': 'Giới tính',
        'dia_chi': 'Địa chỉ',
        'so_dien_thoai': 'Số điện thoại',
        'lop_hoc': 'Lớp học'
    }
    column_exclude_list = ['so_dien_thoai', 'email']
    form_excluded_columns = ['diem']

class ScoreView(AdminAuthenticatedView):
    can_view_details = True
    edit_modal = True
    details_modal = True

    column_labels = {
        'hoc_sinh': 'Tên học sinh',
        'bai_kiem_tra': 'Tên bài kiểm tra',
        'hoc_ky': 'Tên học kì',
        'nam_hoc': 'Tên năm học',
        'mon_hoc': 'Tên môn học',
        'diem_so': 'Điểm'
    }
    column_searchable_list = ['ma_hoc_sinh']

class RolesView(AdminAuthenticatedView):
    can_view_details = True
    edit_modal = True
    details_modal = True

    column_labels = {
        'ten_noi_quy': 'Tên quy định',
        'noi_dung': 'Nội dung chi tiết',
        'gia_tri': 'Giá trị thay đổi',
        'lop_hoc': 'Lớp học áp dụng'
    }
    column_searchable_list = ['ten_noi_quy']

class LogoutView(BaseView):
    @expose('/')
    def index(self):
        logout_user()
        return redirect('/admin')

    def is_accessible(self):
        return current_user.is_authenticated

class MyAdminHomeView(AdminIndexView):
    @expose('/')
    def index(self):
        nh = request.args.get('nh')
        hk = request.args.get('hk')
        mh = request.args.get('mh')
        lop = request.args.get('lop')

        all_subjects = utils.get_all_subjects()
        all_classes = utils.get_all_classes()
        all_terms = utils.get_all_terms()
        all_semesters = utils.get_all_semesters()

        result3 = utils.stats_students_qualified(ma_nam_hoc=nh, ma_hoc_ky=hk, ma_mon_hoc=mh, ma_lop=lop)
        result4 = utils.count_students_qualified_2(ma_nam_hoc=nh, ma_hoc_ky=hk, ma_mon_hoc=mh, ma_lop=lop)
        result5 = utils.count_students_qualified_3(ma_nam_hoc=nh, ma_hoc_ky=hk, ma_mon_hoc=mh, ma_lop=lop)
        result6 = utils.count_students_qualified_4(ma_nam_hoc=nh, ma_hoc_ky=hk, ma_mon_hoc=mh, ma_lop=lop)
        result7 = utils.amount_student_gb_class

        subject_name = utils.get_subject_by_id(id=mh)
        term_name = utils.get_term_by_id(id=hk)
        semester_name = utils.get_semester_by_id(id=nh)

        return self.render('admin/index.html', result3=result3, result4=result4,
                           result5=result5,  result6=result6, lop=lop,
                           mon_hoc=mh, hoc_ky=hk, nam_hoc=nh,
                           subjects=all_subjects, classes=all_classes, terms=all_terms,
                           semesters=all_semesters, result7=result7, subject_name=subject_name,
                           term_name=term_name, semester_name=semester_name)

class StatsView(BaseView):
    @expose('/')
    def index(self):
        nh = request.args.get('nh')
        hk = request.args.get('hk')
        mh = request.args.get('mh')
        lop = request.args.get('lop')

        result3 = utils.get_info_classes(ma_nam_hoc=nh, ma_hoc_ky=hk, ma_mon_hoc=mh, ma_lop=lop)
        result4 = utils.count_students_qualified(ma_nam_hoc=nh, ma_hoc_ky=hk, ma_mon_hoc=mh, ma_lop=lop)
        result5 = utils.count_students_qualified
        result6 = utils.amount_student_gb_class

        all_subjects = utils.get_all_subjects()
        all_classes = utils.get_all_classes()
        all_terms = utils.get_all_terms()
        all_semesters = utils.get_all_semesters()

        subject_name = utils.get_subject_by_id(id=mh)
        term_name = utils.get_term_by_id(id=hk)
        semester_name = utils.get_semester_by_id(id=nh)

        return self.render('admin/stats.html', result3=result3, result4=result4,
                           ma_lop=lop, subjects=all_subjects, classes=all_classes,
                           terms=all_terms, semesters=all_semesters, result5=result5,
                           result6=result6, ma_nam_hoc=nh, ma_hoc_ky=hk,
                           ma_mon_hoc=mh, subject_name=subject_name, term_name=term_name,
                           semester_name=semester_name)


admin = Admin(app=app, name='Trang Quản Trị', template_mode='bootstrap4', index_view=MyAdminHomeView())

admin.add_view(SubjectView(MonHoc, db.session, name='Quản lý môn học'))
admin.add_view(RolesView(NoiQuy, db.session, name='Thay đổi quy định'))
admin.add_view(StatsView(name='Thống kê báo cáo'))

admin.add_view(LogoutView(name='Đăng xuất'))
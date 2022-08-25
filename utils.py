from app.models import Users, Diem, HocSinh, LopHoc, NamHoc, HocKy, MonHoc
import hashlib
from app import db
from sqlalchemy import func, distinct

def get_user_by_id(user_id):
    return Users.query.get(user_id)

def add_student(ten, gioi_tinh, ngay_sinh, dia_chi, sdt, email, ma_lop):
    h = HocSinh(ten_hoc_sinh=ten, ngay_sinh=ngay_sinh, gioi_tinh=gioi_tinh, dia_chi=dia_chi,
                so_dien_thoai=sdt, email=email, ma_lop_hoc=ma_lop)
    db.session.add(h)
    db.session.commit()

def get_students_by_class(ma_lop=None):
    q = db.session.query(HocSinh.ma_hoc_sinh, HocSinh.ten_hoc_sinh)\
        .join(LopHoc, HocSinh.ma_lop_hoc.__eq__(LopHoc.ma_lop_hoc))

    if ma_lop:
        q = q.filter(LopHoc.ma_lop_hoc.__eq__(ma_lop))

    return q.group_by(HocSinh.ten_hoc_sinh).all()

def add_score(ma_hs, ma_mh, ma_hk, ma_nh, ma_bai_kt, diem):
    d = Diem(ma_hoc_sinh=ma_hs, ma_mon_hoc=ma_mh, ma_nam_hoc=ma_nh, ma_hoc_ky=ma_hk,
             ma_bai_kiem_tra=ma_bai_kt, diem_so=diem)
    db.session.add(d)
    db.session.commit()

def stat_average_score(ma_nh=None, ma_lop=None, ma_hk=None):
    q = db.session.query(HocSinh.ten_hoc_sinh, LopHoc.ten_lop_hoc, func.avg(Diem.diem_so))\
        .join(LopHoc, HocSinh.ma_lop_hoc.__eq__(LopHoc.ma_lop_hoc))\
        .join(Diem, HocSinh.ma_hoc_sinh.__eq__(Diem.ma_hoc_sinh))\
        .join(NamHoc, Diem.ma_nam_hoc.__eq__(NamHoc.ma_nam_hoc))\
        .join(HocKy, Diem.ma_hoc_ky.__eq__(HocKy.ma_hoc_ky))

    if ma_lop:
        q = q.filter(LopHoc.ma_lop_hoc.__eq__(ma_lop))
    if ma_nh:
        q = q.filter(NamHoc.ma_nam_hoc.__eq__(ma_nh))
    if ma_hk:
        q = q.filter(HocKy.ma_hoc_ky.__eq__(ma_hk))

    return q.group_by(HocSinh.ten_hoc_sinh, LopHoc.ten_lop_hoc).all()

def check_user_login(username, password, role_id):
    if username and password:
        password = str(hashlib.md5(password.strip().encode('utf-8')).hexdigest())

        return Users.query.filter(Users.username.__eq__(username.strip()),
                                  Users.password.__eq__(password),
                                  Users.user_role_id.__eq__(role_id)).first()

def count_students_qualified(ma_nam_hoc=None, ma_hoc_ky=None, ma_mon_hoc=None, ma_lop=None):
    # Dem SL hoc sinh co DTB >= 5.0
    q = db.session.query(LopHoc.ten_lop_hoc, func.count(distinct(HocSinh.ma_hoc_sinh)))\
        .join(HocSinh, LopHoc.ma_lop_hoc.__eq__(HocSinh.ma_lop_hoc))\
        .join(Diem, HocSinh.ma_hoc_sinh.__eq__(Diem.ma_hoc_sinh)) \
        .join(MonHoc, Diem.ma_mon_hoc.__eq__(MonHoc.ma_mon_hoc))\
        .join(NamHoc, Diem.ma_nam_hoc.__eq__(NamHoc.ma_nam_hoc))\
        .join(HocKy, Diem.ma_hoc_ky.__eq__(HocKy.ma_hoc_ky))

    if ma_nam_hoc:
        q = q.filter(NamHoc.ma_nam_hoc.__eq__(ma_nam_hoc))

    if ma_hoc_ky:
        q = q.filter(HocKy.ma_hoc_ky.__eq__(ma_hoc_ky))

    if ma_mon_hoc:
        q = q.filter(MonHoc.ma_mon_hoc.__eq__(ma_mon_hoc))

    if ma_lop:
        q = q.filter(LopHoc.ma_lop_hoc.__eq__(ma_lop))

    return q.group_by(LopHoc.ten_lop_hoc, HocSinh.ma_hoc_sinh)\
            .having(func.avg(Diem.diem_so) >= 5.0).count()

def get_info_classes(ma_nam_hoc=None, ma_hoc_ky=None, ma_mon_hoc=None, ma_lop=None):
    # Lay ra thong tin tat ca lop hoc (ma lop hoc, ten lop hoc)
    q = db.session.query(LopHoc.ma_lop_hoc, LopHoc.ten_lop_hoc) \
        .join(HocSinh, LopHoc.ma_lop_hoc.__eq__(HocSinh.ma_lop_hoc))\
        .join(Diem, HocSinh.ma_hoc_sinh.__eq__(Diem.ma_hoc_sinh)) \
        .join(NamHoc, Diem.ma_nam_hoc.__eq__(NamHoc.ma_nam_hoc)) \
        .join(HocKy, Diem.ma_hoc_ky.__eq__(HocKy.ma_hoc_ky)) \
        .join(MonHoc, Diem.ma_mon_hoc.__eq__(MonHoc.ma_mon_hoc))

    if ma_nam_hoc:
        q = q.filter(NamHoc.ma_nam_hoc.__eq__(ma_nam_hoc))

    if ma_hoc_ky:
        q = q.filter(HocKy.ma_hoc_ky.__eq__(ma_hoc_ky))

    if ma_mon_hoc:
        q = q.filter(MonHoc.ma_mon_hoc.__eq__(ma_mon_hoc))

    if ma_lop:
        q = q.filter(LopHoc.ma_lop_hoc.__eq__(ma_lop))

    return q.group_by(LopHoc.ma_lop_hoc, LopHoc.ten_lop_hoc)\
            .order_by(LopHoc.ma_lop_hoc).all()

def stats_students_qualified(ma_nam_hoc=None, ma_hoc_ky=None, ma_mon_hoc=None, ma_lop=None):
    # Thong ke DTB cua tat ca hoc sinh
    q = db.session.query(LopHoc.ten_lop_hoc, HocSinh.ten_hoc_sinh,
                         func.avg(Diem.diem_so), LopHoc.ma_lop_hoc)\
            .join(Diem, HocSinh.ma_hoc_sinh.__eq__(Diem.ma_hoc_sinh))\
            .join(LopHoc, HocSinh.ma_lop_hoc.__eq__(LopHoc.ma_lop_hoc))\
            .join(NamHoc, Diem.ma_nam_hoc.__eq__(NamHoc.ma_nam_hoc))\
            .join(HocKy, Diem.ma_hoc_ky.__eq__(HocKy.ma_hoc_ky))\
            .join(MonHoc, Diem.ma_mon_hoc.__eq__(MonHoc.ma_mon_hoc))

    if ma_nam_hoc:
        q = q.filter(NamHoc.ma_nam_hoc.__eq__(ma_nam_hoc))

    if ma_hoc_ky:
        q = q.filter(HocKy.ma_hoc_ky.__eq__(ma_hoc_ky))

    if ma_mon_hoc:
        q = q.filter(MonHoc.ma_mon_hoc.__eq__(ma_mon_hoc))

    if ma_lop:
        q = q.filter(LopHoc.ma_lop_hoc.__eq__(ma_lop))

    return q.group_by(LopHoc.ten_lop_hoc, HocSinh.ten_hoc_sinh)\
            .all()

def count_students_qualified_2(ma_nam_hoc=None, ma_hoc_ky=None, ma_mon_hoc=None, ma_lop=None):
    # Dem SL HocSinh Gioi (>=8.0)
    q = db.session.query(LopHoc.ten_lop_hoc, HocSinh.ma_hoc_sinh, func.count(distinct(HocSinh.ma_hoc_sinh))) \
        .join(HocSinh, LopHoc.ma_lop_hoc.__eq__(HocSinh.ma_lop_hoc)) \
        .join(Diem, HocSinh.ma_hoc_sinh.__eq__(Diem.ma_hoc_sinh)) \
        .join(MonHoc, Diem.ma_mon_hoc.__eq__(MonHoc.ma_mon_hoc)) \
        .join(NamHoc, Diem.ma_nam_hoc.__eq__(NamHoc.ma_nam_hoc)) \
        .join(HocKy, Diem.ma_hoc_ky.__eq__(HocKy.ma_hoc_ky))

    if ma_nam_hoc:
        q = q.filter(NamHoc.ma_nam_hoc.__eq__(ma_nam_hoc))

    if ma_hoc_ky:
        q = q.filter(HocKy.ma_hoc_ky.__eq__(ma_hoc_ky))

    if ma_mon_hoc:
        q = q.filter(MonHoc.ma_mon_hoc.__eq__(ma_mon_hoc))

    if ma_lop:
        q = q.filter(LopHoc.ma_lop_hoc.__eq__(ma_lop))

    return q.group_by(LopHoc.ten_lop_hoc, HocSinh.ma_hoc_sinh) \
        .having(func.avg(Diem.diem_so) >= 8.0).count()

def count_students_qualified_3(ma_nam_hoc=None, ma_hoc_ky=None, ma_mon_hoc=None, ma_lop=None):
    # Dem SL HocSinh Kha (>=6.5 & <8.0)
    q = db.session.query(LopHoc.ten_lop_hoc, HocSinh.ma_hoc_sinh, func.count(distinct(HocSinh.ma_hoc_sinh))) \
        .join(HocSinh, LopHoc.ma_lop_hoc.__eq__(HocSinh.ma_lop_hoc)) \
        .join(Diem, HocSinh.ma_hoc_sinh.__eq__(Diem.ma_hoc_sinh)) \
        .join(MonHoc, Diem.ma_mon_hoc.__eq__(MonHoc.ma_mon_hoc)) \
        .join(NamHoc, Diem.ma_nam_hoc.__eq__(NamHoc.ma_nam_hoc)) \
        .join(HocKy, Diem.ma_hoc_ky.__eq__(HocKy.ma_hoc_ky))

    if ma_nam_hoc:
        q = q.filter(NamHoc.ma_nam_hoc.__eq__(ma_nam_hoc))

    if ma_hoc_ky:
        q = q.filter(HocKy.ma_hoc_ky.__eq__(ma_hoc_ky))

    if ma_mon_hoc:
        q = q.filter(MonHoc.ma_mon_hoc.__eq__(ma_mon_hoc))

    if ma_lop:
        q = q.filter(LopHoc.ma_lop_hoc.__eq__(ma_lop))

    return q.group_by(LopHoc.ten_lop_hoc, HocSinh.ma_hoc_sinh) \
        .having( (func.avg(Diem.diem_so) < 8.0) & (func.avg(Diem.diem_so) >= 6.5) ).count()

def count_students_qualified_4(ma_nam_hoc=None, ma_hoc_ky=None, ma_mon_hoc=None, ma_lop=None):
    # Dem SL HocSinh Kha (>=5.0 & <6.5)
    q = db.session.query(LopHoc.ten_lop_hoc, HocSinh.ma_hoc_sinh, func.count(distinct(HocSinh.ma_hoc_sinh))) \
        .join(HocSinh, LopHoc.ma_lop_hoc.__eq__(HocSinh.ma_lop_hoc)) \
        .join(Diem, HocSinh.ma_hoc_sinh.__eq__(Diem.ma_hoc_sinh)) \
        .join(MonHoc, Diem.ma_mon_hoc.__eq__(MonHoc.ma_mon_hoc)) \
        .join(NamHoc, Diem.ma_nam_hoc.__eq__(NamHoc.ma_nam_hoc)) \
        .join(HocKy, Diem.ma_hoc_ky.__eq__(HocKy.ma_hoc_ky))

    if ma_nam_hoc:
        q = q.filter(NamHoc.ma_nam_hoc.__eq__(ma_nam_hoc))

    if ma_hoc_ky:
        q = q.filter(HocKy.ma_hoc_ky.__eq__(ma_hoc_ky))

    if ma_mon_hoc:
        q = q.filter(MonHoc.ma_mon_hoc.__eq__(ma_mon_hoc))

    if ma_lop:
        q = q.filter(LopHoc.ma_lop_hoc.__eq__(ma_lop))

    return q.group_by(LopHoc.ten_lop_hoc, HocSinh.ma_hoc_sinh) \
        .having( (func.avg(Diem.diem_so) < 6.5) & (func.avg(Diem.diem_so) >= 5.0) ).count()

def get_amount_class():
    return db.session.query(LopHoc.ma_lop_hoc).count()

def get_class_by_id(id):
    return LopHoc.query.get(id)

def get_subject_by_id(id):
    return MonHoc.query.get(id)

def get_term_by_id(id):
    return HocKy.query.get(id)

def get_semester_by_id(id):
    return NamHoc.query.get(id)

def get_all_subjects():
    return db.session.query(MonHoc.ten_mon_hoc, MonHoc.ma_mon_hoc).all()

def get_all_classes():
    return db.session.query(LopHoc.ten_lop_hoc, LopHoc.ma_lop_hoc).all()

def get_all_terms():
    return db.session.query(HocKy.ma_hoc_ky, HocKy.ma_hoc_ky).all()

def get_all_semesters():
    return db.session.query(NamHoc.ten_nam_hoc, NamHoc.ma_nam_hoc).all()

def amount_student_gb_class(ma_lop=None, ma_nam_hoc=None, ma_hoc_ky=None, ten_lop=None):
    # Lay thong tin lop hoc (ten lop, so luong hoc sinh) theo gia tri truyen vao
    q = db.session.query(LopHoc.ten_lop_hoc, func.count(distinct(HocSinh.ma_hoc_sinh)))\
        .join(HocSinh, LopHoc.ma_lop_hoc.__eq__(HocSinh.ma_lop_hoc)) \
        .join(Diem, HocSinh.ma_hoc_sinh.__eq__(Diem.ma_hoc_sinh))\
        .join(HocKy, Diem.ma_hoc_ky.__eq__(HocKy.ma_hoc_ky))\
        .join(NamHoc, Diem.ma_nam_hoc.__eq__(NamHoc.ma_nam_hoc))

    if ma_lop:
        q = q.filter(LopHoc.ma_lop_hoc.__eq__(ma_lop))
    if ma_hoc_ky:
        q = q.filter(HocKy.ma_hoc_ky.__eq__(ma_hoc_ky))
    if ma_nam_hoc:
        q = q.filter(NamHoc.ma_nam_hoc.__eq__(ma_nam_hoc))
    if ten_lop:
        q = q.filter(LopHoc.ten_lop_hoc.contains(ten_lop))

    return q.group_by(LopHoc.ma_lop_hoc).all()

def update_student(id, ma_lop):
    u = HocSinh.query.get(id)
    u.ma_lop_hoc = ma_lop
    db.session.commit()

def students_gb_class(ten_hs=None, ten_lop=None):
    q = db.session.query(HocSinh.ma_hoc_sinh, HocSinh.ten_hoc_sinh, LopHoc.ten_lop_hoc,
                         HocSinh.gioi_tinh, HocSinh.ngay_sinh, HocSinh.dia_chi)\
        .join(LopHoc, HocSinh.ma_lop_hoc.__eq__(LopHoc.ma_lop_hoc))

    if ten_hs:
        q = q.filter(HocSinh.ten_hoc_sinh.contains(ten_hs))
    if ten_lop:
        q = q.filter(LopHoc.ten_lop_hoc.__eq__(ten_lop))

    return q.all()

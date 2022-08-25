from sqlalchemy import Integer, String, Column, Enum, ForeignKey, Float, Boolean, DateTime
from app import app, db
from sqlalchemy.orm import relationship, backref
from flask_login import LoginManager, UserMixin
from enum import Enum as CommonEnum

class ChucVu(CommonEnum):
    ADMIN = 1
    NHANVIEN = 2
    GIAOVIEN = 3

class Users(db.Model, UserMixin):
    id = Column(Integer, primary_key=True, autoincrement=True)
    ten = Column(String(25), nullable=False)
    username = Column(String(25), nullable=False, unique=True)
    password = Column(String(50), nullable=False)
    active = Column(Boolean, default=True)
    user_role_id = Column(Integer, ForeignKey('user_role.id'), nullable=False)

    def __str__(self):
        return self.username

class UserRole(db.Model):
    id = Column(Integer, primary_key=True, autoincrement=True)
    chuc_vu = Column(String(25), nullable=False)

    users = relationship('Users', backref='user_role', lazy=True)

class HocSinh(db.Model):
    ma_hoc_sinh = Column(Integer, primary_key=True, autoincrement=True)
    ten_hoc_sinh = Column(String(25), nullable=False)
    ngay_sinh = Column(DateTime)
    gioi_tinh = Column(Integer, default=1)
    dia_chi = Column(String(100), nullable=False)
    so_dien_thoai = Column(String(15))
    email = Column(String(50))
    ma_lop_hoc = Column(Integer, ForeignKey('lop_hoc.ma_lop_hoc'), nullable=False)

    diem = relationship('Diem', backref='hoc_sinh', lazy=True)

    def __str__(self):
        return self.ten_hoc_sinh

class LopHoc(db.Model):
    ma_lop_hoc = Column(Integer, primary_key=True, autoincrement=True)
    ten_lop_hoc = Column(String(25), nullable=False)
    ma_khoi_lop = Column(Integer, ForeignKey('khoi_lop.ma_khoi_lop'), nullable=False)

    hoc_sinh = relationship('HocSinh', backref='lop_hoc', lazy=True)

    def __str__(self):
        return self.ten_lop_hoc

class KhoiLop(db.Model):
    ma_khoi_lop = Column(Integer, primary_key=True, autoincrement=True)
    ten_khoi_lop = Column(String(25), nullable=False)

    lop_hoc = relationship('LopHoc', backref='khoi_lop', lazy=True)

    def __str__(self):
        return self.ten_khoi_lop

class BaiKiemTra(db.Model):
    ma_bai_kiem_tra = Column(Integer, primary_key=True, autoincrement=True)
    ten_bai_kiem_tra = Column(String(50), nullable=False)

    diem = relationship('Diem', backref='bai_kiem_tra', lazy=True)

    def __str__(self):
        return self.ten_bai_kiem_tra

class HocKy(db.Model):
    ma_hoc_ky = Column(Integer, primary_key=True, autoincrement=True)
    ten_hoc_ky = Column(String(50), nullable=False)

    diem = relationship('Diem', backref='hoc_ky', lazy=True)

    def __str__(self):
        return self.ten_hoc_ky

class NamHoc(db.Model):
    ma_nam_hoc = Column(Integer, primary_key=True, autoincrement=True)
    ten_nam_hoc = Column(String(50), nullable=False)

    diem = relationship('Diem', backref='nam_hoc', lazy=True)

    def __str__(self):
        return self.ten_nam_hoc

class MonHoc(db.Model):
    ma_mon_hoc = Column(Integer, primary_key=True, autoincrement=True)
    ten_mon_hoc = Column(String(50), nullable=False)

    diem = relationship('Diem', backref='mon_hoc', lazy=True)

    def __str__(self):
        return self.ten_mon_hoc

class Diem(db.Model):
    ma_diem = Column(Integer, primary_key=True, autoincrement=True)
    ma_hoc_sinh = Column(Integer, ForeignKey(HocSinh.ma_hoc_sinh), nullable=False)
    ma_mon_hoc = Column(Integer, ForeignKey(MonHoc.ma_mon_hoc), nullable=False)
    ma_nam_hoc = Column(Integer, ForeignKey(NamHoc.ma_nam_hoc), nullable=False)
    ma_hoc_ky = Column(Integer, ForeignKey(HocKy.ma_hoc_ky), nullable=False)
    ma_bai_kiem_tra = Column(Integer, ForeignKey(BaiKiemTra.ma_bai_kiem_tra), nullable=False)
    diem_so = Column(Float, default=0)

class NoiQuy(db.Model):
    ma_noi_quy = Column(Integer, primary_key=True, autoincrement=True)
    ten_noi_quy = Column(String(100), nullable=False)
    noi_dung = Column(String(255), nullable=False)
    gia_tri = Column(Integer, nullable=False)

if __name__ == '__main__':
    db.create_all()
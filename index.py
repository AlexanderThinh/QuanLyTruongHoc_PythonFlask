from app import app, login
from flask import render_template, request, redirect, url_for, jsonify
from app.admin import *
from flask_login import login_user
import utils, random
from flask_login import login_required

@app.route('/')
def home():

    return render_template('index.html')

@login.user_loader
def load_user(user_id):
    return utils.get_user_by_id(user_id=user_id)

@app.route('/admin/login', methods=['post'])
def admin_login():
    # username = request.form['username']
    # password = request.form['password']
    #
    # user_admin = utils.check_user_login(username=username, password=password, role='ADMIN')
    # if user_admin:
    #     login_user(user=user_admin)

    return redirect('/admin')

@app.route('/admin/login-2', methods=['post'])
def admin_login_2():
    username = request.json.get('username')
    password = request.json.get('password')

    user_admin = utils.check_user_login(username=username, password=password, role_id=1)
    if user_admin:
        login_user(user=user_admin)
        return jsonify({
            'status': 200,
        })
    return jsonify({
        'status': 404,
        'err_msg': 'Thông tin đăng nhập không chính xác'
    })

@app.route('/staff-login', methods=['post', 'get'])
def staff_login():
    err_msg = ''
    if request.method.__eq__('POST'):
        try:
            username = request.form.get('username')
            password = request.form.get('password')

            staff = utils.check_user_login(username=username, password=password, role_id=2)

            if staff:
                login_user(user=staff)
                return redirect(url_for('staff_login'))
            else:
                err_msg = 'Thông tin đăng nhập không chính xác!'
        except Exception as ex:
            err_msg = str(ex)

    return render_template('staff.html', err_msg=err_msg)

@app.route('/teacher-login', methods=['post', 'get'])
def teacher_login():
    err_msg = ''
    if request.method.__eq__('POST'):
        try:
            username = request.form.get('username')
            password = request.form.get('password')

            teacher = utils.check_user_login(username=username, password=password, role_id=3)

            if teacher:
                login_user(user=teacher)
                return redirect(url_for('teacher_login'))
            else:
                err_msg = 'Thông tin đăng nhập không chính xác!'
        except Exception as ex:
            err_msg = str(ex)

    return render_template('teacher.html', err_msg=err_msg)

@app.route('/api/add-students', methods=['post', 'get'])
@login_required
def add_student():
    try:
        name = request.json.get('name')
        sex = request.json.get('sex')
        birthday = request.json.get('birthday')
        address = request.json.get('address')
        phone = request.json.get('phone')
        email = request.json.get('email')
        amount_class = utils.get_amount_class()
        ma_lop = random.randint(1, amount_class)
        if name and sex and birthday and address and phone and email:
            utils.add_student(ten=name, gioi_tinh=sex, ngay_sinh=birthday, dia_chi=address,
                            sdt=phone, email=email, ma_lop=ma_lop)
    except:
        return jsonify({
            'status': 400,
            'err_msg': 'Lưu thông tin KHÔNG thành công!'
        })
    return jsonify({
        'status': 200,
        'succ_msg': 'Lưu thông tin thành công!'
    })

@app.route('/add_student')
def render_add_student_page():
    return render_template('add_students.html')

@app.route('/input-scores')
def render_input_scores_page():
    ma_lop = request.args.get('lop')
    ma_mh = request.args.get('mh')
    ma_hk = request.args.get('hk')
    ma_nh = request.args.get('nh')

    all_subjects = utils.get_all_subjects()
    all_classes = utils.get_all_classes()
    all_terms = utils.get_all_terms()
    all_semesters = utils.get_all_semesters()

    list = utils.get_students_by_class(ma_lop=ma_lop)

    class_name = utils.get_class_by_id(id=ma_lop)
    subject_name = utils.get_subject_by_id(id=ma_mh)
    term_name = utils.get_term_by_id(id=ma_hk)
    semester_name = utils.get_semester_by_id(id=ma_nh)


    return render_template('input_scores.html', list=list, ma_lop=ma_lop,
                           ma_mh=ma_mh, ma_hk=ma_hk, ma_nh=ma_nh,
                           subjects=all_subjects, classes=all_classes, terms=all_terms,
                           semesters=all_semesters, class_name=class_name, subject_name=subject_name,
                           term_name=term_name, semester_name=semester_name)

@app.route('/api/input-scores', methods=['post'])
def input_scores():
    ma_lop = request.json.get('maLop')
    mon_hoc = request.json.get('monHoc')
    hoc_ky = request.json.get('hocKy')
    nam_hoc = request.json.get('namHoc')
    diem = request.json.get('diem')

    obj = utils.get_students_by_class(ma_lop=ma_lop)

    try:
        if hoc_ky == 1:
            tmp = 0
            count = 0
            for i in obj:
                if count != 0:
                    tmp += 3

                utils.add_score(ma_hs=i[0], ma_mh=mon_hoc, ma_hk=hoc_ky, ma_nh=nam_hoc, ma_bai_kt=1, diem=diem[tmp])
                utils.add_score(ma_hs=i[0], ma_mh=mon_hoc, ma_hk=hoc_ky, ma_nh=nam_hoc, ma_bai_kt=2, diem=diem[tmp + 1])
                utils.add_score(ma_hs=i[0], ma_mh=mon_hoc, ma_hk=hoc_ky, ma_nh=nam_hoc, ma_bai_kt=3, diem=diem[tmp + 2])

                count += 1
        elif hoc_ky == 2:
            tmp2 = 0
            count2 = 0
            for i in obj:
                if count2 != 0:
                    tmp2 += 3

                utils.add_score(ma_hs=i[0], ma_mh=mon_hoc, ma_hk=hoc_ky, ma_nh=nam_hoc, ma_bai_kt=4, diem=diem[tmp2])
                utils.add_score(ma_hs=i[0], ma_mh=mon_hoc, ma_hk=hoc_ky, ma_nh=nam_hoc, ma_bai_kt=5, diem=diem[tmp2 + 1])
                utils.add_score(ma_hs=i[0], ma_mh=mon_hoc, ma_hk=hoc_ky, ma_nh=nam_hoc, ma_bai_kt=6, diem=diem[tmp2 + 2])

                count2 += 1
    except:
        return jsonify({
            'status': 404,
            'noti': 'Lỗi. Nhập điểm KHÔNG thành công'
        })
    return jsonify({
        'status': 200,
        'noti': 'Nhập điểm thành công'
    })

@app.route('/output-scores')
def render_output_scores_page():
    ma_lop = request.args.get('lop')
    ma_nh = request.args.get('nh')

    all_classes = utils.get_all_classes()
    all_semesters = utils.get_all_semesters()

    lop = utils.get_class_by_id(id=ma_lop)
    nam_hoc = utils.get_semester_by_id(id=ma_nh)

    list = utils.stat_average_score(ma_nh=ma_nh, ma_lop=ma_lop, ma_hk=1)
    list2 = utils.stat_average_score(ma_nh=ma_nh, ma_lop=ma_lop, ma_hk=2)

    return render_template('output_scores.html', classes=all_classes, semesters=all_semesters,
                           ma_nh=ma_nh, ma_lop=ma_lop, list2=list2,
                           lop=lop, nam_hoc=nam_hoc, list=list)

@app.route('/update-class')
def render_update_student_class_page():
    name = request.args.get('name')
    class_name = request.args.get('class_name')

    list = utils.students_gb_class(ten_hs=name, ten_lop=class_name)

    all_classes = utils.get_all_classes()
    amount = utils.amount_student_gb_class(ten_lop=class_name)

    return render_template('update_class.html', list=list, classes=all_classes,
                           class_name=class_name, amount=amount)

@app.route('/api/update-class', methods=['get', 'post'])
def update_student_class():
    try:
        id = request.json.get('id')
        class_id = request.json.get('classId')

        utils.update_student(id=id, ma_lop=class_id)
    except:
        return jsonify({
            'status': 400,
            'err_msg': 'Điều chỉnh KHÔNG thành công!'
        })
    return jsonify({
        'status': 200,
        'success_msg': 'Điều chỉnh thành công!'
    })

@app.route('/logout')
def logout():
    logout_user()

    return redirect(url_for('home'))

if __name__ == '__main__':
    app.run(debug=True)
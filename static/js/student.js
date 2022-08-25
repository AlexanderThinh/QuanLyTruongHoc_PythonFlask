
function handleAdminLogin() {
    const username = document.querySelector('#username')
    const password = document.querySelector('#pwd')
    const btnLogin = document.querySelector('#btnLogin')

    if (username.value != '' && password.value != '') {
      fetch('/admin/login-2', {
        method: 'post',
        body: JSON.stringify({
          'username': username.value,
          'password': password.value
        }),
        headers: {
          'Content-Type': 'application/json'
        }
      }).then(resolve => resolve.json()).then(data => {
        if (data.status == 404) {
          const noti = document.querySelector('.noti')
          noti.style.display = 'block'
          noti.innerText = data.err_msg
          username.focus()
          username.value = ''
          password.value = ''
        } else {
          btnLogin.click()
        }
      }).catch(err => {
        console.log(err)
      })
  }
}

function addStudent() {
    const name = document.querySelector('#name')
    const sex = document.querySelector('#sex')
    const birthday = document.querySelector('#birthday')
    const address = document.querySelector('#address')
    const phone = document.querySelector('#phone')
    const email = document.querySelector('#email')
    const radio1 = document.querySelector('#radio1')
    const radio2 = document.querySelector('#radio2')
    const noti = document.querySelector('.noti')
    var sexValue = 0

    if (name.value && birthday.value && address.value && phone.value && email.value) {
        if (radio1.checked) {
            sexValue = radio1.value
        } else if (radio2.checked) {
            sexValue = radio2.value
        }

        fetch('/api/add-students', {
            method: 'post',
            body: JSON.stringify({
                'name': name.value,
                'sex': sexValue,
                'birthday': birthday.value,
                'address': address.value,
                'phone': phone.value,
                'email': email.value
            }),
            headers: {
                'Content-Type': 'application/json'
            }
        })
        .then(resolve => resolve.json())
        .then(data => {
            if (data.status == 200) {
                noti.style.opacity = 1
                noti.innerText = data.succ_msg
                name.value = birthday.value = address.value = phone.value = email.value = ''
                radio1.checked = true
                name.focus()
            } else {
                noti.innerText = data.err_msg
            }
        }).catch(err => alert(err))
    }
}

function checkAge() {
    var currentYear = new Date().getFullYear()
    var birthday = document.querySelector('#birthday')
    var date = new Date(birthday.value)
    var age = currentYear - date.getFullYear()

    if (birthday.value) {
        if (age < 15) {
            alert('Học sinh chưa đủ tuổi nhập học theo quy định')
            birthday.value = ''
            birthday.focus()
        } else if (age > 20) {
            alert('Học sinh vượt quá độ tuổi nhập học theo quy định')
            birthday.value = ''
            birthday.focus()
        }
    }
}

function hireNoti() {
    const noti = document.querySelector('.noti')
    noti.style.opacity = 0
    noti.style.transition = 'all 1s'
}

function handleInputScore(ma_lop, ma_mh, ma_hk, ma_nh) {
    const diem = document.querySelectorAll('.diem')
    const inputScoreOption = document.querySelector('#inputScoreOption')
    var arrScore = [], isInputFull = true

    for(var i = 0; i < diem.length; i++) {
        if(diem[i].value == '') {
            alert('Vui lòng nhập đầy đủ điểm số!')
            diem[i].focus()
            isInputFull = false
            break;
        }
    }

    for(var i = 0; i < diem.length; i++) {
      arrScore.push(diem[i].value)
    }

    if (isInputFull) {
        fetch('/api/input-scores', {
            method: 'post',
            body: JSON.stringify({
                'maLop': ma_lop,
                'monHoc': ma_mh,
                'hocKy': ma_hk,
                'namHoc': ma_nh,
                'diem': arrScore
            }),
            headers: {
                'Content-Type': 'application/json'
            }
        })
        .then(resolve => resolve.json())
        .then(data => {
           if (data.status == 200) {
               alert(data.noti)
               inputScoreOption.click()
           } else {
               alert(data.noti)
               diem.forEach((item, index) => {
                    item.value = ''
               })
           }
        })
    }
}

function handleUpdateClass(studentId) {
    var name = document.querySelector('#tenHocSinh')
    var studentIdShow = document.querySelector('#maHocSinh')
    var currentClass = document.querySelector('#currentClass')
    var className = document.querySelector('#lopHoc')

    var studentItem = document.querySelector('.row-'+studentId)
    var nameSelected = studentItem.querySelector('.student-name')
    var classSelected = studentItem.querySelector('.class-name')

    var btnSave = document.querySelector('#btn-save')
    var myModal = document.querySelector('#myModal')

    name.innerText = nameSelected.innerText
    currentClass.innerText = classSelected.innerText
    studentIdShow.innerText = studentId
    myModal.classList.add('active')

    btnSave.onclick = function() {
        if (name.innerText) {
            fetch('/api/update-class', {
                method: 'post',
                body: JSON.stringify({
                    'id': studentId,
                    'classId': className.value
                }),
                headers: {
                    'Content-Type': 'application/json'
                }
            })
            .then(response => response.json())
            .then(data => {
                if (data.status == 200) {
                    alert(data.success_msg)
                    myModal.classList.remove('active')
                    location.reload()
                } else {
                    alert(data.err_msg)
                }
            })
            .catch(err => console.log(err))
        }
    }
}


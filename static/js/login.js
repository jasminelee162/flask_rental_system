$(document).ready(function () {

    // 注册
    $('#registe-btn').on('click', function () {
        $('#registeform').bootstrapValidator({
            message: 'This value is not valid',
            fields: {
                username: {
                    message: 'The username is not valid',
                    validators: {
                        notEmpty: {
                            message: '用户名不能为空'
                        },
                        stringLength: {
                            min: 6,
                            max: 30,
                            message: '用户名长度必须在6到30位之间'
                        },
                        regexp: {
                            regexp: /^[a-zA-Z0-9_\.]+$/,
                            message: '用户名只能包含大写、小写、数字和下划线'
                        },
                        different: {
                            field: 'password',
                            message: '用户名不能与密码相同'
                        }
                    }
                },
                email: {
                    validators: {
                        notEmpty: {
                            message: '邮箱不能为空'
                        },
                        emailAddress: {
                            message: '无效的邮箱地址'
                        }
                    }
                },
                password: {
                    validators: {
                        notEmpty: {
                            message: '密码不能为空'
                        },
                        identical: {
                            field: 'confirmPassword',
                            message: '与确认密码不一致'
                        },
                        different: {
                            field: 'username',
                            message: '密码不能与用户名相同'
                        }
                    }
                },
                confirmPassword: {
                    validators: {
                        notEmpty: {
                            message: '确认密码不能为空'
                        },
                        identical: {
                            field: 'password',
                            message: '与密码不一致'
                        },
                        different: {
                            field: 'username',
                            message: '确认密码不能与用户名相同'
                        }
                    }
                }
            }
        });
        var validator = $('#registeform').data("bootstrapValidator"); //获取validator对象
        validator.validate(); //手动触发验证
        if (validator.isValid()) { //通过验证
            $.ajax({
                type: 'post',
                url: '/register',
                data: $('#registeform').serialize(),
                dataType: 'json',
                success: function (result) {
                    if (result['valid'] == '0') {
                        alert(result['msg'])
                        var validatorObj = $("#registeform").data('bootstrapValidator');
                        if (validatorObj) {
                            $("#registeform").data('bootstrapValidator').destroy(); //或者 validatorObj.destroy(); 都可以，销毁验证
                            $('#registeform').data('bootstrapValidator', null);
                        }
                    } else {
                        window.location.href = "/user/" + result['msg'];
                    }
                },

            })
        }
    });

    // 登录表单验证器
    $('#loginForm').bootstrapValidator({
        message: 'This value is not valid',
        feedbackIcons: {
            valid: 'glyphicon glyphicon-ok',
            invalid: 'glyphicon glyphicon-remove',
            validating: 'glyphicon glyphicon-refresh'
        },
        fields: {
            username: {
                message: 'The username is not valid',
                validators: {
                    notEmpty: {
                        message: '用户名不能为空'
                    },
                    stringLength: {
                        min: 6,
                        max: 30,
                        message: '用户名长度必须在6到30位之间'
                    },
                    regexp: {
                        regexp: /^[a-zA-Z0-9_\.]+$/,
                        message: '用户名只能包含大写、小写、数字和下划线'
                    }
                }
            },
            password: {
                validators: {
                    notEmpty: {
                        message: '密码不能为空'
                    },
                    different: {
                        field: 'username',
                        message: '密码不能与用户名相同'
                    }
                }
            },
            captcha: {
                validators: {
                    notEmpty: {
                        message: '请输入验证码'
                    }
                }
            }
        }
    });

    // 刷新验证码
    function refreshCaptcha() {
        var captchaImg = document.getElementById('captchaImg');
        if (captchaImg) {
            captchaImg.src = '/captcha?' + new Date().getTime();
        }
    }

    // 点击验证码图片时刷新
    $('#captchaImg').click(function() {
        refreshCaptcha();
    });

    // 处理登录按钮点击
    $('#login-btn').click(function(e) {
        e.preventDefault();
        var $form = $('#loginForm');
        var validator = $form.data('bootstrapValidator');
        
        validator.validate();
        if (validator.isValid()) {
            $.ajax({
                url: $form.attr('action'),
                type: 'POST',
                data: $form.serialize(),
                dataType: 'json',
                success: function(response) {
                    if (response.valid === '0') {
                        // 登录失败
                        alert(response.msg);
                        refreshCaptcha();
                        validator.resetForm();
                    } else {
                        // 登录成功，根据用户类型跳转
                        if (response.is_landlord === '1') {
                            window.location.href = '/landlord/' + response.msg;
                        } else {
                            window.location.href = '/user/' + response.msg;
                        }
                    }
                },
                error: function() {
                    alert('登录请求失败，请稍后重试');
                    refreshCaptcha();
                }
            });
        }
    });

    // 退出登录
    $("#logoutBtn").click(function(e) {
        e.preventDefault();
        if (confirm('确定要退出登录吗？')) {
            $.post('/logout', function(response) {
                if (response.valid === '1') {
                    window.location.href = '/';
                } else {
                    alert('退出登录失败，请稍后重试');
                }
            });
        }
    });
});
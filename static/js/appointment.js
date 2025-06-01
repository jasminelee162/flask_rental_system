// 预约功能
$(document).ready(function() {
    // 初始化预约按钮状态
    updateAppointmentButton();

    // 点击预约按钮
    $('#btn-appointment').click(function() {
        const isAppointed = $(this).hasClass('appointed');
        const houseId = $(this).data('house-id');

        if(isAppointed) {
            // 取消预约
            if(confirm('确定要取消预约吗？')) {
                cancelAppointment(houseId);
            }
        } else {
            // 打开预约模态框
            $('#appointmentModal').modal('show');
        }
    });

    // 确认预约
    $('#confirmAppointment').click(function() {
        const houseId = $('#btn-appointment').data('house-id');
        const time = $('#appointmentTime').val();
        const note = $('#appointmentNote').val();

        if(!time) {
            alert('请选择预约时间');
            return;
        }

        createAppointment(houseId, time, note);
    });
});

// 创建预约
function createAppointment(houseId, time, note) {
    $.ajax({
        url: '/appointment/create',
        type: 'POST',
        data: {
            house_id: houseId,
            appointment_time: time,
            note: note || ''
        },
        success: function(response) {
            if(response.success) {
                $('#appointmentModal').modal('hide');
                updateAppointmentButton(true);
                alert('预约成功！');
            } else {
                alert(response.message || '预约失败');
            }
        },
        error: function() {
            alert('网络错误，请重试');
        }
    });
}

// 取消预约
function cancelAppointment(houseId) {
    $.ajax({
        url: '/appointment/cancel',
        type: 'POST',
        data: { house_id: houseId },
        success: function(response) {
            if(response.success) {
                updateAppointmentButton(false);
                alert('已取消预约');
            } else {
                alert(response.message || '取消预约失败');
            }
        },
        error: function() {
            alert('网络错误，请重试');
        }
    });
}

// 更新预约按钮状态
function updateAppointmentButton(isAppointed) {
    const $btn = $('#btn-appointment');
    if(isAppointed !== undefined) {
        $btn.toggleClass('appointed', isAppointed);
        $btn.find('i').text(isAppointed ? ' 已预约' : ' 预约看房');
    } else {
        // 从服务器获取当前状态
        const houseId = $btn.data('house-id');
        $.get('/appointment/status?house_id=' + houseId, function(response) {
            if(response.success) {
                $btn.toggleClass('appointed', response.is_appointed);
                $btn.find('i').text(response.is_appointed ? ' 已预约' : ' 预约看房');
            }
        });
    }
}
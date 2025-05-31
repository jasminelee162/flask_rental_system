console.log("chat.js loaded");

$(document).ready(function () {
  const userId = getCookie('userId'); // 当前用户ID
  let currentTargetId = null; // 当前聊天对象ID
  let userIdToName = {}; // 用户ID到名字的映射

  // 点击消息图标时加载联系人列表并显示
  $('#msg-icon').on('click', function (e) {
    console.log("点击了消息图标");
    e.preventDefault();
    loadChatUserList();
    const dropdown = $('#chat-dropdown');
    if (dropdown.css('display') === 'none') {
      dropdown.css('display', 'flex');
    } else {
      dropdown.css('display', 'none');
    }
  });

  // 加载联系人列表（支持回调），新增参数 landlordId
  function loadChatUserList(callback, landlordId) {
    const params = landlordId ? { landlord_id: landlordId } : {};
    $.get('/chat/list', params, function (data) {
      console.log("data", data);
      const userList = $('#chat-user-list');
      userList.empty();
      userIdToName = {};
      data.forEach(user => {
        userIdToName[user.id] = user.name;
        userList.append(`<li class="chat-user" data-id="${user.id}">${user.name}</li>`);
      });
      if (callback) callback();
    });
  }


  // 点击联系人，加载聊天记录
  $(document).on('click', '.chat-user', function () {
    const targetName = $(this).text();
    currentTargetId = $(this).attr('data-id');
    $('#chat-user-name').text(targetName);

    $.get('/chat/messages', { target_id: currentTargetId }, function (data) {
      const msgBox = $('#chat-messages');
      msgBox.empty();
      data.forEach(msg => {
        const isSelf = (msg.sender === parseInt(userId));
        const bubbleClass = isSelf ? 'my-message' : 'other-message';
        const rowClass = isSelf ? 'self' : '';
        msgBox.append(`
          <div class="message-row ${rowClass}">
            <div class="${bubbleClass}">
              ${msg.message}
            </div>
          </div>
        `);
      });
      msgBox.scrollTop(msgBox[0].scrollHeight);
    });
  });

  // 点击发送按钮
  $('#send-message').click(function () {
    const content = $('#chat-input-text').val();
    if (!content.trim() || !currentTargetId) return;
    $.post('/chat/send', {
      receiver_id: currentTargetId,
      message: content
    }, function () {
      const bubble = `
        <div class="message-row self">
          <div class="my-message">${escapeHtml(content)}</div>
        </div>
      `;
      $('#chat-messages').append(bubble);
      $('#chat-input-text').val('');
      const msgBox = $('#chat-messages');
      msgBox.scrollTop(msgBox[0].scrollHeight);
    });
  });

  // 防止 XSS 注入
  function escapeHtml(text) {
    return $('<div>').text(text).html();
  }

  // 点击空白区域关闭联系人列表
  $(document).on('click', function (e) {
    if (!$(e.target).closest('#msg-icon').length && !$(e.target).closest('#chat-dropdown').length) {
      $('#chat-dropdown').hide();
    }
  });

  // 获取 Cookie
  function getCookie(name) {
    const value = `; ${document.cookie}`;
    const parts = value.split(`; ${name}=`);
    if (parts.length === 2) return parts.pop().split(';').shift();
  }

  // ✅ 点击“联系房东”图标打开聊天框并自动跳转到房东会话
  $(document).on('click', '#btn-contact-landlord', function () {
    console.log("点击了“联系房东”图标");

    const landlordId = $(this).data('id');
    console.log("landlordId", landlordId);

    // ✅ 模拟点击消息图标，自动弹出聊天框
    $('#msg-icon').click();

    // ✅ 延迟，等待联系人列表渲染完毕后再点击房东
    setTimeout(function () {
      loadChatUserList(function () {
        console.log("加载联系人列表后自动进入房东聊天窗口");

        const landlordLi = $(`.chat-user[data-id="${landlordId}"]`);
        if (landlordLi.length > 0) {
          console.log('成功找到房东联系人，自动点击进入聊天', landlordId);
            $('#chat-dropdown').css('display', 'flex'); // 👈 显式展开
          landlordLi.click();
        } else {
          console.warn('未找到房东联系人，请确保其存在于聊天列表中');
        }
      }, landlordId);
    }, 200);
  });



});
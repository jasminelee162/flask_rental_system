console.log("chat.js loaded");

$(document).ready(function () {
  const landlordId = getCookie('landlordId'); // 当前商家ID
  let currentTargetId = null; // 当前聊天对象（用户）ID
  let userIdToName = {}; // 用户ID到名字的映射

  // 点击消息图标时加载联系人列表并显示
  $('#msg-icon').on('click', function (e) {
    console.log("点击了消息图标");
    e.preventDefault();
    loadChatUserList(landlordId, function () {
      $('#chat-dropdown').css('display', 'flex');
    });
  });

  // 加载联系人列表，参数 landlordId 必传，回调可选
  function loadChatUserList(landlordId, callback) {
    if (!landlordId) {
      console.warn('缺少商家ID，无法加载联系人列表');
      return;
    }
    $.get('/chat/list', { landlord_id: landlordId }, function (data) {
      console.log("联系人列表数据:", data);
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

  // 点击联系人，加载聊天记录（商家与用户的聊天）
  $(document).on('click', '.chat-user', function () {
    const targetName = $(this).text();
    currentTargetId = $(this).attr('data-id'); // 用户ID
    $('#chat-user-name').text(targetName);

    $.get('/chat/messages', { target_id: currentTargetId }, function (data) {
      const msgBox = $('#chat-messages');
      msgBox.empty();
      data.forEach(msg => {
        // 判断消息是否由当前商家发送
        const isSelf = (msg.sender === parseInt(landlordId));
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

  // 点击发送按钮，商家给用户发消息
  $('#send-message').click(function () {
    const content = $('#chat-input-text').val();
    if (!content.trim() || !currentTargetId) return;

    $.post('/chat/send', {
      receiver_id: currentTargetId, // 用户ID
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

  // 商家端专用：点击聊天导航加载聊天部分（保留原功能）
  $("#chatNav").on("click", function (e) {
    e.preventDefault(); // 阻止默认跳转
    let url = $(this).attr("href");
    $.get(url, function (data) {
      $("main.container").html(data);
    });
  });

});

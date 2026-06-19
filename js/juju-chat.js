// Juju 🤖 - Chat Widget
(function() {
  if (document.getElementById('juju-chat-widget')) return;

  const styles = document.createElement('style');
  styles.textContent = `
    #juju-chat-widget {
      position: fixed; bottom: 20px; right: 20px; z-index: 9999;
      font-family: 'Segoe UI', system-ui, -apple-system, sans-serif;
    }
    #juju-chat-btn {
      width: 60px; height: 60px; border-radius: 50%;
      background: linear-gradient(135deg, #C79A2E, #a67c00);
      color: white; border: none; cursor: pointer;
      font-size: 28px; box-shadow: 0 4px 20px rgba(199,154,46,0.4);
      transition: all 0.3s ease; display: flex; align-items: center; justify-content: center;
    }
    #juju-chat-btn:hover { transform: scale(1.1); box-shadow: 0 6px 25px rgba(199,154,46,0.6); }
    #juju-chat-panel {
      position: fixed; bottom: 90px; right: 20px; width: 380px; height: 520px;
      background: #0D1B2A; border-radius: 16px; box-shadow: 0 10px 40px rgba(0,0,0,0.4);
      display: none; flex-direction: column; overflow: hidden;
      border: 1px solid rgba(199,154,46,0.3);
    }
    #juju-chat-panel.open { display: flex; }
    #juju-chat-header {
      background: linear-gradient(135deg, #0D1B2A, #142D4C); padding: 16px 20px;
      border-bottom: 1px solid rgba(199,154,46,0.2); display: flex;
      align-items: center; gap: 12px;
    }
    #juju-chat-header h3 { margin: 0; color: #C79A2E; font-size: 16px; flex: 1; }
    #juju-chat-header .close-btn {
      background: none; border: none; color: rgba(255,255,255,0.6);
      cursor: pointer; font-size: 20px; padding: 0 4px;
    }
    #juju-chat-header .close-btn:hover { color: white; }
    #juju-chat-avatar {
      width: 36px; height: 36px; border-radius: 50%;
      background: linear-gradient(135deg, #C79A2E, #a67c00); display: flex;
      align-items: center; justify-content: center; font-size: 20px;
    }
    #juju-chat-messages {
      flex: 1; overflow-y: auto; padding: 16px; display: flex;
      flex-direction: column; gap: 10px;
    }
    .juju-msg {
      max-width: 85%; padding: 10px 14px; border-radius: 12px;
      font-size: 14px; line-height: 1.5; word-wrap: break-word;
    }
    .juju-msg.bot {
      background: #142D4C; color: #e0e0e0; align-self: flex-start;
      border-bottom-left-radius: 4px;
    }
    .juju-msg.user {
      background: #C79A2E; color: #0D1B2A; align-self: flex-end;
      border-bottom-right-radius: 4px; font-weight: 500;
    }
    .juju-msg.loading {
      background: #142D4C; color: #888; align-self: flex-start;
      font-style: italic; display: flex; gap: 4px; align-items: center;
    }
    .juju-msg.loading::after {
      content: ''; display: inline-block; width: 8px; height: 8px;
      background: #C79A2E; border-radius: 50%; animation: juju-bounce 1s infinite;
    }
    @keyframes juju-bounce { 0%,100% { opacity: 0.3; transform: scale(0.8); } 50% { opacity: 1; transform: scale(1.2); } }
    #juju-chat-input {
      padding: 12px 16px; border-top: 1px solid rgba(199,154,46,0.2);
      display: flex; gap: 8px; background: #0a1628;
    }
    #juju-chat-input input {
      flex: 1; padding: 10px 14px; border-radius: 25px; border: 1px solid rgba(199,154,46,0.3);
      background: #142D4C; color: white; font-size: 13px; outline: none;
    }
    #juju-chat-input input:focus { border-color: #C79A2E; }
    #juju-chat-input input::placeholder { color: rgba(255,255,255,0.4); }
    #juju-chat-input button {
      background: linear-gradient(135deg, #C79A2E, #a67c00); color: #0D1B2A;
      border: none; border-radius: 50%; width: 40px; height: 40px;
      cursor: pointer; font-size: 18px; display: flex; align-items: center;
      justify-content: center; transition: all 0.2s;
    }
    #juju-chat-input button:hover { transform: scale(1.05); }
    #juju-chat-input button:disabled { opacity: 0.5; cursor: not-allowed; }
  `;
  document.head.appendChild(styles);

  // Widget HTML
  const widget = document.createElement('div');
  widget.id = 'juju-chat-widget';
  widget.innerHTML = `
    <div id="juju-chat-panel">
      <div id="juju-chat-header">
        <div id="juju-chat-avatar">🤖</div>
        <h3>Juju — COO</h3>
        <button class="close-btn" onclick="toggleJujuChat()">✕</button>
      </div>
      <div id="juju-chat-messages">
        <div class="juju-msg bot">Olá! 👋 Sou a Juju, COO do Grupo Zadok. Como posso ajudar?</div>
      </div>
      <div id="juju-chat-input">
        <input id="juju-chat-input-field" type="text" placeholder="Digite sua mensagem..." 
               onkeypress="if(event.key==='Enter') sendJujuMessage()">
        <button id="juju-send-btn" onclick="sendJujuMessage()">➤</button>
      </div>
    </div>
    <button id="juju-chat-btn" onclick="toggleJujuChat()">🤖</button>
  `;
  document.body.appendChild(widget);

  window.jujuChatOpen = false;
  window.toggleJujuChat = function() {
    const panel = document.getElementById('juju-chat-panel');
    const btn = document.getElementById('juju-chat-btn');
    window.jujuChatOpen = !window.jujuChatOpen;
    panel.classList.toggle('open', window.jujuChatOpen);
    btn.style.display = window.jujuChatOpen ? 'none' : 'flex';
    if (window.jujuChatOpen) {
      document.getElementById('juju-chat-input-field').focus();
    }
  };

  window.sendJujuMessage = async function() {
    const input = document.getElementById('juju-chat-input-field');
    const btn = document.getElementById('juju-send-btn');
    const msg = input.value.trim();
    if (!msg) return;

    const messages = document.getElementById('juju-chat-messages');
    
    // Adicionar mensagem do usuário
    messages.innerHTML += `<div class="juju-msg user">${escapeHtml(msg)}</div>`;
    messages.innerHTML += `<div class="juju-msg loading">Pensando</div>`;
    messages.scrollTop = messages.scrollHeight;
    
    input.value = '';
    btn.disabled = true;

    try {
      const response = await fetch('/api/juju/chat', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ message: msg })
      });
      
      const data = await response.json();
      
      // Remover loading e adicionar resposta
      const loading = messages.querySelector('.juju-msg.loading');
      if (loading) loading.remove();
      
      messages.innerHTML += `<div class="juju-msg bot">${escapeHtml(data.reply)}</div>`;
      messages.scrollTop = messages.scrollHeight;
    } catch (err) {
      const loading = messages.querySelector('.juju-msg.loading');
      if (loading) loading.remove();
      messages.innerHTML += `<div class="juju-msg bot">❌ Erro ao conectar. Tente novamente.</div>`;
    } finally {
      btn.disabled = false;
    }
  };

  function escapeHtml(str) {
    const div = document.createElement('div');
    div.textContent = str;
    return div.innerHTML;
  }
})();

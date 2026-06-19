// Configuração do LMS Lumethos - API Bridge Local
const API_CONFIG = {
  // Substitui o Supabase - usa backend local
  BASE_URL: window.location.origin + '/api',
  
  // Função de login
  async login(email, password) {
    const res = await fetch(`${this.BASE_URL}/auth/login`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ email, password })
    });
    const data = await res.json();
    if (!res.ok) throw new Error(data.error || 'Erro ao fazer login');
    localStorage.setItem('lms_token', data.token);
    localStorage.setItem('lms_user', JSON.stringify(data.user));
    return data;
  },

  getToken() { return localStorage.getItem('lms_token'); },
  getUser() { 
    try { return JSON.parse(localStorage.getItem('lms_user')); }
    catch { return null; }
  },
  logout() { 
    localStorage.removeItem('lms_token');
    localStorage.removeItem('lms_user');
  },
  isAuthenticated() { return !!this.getToken(); },

  async fetch(endpoint, options = {}) {
    const token = this.getToken();
    const headers = { 'Content-Type': 'application/json', ...options.headers };
    if (token) headers['Authorization'] = `Bearer ${token}`;
    
    const res = await fetch(`${this.BASE_URL}${endpoint}`, { ...options, headers });
    const data = await res.json();
    if (!res.ok) throw new Error(data.error || `Erro ${res.status}`);
    return data;
  },

  // CRUD
  getCursos() { return this.fetch('/cursos'); },
  getModulos(cursoId) { return this.fetch(`/modulos/${cursoId}`); },
  getAulas(moduloId) { return this.fetch(`/aulas/${moduloId}`); },
  getUsuarios() { return this.fetch('/usuarios'); },
  getEntregas() { return this.fetch('/entregas'); },
  getProgresso(cursoId) { return this.fetch(`/progresso/${cursoId}`); },
  
  criarCurso(dados) { return this.fetch('/cursos', { method: 'POST', body: JSON.stringify(dados) }); },
  criarModulo(dados) { return this.fetch('/modulos', { method: 'POST', body: JSON.stringify(dados) }); },
  criarAula(dados) { return this.fetch('/aulas', { method: 'POST', body: JSON.stringify(dados) }); },
  criarUsuario(dados) { return this.fetch('/usuarios', { method: 'POST', body: JSON.stringify(dados) }); },
  
  atualizarCurso(id, dados) { return this.fetch(`/cursos/${id}`, { method: 'PUT', body: JSON.stringify(dados) }); },
  atualizarModulo(id, dados) { return this.fetch(`/modulos/${id}`, { method: 'PUT', body: JSON.stringify(dados) }); },
  atualizarAula(id, dados) { return this.fetch(`/aulas/${id}`, { method: 'PUT', body: JSON.stringify(dados) }); },
  
  deletarCurso(id) { return this.fetch(`/cursos/${id}`, { method: 'DELETE' }); },
  deletarModulo(id) { return this.fetch(`/modulos/${id}`, { method: 'DELETE' }); },
  deletarAula(id) { return this.fetch(`/aulas/${id}`, { method: 'DELETE' }); },
  deletarUsuario(id) { return this.fetch(`/usuarios/${id}`, { method: 'DELETE' }); },

  matricular(alunoId, cursoId) { return this.fetch('/matriculas', { method: 'POST', body: JSON.stringify({ aluno_id: alunoId, curso_id: cursoId }) }); },
  desmatricular(id) { return this.fetch(`/matriculas/${id}`, { method: 'DELETE' }); },

  concluirAula(aulaId) { return this.fetch('/aulas/concluir', { method: 'POST', body: JSON.stringify({ aula_id: aulaId }) }); },
  
  enviarEntrega(moduloId, conteudo) { return this.fetch('/entregas', { method: 'POST', body: JSON.stringify({ modulo_id: moduloId, conteudo }) }); },
  corrigirEntrega(id, nota, feedback) { return this.fetch(`/entregas/corrigir/${id}`, { method: 'POST', body: JSON.stringify({ nota, feedback }) }); },

  // Juju IA
  async chatJuju(message) {
    const res = await fetch(`${this.BASE_URL}/juju/chat`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ message })
    });
    const data = await res.json();
    if (!res.ok) throw new Error(data.error || 'Erro');
    return data.reply;
  }
};

// Tornar global
window.API = API_CONFIG;

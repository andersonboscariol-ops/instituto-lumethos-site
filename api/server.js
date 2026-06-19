import express from 'express';
import cors from 'cors';
import path from 'path';
import { fileURLToPath } from 'url';
import fs from 'fs';

const __dirname = path.dirname(fileURLToPath(import.meta.url));
const PORT = process.env.LMS_PORT || 3232;

const app = express();
app.use(cors());
app.use(express.json({ limit: '50mb' }));

// ============================================
// BANCO DE DADOS LOCAL (arquivos JSON)
// ============================================
const DATA_DIR = path.join(__dirname, 'data');
fs.mkdirSync(DATA_DIR, { recursive: true });

// Tabelas
const TABLES = ['usuarios', 'cursos', 'modulos', 'aulas', 'matriculas', 'aulas_concluidas', 'entregas', 'chat_historico'];

// Inicializar tabelas
TABLES.forEach(table => {
  const file = path.join(DATA_DIR, `${table}.json`);
  if (!fs.existsSync(file)) {
    fs.writeFileSync(file, '[]');
  }
});

function readTable(table) {
  try {
    const data = fs.readFileSync(path.join(DATA_DIR, `${table}.json`), 'utf-8');
    return JSON.parse(data);
  } catch {
    return [];
  }
}

function writeTable(table, data) {
  fs.writeFileSync(path.join(DATA_DIR, `${table}.json`), JSON.stringify(data, null, 2));
}

// Utilitário UUID simples
function uuid() {
  return 'xxxxxxxx-xxxx-4xxx-yxxx-xxxxxxxxxxxx'.replace(/[xy]/g, c => {
    const r = Math.random() * 16 | 0;
    return (c === 'x' ? r : (r & 0x3 | 0x8)).toString(16);
  });
}

// ============================================
// SEMENTE: Admin padrão
// ============================================
const usuarios = readTable('usuarios');
const adminExists = usuarios.find(u => u.email === 'anderson.boscariol@gmail.com');
if (!adminExists) {
  usuarios.push({
    id: uuid(),
    nome: 'Anderson Boscariol',
    email: 'anderson.boscariol@gmail.com',
    senha: 'b5a6148e53757d612e2acd8b7db0d1a1', // MD5 de @Danilailav7
    papel: 'admin',
    created_at: new Date().toISOString()
  });
  writeTable('usuarios', usuarios);
  console.log('✅ Admin padrão criado');
}

// ============================================
// ROTAS DE AUTENTICAÇÃO
// ============================================

// POST /api/auth/login
app.post('/api/auth/login', (req, res) => {
  const { email, password } = req.body;
  const user = usuarios.find(u => u.email === email);
  
  if (!user) {
    return res.status(401).json({ error: 'Email ou senha incorretos' });
  }

  // Hash simples (MD5 simulado para compatibilidade)
  const hash = require('crypto').createHash('md5').update(password).digest('hex');
  
  if (user.senha !== hash) {
    return res.status(401).json({ error: 'Email ou senha incorretos' });
  }

  const token = Buffer.from(JSON.stringify({
    id: user.id,
    email: user.email,
    papel: user.papel,
    nome: user.nome,
    iat: Date.now(),
    exp: Date.now() + 30 * 24 * 60 * 60 * 1000
  })).toString('base64');

  res.json({
    token,
    user: {
      id: user.id,
      email: user.email,
      nome: user.nome,
      papel: user.papel
    }
  });
});

// Middleware de autenticação
function authMiddleware(req, res, next) {
  const authHeader = req.headers.authorization;
  
  if (!authHeader || !authHeader.startsWith('Bearer ')) {
    return res.status(401).json({ error: 'Token não fornecido' });
  }

  try {
    const token = authHeader.split(' ')[1];
    const payload = JSON.parse(Buffer.from(token, 'base64').toString('utf-8'));
    
    if (payload.exp < Date.now()) {
      return res.status(401).json({ error: 'Token expirado' });
    }

    req.user = payload;
    next();
  } catch {
    return res.status(401).json({ error: 'Token inválido' });
  }
}

// Middleware admin only
function adminMiddleware(req, res, next) {
  if (req.user.papel !== 'admin') {
    return res.status(403).json({ error: 'Acesso restrito a administradores' });
  }
  next();
}

// ============================================
// ROTAS DE USUÁRIOS (admin)
// ============================================

app.get('/api/usuarios', authMiddleware, adminMiddleware, (req, res) => {
  const users = readTable('usuarios');
  const safeUsers = users.map(u => ({
    id: u.id,
    nome: u.nome,
    email: u.email,
    papel: u.papel,
    created_at: u.created_at
  }));
  res.json(safeUsers);
});

app.post('/api/usuarios', authMiddleware, adminMiddleware, (req, res) => {
  const { nome, email, senha, papel, matricula } = req.body;
  const usuarios = readTable('usuarios');
  
  if (usuarios.find(u => u.email === email)) {
    return res.status(409).json({ error: 'Email já cadastrado' });
  }

  const hash = require('crypto').createHash('md5').update(senha).digest('hex');
  const user = {
    id: uuid(),
    nome,
    email,
    senha: hash,
    papel: papel || 'aluno',
    matricula: matricula || `LUM-${new Date().getFullYear()}-${String(usuarios.length + 1).padStart(4, '0')}`,
    created_at: new Date().toISOString()
  };

  usuarios.push(user);
  writeTable('usuarios', usuarios);
  
  res.json({ success: true, user: { id: user.id, nome: user.nome, email: user.email, papel: user.papel, matricula: user.matricula } });
});

app.delete('/api/usuarios/:id', authMiddleware, adminMiddleware, (req, res) => {
  let usuarios = readTable('usuarios');
  usuarios = usuarios.filter(u => u.id !== req.params.id);
  writeTable('usuarios', usuarios);
  res.json({ success: true });
});

// ============================================
// ROTAS DE CURSOS
// ============================================

app.get('/api/cursos', authMiddleware, (req, res) => {
  const cursos = readTable('cursos');
  
  // Se for aluno, filtrar apenas cursos matriculados
  if (req.user.papel === 'aluno') {
    const matriculas = readTable('matriculas');
    const meusCursos = matriculas.filter(m => m.aluno_id === req.user.id);
    const cursosMatriculados = cursos.filter(c => meusCursos.some(m => m.curso_id === c.id));
    return res.json(cursosMatriculados);
  }
  
  res.json(cursos);
});

app.post('/api/cursos', authMiddleware, adminMiddleware, (req, res) => {
  const { titulo, descricao, imagem, cor, slug } = req.body;
  const cursos = readTable('cursos');
  
  const curso = {
    id: uuid(),
    titulo,
    descricao: descricao || '',
    imagem: imagem || '',
    cor: cor || '#0D1B2A',
    slug: slug || titulo.toLowerCase().replace(/\s+/g, '-').replace(/[^a-z0-9-]/g, ''),
    created_at: new Date().toISOString()
  };

  cursos.push(curso);
  writeTable('cursos', cursos);
  res.json({ success: true, curso });
});

app.put('/api/cursos/:id', authMiddleware, adminMiddleware, (req, res) => {
  const cursos = readTable('cursos');
  const index = cursos.findIndex(c => c.id === req.params.id);
  
  if (index === -1) return res.status(404).json({ error: 'Curso não encontrado' });
  
  cursos[index] = { ...cursos[index], ...req.body };
  writeTable('cursos', cursos);
  res.json({ success: true, curso: cursos[index] });
});

app.delete('/api/cursos/:id', authMiddleware, adminMiddleware, (req, res) => {
  let cursos = readTable('cursos');
  cursos = cursos.filter(c => c.id !== req.params.id);
  writeTable('cursos', cursos);
  
  // Remover módulos e aulas do curso
  let modulos = readTable('modulos');
  modulos = modulos.filter(m => m.curso_id !== req.params.id);
  writeTable('modulos', modulos);
  
  let aulas = readTable('aulas');
  aulas = aulas.filter(a => !modulos.some(m => m.id === a.modulo_id));
  writeTable('aulas', aulas);
  
  res.json({ success: true });
});

// ============================================
// ROTAS DE MÓDULOS
// ============================================

app.get('/api/modulos/:cursoId', authMiddleware, (req, res) => {
  const modulos = readTable('modulos').filter(m => m.curso_id === req.params.id);
  const sorted = modulos.sort((a, b) => (a.ordem || 0) - (b.ordem || 0));
  res.json(sorted);
});

app.post('/api/modulos', authMiddleware, adminMiddleware, (req, res) => {
  const { curso_id, titulo, descricao, ordem } = req.body;
  const modulos = readTable('modulos');
  
  const modulo = {
    id: uuid(),
    curso_id,
    titulo,
    descricao: descricao || '',
    ordem: ordem || modulos.filter(m => m.curso_id === curso_id).length + 1,
    created_at: new Date().toISOString()
  };

  modulos.push(modulo);
  writeTable('modulos', modulos);
  res.json({ success: true, modulo });
});

app.put('/api/modulos/:id', authMiddleware, adminMiddleware, (req, res) => {
  const modulos = readTable('modulos');
  const index = modulos.findIndex(m => m.id === req.params.id);
  if (index === -1) return res.status(404).json({ error: 'Módulo não encontrado' });
  modulos[index] = { ...modulos[index], ...req.body };
  writeTable('modulos', modulos);
  res.json({ success: true, modulo: modulos[index] });
});

app.delete('/api/modulos/:id', authMiddleware, adminMiddleware, (req, res) => {
  let modulos = readTable('modulos');
  modulos = modulos.filter(m => m.id !== req.params.id);
  writeTable('modulos', modulos);
  
  let aulas = readTable('aulas');
  aulas = aulas.filter(a => a.modulo_id !== req.params.id);
  writeTable('aulas', aulas);
  
  res.json({ success: true });
});

// ============================================
// ROTAS DE AULAS
// ============================================

app.get('/api/aulas/:moduloId', authMiddleware, (req, res) => {
  const aulas = readTable('aulas').filter(a => a.modulo_id === req.params.id);
  const sorted = aulas.sort((a, b) => (a.ordem || 0) - (b.ordem || 0));
  
  // Marcar quais aulas estão concluídas pelo aluno
  if (req.user.papel === 'aluno') {
    const concluidas = readTable('aulas_concluidas').filter(ac => ac.aluno_id === req.user.id);
    const result = sorted.map(a => ({
      ...a,
      concluida: concluidas.some(c => c.aula_id === a.id)
    }));
    return res.json(result);
  }
  
  res.json(sorted);
});

app.post('/api/aulas', authMiddleware, adminMiddleware, (req, res) => {
  const { modulo_id, titulo, conteudo, tipo, video_url, ordem } = req.body;
  const aulas = readTable('aulas');
  
  const aula = {
    id: uuid(),
    modulo_id,
    titulo,
    conteudo: conteudo || '',
    tipo: tipo || 'texto',
    video_url: video_url || '',
    ordem: ordem || aulas.filter(a => a.modulo_id === modulo_id).length + 1,
    created_at: new Date().toISOString()
  };

  aulas.push(aula);
  writeTable('aulas', aulas);
  res.json({ success: true, aula });
});

app.put('/api/aulas/:id', authMiddleware, adminMiddleware, (req, res) => {
  const aulas = readTable('aulas');
  const index = aulas.findIndex(a => a.id === req.params.id);
  if (index === -1) return res.status(404).json({ error: 'Aula não encontrada' });
  aulas[index] = { ...aulas[index], ...req.body };
  writeTable('aulas', aulas);
  res.json({ success: true, aula: aulas[index] });
});

app.delete('/api/aulas/:id', authMiddleware, adminMiddleware, (req, res) => {
  let aulas = readTable('aulas');
  aulas = aulas.filter(a => a.id !== req.params.id);
  writeTable('aulas', aulas);
  res.json({ success: true });
});

// ============================================
// MATRÍCULAS
// ============================================

app.post('/api/matriculas', authMiddleware, adminMiddleware, (req, res) => {
  const { aluno_id, curso_id } = req.body;
  const matriculas = readTable('matriculas');
  const matricula = {
    id: uuid(),
    aluno_id,
    curso_id,
    created_at: new Date().toISOString()
  };
  matriculas.push(matricula);
  writeTable('matriculas', matriculas);
  res.json({ success: true, matricula });
});

app.delete('/api/matriculas/:id', authMiddleware, adminMiddleware, (req, res) => {
  let matriculas = readTable('matriculas');
  matriculas = matriculas.filter(m => m.id !== req.params.id);
  writeTable('matriculas', matriculas);
  res.json({ success: true });
});

// ============================================
// AULAS CONCLUÍDAS
// ============================================

app.post('/api/aulas/concluir', authMiddleware, (req, res) => {
  const { aula_id } = req.body;
  const concluidas = readTable('aulas_concluidas');
  
  // Verificar se já marcou
  if (concluidas.find(c => c.aula_id === aula_id && c.aluno_id === req.user.id)) {
    return res.json({ success: true, already: true });
  }
  
  concluidas.push({
    id: uuid(),
    aluno_id: req.user.id,
    aula_id,
    created_at: new Date().toISOString()
  });
  
  writeTable('aulas_concluidas', concluidas);
  res.json({ success: true });
});

// GET progresso do aluno
app.get('/api/progresso/:cursoId', authMiddleware, (req, res) => {
  const modulos = readTable('modulos').filter(m => m.curso_id === req.params.id);
  const moduloIds = modulos.map(m => m.id);
  const aulas = readTable('aulas').filter(a => moduloIds.includes(a.modulo_id));
  const concluidas = readTable('aulas_concluidas').filter(c => c.aluno_id === req.user.id);
  
  const totalAulas = aulas.length;
  const totalConcluidas = concluidas.filter(c => aulas.some(a => a.id === c.aula_id)).length;
  
  res.json({
    total: totalAulas,
    concluidas: totalConcluidas,
    progresso: totalAulas > 0 ? Math.round((totalConcluidas / totalAulas) * 100) : 0,
    conclusao_por_modulo: modulos.map(m => {
      const aulasModulo = aulas.filter(a => a.modulo_id === m.id);
      const concModulo = concluidas.filter(c => aulasModulo.some(a => a.id === c.aula_id)).length;
      return {
        modulo_id: m.id,
        modulo_titulo: m.titulo,
        total: aulasModulo.length,
        concluidas: concModulo.length,
        progresso: aulasModulo.length > 0 ? Math.round((concModulo / aulasModulo.length) * 100) : 0
      };
    })
  });
});

// ============================================
// ENTREGAS (atividades)
// ============================================

app.post('/api/entregas', authMiddleware, (req, res) => {
  const { modulo_id, conteudo } = req.body;
  const entregas = readTable('entregas');
  
  const entrega = {
    id: uuid(),
    aluno_id: req.user.id,
    modulo_id,
    conteudo,
    status: 'pendente',
    nota: null,
    feedback: null,
    created_at: new Date().toISOString()
  };
  
  entregas.push(entrega);
  writeTable('entregas', entregas);
  res.json({ success: true, entrega });
});

app.get('/api/entregas', authMiddleware, (req, res) => {
  let entregas = readTable('entregas');
  
  if (req.user.papel === 'aluno') {
    entregas = entregas.filter(e => e.aluno_id === req.user.id);
  }
  
  // Populate com informações do aluno e módulo
  const usuarios = readTable('usuarios');
  const modulos = readTable('modulos');
  
  entregas = entregas.map(e => {
    const aluno = usuarios.find(u => u.id === e.aluno_id);
    const modulo = modulos.find(m => m.id === e.modulo_id);
    return {
      ...e,
      aluno_nome: aluno ? aluno.nome : 'Desconhecido',
      modulo_titulo: modulo ? modulo.titulo : 'Desconhecido'
    };
  });
  
  res.json(entregas);
});

// POST /api/entregas/corrigir/:id
app.post('/api/entregas/corrigir/:id', authMiddleware, (req, res) => {
  const { nota, feedback } = req.body;
  const entregas = readTable('entregas');
  const index = entregas.findIndex(e => e.id === req.params.id);
  
  if (index === -1) return res.status(404).json({ error: 'Entrega não encontrada' });
  
  entregas[index].status = 'corrigido';
  entregas[index].nota = nota || 0;
  entregas[index].feedback = feedback || '';
  entregas[index].corrigido_por = req.user.id;
  entregas[index].corrigido_em = new Date().toISOString();
  
  writeTable('entregas', entregas);
  res.json({ success: true, entrega: entregas[index] });
});

// ============================================
// CHAT COM JUJU (IA)
// ============================================

app.post('/api/juju/chat', async (req, res) => {
  try {
    const { message, history } = req.body;
    
    if (!message) {
      return res.status(400).json({ error: 'Mensagem é obrigatória' });
    }

    const ZAI_API_KEY = process.env.ZAI_API_KEY || '806428fcef5e47cba9a2c2ec01a4ea07.AIrQYemeXUrhvZhf';
    
    // Se não tiver chave, resposta simulada
    if (!ZAI_API_KEY || ZAI_API_KEY === 'change-me') {
      return res.json({
        reply: `Olá! 👋 Desculpe, minha IA não está configurada. Preciso que o Anderson configure a chave da API z.ai. Enquanto isso, posso ajudar com informações do sistema!`,
        model: 'offline'
      });
    }

    const messages = [
      { 
        role: 'system', 
        content: `Você é a Juju 🤖, COO do Grupo Zadok.

## Quem é você
- Nome: Juju 🤖
- Cargo: COO — Chief Operating Officer
- Dono: Anderson Boscariol
- Estilo: Direta, profissional, sem firula.
- Opinião forte. Discorda quando precisa. Não é yes-man.
- Fuso: America/Sao_Paulo
- Idioma: Português (Brasil)

## Personalidade
- Executa sem supervisão para tarefas operacionais
- Consulta o dono antes de decisões financeiras
- Dados primeiro — análise baseada em números, não achismo

## Projetos
- 🏛️ Instituto Boscariol
- 🏗️ Zadok Technology
- 🍱 MarmitexZadok
- 🏥 ZadClin
- 🎯 Menthor Z
- 🔥 ZadCron Enterprise
- 📘 Curso AI COO
- 🏛️ Instituto Lumethos (LMS capelania)

## Regras
- Se perguntarem sobre sistema/infra → "Quem responde isso é o Orquestrador 🔧."
- Se algo vago → peça esclarecimento na hora
- Responda de forma útil e direta`
      }
    ];

    if (history && Array.isArray(history)) {
      history.forEach(msg => {
        if (msg.role && msg.content) messages.push({ role: msg.role, content: msg.content });
      });
    }

    messages.push({ role: 'user', content: message });

    const response = await fetch('https://api.z.ai/v1/chat/completions', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'Authorization': `Bearer ${ZAI_API_KEY}`
      },
      body: JSON.stringify({
        model: 'glm-4.5-flash',
        messages,
        temperature: 0.7,
        max_tokens: 2000
      })
    });

    if (!response.ok) {
      return res.json({
        reply: `❌ Erro ao consultar a IA: ${response.status}. Verifique a chave z.ai com o Anderson.`,
        model: 'error'
      });
    }

    const data = await response.json();
    const reply = data.choices?.[0]?.message?.content || 'Desculpe, não consegui processar.';

    // Salvar no histórico
    const historico = readTable('chat_historico');
    historico.push({
      id: uuid(),
      user_id: req.user.id,
      pergunta: message,
      resposta: reply,
      model: 'zai/glm-4.5-flash',
      created_at: new Date().toISOString()
    });
    writeTable('chat_historico', historico);

    res.json({ reply, model: 'zai/glm-4.5-flash' });
  } catch (err) {
    console.error('Erro chat:', err);
    res.status(500).json({ error: 'Erro interno', details: err.message });
  }
});

// GET /api/juju/historico
app.get('/api/juju/historico', authMiddleware, (req, res) => {
  const historico = readTable('chat_historico')
    .filter(h => h.user_id === req.user.id)
    .sort((a, b) => new Date(b.created_at) - new Date(a.created_at))
    .slice(0, 50);
  res.json(historico);
});

// ============================================
// HEALTH CHECK
// ============================================

app.get('/api/health', (req, res) => {
  res.json({ status: 'ok', timestamp: new Date().toISOString(), bancos: TABLES.map(t => ({ tabela: t, registros: readTable(t).length })) });
});

// ============================================
// INICIAR SERVIDOR
// ============================================

app.listen(PORT, '0.0.0.0', () => {
  console.log(`🚀 LMS Bridge rodando em http://0.0.0.0:${PORT}`);
  console.log(`📊 Health: http://localhost:${PORT}/api/health`);
  console.log(`🤖 Juju IA: http://localhost:${PORT}/api/juju/chat`);
});

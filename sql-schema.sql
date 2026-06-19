-- ============================================================
-- INSTITUTO LUMETHOS — Schema do Banco de Dados (Supabase)
-- Execute este SQL no SQL Editor do Supabase Dashboard
-- ============================================================

-- 1. CATEGORIAS DE CURSOS
CREATE TABLE IF NOT EXISTS categorias (
  id UUID DEFAULT gen_random_uuid() PRIMARY KEY,
  nome TEXT NOT NULL,
  slug TEXT UNIQUE NOT NULL,
  descricao TEXT,
  cor TEXT DEFAULT '#C79A2E',
  icone TEXT,
  ordem INTEGER DEFAULT 0,
  created_at TIMESTAMPTZ DEFAULT NOW()
);

-- 2. CURSOS
CREATE TABLE IF NOT EXISTS cursos (
  id UUID DEFAULT gen_random_uuid() PRIMARY KEY,
  titulo TEXT NOT NULL,
  slug TEXT UNIQUE NOT NULL,
  descricao TEXT,
  descricao_curta TEXT,
  categoria_id UUID REFERENCES categorias(id),
  imagem_url TEXT,
  imagem_card TEXT,
  carga_horaria TEXT DEFAULT '150h',
  nivel TEXT DEFAULT 'iniciante',
  destaque BOOLEAN DEFAULT false,
  gratuito BOOLEAN DEFAULT false,
  preco DECIMAL(10,2) DEFAULT 0,
  status TEXT DEFAULT 'rascunho',
  conteudo_markdown TEXT,
  progresso_liberacao TEXT DEFAULT 'linear',
  ordem INTEGER DEFAULT 0,
  created_at TIMESTAMPTZ DEFAULT NOW(),
  updated_at TIMESTAMPTZ DEFAULT NOW()
);

-- 3. MÓDULOS
CREATE TABLE IF NOT EXISTS modulos (
  id UUID DEFAULT gen_random_uuid() PRIMARY KEY,
  curso_id UUID REFERENCES cursos(id) ON DELETE CASCADE,
  titulo TEXT NOT NULL,
  slug TEXT,
  descricao TEXT,
  ordem INTEGER DEFAULT 0,
  carga_horaria TEXT DEFAULT '10h',
  conteudo_markdown TEXT,
  video_url TEXT,
  video_duration TEXT,
  quiz JSONB,
  created_at TIMESTAMPTZ DEFAULT NOW(),
  updated_at TIMESTAMPTZ DEFAULT NOW()
);

-- 4. AULAS/LIÇÕES
CREATE TABLE IF NOT EXISTS aulas (
  id UUID DEFAULT gen_random_uuid() PRIMARY KEY,
  modulo_id UUID REFERENCES modulos(id) ON DELETE CASCADE,
  titulo TEXT NOT NULL,
  tipo TEXT DEFAULT 'texto',
  conteudo_markdown TEXT,
  video_url TEXT,
  video_duration TEXT,
  ordem INTEGER DEFAULT 0,
  created_at TIMESTAMPTZ DEFAULT NOW(),
  updated_at TIMESTAMPTZ DEFAULT NOW()
);

-- 5. ALUNOS
CREATE TABLE IF NOT EXISTS alunos (
  id UUID DEFAULT gen_random_uuid() PRIMARY KEY,
  email TEXT UNIQUE NOT NULL,
  nome TEXT NOT NULL,
  avatar_url TEXT,
  auth_id TEXT UNIQUE,
  created_at TIMESTAMPTZ DEFAULT NOW()
);

-- 6. MATRÍCULAS
CREATE TABLE IF NOT EXISTS matriculas (
  id UUID DEFAULT gen_random_uuid() PRIMARY KEY,
  aluno_id UUID REFERENCES alunos(id) ON DELETE CASCADE,
  curso_id UUID REFERENCES cursos(id) ON DELETE CASCADE,
  status TEXT DEFAULT 'ativo',
  progresso INTEGER DEFAULT 0,
  modulo_atual INTEGER DEFAULT 1,
  aula_atual TEXT,
  data_inicio TIMESTAMPTZ DEFAULT NOW(),
  data_conclusao TIMESTAMPTZ,
  UNIQUE(aluno_id, curso_id)
);

-- 7. PROGRESSO DOS MÓDULOS
CREATE TABLE IF NOT EXISTS progresso_modulos (
  id UUID DEFAULT gen_random_uuid() PRIMARY KEY,
  matricula_id UUID REFERENCES matriculas(id) ON DELETE CASCADE,
  modulo_id UUID REFERENCES modulos(id) ON DELETE CASCADE,
  concluido BOOLEAN DEFAULT false,
  quiz_nota DECIMAL(5,2),
  quiz_concluido BOOLEAN DEFAULT false,
  aulas_concluidas TEXT[] DEFAULT '{}',
  data_conclusao TIMESTAMPTZ,
  UNIQUE(matricula_id, modulo_id)
);

-- ============================================================
-- ROW LEVEL SECURITY
-- ============================================================
ALTER TABLE cursos ENABLE ROW LEVEL SECURITY;
ALTER TABLE modulos ENABLE ROW LEVEL SECURITY;
ALTER TABLE aulas ENABLE ROW LEVEL SECURITY;
ALTER TABLE matriculas ENABLE ROW LEVEL SECURITY;
ALTER TABLE progresso_modulos ENABLE ROW LEVEL SECURITY;
ALTER TABLE alunos ENABLE ROW LEVEL SECURITY;
ALTER TABLE categorias ENABLE ROW LEVEL SECURITY;

-- Políticas de segurança
DROP POLICY IF EXISTS "Cursos publicos" ON cursos;
CREATE POLICY "Cursos publicos" ON cursos FOR SELECT USING (status = 'publicado' OR status = 'rascunho');

DROP POLICY IF EXISTS "Modulos publicos" ON modulos;
CREATE POLICY "Modulos publicos" ON modulos FOR SELECT USING (true);

DROP POLICY IF EXISTS "Aulas publicas" ON aulas;
CREATE POLICY "Aulas publicas" ON aulas FOR SELECT USING (true);

DROP POLICY IF EXISTS "Categorias publicas" ON categorias;
CREATE POLICY "Categorias publicas" ON categorias FOR SELECT USING (true);

DROP POLICY IF EXISTS "Alunos leem proprios" ON alunos;
CREATE POLICY "Alunos leem proprios" ON alunos FOR SELECT USING (auth.uid()::text = auth_id OR auth_id IS NULL);

DROP POLICY IF EXISTS "Matriculas proprias" ON matriculas;
CREATE POLICY "Matriculas proprias" ON matriculas FOR SELECT USING (aluno_id IN (SELECT id FROM alunos WHERE auth_id = auth.uid()::text));

DROP POLICY IF EXISTS "Progresso proprio" ON progresso_modulos;
CREATE POLICY "Progresso proprio" ON progresso_modulos FOR SELECT USING (matricula_id IN (SELECT id FROM matriculas WHERE aluno_id IN (SELECT id FROM alunos WHERE auth_id = auth.uid()::text)));

-- ============================================================
-- ADMIN: criar políticas para admin inserir/atualizar/deletar
-- ============================================================
DROP POLICY IF EXISTS "Admin pode inserir cursos" ON cursos;
CREATE POLICY "Admin pode inserir cursos" ON cursos FOR INSERT WITH CHECK (true);

DROP POLICY IF EXISTS "Admin pode atualizar cursos" ON cursos;
CREATE POLICY "Admin pode atualizar cursos" ON cursos FOR UPDATE USING (true);

DROP POLICY IF EXISTS "Admin pode deletar cursos" ON cursos;
CREATE POLICY "Admin pode deletar cursos" ON cursos FOR DELETE USING (true);

-- Admin policies for other tables
DROP POLICY IF EXISTS "Admin modulos insert" ON modulos;
CREATE POLICY "Admin modulos insert" ON modulos FOR INSERT WITH CHECK (true);
DROP POLICY IF EXISTS "Admin modulos update" ON modulos;
CREATE POLICY "Admin modulos update" ON modulos FOR UPDATE USING (true);
DROP POLICY IF EXISTS "Admin modulos delete" ON modulos;
CREATE POLICY "Admin modulos delete" ON modulos FOR DELETE USING (true);

DROP POLICY IF EXISTS "Admin aulas insert" ON aulas;
CREATE POLICY "Admin aulas insert" ON aulas FOR INSERT WITH CHECK (true);
DROP POLICY IF EXISTS "Admin aulas update" ON aulas;
CREATE POLICY "Admin aulas update" ON aulas FOR UPDATE USING (true);
DROP POLICY IF EXISTS "Admin aulas delete" ON aulas;
CREATE POLICY "Admin aulas delete" ON aulas FOR DELETE USING (true);

DROP POLICY IF EXISTS "Admin categorias insert" ON categorias;
CREATE POLICY "Admin categorias insert" ON categorias FOR INSERT WITH CHECK (true);
DROP POLICY IF EXISTS "Admin categorias update" ON categorias;
CREATE POLICY "Admin categorias update" ON categorias FOR UPDATE USING (true);
DROP POLICY IF EXISTS "Admin categorias delete" ON categorias;
CREATE POLICY "Admin categorias delete" ON categorias FOR DELETE USING (true);

DROP POLICY IF EXISTS "Admin alunos" ON alunos;
CREATE POLICY "Admin alunos" ON alunos FOR ALL USING (true);

DROP POLICY IF EXISTS "Admin matriculas" ON matriculas;
CREATE POLICY "Admin matriculas" ON matriculas FOR ALL USING (true);

DROP POLICY IF EXISTS "Admin progresso" ON progresso_modulos;
CREATE POLICY "Admin progresso" ON progresso_modulos FOR ALL USING (true);

-- Allow insert for matriculas by alunos
DROP POLICY IF EXISTS "Aluno pode inserir matricula" ON matriculas;
CREATE POLICY "Aluno pode inserir matricula" ON matriculas FOR INSERT WITH CHECK (aluno_id IN (SELECT id FROM alunos WHERE auth_id = auth.uid()::text));

-- ============================================================
-- SEED DATA: Categoria Capelania
-- ============================================================
INSERT INTO categorias (nome, slug, descricao, cor, icone, ordem)
VALUES ('Capelania', 'capelania', 'Cursos de capacitação em Capelania Evangélica', '#C79A2E', 'heart', 1)
ON CONFLICT (slug) DO NOTHING;

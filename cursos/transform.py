#!/usr/bin/env python3
"""Apply Netflix-style hero + dark theme to all 9 course pages."""
import re, os

COURSES_DIR = '/var/www/lumethos/cursos'

# Course data for hero construction
courses = {
    'capelania': {
        'title': 'Capelania Cristã',
        'desc': 'Formação completa para assistência espiritual em hospitais, presídios, escolas e empresas.',
        'hours': '150h', 'modules': '15',
        'checkout': 'capelania-crista',
        'modules_count': '15',
        'sections_after_hero': {
            'sobre_desc': '<p>O <strong>Curso de Capelania Cristã</strong> é uma formação completa para quem deseja atuar como capelão em hospitais, presídios, forças armadas, escolas e empresas. Oferece base bíblica, teológica e prática para o exercício do ministério de capelania com excelência e sensibilidade.</p><p>Ideal para pastores, missionários, líderes e voluntários. Certificação com registro institucional e validade em todo o Brasil.</p>',
            'diferenciais': '''<div class="diferenciais">
        <div class="dif-card">
          <h4>📜 Certificado Digital</h4>
          <p>Certificado de conclusão com verificação por QR Code</p>
        </div>
        <div class="dif-card">
          <h4>🎓 Certificação Institucional</h4>
          <p>Válida em todo o Brasil com matrícula única LUM-2026</p>
        </div>
        <div class="dif-card">
          <h4>📚 Biblioteca do Capelão</h4>
          <p>Acesso vitalício ao acervo teológico e ministerial</p>
        </div>
        <div class="dif-card">
          <h4>⏰ Estude no seu Ritmo</h4>
          <p>Curso 100% online com acesso vitalício ao conteúdo</p>
        </div>
      </div>''',
            'modulos_title': '15 Módulos de Formação',
            'modulos': '''<div class="modulos-grid"><div class="modulo-card"><div class="mod-num">MÓDULO 01</div><div class="mod-name">Fundamentos da Capelania</div></div><div class="modulo-card"><div class="mod-num">MÓDULO 02</div><div class="mod-name">Capelania Hospitalar</div></div><div class="modulo-card"><div class="mod-num">MÓDULO 03</div><div class="mod-name">Capelania Prisional</div></div><div class="modulo-card"><div class="mod-num">MÓDULO 04</div><div class="mod-name">Capelania Militar</div></div><div class="modulo-card"><div class="mod-num">MÓDULO 05</div><div class="mod-name">Capelania Escolar e Empresarial</div></div><div class="modulo-card"><div class="mod-num">MÓDULO 06</div><div class="mod-name">Aconselhamento Pastoral</div></div><div class="modulo-card"><div class="mod-num">MÓDULO 07</div><div class="mod-name">Teologia Prática</div></div><div class="modulo-card"><div class="mod-num">MÓDULO 08</div><div class="mod-name">Hermenêutica e Exegese</div></div><div class="modulo-card"><div class="mod-num">MÓDULO 09</div><div class="mod-name">Ética Cristã e Bioética</div></div><div class="modulo-card"><div class="mod-num">MÓDULO 10</div><div class="mod-name">Primeiros Socorros Espirituais</div></div><div class="modulo-card"><div class="mod-num">MÓDULO 11</div><div class="mod-name">Gestão Ministerial</div></div><div class="modulo-card"><div class="mod-num">MÓDULO 12</div><div class="mod-name">Pregação e Ensino</div></div><div class="modulo-card"><div class="mod-num">MÓDULO 13</div><div class="mod-name">Liderança Cristã</div></div><div class="modulo-card"><div class="mod-num">MÓDULO 14</div><div class="mod-name">Missiologia e Ação Social</div></div><div class="modulo-card"><div class="mod-num">MÓDULO 15</div><div class="mod-name">Projeto Integrador de Capelania</div></div></div>'''
        }
    },
    'teologia': {
        'title': 'Teologia',
        'desc': 'Fundamentos teológicos sólidos: sistemática, bíblica, histórica, apologética e hermenêutica.',
        'hours': '150h', 'modules': '10',
        'checkout': 'teologia',
        'modules_count': '10',
        'sections_after_hero': {
            'sobre_desc': '<p>O <strong>Curso de Teologia</strong> oferece uma base sólida nas principais áreas do conhecimento teológico: Teologia Sistemática, Bíblica, Histórica, Apologética e Hermenêutica. Uma formação completa para quem deseja compreender as Escrituras com profundidade acadêmica.</p><p>Ideal para pastores, líderes e estudiosos da Bíblia. Certificado com registro institucional.</p>',
            'diferenciais': '''<div class="diferenciais">
        <div class="dif-card">
          <h4>📜 Certificado Digital</h4>
          <p>Certificado de conclusão com verificação por QR Code</p>
        </div>
        <div class="dif-card">
          <h4>🎓 Certificação Institucional</h4>
          <p>Válida em todo o Brasil com matrícula única LUM-2026</p>
        </div>
        <div class="dif-card">
          <h4>📚 Biblioteca Teológica</h4>
          <p>Acesso vitalício ao acervo de estudos</p>
        </div>
        <div class="dif-card">
          <h4>⏰ Estude no seu Ritmo</h4>
          <p>Curso 100% online com acesso vitalício ao conteúdo</p>
        </div>
      </div>''',
            'modulos_title': '10 Módulos de Formação',
            'modulos': '''<div class="modulos-grid"><div class="modulo-card"><div class="mod-num">MÓDULO 01</div><div class="mod-name">Introdução à Teologia</div></div><div class="modulo-card"><div class="mod-num">MÓDULO 02</div><div class="mod-name">Teologia Sistemática I</div></div><div class="modulo-card"><div class="mod-num">MÓDULO 03</div><div class="mod-name">Teologia Sistemática II</div></div><div class="modulo-card"><div class="mod-num">MÓDULO 04</div><div class="mod-name">Teologia Bíblica</div></div><div class="modulo-card"><div class="mod-num">MÓDULO 05</div><div class="mod-name">Teologia Histórica</div></div><div class="modulo-card"><div class="mod-num">MÓDULO 06</div><div class="mod-name">Apologética Cristã</div></div><div class="modulo-card"><div class="mod-num">MÓDULO 07</div><div class="mod-name">Hermenêutica</div></div><div class="modulo-card"><div class="mod-num">MÓDULO 08</div><div class="mod-name">Exegese do Antigo Testamento</div></div><div class="modulo-card"><div class="mod-num">MÓDULO 09</div><div class="mod-name">Exegese do Novo Testamento</div></div><div class="modulo-card"><div class="mod-num">MÓDULO 10</div><div class="mod-name">Teologia Contemporânea</div></div></div>'''
        }
    },
    'pastoral': {
        'title': 'Ministério Pastoral',
        'desc': 'Formação para liderança eclesiástica com pregação, cuidado pastoral e administração.',
        'hours': '120h', 'modules': '12',
        'checkout': 'ministerio-pastoral',
        'modules_count': '12',
        'sections_after_hero': {
            'sobre_desc': '<p>O <strong>Curso de Ministério Pastoral</strong> é uma formação completa para pastores e líderes eclesiásticos. Abrange pregação expositiva, aconselhamento pastoral, administração da igreja, liderança e desenvolvimento ministerial.</p><p>Ideal para pastores, obreiros e seminaristas. Certificação com registro institucional.</p>',
            'diferenciais': '''<div class="diferenciais">
        <div class="dif-card">
          <h4>📜 Certificado Digital</h4>
          <p>Certificado de conclusão com verificação por QR Code</p>
        </div>
        <div class="dif-card">
          <h4>🎓 Certificação Institucional</h4>
          <p>Válida em todo o Brasil com matrícula única LUM-2026</p>
        </div>
        <div class="dif-card">
          <h4>📚 Estudos Ministeriais</h4>
          <p>Acesso vitalício ao acervo pastoral</p>
        </div>
        <div class="dif-card">
          <h4>⏰ Estude no seu Ritmo</h4>
          <p>Curso 100% online com acesso vitalício ao conteúdo</p>
        </div>
      </div>''',
            'modulos_title': '12 Módulos de Formação',
            'modulos': '''<div class="modulos-grid"><div class="modulo-card"><div class="mod-num">MÓDULO 01</div><div class="mod-name">Vocação Pastoral</div></div><div class="modulo-card"><div class="mod-num">MÓDULO 02</div><div class="mod-name">Pregação Expositiva</div></div><div class="modulo-card"><div class="mod-num">MÓDULO 03</div><div class="mod-name">Aconselhamento Pastoral</div></div><div class="modulo-card"><div class="mod-num">MÓDULO 04</div><div class="mod-name">Administração Eclesiástica</div></div><div class="modulo-card"><div class="mod-num">MÓDULO 05</div><div class="mod-name">Liderança Cristã</div></div><div class="modulo-card"><div class="mod-num">MÓDULO 06</div><div class="mod-name">Teologia Prática</div></div><div class="modulo-card"><div class="mod-num">MÓDULO 07</div><div class="mod-name">Discipulado e Mentoria</div></div><div class="modulo-card"><div class="mod-num">MÓDULO 08</div><div class="mod-name">Liturgia e Culto</div></div><div class="modulo-card"><div class="mod-num">MÓDULO 09</div><div class="mod-name">Missões e Evangelismo</div></div><div class="modulo-card"><div class="mod-num">MÓDULO 10</div><div class="mod-name">Ensino e Pedagogia Cristã</div></div><div class="modulo-card"><div class="mod-num">MÓDULO 11</div><div class="mod-name">Gestão de Conflitos</div></div><div class="modulo-card"><div class="mod-num">MÓDULO 12</div><div class="mod-name">Projeto Pastoral Integrador</div></div></div>'''
        }
    },
    'diaconal': {
        'title': 'Ministério Diaconal',
        'desc': 'Capacitação para o serviço cristão prático com assistência social e ação comunitária.',
        'hours': '100h', 'modules': '10',
        'checkout': 'ministerio-diaconal',
        'modules_count': '10',
        'sections_after_hero': {
            'sobre_desc': '<p>O <strong>Curso de Ministério Diaconal</strong> capacita para o serviço cristão prático. Abrange assistência social, ação comunitária, visitas, acolhimento e suporte às famílias da igreja local.</p><p>Ideal para diáconos, diaconisas e líderes de ação social. Certificação com registro institucional.</p>',
            'diferenciais': '''<div class="diferenciais">
        <div class="dif-card">
          <h4>📜 Certificado Digital</h4>
          <p>Certificado de conclusão com verificação por QR Code</p>
        </div>
        <div class="dif-card">
          <h4>🎓 Certificação Institucional</h4>
          <p>Válida em todo o Brasil com matrícula única LUM-2026</p>
        </div>
        <div class="dif-card">
          <h4>📚 Biblioteca Teológica</h4>
          <p>Acesso vitalício ao acervo de estudos</p>
        </div>
        <div class="dif-card">
          <h4>⏰ Estude no seu Ritmo</h4>
          <p>Curso 100% online com acesso vitalício ao conteúdo</p>
        </div>
      </div>''',
            'modulos_title': '10 Módulos de Formação',
            'modulos': '''<div class="modulos-grid"><div class="modulo-card"><div class="mod-num">MÓDULO 01</div><div class="mod-name">Fundamento Bíblico do Diaconato</div></div><div class="modulo-card"><div class="mod-num">MÓDULO 02</div><div class="mod-name">História do Diaconato</div></div><div class="modulo-card"><div class="mod-num">MÓDULO 03</div><div class="mod-name">Assistência Social Cristã</div></div><div class="modulo-card"><div class="mod-num">MÓDULO 04</div><div class="mod-name">Ação Comunitária</div></div><div class="modulo-card"><div class="mod-num">MÓDULO 05</div><div class="mod-name">Visitas e Acolhimento</div></div><div class="modulo-card"><div class="mod-num">MÓDULO 06</div><div class="mod-name">Aconselhamento Familiar</div></div><div class="modulo-card"><div class="mod-num">MÓDULO 07</div><div class="mod-name">Administração e Finanças</div></div><div class="modulo-card"><div class="mod-num">MÓDULO 08</div><div class="mod-name">Liturgia e Celebração</div></div><div class="modulo-card"><div class="mod-num">MÓDULO 09</div><div class="mod-name">Ética Cristã</div></div><div class="modulo-card"><div class="mod-num">MÓDULO 10</div><div class="mod-name">Projeto Diaconal Integrador</div></div></div>'''
        }
    },
    'hinologia': {
        'title': 'Hinologia Cristã',
        'desc': 'Estudo da música sacra, hinódia brasileira, técnica vocal e regência.',
        'hours': '80h', 'modules': '8',
        'checkout': 'hinologia-crista',
        'modules_count': '8',
        'sections_after_hero': {
            'sobre_desc': '<p>O <strong>Curso de Hinologia Cristã</strong> é um estudo aprofundado da música sacra, hinódia brasileira, técnica vocal e regência. Prepara músicos e ministros de louvor para o serviço litúrgico com excelência e fundamentação teológica.</p><p>Ideal para músicos, cantores, regentes e ministros de louvor. Certificação com registro institucional.</p>',
            'diferenciais': '''<div class="diferenciais">
        <div class="dif-card">
          <h4>📜 Certificado Digital</h4>
          <p>Certificado de conclusão com verificação por QR Code</p>
        </div>
        <div class="dif-card">
          <h4>🎓 Certificação Institucional</h4>
          <p>Válida em todo o Brasil com matrícula única LUM-2026</p>
        </div>
        <div class="dif-card">
          <h4>📚 Partituras e Hinos</h4>
          <p>Acesso ao acervo musical</p>
        </div>
        <div class="dif-card">
          <h4>⏰ Estude no seu Ritmo</h4>
          <p>Curso 100% online com acesso vitalício ao conteúdo</p>
        </div>
      </div>''',
            'modulos_title': '8 Módulos de Formação',
            'modulos': '''<div class="modulos-grid"><div class="modulo-card"><div class="mod-num">MÓDULO 01</div><div class="mod-name">Introdução à Hinologia</div></div><div class="modulo-card"><div class="mod-num">MÓDULO 02</div><div class="mod-name">História da Música Sacra</div></div><div class="modulo-card"><div class="mod-num">MÓDULO 03</div><div class="mod-name">Hinódia Brasileira</div></div><div class="modulo-card"><div class="mod-num">MÓDULO 04</div><div class="mod-name">Teologia do Louvor</div></div><div class="modulo-card"><div class="mod-num">MÓDULO 05</div><div class="mod-name">Técnica Vocal</div></div><div class="modulo-card"><div class="mod-num">MÓDULO 06</div><div class="mod-name">Regência de Coral</div></div><div class="modulo-card"><div class="mod-num">MÓDULO 07</div><div class="mod-name">Liturgia Musical</div></div><div class="modulo-card"><div class="mod-num">MÓDULO 08</div><div class="mod-name">Projeto Musical Integrador</div></div></div>'''
        }
    },
    'infantil': {
        'title': 'Ministério Infantil',
        'desc': 'Formação para ensino bíblico criativo e discipulado de crianças na igreja local.',
        'hours': '100h', 'modules': '10',
        'checkout': 'ministerio-infantil',
        'modules_count': '10',
        'sections_after_hero': {
            'sobre_desc': '<p>O <strong>Curso de Ministério Infantil</strong> capacita para o ensino bíblico criativo e o discipulado de crianças. Aborda psicologia infantil, pedagogia cristã, planejamento de aulas e materiais didáticos.</p><p>Ideal para professores da Escola Bíblica, líderes e voluntários do ministério infantil. Certificação com registro institucional.</p>',
            'diferenciais': '''<div class="diferenciais">
        <div class="dif-card">
          <h4>📜 Certificado Digital</h4>
          <p>Certificado de conclusão com verificação por QR Code</p>
        </div>
        <div class="dif-card">
          <h4>🎓 Certificação Institucional</h4>
          <p>Válida em todo o Brasil com matrícula única LUM-2026</p>
        </div>
        <div class="dif-card">
          <h4>📚 Recursos Didáticos</h4>
          <p>Acesso vitalício ao acervo pedagógico</p>
        </div>
        <div class="dif-card">
          <h4>⏰ Estude no seu Ritmo</h4>
          <p>Curso 100% online com acesso vitalício ao conteúdo</p>
        </div>
      </div>''',
            'modulos_title': '10 Módulos de Formação',
            'modulos': '''<div class="modulos-grid"><div class="modulo-card"><div class="mod-num">MÓDULO 01</div><div class="mod-name">Fundamentos do Ministério Infantil</div></div><div class="modulo-card"><div class="mod-num">MÓDULO 02</div><div class="mod-name">Psicologia Infantil</div></div><div class="modulo-card"><div class="mod-num">MÓDULO 03</div><div class="mod-name">Pedagogia Cristã</div></div><div class="modulo-card"><div class="mod-num">MÓDULO 04</div><div class="mod-name">Ensino Bíblico Criativo</div></div><div class="modulo-card"><div class="mod-num">MÓDULO 05</div><div class="mod-name">Contação de Histórias</div></div><div class="modulo-card"><div class="mod-num">MÓDULO 06</div><div class="mod-name">Música e Louvor Infantil</div></div><div class="modulo-card"><div class="mod-num">MÓDULO 07</div><div class="mod-name">Discipulado de Crianças</div></div><div class="modulo-card"><div class="mod-num">MÓDULO 08</div><div class="mod-name">Eventos e Projetos Infantis</div></div><div class="modulo-card"><div class="mod-num">MÓDULO 09</div><div class="mod-name">Família e Igreja</div></div><div class="modulo-card"><div class="mod-num">MÓDULO 10</div><div class="mod-name">Projeto Infantil Integrador</div></div></div>'''
        }
    },
    'jovens': {
        'title': 'Ministério dos Jovens',
        'desc': 'Formação para liderança de jovens na igreja contemporânea',
        'hours': '120h', 'modules': '8',
        'checkout': 'ministerio-dos-jovens',
        'modules_count': '8',
        'sections_after_hero': {
            'sobre_desc': '<p>O <strong>Ministério dos Jovens</strong> é um campo vibrante e desafiador da igreja contemporânea. Liderar jovens requer compreensão profunda de sua realidade, linguagem e anseios, aliada a uma base bíblica sólida e métodos pedagógicos eficazes.</p><p>Ideal para líderes de jovens, pastores, educadores cristãos e voluntários. Certificação com registro institucional.</p>',
            'diferenciais': '''<div class="diferenciais">
        <div class="dif-card">
          <h4>📜 Certificado Digital</h4>
          <p>Certificado de conclusão com verificação por QR Code</p>
        </div>
        <div class="dif-card">
          <h4>🎓 Certificação Institucional</h4>
          <p>Válida em todo o Brasil com matrícula única LUM-2026</p>
        </div>
        <div class="dif-card">
          <h4>📚 Biblioteca Teológica</h4>
          <p>Acesso vitalício ao acervo de estudos</p>
        </div>
        <div class="dif-card">
          <h4>⏰ Estude no seu Ritmo</h4>
          <p>Curso 100% online com acesso vitalício ao conteúdo</p>
        </div>
      </div>''',
            'modulos_title': '4 Módulos de Formação',
            'modulos': '''<div class="modulos-grid"><div class="modulo-card"><div class="mod-num">MÓDULO 01</div><div class="mod-name">Liderança Juvenil</div></div><div class="modulo-card"><div class="mod-num">MÓDULO 02</div><div class="mod-name">Discipulado de Adolescentes</div></div><div class="modulo-card"><div class="mod-num">MÓDULO 03</div><div class="mod-name">Pedagogia Cristã para Jovens</div></div><div class="modulo-card"><div class="mod-num">MÓDULO 04</div><div class="mod-name">Eventos e Projetos Juvenis</div></div></div>'''
        }
    },
    'patristica': {
        'title': 'Patrística',
        'desc': 'Estudo dos Pais da Igreja e fundamentos da teologia cristã',
        'hours': '120h', 'modules': '8',
        'checkout': 'patristica',
        'modules_count': '8',
        'sections_after_hero': {
            'sobre_desc': '<p>A <strong>Patrística</strong> é o estudo dos Pais da Igreja — os primeiros escritores e teólogos cristãos que moldaram a doutrina, liturgia e organização eclesial nos primeiros séculos do cristianismo. Compreender a Patrística é essencial para entender as raízes da fé cristã.</p><p>Curso ideal para estudantes de teologia, seminário e interessados na história do pensamento cristão. Certificado com registro institucional.</p>',
            'diferenciais': '''<div class="diferenciais">
        <div class="dif-card">
          <h4>📜 Certificado Digital</h4>
          <p>Certificado de conclusão com verificação por QR Code</p>
        </div>
        <div class="dif-card">
          <h4>🎓 Certificação Institucional</h4>
          <p>Válida em todo o Brasil com matrícula única LUM-2026</p>
        </div>
        <div class="dif-card">
          <h4>📚 Biblioteca Teológica</h4>
          <p>Acesso vitalício ao acervo de estudos</p>
        </div>
        <div class="dif-card">
          <h4>⏰ Estude no seu Ritmo</h4>
          <p>Curso 100% online com acesso vitalício ao conteúdo</p>
        </div>
      </div>''',
            'modulos_title': '5 Módulos de Formação',
            'modulos': '''<div class="modulos-grid"><div class="modulo-card"><div class="mod-num">MÓDULO 01</div><div class="mod-name">Introdução à Patrística</div></div><div class="modulo-card"><div class="mod-num">MÓDULO 02</div><div class="mod-name">Pais Apostólicos</div></div><div class="modulo-card"><div class="mod-num">MÓDULO 03</div><div class="mod-name">Pais Apologistas</div></div><div class="modulo-card"><div class="mod-num">MÓDULO 04</div><div class="mod-name">Pais Alexandrinos e Antioquenos</div></div><div class="modulo-card"><div class="mod-num">MÓDULO 05</div><div class="mod-name">Pais Latinos</div></div></div>'''
        }
    },
    'historia-igreja': {
        'title': 'História da Igreja',
        'desc': 'Jornada pelos 2000 anos de história do cristianismo',
        'hours': '120h', 'modules': '8',
        'checkout': 'historia-da-igreja',
        'modules_count': '8',
        'sections_after_hero': {
            'sobre_desc': '<p>A <strong>História da Igreja</strong> é o estudo da trajetória do cristianismo ao longo dos séculos — desde a Igreja primitiva até a contemporaneidade. Conhecer essa história é fundamental para entender o presente e projetar o futuro do ministério cristão.</p><p>Curso essencial para líderes, pastores e estudantes de teologia. Certificado com registro institucional.</p>',
            'diferenciais': '''<div class="diferenciais">
        <div class="dif-card">
          <h4>📜 Certificado Digital</h4>
          <p>Certificado de conclusão com verificação por QR Code</p>
        </div>
        <div class="dif-card">
          <h4>🎓 Certificação Institucional</h4>
          <p>Válida em todo o Brasil com matrícula única LUM-2026</p>
        </div>
        <div class="dif-card">
          <h4>📚 Biblioteca Teológica</h4>
          <p>Acesso vitalício ao acervo de estudos</p>
        </div>
        <div class="dif-card">
          <h4>⏰ Estude no seu Ritmo</h4>
          <p>Curso 100% online com acesso vitalício ao conteúdo</p>
        </div>
      </div>''',
            'modulos_title': '5 Módulos de Formação',
            'modulos': '''<div class="modulos-grid"><div class="modulo-card"><div class="mod-num">MÓDULO 01</div><div class="mod-name">Igreja Primitiva (30-313)</div></div><div class="modulo-card"><div class="mod-num">MÓDULO 02</div><div class="mod-name">Cristandade Medieval (313-1500)</div></div><div class="modulo-card"><div class="mod-num">MÓDULO 03</div><div class="mod-name">Reforma e Contrarreforma (1500-1648)</div></div><div class="modulo-card"><div class="mod-num">MÓDULO 04</div><div class="mod-name">Igreja Moderna (1648-1900)</div></div><div class="modulo-card"><div class="mod-num">MÓDULO 05</div><div class="mod-name">Igreja Contemporânea (1900-presente)</div></div></div>'''
        }
    }
}

NEW_STYLE = '''
    *{margin:0;padding:0;box-sizing:border-box}
    body{font-family:'Inter',sans-serif;background:#0D1B2A;color:#fff;line-height:1.6}
    a{text-decoration:none;color:inherit}

    /* ===== NETFLIX HERO ===== */
    .netflix-hero {
      position: relative;
      min-height: 85vh;
      display: flex;
      align-items: center;
      background: #0D1B2A;
      overflow: hidden;
      padding: 80px 0 60px;
    }
    .netflix-hero-bg {
      position: absolute;
      inset: 0;
      width: 100%;
      height: 100%;
      object-fit: cover;
      filter: brightness(0.35);
      transform: scale(1.05);
    }
    .netflix-hero-overlay {
      position: absolute;
      inset: 0;
      background: linear-gradient(180deg, rgba(13,27,42,0.2) 0%, rgba(13,27,42,0.7) 50%, #0D1B2A 100%);
      z-index: 2;
    }
    .netflix-hero-content {
      position: relative;
      z-index: 3;
      max-width: 680px;
      padding: 0 48px;
    }
    .netflix-hero-badge {
      display: inline-block;
      background: rgba(199,154,46,0.2);
      border: 1px solid rgba(199,154,46,0.3);
      color: #C79A2E;
      font-size: 11px;
      font-weight: 700;
      text-transform: uppercase;
      letter-spacing: 2px;
      padding: 6px 16px;
      border-radius: 4px;
      margin-bottom: 20px;
    }
    .netflix-hero-content h1 {
      font-family: 'Libre Baskerville', serif;
      font-size: clamp(38px, 7vw, 72px);
      color: #fff;
      line-height: 1.05;
      margin: 0 0 16px;
      text-shadow: 0 2px 12px rgba(0,0,0,0.5);
    }
    .netflix-hero-desc {
      color: rgba(255,255,255,0.85);
      font-size: 18px;
      line-height: 1.6;
      max-width: 520px;
      margin: 0 0 28px;
    }
    .netflix-hero-stats {
      display: flex;
      align-items: center;
      gap: 12px;
      flex-wrap: wrap;
      color: rgba(255,255,255,0.6);
      font-size: 14px;
      margin-bottom: 32px;
    }
    .netflix-hero-stats strong { color: #C79A2E; font-weight: 700; }
    .netflix-hero-stats .dot { color: rgba(255,255,255,0.2); }
    .netflix-hero-actions { display: flex; gap: 12px; flex-wrap: wrap; }
    .netflix-btn-play {
      display: inline-flex;
      align-items: center;
      gap: 8px;
      padding: 14px 32px;
      background: #C79A2E;
      color: #0D1B2A;
      font-weight: 700;
      font-size: 16px;
      border-radius: 6px;
      text-decoration: none;
      transition: all 0.2s;
    }
    .netflix-btn-play:hover { background: #d4a83a; transform: scale(1.04); }
    .netflix-btn-info {
      display: inline-flex;
      align-items: center;
      gap: 8px;
      padding: 14px 28px;
      background: rgba(255,255,255,0.12);
      color: #fff;
      font-weight: 600;
      font-size: 16px;
      border-radius: 6px;
      text-decoration: none;
      transition: all 0.2s;
      backdrop-filter: blur(4px);
    }
    .netflix-btn-info:hover { background: rgba(255,255,255,0.22); }

    /* ===== DARK SECTIONS ===== */
    .section{padding:56px 0}
    .section.dark{background:#0D1B2A}
    .section.darker{background:#152238}
    .container{max-width:960px;margin:0 auto;padding:0 24px}
    .section-title{font-family:'Libre Baskerville',serif;font-size:28px;color:#fff;margin-bottom:6px}
    .section-tag{font-size:12px;font-weight:700;color:#C79A2E;text-transform:uppercase;letter-spacing:1.5px;margin-bottom:12px}
    .desc-text{font-size:16px;color:rgba(255,255,255,0.75);line-height:1.9;max-width:720px}
    .desc-text p{margin-bottom:16px}
    .desc-text strong{color:#C79A2E}
    .diferenciais{display:grid;grid-template-columns:repeat(auto-fit,minmax(220px,1fr));gap:16px;margin-top:28px}
    .dif-card{background:rgba(255,255,255,0.04);padding:22px 24px;border-radius:12px;border-left:3px solid #C79A2E}
    .dif-card h4{font-size:14px;font-weight:700;color:#fff;margin-bottom:4px}
    .dif-card p{font-size:13px;color:rgba(255,255,255,0.5);line-height:1.5}
    .modulos-grid{display:grid;grid-template-columns:repeat(auto-fill,minmax(280px,1fr));gap:12px;margin-top:28px}
    .modulo-card{background:rgba(255,255,255,0.03);border:1px solid rgba(255,255,255,0.06);border-radius:10px;padding:16px 20px;transition:all 0.15s}
    .modulo-card:hover{border-color:#C79A2E;box-shadow:0 2px 12px rgba(199,154,46,0.12)}
    .mod-num{font-size:11px;font-weight:700;color:#C79A2E;text-transform:uppercase;letter-spacing:1px;margin-bottom:4px}
    .mod-name{font-size:15px;font-weight:600;color:#fff}
    .cta-section{background:#0D1B2A;padding:48px 0;text-align:center;border-top:1px solid rgba(199,154,46,0.1)}
    .cta-section h2{font-family:'Libre Baskerville',serif;font-size:30px;color:#fff;margin-bottom:12px}
    .cta-section p{color:rgba(255,255,255,0.6);margin-bottom:28px;font-size:16px}
    .btn-gold{display:inline-block;padding:14px 40px;background:#C79A2E;color:#0D1B2A;border-radius:8px;font-size:15px;font-weight:700;transition:all 0.2s;text-decoration:none}
    .btn-gold:hover{background:#d4a83a;transform:translateY(-1px)}
    .btn-outline{display:inline-block;padding:14px 36px;border:1px solid rgba(255,255,255,0.2);color:rgba(255,255,255,0.8);border-radius:8px;font-size:14px;font-weight:600;transition:all 0.2s;margin-left:12px;text-decoration:none}
    .btn-outline:hover{border-color:#C79A2E;color:#C79A2E}

    @media(max-width:768px){
      .netflix-hero{min-height:75vh}
      .netflix-hero-content{padding:0 24px}
      .netflix-hero-content h1{font-size:36px}
      .netflix-hero-desc{font-size:16px}
      .cta-section h2{font-size:24px}
    }
'''

def build_netflix_hero(slug, data):
    return f'''  <section class="netflix-hero">
    <img class="netflix-hero-bg" src="../img/cursos/{slug}.png" alt="{data['title']}">
    <div class="netflix-hero-overlay"></div>
    <div class="netflix-hero-content">
      <span class="netflix-hero-badge">Curso de Formação Ministerial</span>
      <h1>{data['title']}</h1>
      <p class="netflix-hero-desc">{data['desc']}</p>
      <div class="netflix-hero-stats">
        <span><strong>{data['hours']}</strong> Carga Horária</span>
        <span class="dot">·</span>
        <span><strong>{data['modules']}</strong> Módulos</span>
        <span class="dot">·</span>
        <span>100% Online</span>
        <span class="dot">·</span>
        <span>Certificado MIRC</span>
      </div>
      <div class="netflix-hero-actions">
        <a href="https://cursos.institutolumethos.online/checkout/{data['checkout']}" class="netflix-btn-play">▶ Matricular Agora</a>
        <a href="#sobre" class="netflix-btn-info">ℹ Saiba Mais</a>
      </div>
    </div>
  </section>'''


def build_sections_after_hero(data):
    sec = data['sections_after_hero']
    # We need to remove the duplicate diff cards that exist in some files
    return f'''  <section class="section dark" id="sobre">
    <div class="container">
      <div class="section-tag">Sobre o Curso</div>
      <h2 class="section-title">{data['title']}</h2>
      <div class="desc-text">{sec['sobre_desc']}</div>
      {sec['diferenciais']}
    </div>
  </section>

  <section class="section darker">
    <div class="container">
      <div class="section-tag">Conteúdo Programático</div>
      <h2 class="section-title">{sec['modulos_title']}</h2>
      {sec['modulos']}
    </div>
  </section>'''


for slug, data in courses.items():
    filepath = os.path.join(COURSES_DIR, f'{slug}.html')
    with open(filepath, 'r') as f:
        content = f.read()

    # 1. Replace old style block with new Netflix-style block
    # Match from the first "*{margin" style to the closing </style> before </head>
    content = re.sub(
        r'  <style>\n    \*\{margin:0;padding:0;box-sizing:border-box\}.*?\n  </style>',
        f'  <style>{NEW_STYLE}  </style>',
        content,
        flags=re.DOTALL
    )

    # 2. Replace the old curso-hero section
    content = re.sub(
        r'  <section class="curso-hero">.*?</section>',
        build_netflix_hero(slug, data),
        content,
        flags=re.DOTALL
    )

    # 3. Replace the sections after hero (first white section + first gray section)
    # Find and replace the "Sobre o Curso" section
    old_sobre_pattern = r'  <section class="section white">.*?</section>'
    content = re.sub(old_sobre_pattern, '', content, flags=re.DOTALL)

    old_gray_pattern = r'  <section class="section gray">.*?</section>'
    content = re.sub(old_gray_pattern, '', content, flags=re.DOTALL)

    # 4. Insert the new dark sections after the hero and before CTA
    # Find the CTA section and insert before it
    cta_marker = '  <section class="cta-section">'
    new_sections = build_sections_after_hero(data)
    content = content.replace(cta_marker, new_sections + '\n\n  ' + cta_marker)

    # 5. Fix dropdown navbar inline styles - change background from #fff to #0D1B2A
    # Find the dropdown ul and fix colors
    content = content.replace(
        'background:#fff;border:1px solid rgba(13,27,42,0.08)',
        'background:#0D1B2A;border:1px solid rgba(199,154,46,0.15)'
    )
    # Fix box-shadow to be darker
    content = content.replace(
        'box-shadow:0 12px 40px rgba(0,0,0,0.12)',
        'box-shadow:0 12px 40px rgba(0,0,0,0.5)'
    )
    # Fix dropdown link text colors from #0D1B2A to #fff for normal links
    content = content.replace(
        'color:#0D1B2A;font-size:13.5px;font-weight:500',
        'color:#fff;font-size:13.5px;font-weight:500'
    )
    # Keep the "Ver Todos" link gold
    content = content.replace(
        'color:#C79A2E;font-size:13.5px;font-weight:700;text-decoration:none;border-bottom:1px solid rgba(13,27,42,0.06)',
        'color:#C79A2E;font-size:13.5px;font-weight:700;text-decoration:none;border-bottom:1px solid rgba(199,154,46,0.15)'
    )

    with open(filepath, 'w') as f:
        f.write(content)

    print(f'✅ Updated {slug}.html')

print('\n🎉 All 9 course pages updated with Netflix-style hero!')

import os, re

CSS_BLOCK = '''<!-- DROPDOWN LUMETHOS -->
<style>
.nav-item.dropdown { position: relative; }
.nav-item.dropdown .dropdown-menu {
  display: none !important;
  position: absolute !important;
  top: 100% !important;
  left: 50% !important;
  transform: translateX(-50%) !important;
  background: #fff !important;
  border: 1px solid rgba(13,27,42,0.08) !important;
  border-radius: 12px !important;
  padding: 8px !important;
  min-width: 230px !important;
  box-shadow: 0 12px 40px rgba(0,0,0,0.12) !important;
  z-index: 9999 !important;
  list-style: none !important;
  margin: 8px 0 0 !important;
}
.nav-item.dropdown:hover .dropdown-menu {
  display: block !important;
}
.nav-item.dropdown .dropdown-arrow {
  font-size: 10px;
  margin-left: 4px;
  display: inline-block;
  transition: transform 0.2s;
}
.nav-item.dropdown:hover .dropdown-arrow {
  transform: rotate(180deg);
}
.dropdown-menu li { margin: 0 !important; }
.dropdown-link {
  display: block !important;
  padding: 10px 14px !important;
  color: #0D1B2A !important;
  font-size: 13.5px !important;
  font-weight: 500 !important;
  text-decoration: none !important;
  border-radius: 8px !important;
  white-space: nowrap !important;
  line-height: 1.4 !important;
}
.dropdown-link:hover { background: rgba(199,154,46,0.08) !important; color: #C79A2E !important; }
.dropdown-link:first-child { font-weight: 700 !important; color: #C79A2E !important; border-bottom: 1px solid rgba(13,27,42,0.06) !important; margin-bottom: 4px !important; padding-bottom: 12px !important; }
@media (max-width: 1023px) {
  .nav-item.dropdown .dropdown-menu {
    position: static !important;
    transform: none !important;
    background: transparent !important;
    border: none !important;
    box-shadow: none !important;
    padding: 0 0 0 16px !important;
    min-width: auto !important;
    margin: 0 !important;
  }
  .nav-item.dropdown:hover .dropdown-menu { display: none !important; }
  .nav-item.dropdown.open .dropdown-menu { display: block !important; }
  .dropdown-link { color: rgba(255,255,255,0.85) !important; font-size: 14px !important; padding: 8px 14px !important; }
  .dropdown-link:first-child { color: #C79A2E !important; border-bottom: 1px solid rgba(255,255,255,0.1) !important; }
}
</style>'''

JS_BLOCK = '''<script>
document.addEventListener('DOMContentLoaded', function(){
  var dd = document.querySelectorAll('.nav-item.dropdown > a');
  dd.forEach(function(link){
    link.addEventListener('click', function(e){
      if(window.innerWidth < 1024) {
        e.preventDefault();
        this.parentElement.classList.toggle('open');
      }
    });
  });
  document.addEventListener('click', function(e){
    if(!e.target.closest('.nav-item.dropdown')){
      document.querySelectorAll('.nav-item.dropdown.open').forEach(function(el){
        el.classList.remove('open');
      });
    }
  });
});
</script>'''

pages = ['index.html', 'capelania.html', 'escolas.html', 'biblioteca.html',
         'sobre.html', 'centelhaz.html', 'studio.html', 'teologia.html',
         'diaconia.html', 'cursos.html']

for p in pages:
    path = '/var/www/lumethos/' + p
    if not os.path.exists(path):
        print(f'{p}: not found')
        continue
    content = open(path).read()
    
    # Add CSS before </head>
    if 'DROPDOWN LUMETHOS' not in content:
        content = content.replace('</head>', CSS_BLOCK + '\n</head>')
    
    # Add JS before </body>
    if 'DROPDOWN JS' not in content:
        content = content.replace('</body>', JS_BLOCK + '\n</body>')
    
    open(path, 'w').write(content)
    print(f'{p}: OK')

# Pages inside cursos/
for p in ['capelania', 'teologia', 'pastoral', 'diaconal', 'hinologia',
          'infantil', 'jovens', 'patristica', 'historia-igreja']:
    path = '/var/www/lumethos/cursos/' + p + '.html'
    if not os.path.exists(path):
        print(f'cursos/{p}.html: not found')
        continue
    content = open(path).read()
    if 'DROPDOWN LUMETHOS' not in content:
        content = content.replace('</head>', CSS_BLOCK + '\n</head>')
    if 'DROPDOWN JS' not in content:
        content = content.replace('</body>', JS_BLOCK + '\n</body>')
    open(path, 'w').write(content)
    print(f'cursos/{p}.html: OK')

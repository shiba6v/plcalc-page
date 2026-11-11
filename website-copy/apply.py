from pathlib import Path
import json,re,html,shutil

def apply_landing(s,c):
    esc=html.escape
    s=re.sub(r'(<h1\b[^>]*>).*?(</h1>)',lambda m:m[1]+esc(c['headline'])+m[2],s,count=1,flags=re.S)
    ps=list(re.finditer(r'(<p\b[^>]*>).*?(</p>)',s,re.S))
    p=ps[1];s=s[:p.start()]+p[1]+esc(c['lead'])+p[2]+s[p.end():]
    s=re.sub(r'<title>.*?</title>','<title>'+esc(c['title'])+'</title>',s,count=1,flags=re.S)
    def meta(m):
        t=m[0]
        if re.search(r'(?:name|property)=[\"\x27](?:description|og:description|twitter:description)[\"\x27]',t):value=c['description']
        elif re.search(r'(?:name|property)=[\"\x27](?:og:title|twitter:title)[\"\x27]',t):value=c['title']
        else:return t
        return re.sub(r'content=([\"\x27]).*?\1',lambda _: 'content="'+esc(value,quote=True)+'"',t)
    s=re.sub(r'<meta\b[^>]*>',meta,s)
    def schema(m):
        try:d=json.loads(m[2])
        except ValueError:return m[0]
        if isinstance(d,dict) and d.get('@type') in ['SoftwareApplication','MobileApplication']:
            d['description']=c['description']
            if c['app']=='meishi':d['softwareVersion']='1.5.0'
        return m[1]+json.dumps(d,ensure_ascii=False)+m[3]
    s=re.sub(r'(<script\b[^>]*type="application/ld\+json"[^>]*>)(.*?)(</script>)',schema,s,flags=re.S)
    card='<section class="web-guide-link" aria-label="使い方の記事"><p>画面で見る使い方</p><a href="'+esc(c['article_path'])+'">'+esc(c['article'])+' →</a></section>'
    s=re.sub(r'<section class="web-guide-link"[^>]*>.*?</section>','',s,flags=re.S)
    # Keep the link next to the existing usage section.
    m=re.search(r'<section\b[^>]*id="(?:how-to|how|quiz)"[^>]*>.*?</section>',s,re.S)
    if m:s=s[:m.end()]+card+s[m.end():]
    else:
        m=re.search(r'<section\b[^>]*class="[^"]*walkthrough[^"]*"[^>]*>.*?</section>',s,re.S)
        if m:s=s[:m.end()]+card+s[m.end():]
        else:s=s.replace('</main>',card+'</main>',1)
    css='<style id="web-guide-link-style">.web-guide-link{box-sizing:border-box;max-width:1080px;margin:32px auto;padding:24px;border:1px solid #d4e1e2;border-radius:16px;background:#f1f7f7;color:#173b41}.web-guide-link p{font-size:13px;margin:0 0 6px}.web-guide-link a{font-size:20px;font-weight:700;line-height:1.6;color:#086b78;text-decoration:underline;text-underline-offset:4px}@media(max-width:700px){.web-guide-link{margin:24px 18px;padding:20px}}</style>'
    if 'id="web-guide-link-style"' not in s:s=s.replace('</head>',css+'</head>',1)
    return s

def restore(base):
    c=json.loads((base/'config.json').read_text());root=base.parent
    home=root/c['home'];site=root/c['site']
    home.write_text(apply_landing(home.read_text(),c))
    dst=site/c['slug']/'index.html';dst.parent.mkdir(parents=True,exist_ok=True)
    shutil.copyfile(base/'article.html',dst)
    sm=site/'sitemap.xml';s=sm.read_text()
    if c['article_url'] not in s:s=s.replace('</urlset>','<url><loc>'+html.escape(c['article_url'])+'</loc><lastmod>2026-11-11</lastmod></url></urlset>')
    sm.write_text(s)

if __name__=='__main__':restore(Path(__file__).resolve().parent)

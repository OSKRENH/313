from __future__ import annotations

import json
import urllib.request
from pathlib import Path

from bs4 import BeautifulSoup

URL = "https://go313.ru/"
ROOT = Path(".")

request = urllib.request.Request(URL, headers={"User-Agent": "Mozilla/5.0"})
with urllib.request.urlopen(request, timeout=40) as response:
    html = response.read().decode("utf-8", errors="replace")

soup = BeautifulSoup(html, "html.parser")

manual_meta = [
    ("Квартира Хюгге", "Миасс"),
    ("Салон красоты", "Увильды"),
    ("Баня", "Челябинск"),
    ("Квартира на Лесопарковой", "Челябинск"),
    ("Книжный магазин и кофейня", "Екатеринбург"),
    ("Салон массажа и медитации", "Челябинская область"),
    ("Летнее кафе", "Москва"),
    ("Апартаменты", "Челябинск"),
    ("Эстетическая косметология", "Массандра"),
    ("Загородный дом", "Тель-Авив"),
    ("Свадебный шоурум", "Челябинск"),
    ("Home Sweet Home", "Челябинск"),
    ("Квартира", "Челябинск"),
    ("Квартира", "Челябинск"),
]


def image_urls(element):
    urls = []
    if not element:
        return urls
    for node in element.select('[data-img-zoom-url], [data-original], meta[itemprop="image"]'):
        for attribute in ("data-img-zoom-url", "data-original", "content"):
            value = node.get(attribute)
            if value and "static.tildacdn.com" in value and value not in urls:
                urls.append(value)
    return urls


raw_projects = []
for card in soup.select("#rec739874198 li.t-card__col"):
    link = card.select_one('a.t-card__link[href^="#rec"]')
    if not link:
        continue
    target = soup.select_one(link.get("href"))
    images = image_urls(target)
    if not images and target:
        images = image_urls(target.find_next_sibling("div", class_="t-rec"))
    cover_node = card.select_one("[data-original]")
    cover = cover_node.get("data-original") if cover_node else (images[0] if images else "")
    if cover and cover not in images:
        images.insert(0, cover)
    raw_projects.append({"cover": cover, "images": images})

if len(raw_projects) < len(manual_meta):
    raise RuntimeError(f"Expected at least {len(manual_meta)} project cards, got {len(raw_projects)}")

projects = []
for (title, location), raw in zip(manual_meta, raw_projects):
    projects.append({
        "title": title,
        "location": location,
        "cover": raw["cover"],
        "images": raw["images"],
    })

js_template = r'''const projects=__PROJECTS__;
const grid=document.querySelector('[data-project-grid]');
const sentinel=document.querySelector('[data-project-sentinel]');
const endLabel=document.querySelector('[data-projects-end]');
const dialog=document.querySelector('[data-project-dialog]');
const dialogTitle=document.querySelector('[data-dialog-title]');
const dialogLocation=document.querySelector('[data-dialog-location]');
const dialogGallery=document.querySelector('[data-dialog-gallery]');
const closeDialogButton=document.querySelector('[data-dialog-close]');
const batchSize=4;let rendered=0,loading=false,projectObserver,scrollScheduled=false;
const revealObserver='IntersectionObserver'in window?new IntersectionObserver(entries=>{entries.forEach(entry=>{if(!entry.isIntersecting)return;entry.target.classList.add('is-visible');revealObserver.unobserve(entry.target)})},{threshold:.06,rootMargin:'0px 0px -2%'}):null;
function observeReveals(){document.querySelectorAll('.reveal:not(.is-visible)').forEach(element=>{if(revealObserver)revealObserver.observe(element);else element.classList.add('is-visible')})}
function handleImageError(image){image.closest('.project-media, figure, .author-photo')?.classList.add('image-missing');image.remove()}
function makeProjectCard(project,index){const article=document.createElement('article');article.className='project-card reveal';article.innerHTML=`<button class="project-button" type="button" aria-label="Открыть проект ${project.title}"><div class="project-media"><img src="${project.cover}" alt="${project.title}, ${project.location}" loading="lazy" decoding="async"><span class="project-number">${String(index+1).padStart(2,'0')}</span></div><div class="project-meta"><div><h3>${project.title}</h3><p>${project.location}</p></div><span class="project-count">${project.images.length} фото</span></div></button>`;article.querySelector('img').addEventListener('error',event=>handleImageError(event.currentTarget));article.querySelector('button').addEventListener('click',()=>openProject(project));return article}
function loadNextBatch(){if(loading||rendered>=projects.length||!grid)return;loading=true;const next=projects.slice(rendered,rendered+batchSize),fragment=document.createDocumentFragment();next.forEach((project,localIndex)=>fragment.append(makeProjectCard(project,rendered+localIndex)));grid.append(fragment);rendered+=next.length;observeReveals();loading=false;if(rendered>=projects.length){if(sentinel)sentinel.hidden=true;if(endLabel)endLabel.hidden=false;projectObserver?.disconnect();window.removeEventListener('scroll',scheduleScrollCheck)}else requestAnimationFrame(maybeLoadMore)}
function maybeLoadMore(){if(!sentinel||rendered>=projects.length)return;const rect=sentinel.getBoundingClientRect();if(rect.top<window.innerHeight+1200)loadNextBatch()}
function scheduleScrollCheck(){if(scrollScheduled)return;scrollScheduled=true;requestAnimationFrame(()=>{scrollScheduled=false;maybeLoadMore()})}
function openProject(project){if(!dialog)return;dialogTitle.textContent=project.title;dialogLocation.textContent=project.location;dialogGallery.replaceChildren();project.images.forEach((src,index)=>{const figure=document.createElement('figure'),image=document.createElement('img');image.src=src;image.alt=`${project.title} — изображение ${index+1}`;image.loading=index<2?'eager':'lazy';image.decoding='async';image.addEventListener('error',()=>handleImageError(image));figure.append(image);dialogGallery.append(figure)});dialog.showModal();document.body.classList.add('dialog-open');dialog.scrollTop=0}
function closeProject(){if(!dialog?.open)return;dialog.close();document.body.classList.remove('dialog-open')}
closeDialogButton?.addEventListener('click',closeProject);dialog?.addEventListener('click',event=>{if(event.target===dialog)closeProject()});dialog?.addEventListener('cancel',()=>document.body.classList.remove('dialog-open'));
if('IntersectionObserver'in window&&sentinel){projectObserver=new IntersectionObserver(entries=>{if(entries.some(entry=>entry.isIntersecting))loadNextBatch()},{rootMargin:'1200px 0px 1200px',threshold:0});projectObserver.observe(sentinel)}
window.addEventListener('scroll',scheduleScrollCheck,{passive:true});window.addEventListener('resize',scheduleScrollCheck,{passive:true});loadNextBatch();observeReveals();requestAnimationFrame(maybeLoadMore);
const header=document.querySelector('[data-header]'),menuButton=document.querySelector('.menu-toggle'),nav=document.querySelector('.site-nav');
function updateHeader(){header?.classList.toggle('is-scrolled',window.scrollY>40)}
function closeMenu(){menuButton?.setAttribute('aria-expanded','false');nav?.classList.remove('is-open');header?.classList.remove('menu-open');document.body.classList.remove('menu-open')}
function toggleMenu(){const isOpen=menuButton?.getAttribute('aria-expanded')==='true';if(isOpen){closeMenu();return}menuButton?.setAttribute('aria-expanded','true');nav?.classList.add('is-open');header?.classList.add('menu-open');document.body.classList.add('menu-open')}
updateHeader();window.addEventListener('scroll',updateHeader,{passive:true});menuButton?.addEventListener('click',toggleMenu);nav?.querySelectorAll('a').forEach(link=>link.addEventListener('click',closeMenu));window.addEventListener('keydown',event=>{if(event.key==='Escape'){closeMenu();closeProject()}});
const form=document.querySelector('[data-contact-form]'),formStatus=document.querySelector('[data-form-status]');form?.addEventListener('submit',event=>{event.preventDefault();if(!form.reportValidity())return;const data=new FormData(form),subject=encodeURIComponent(`Новый запрос на дизайн-проект — ${data.get('name')}`),body=encodeURIComponent([`Имя: ${data.get('name')}`,`Способ связи: ${data.get('method')}`,`Контакт: ${data.get('contact')}`,'',String(data.get('message'))].join('\n'));formStatus.textContent='Открываем почтовое приложение…';window.location.href=`mailto:hello@we313.ru?subject=${subject}&body=${body}`});
const year=document.querySelector('[data-year]');if(year)year.textContent=new Date().getFullYear();
'''

css = r'''.brand-logo-svg{display:block;width:70px;height:auto}.brand{gap:0}.brand-note{display:none}.section-head--single{grid-template-columns:1fr;gap:0}.footer-brand{font-size:clamp(72px,12vw,180px);line-height:.7;letter-spacing:-.08em;font-weight:700}.hero--tilda{position:relative;min-height:100svh;background:#15363d;color:var(--white);overflow:hidden;isolation:isolate}.hero-art{position:absolute;inset:0;z-index:0;background:#15363d url('assets/hero-pattern.svg') center/cover no-repeat}.hero-art img{display:none}.hero-art::after{content:none}.hero-content--tilda{position:relative;z-index:2;min-height:100svh;display:flex;flex-direction:column;padding:clamp(118px,14vh,158px) var(--pad) 44px}.hero-lockup{width:min(58vw,860px);margin-top:clamp(20px,5vh,58px)}.hero-logo-large{display:block;width:100%;height:auto;object-fit:contain}.hero-bottom--tilda{margin-top:auto}.hero-bottom--tilda p{max-width:520px}.site-header:not(.is-scrolled){background:transparent;border-color:transparent}.site-header:not(.is-scrolled) .header-cta{background:rgba(250,250,248,.92);padding:14px 28px;border-radius:999px;color:var(--ink)}.site-header:not(.is-scrolled) .header-cta::after{display:none}.site-header.is-scrolled .header-cta{padding:0;background:transparent;border-radius:0}.project-media{background:#d7d3ca;overflow:hidden}.project-media img{width:100%;height:100%;object-fit:cover}.project-card{content-visibility:visible}.project-sentinel[hidden],.projects-end[hidden]{display:none!important}@media(max-width:980px){:root{--pad:clamp(20px,5vw,36px)}html,body{max-width:100%;overflow-x:hidden}body.menu-open,body.dialog-open{overflow:hidden;touch-action:none}.site-header{grid-template-columns:1fr auto;min-height:86px;padding:14px var(--pad);gap:18px}.site-header.is-scrolled{min-height:74px}.brand{position:relative;z-index:72}.brand-logo-svg{width:104px}.header-cta{display:none}.menu-toggle{position:relative;z-index:72;display:block;justify-self:end;width:52px;height:52px;padding:12px;border:0;background:transparent}.menu-toggle span:not(.sr-only){position:absolute;left:12px;width:28px;height:1px;margin:0;background:currentColor}.menu-toggle span:not(.sr-only):first-child{top:20px}.menu-toggle span:not(.sr-only):nth-child(2){top:31px}.menu-toggle[aria-expanded="true"] span:not(.sr-only):first-child{top:26px;transform:rotate(45deg)}.menu-toggle[aria-expanded="true"] span:not(.sr-only):nth-child(2){top:26px;transform:rotate(-45deg)}.site-nav{position:fixed;inset:0;z-index:70;display:flex;flex-direction:column;align-items:flex-start;justify-content:flex-start;gap:0;padding:130px var(--pad) 48px;background:#15363d;color:var(--paper);visibility:hidden;opacity:0;pointer-events:none;transform:none;transition:opacity .28s var(--ease),visibility .28s}.site-nav.is-open{visibility:visible;opacity:1;pointer-events:auto}.site-nav a{display:block;width:100%;padding:18px 0;border-bottom:1px solid rgba(241,238,231,.28);font-size:clamp(36px,9vw,64px);line-height:.95;letter-spacing:-.045em;text-transform:uppercase}.site-nav a::after{display:none}.site-header.menu-open{color:var(--paper)!important;background:#15363d!important;border-color:rgba(241,238,231,.2)!important;backdrop-filter:none}.site-header.menu-open .brand-logo-svg{color:var(--paper)}.hero--tilda,.hero-content--tilda{min-height:100dvh}.hero-content--tilda{padding:112px var(--pad) 34px}.hero-lockup{width:min(78vw,680px);margin-top:8vh}.hero-bottom--tilda{grid-template-columns:minmax(0,1fr) 64px;gap:20px}.hero-bottom--tilda p{font-size:18px;line-height:1.35}.round-link{width:62px;height:62px}.section{padding:88px var(--pad)}.section-head{grid-template-columns:1fr;gap:26px;margin-bottom:52px}.section h2{font-size:clamp(44px,12vw,82px)}.authors-grid,.price-layout,.contact-layout{grid-template-columns:1fr}.author-card:nth-child(2){margin-top:24px}.scope-list li{grid-template-columns:52px 1fr;gap:12px 18px}.scope-list li p{grid-column:2}.price-layout,.contact-layout{gap:56px}.project-grid{grid-template-columns:1fr;gap:54px}.project-card,.project-card:nth-child(n){grid-column:1;margin-top:0}.project-media,.project-card:nth-child(n) .project-media{aspect-ratio:4/3}.project-meta{gap:14px}.project-meta h3{font-size:clamp(26px,7vw,40px)}.project-count{font-size:10px}.project-sentinel{height:140px}.dialog-shell{padding:0 var(--pad) 48px}.dialog-header{min-height:96px;padding:18px 0}.dialog-header h2{font-size:clamp(30px,9vw,54px)}.dialog-close{width:46px;height:46px;font-size:30px}.dialog-gallery{grid-template-columns:1fr;gap:18px;padding-top:20px}.dialog-gallery figure,.dialog-gallery figure:nth-child(even){grid-column:1;margin-top:0}.dialog-gallery img{width:100%;height:auto;min-height:0;max-height:none;object-fit:contain}}@media(max-width:700px){.site-header{min-height:78px}.site-header.is-scrolled{min-height:68px}.brand-logo-svg{width:102px}.hero-art{background-image:url('assets/hero-pattern-mobile.svg');background-position:center;background-size:cover}.hero-content--tilda{min-height:max(720px,100dvh);padding:100px 22px 28px}.hero-lockup{width:84vw;max-width:590px;margin-top:12vh}.hero-bottom--tilda{grid-template-columns:1fr 58px;align-items:end;margin-top:auto}.hero-bottom--tilda p{font-size:16px;line-height:1.45}.round-link{width:56px;height:56px;font-size:22px}.section{padding:76px 22px}.section h2{font-size:clamp(42px,13vw,70px)}.eyebrow{font-size:10px}.project-grid{gap:48px}.project-media,.project-card:nth-child(n) .project-media{aspect-ratio:1/1}.project-meta{grid-template-columns:minmax(0,1fr) auto;padding-top:13px;margin-top:11px}.project-meta h3{font-size:28px;line-height:.98}.project-meta p{font-size:10px}.project-count{padding-top:2px}.site-footer{grid-template-columns:1fr;align-items:start}.site-footer>a:last-child{justify-self:start}.scope-list li{grid-template-columns:38px 1fr;padding:22px 0}.scope-list h3{font-size:25px}.contact-methods{gap:7px}.contact-methods span{padding:10px 14px}.dialog-header{align-items:flex-start}.dialog-header .eyebrow{margin-bottom:5px}.dialog-close{flex:0 0 auto}}@media(max-width:380px){.hero-lockup{width:88vw}.hero-bottom--tilda p{font-size:15px}.project-meta h3{font-size:25px}.site-nav a{font-size:34px}}@media(prefers-reduced-motion:reduce){.site-nav,.menu-toggle span,.project-media img{transition:none!important}}
'''

desktop_svg = '''<?xml version="1.0" encoding="UTF-8"?>
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1920 1080" preserveAspectRatio="xMidYMid slice"><rect width="1920" height="1080" fill="#15363d"/><defs><path id="p" d="M0 0 A280 280 0 0 1 280 280 A280 280 0 0 1 0 0Z"/></defs><g transform="translate(360 720)"><use href="#p" transform="rotate(180)" fill="#045a76"/><use href="#p" transform="rotate(-90)" fill="#13a7c4"/><use href="#p" transform="rotate(90)" fill="#d2e9e5"/><use href="#p" fill="#13a7c4"/></g><g transform="translate(920 720)"><use href="#p" transform="rotate(180)" fill="#58ad9d"/><use href="#p" transform="rotate(90)" fill="#d2e9e5"/><use href="#p" fill="#045a76"/></g><g transform="translate(1200 440)"><use href="#p" transform="rotate(180)" fill="#58ad9d"/><use href="#p" transform="rotate(-90)" fill="#d2e9e5"/><use href="#p" transform="rotate(90)" fill="#13a7c4"/><use href="#p" fill="#58ad9d"/></g><g transform="translate(1480 720)"><use href="#p" transform="rotate(-90)" fill="#13a7c4"/><use href="#p" transform="rotate(90)" fill="#58ad9d"/><use href="#p" fill="#58ad9d"/></g><g transform="translate(2040 720)"><use href="#p" transform="rotate(180)" fill="#045a76"/><use href="#p" transform="rotate(90)" fill="#13a7c4"/></g></svg>'''

mobile_svg = '''<?xml version="1.0" encoding="UTF-8"?>
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 750 1334" preserveAspectRatio="xMidYMid slice"><rect width="750" height="1334" fill="#15363d"/><defs><path id="p" d="M0 0 A230 230 0 0 1 230 230 A230 230 0 0 1 0 0Z"/></defs><g transform="translate(660 330)"><use href="#p" transform="rotate(180)" fill="#58ad9d"/><use href="#p" transform="rotate(-90)" fill="#d2e9e5"/><use href="#p" transform="rotate(90)" fill="#13a7c4"/><use href="#p" fill="#045a76"/></g><g transform="translate(105 850)"><use href="#p" transform="rotate(180)" fill="#045a76"/><use href="#p" transform="rotate(-90)" fill="#13a7c4"/><use href="#p" transform="rotate(90)" fill="#d2e9e5"/><use href="#p" fill="#58ad9d"/></g><g transform="translate(565 930)"><use href="#p" transform="rotate(180)" fill="#13a7c4"/><use href="#p" transform="rotate(-90)" fill="#58ad9d"/><use href="#p" transform="rotate(90)" fill="#045a76"/><use href="#p" fill="#58ad9d"/></g><g transform="translate(335 1290)"><use href="#p" transform="rotate(180)" fill="#d2e9e5"/><use href="#p" transform="rotate(-90)" fill="#58ad9d"/></g></svg>'''

(ROOT / "script.js").write_text(js_template.replace("__PROJECTS__", json.dumps(projects, ensure_ascii=False, separators=(",", ":"))), encoding="utf-8")
(ROOT / "hero-tilda.css").write_text(css, encoding="utf-8")
(ROOT / "assets").mkdir(exist_ok=True)
(ROOT / "assets" / "hero-pattern.svg").write_text(desktop_svg, encoding="utf-8")
(ROOT / "assets" / "hero-pattern-mobile.svg").write_text(mobile_svg, encoding="utf-8")
print(f"Built {len(projects)} projects with {sum(len(project['images']) for project in projects)} images")

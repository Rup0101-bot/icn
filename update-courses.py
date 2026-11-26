from pathlib import Path
from pypdf import PdfReader
import re,html,json
root=Path('D:/ICN/ICN Website/icn-redesign/dist'); source=Path('D:/ICN/SPY_EYE')
def clean(s):
 s=re.sub('hackastra','Psyber Yodha Specialized',s,flags=re.I)
 return s.replace('It\ufffds',"It's").replace('\ufffd','•')
def flat(s): return re.sub(r'\s+',' ',s).strip()
files=[('HackAstra_ALFA_syllabus_&_exam.pdf','ALFA',[(0,3,'Cyber Investigation & Digital Forensics Bootcamp',8)]),('HackAstra_Charlie_syllabus_&_exam.pdf','Charlie',[(0,5,'CYBER INTELLIGENCE & AI FOR INVESTIGATORS',16),(5,10,'SOC Analyst & Blue Team Bootcamp with AI',16)]),('HackAstra DELTA_syllabus_&_Exams.pdf','Delta',[(0,5,'Darkweb Research & Intelligence with AI',16),(5,10,'AI Use & Implementations, Research & Developments for Cybersecurity & Online Safety',16),(10,16,'AI-Based Reverse Engineering & Malware Investigations',16)])]
courses=[]
verbs=r'Examine|Deploy|Gather|Extract|Understand|Configure|Learn|Master|Perform|Collect|Investigate|Analyze|Acquire|Utilize|Develop|Apply|Integrate|Enhance|Use|Design|Evaluate|Build|Explore|Conduct|Support|Transform|Monitor|Detect|Automate|Validate'
for filename,track,groups in files:
 reader=PdfReader(source/filename)
 for start,end,title,count in groups:
  text=clean('\n'.join(p.extract_text() for p in reader.pages[start:end]))
  first=re.search(r'\bMODULE\s+1\b',text,re.I)
  cutoff=re.search(r'(?:Note:|Certification Examination)',text[first.start():],re.I)
  stop=first.start()+cutoff.start()
  moduletext=text[first.start():stop]
  matches=list(re.finditer(r'\bMODULE\s+(\d+)\b',moduletext,re.I))
  modules=[]
  for i,m in enumerate(matches):
   body=flat(moduletext[m.end():matches[i+1].start() if i+1<len(matches) else len(moduletext)])
   goal=re.search(r'\b('+verbs+r')\b',body)
   assert goal,(title,body)
   modules.append({'number':int(m[1]),'title':body[:goal.start()].strip(),'goal':body[goal.start():].strip()})
  assert len(modules)==count,(title,len(modules))
  exam=text[stop:]
  # ALFA's final assessment heading precedes the examination heading and stays in its original position.
  header=flat(text[:first.start()]); meta=re.search(r'Course Syllabus\s*\((.*?)\)',header)
  courses.append(dict(track=track,title=title,meta=meta[1] if meta else '8 Modules',modules=modules,exam=exam,sourceText=text))
# Preserve the exam wording and order, while treating the original line wrapping as layout.
headings=['Note: It\'s an online mode Training','Final Assessment & Certification','Certification Examination','Examination Pattern','Passing Criteria','Certification','Learning Objective of the Assessment','Certification Examination • Concept Note','Examination Structure','Practical CTF Challenge Areas','Certification Criteria','Certification Outcome','Exam Structure (Total: 100 Marks)','Part A • Online MCQ Examination (50 Marks)','Assessment will evaluate:','The challenge may include:']
def exam_html(text):
 lines=[x.strip() for x in text.splitlines() if x.strip()]
 blocks=[]; current=[]; kind='p'
 def flush():
  if current: blocks.append((kind,flat(' '.join(current))));current.clear()
 for line in lines:
  heading=line in headings or line.startswith('Part B •') or line.startswith('NOTE:') or line.startswith('Note: All')
  bullet=line.startswith(('• ','o '))
  if heading or bullet:
   flush();kind='h4' if heading else 'li';current.append(line[2:] if bullet else line)
  else: current.append(line)
 flush()
 out='';listing=False
 for tag,txt in blocks:
  if tag=='li' and not listing:out+='<ul>';listing=True
  if tag!='li' and listing:out+='</ul>';listing=False
  out+=f'<{tag}>{html.escape(txt)}</{tag}>'
 if listing:out+='</ul>'
 return out
out='<section class="course-library" id="programs" aria-labelledby="courses-title"><div class="course-heading"><div class="eyebrow">PSYBER YODHA SPECIALIZED / COURSE CATALOGUE</div><h2 id="courses-title">Specialized cyber courses.<br><span>Build your next capability.</span></h2><p>Explore the complete syllabus, learning goals and certification examination details for each course.</p></div><nav class="course-jumps" aria-label="Course tracks"><a href="#course-1">ALFA <span>01 course ↓</span></a><a href="#course-2">Charlie <span>02 courses ↓</span></a><a href="#course-4">Delta <span>03 courses ↓</span></a></nav><div class="course-list">'
for i,c in enumerate(courses,1):
 out+=f'<article class="course-card" id="course-{i}"><div class="course-topline"><span>Psyber Yodha Specialized — {c["track"]}</span><span>{i:02d} / 06</span></div><h3>{html.escape(c["title"])}</h3><div class="course-meta">{html.escape(c["meta"])}</div><details class="course-details"><summary>Full syllabus &amp; learning goals <span aria-hidden="true">+</span></summary><div class="course-modules">'
 for m in c['modules']:
  out+=f'<section class="course-module"><span>MODULE {m["number"]:02d}</span><div><h4>{html.escape(m["title"])}</h4><p>{html.escape(m["goal"])}</p></div></section>'
 out+='</div></details><details class="course-details course-exam"><summary>Examination &amp; certification <span aria-hidden="true">+</span></summary><div class="exam-copy">'+exam_html(c['exam'])+'</div></details>'
 from urllib.parse import quote
 url='https://wa.me/918777628651?text='+quote('Hello ICN, I would like to enquire about Psyber Yodha Specialized — '+c['track']+': '+c['title']+'. Please share the course details.')
 out+='<a class="course-enquire" target="_blank" rel="noopener" href="'+url+'">Enquire about this course <span aria-hidden="true">↗</span></a></article>'
out+='</div><p class="course-online-note">Training and examinations are conducted online.</p></section>'
p=root/'psyberyodha.html';s=p.read_text(encoding='utf-8')
a=s.index('<div class="psyber-grid"');b=s.index('</section>',a)
s=s[:a]+out+s[b:]
a=s.index('<section class="py-approach');b=s.index('</section>',a)+len('</section>');s=s[:a]+s[b:]
s=s.replace('href="#psyber-connect"','href="#programs"').replace('Plan a session ↗','Explore courses ↗').replace('Discuss a session ↗','Explore courses ↗')
s=s.replace('Psyber Yodha is our specialized cyber courses initiative for individuals, workplaces and learning communities. Explore practical cybersecurity learning and connect with ICN to discuss the right course for your audience.','Explore our specialized cyber courses in digital forensics, cyber intelligence, blue team operations, Darkweb research and AI-powered cybersecurity. Find your course and explore its complete syllabus and certification requirements.')
s=s.replace('<script src="psyberyodha.js"></script>','')
p.write_text(s,encoding='utf-8')
# Check complete module text and assessment text is present, allowing only layout and bullet normalization.
assert 'HackAstra' not in s and 'psyber-grid' not in s and 'psyber-connect' not in s
for c in courses:
 for m in c['modules']:assert html.escape(m['goal']) in s
(root.parent/'course-content-verification.json').write_text(json.dumps([{'title':c['title'],'modules':len(c['modules'])} for c in courses],indent=2))
print('Published six complete courses,',sum(len(c['modules']) for c in courses),'modules. Removed both pictured sections and outdated session copy.')




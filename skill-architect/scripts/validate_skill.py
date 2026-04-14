#!/usr/bin/env python3
"""Validate a target skill's structural compliance with the Agent Skills spec."""
import json, os, re, sys
try:
    import yaml
except ImportError:
    print(json.dumps({"status":"FAIL","error":"pyyaml not installed","checks":[],"summary":{"pass":0,"fail":1,"warning":0,"total":1}},indent=2))
    sys.exit(1)

def chk(name,passed,detail="",warning=False):
    return {"name":name,"status":"PASS" if passed else ("WARNING" if warning else "FAIL"),"detail":detail}

def validate(sp):
    r=[]; sp=os.path.abspath(sp); dn=os.path.basename(sp)
    smp=os.path.join(sp,"SKILL.md")
    if not os.path.isfile(smp):
        r.append(chk("skill_md_exists",False,f"SKILL.md not found in {sp}")); return r
    r.append(chk("skill_md_exists",True))
    with open(smp,"r",encoding="utf-8") as f: content=f.read()
    lines=content.split("\n")
    fm=None
    if content.startswith("---"):
        ei=content.find("---",3)
        if ei>0:
            try: fm=yaml.safe_load(content[3:ei].strip()); r.append(chk("frontmatter_valid",True))
            except yaml.YAMLError as e: r.append(chk("frontmatter_valid",False,str(e)))
        else: r.append(chk("frontmatter_valid",False,"No closing ---"))
    else: r.append(chk("frontmatter_valid",False,"No opening ---"))
    if fm is None: fm={}
    nm=str(fm.get("name","") or "")
    nv=bool(nm and len(nm)<=64 and re.match(r'^[a-z0-9]([a-z0-9-]*[a-z0-9])?$',nm) and '--' not in nm)
    r.append(chk("name_format",nv,f"name='{nm}'"))
    r.append(chk("name_matches_dir",nm==dn,f"name='{nm}', dir='{dn}'"))
    ds=str(fm.get("description","") or "").strip()
    r.append(chk("description_present",len(ds)>0))
    r.append(chk("description_length",len(ds)<=1024,f"{len(ds)} chars"))
    dl=ds.lower()
    ht=any(p in dl for p in["use when","use this","use for","activate when"])
    r.append(chk("description_trigger_hint",ht,"" if ht else "No trigger hint",warning=not ht))
    lc=len(lines)
    r.append(chk("line_count",lc<=500,f"{lc} lines"))
    fmr=content[3:content.find("---",3)] if content.startswith("---") else ""
    r.append(chk("no_xml_in_frontmatter",not bool(re.search(r'<[^>]+>',fmr))))
    r.append(chk("no_readme",not os.path.isfile(os.path.join(sp,"README.md"))))
    bs=content.find("---",3)+3 if content.startswith("---") else 0
    r.append(chk("body_present",len(content[bs:].strip())>0))
    refs=set(m.group() for m in re.finditer(r'(?:references|scripts|assets)/[^\s)>\]`]+',content))
    miss=[rf for rf in refs if not os.path.exists(os.path.join(sp,rf))]
    r.append(chk("reference_integrity",len(miss)==0,"" if not miss else f"Missing: {', '.join(miss)}"))
    actual=set()
    for sd in["scripts","references","assets"]:
        sdp=os.path.join(sp,sd)
        if os.path.isdir(sdp):
            for fn in os.listdir(sdp):
                if fn.startswith("__") or fn.startswith("."): continue
                actual.add(os.path.join(sd,fn))
    orph=actual-refs
    r.append(chk("no_orphan_files",len(orph)==0,"" if not orph else f"Unreferenced: {', '.join(sorted(orph))}",warning=len(orph)>0))
    ap=[r'\bproperly\b',r'\bcorrectly\b',r'\bas needed\b',r'\bas appropriate\b',r'\bmight want to\b',r'\bif necessary\b']
    af=[]
    for i,line in enumerate(lines,1):
        for p in ap:
            m=re.search(p,line,re.IGNORECASE)
            if m: af.append(f"L{i}: {m.group()}")
    r.append(chk("ambiguous_expressions",len(af)==0,"" if not af else f"Found {len(af)}: {'; '.join(af[:5])}",warning=True))
    sp_=[
        (r'(?:api[_-]?key|password|secret|token)\s*[=:]\s*["\'][^"\']+["\']',"Hardcoded secret"),
        (r'rm\s+-rf\s+/',"Dangerous rm -rf"),
        (r'curl\s+.*\|\s*(?:ba)?sh',"Pipe curl to shell"),
        (r'\beval\s*\(',"eval usage"),
    ]
    si=[]
    for i,line in enumerate(lines,1):
        for p,d in sp_:
            if re.search(p,line,re.IGNORECASE): si.append(f"L{i}: {d}")
    r.append(chk("security_check",len(si)==0,"" if not si else f"Issues: {'; '.join(si)}"))
    return r

def main():
    if len(sys.argv)<2: print("Usage: python validate_skill.py /path/to/skill/"); sys.exit(1)
    sp=sys.argv[1]
    if not os.path.isdir(sp): print(json.dumps({"status":"FAIL","error":f"Not a directory: {sp}"},indent=2)); sys.exit(1)
    r=validate(sp)
    pc=sum(1 for x in r if x["status"]=="PASS")
    fc=sum(1 for x in r if x["status"]=="FAIL")
    wc=sum(1 for x in r if x["status"]=="WARNING")
    o={"status":"PASS" if fc==0 else "FAIL","checks":r,"summary":{"pass":pc,"fail":fc,"warning":wc,"total":len(r)}}
    print(json.dumps(o,indent=2,ensure_ascii=False))
    sys.exit(0 if fc==0 else 1)

if __name__=="__main__": main()

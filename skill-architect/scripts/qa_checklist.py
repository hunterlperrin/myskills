#!/usr/bin/env python3
"""Run Tessle Validation + Anthropic checklist + content heuristics on a target skill."""
import json, os, re, sys
try:
    import yaml
except ImportError:
    print(json.dumps({"status":"FAIL","error":"pyyaml not installed","checks":[],"summary":{"pass":0,"fail":1,"warning":0,"total":1}},indent=2))
    sys.exit(1)

def chk(name,passed,detail="",warning=False):
    return {"name":name,"status":"PASS" if passed else ("WARNING" if warning else "FAIL"),"detail":detail}

def run_qa(sp):
    r=[]; sp=os.path.abspath(sp); dn=os.path.basename(sp)
    smp=os.path.join(sp,"SKILL.md")
    if not os.path.isfile(smp):
        r.append(chk("skill_md_exists",False,"SKILL.md not found")); return r
    with open(smp,"r",encoding="utf-8") as f: content=f.read()
    lines=content.split("\n"); lc=len(lines)
    fm={}; body=content
    if content.startswith("---"):
        ei=content.find("---",3)
        if ei>0:
            try: fm=yaml.safe_load(content[3:ei].strip()) or {}
            except: pass
            body=content[ei+3:].strip()
    nm=str(fm.get("name","")); ds=str(fm.get("description","")).strip()
    # Tessle Validation
    r.append(chk("tessle_line_count",lc<=500,f"{lc} lines"))
    r.append(chk("tessle_frontmatter_valid",bool(fm)))
    r.append(chk("tessle_name_field",bool(nm) and len(nm)<=64,f"name='{nm}'"))
    r.append(chk("tessle_description_field",bool(ds) and len(ds)<=1024,f"{len(ds)} chars"))
    fp=bool(re.search(r'\b(?:I|We)\s+(?:will|can|do|am|are|have)\b',ds))
    r.append(chk("tessle_description_voice",not fp))
    dl=ds.lower()
    ht=any(p in dl for p in["use when","use this","use for","activate when"])
    r.append(chk("tessle_description_trigger_hint",ht,warning=not ht))
    r.append(chk("tessle_body_present",len(body)>100,f"Body: {len(body)} chars"))
    r.append(chk("tessle_body_examples",bool(re.search(r'(?:example|```|quick example)',body,re.IGNORECASE)),warning=True))
    r.append(chk("tessle_body_output_format",bool(re.search(r'(?:output|result|produces|returns|delivers)',body,re.IGNORECASE)),warning=True))
    # Anthropic subset
    r.append(chk("anthropic_folder_kebab_case",bool(re.match(r'^[a-z0-9]+(-[a-z0-9]+)*$',dn)),f"dir='{dn}'"))
    r.append(chk("anthropic_no_readme",not os.path.isfile(os.path.join(sp,"README.md"))))
    fmr=content[3:content.find("---",3)] if content.startswith("---") else ""
    r.append(chk("anthropic_no_xml_frontmatter",not bool(re.search(r'<[^>]+>',fmr))))
    r.append(chk("anthropic_instructions_actionable",bool(re.search(r'^\s*(?:\d+\.|[-*])\s+',body,re.MULTILINE)),warning=True))
    r.append(chk("anthropic_error_handling",bool(re.search(r'(?:troubleshoot|error|problem)',body,re.IGNORECASE)),warning=True))
    r.append(chk("anthropic_examples_provided",bool(re.search(r'## .*(?:example|quick)',body,re.IGNORECASE)),warning=True))
    r.append(chk("anthropic_references_linked",bool(re.search(r'(?:Read|read)\s+.*references/',body)),warning=True))
    # Heuristics
    ic=False; cc=0
    for line in lines:
        if line.strip().startswith("```"): ic=not ic
        elif ic: cc+=1
    cr=cc/max(lc,1)
    r.append(chk("heuristic_code_ratio",cr<0.4,f"{cr:.0%} code",warning=cr>=0.3))
    secs=re.split(r'^##\s+',body,flags=re.MULTILINE)
    if len(secs)>1:
        sl=[len(s.split("\n")) for s in secs[1:]]
        mx=max(sl); av=sum(sl)/len(sl)
        r.append(chk("heuristic_section_length",mx<=80,f"avg={av:.0f}, max={mx}",warning=mx>60))
    else:
        r.append(chk("heuristic_section_length",False,"No sections",warning=True))
    return r

def main():
    if len(sys.argv)<2: print("Usage: python qa_checklist.py /path/to/skill/"); sys.exit(1)
    sp=sys.argv[1]
    if not os.path.isdir(sp): print(json.dumps({"status":"FAIL","error":f"Not a dir: {sp}"},indent=2)); sys.exit(1)
    r=run_qa(sp)
    pc=sum(1 for x in r if x["status"]=="PASS")
    fc=sum(1 for x in r if x["status"]=="FAIL")
    wc=sum(1 for x in r if x["status"]=="WARNING")
    o={"status":"PASS" if fc==0 else "FAIL","checks":r,"summary":{"pass":pc,"fail":fc,"warning":wc,"total":len(r)}}
    print(json.dumps(o,indent=2,ensure_ascii=False))
    print("\n--- Human Summary ---")
    for c in r:
        ic="✅" if c["status"]=="PASS" else ("⚠️" if c["status"]=="WARNING" else "❌")
        d=f" — {c['detail']}" if c["detail"] else ""
        print(f"  {ic} {c['name']}{d}")
    print(f"\n  Total: {pc} PASS, {fc} FAIL, {wc} WARNING / {len(r)}")
    sys.exit(0 if fc==0 else 1)

if __name__=="__main__": main()

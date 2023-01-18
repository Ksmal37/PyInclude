import os
import sys

def get_includes(code):
	lines=code.split("\n")
	includes=[]
	for lineno,line in enumerate(lines):
		spl=line.split()
		if len(spl)>1 and spl[0]=="#!include":
			includes.append([lineno,spl[1]])
	return includes

def magic_to_abs(path,curpath=""):
	abspath=path
	if not path.startswith("/"):
		srcpaths=[i+"/"+path for i in [curpath]+sys.path]
		for srcpath in srcpaths:
			if os.path.exists(srcpath):
				abspath=srcpath
	return abspath
		

def code_magic_to_abs(code,path=""):
	lines=code.split("\n")
	for inc in get_includes(code):
		lines[inc[0]]="#!include "+magic_to_abs(inc[1],path)
	return "\n".join(lines)

	
	
	
def step_text_process(code,path="",inclass=""):
	code=code_magic_to_abs(code,path=path)
	lines=code.split("\n")
	includes=get_includes(code)
	for inc in includes:
		with open(inc[1],"r") as f:
			addcode=code_magic_to_abs(f.read(),path=inc[1][:inc[1].rindex("/")])
			addlines=addcode.split("\n")
			lines[inc[0]:inc[0]+1]=addlines
	return "\n".join(lines),len(includes)
		
	

def text_process(code,path=""):
	afc=None
	while afc!=0:
		code,afc=step_text_process(code,path=path)
	return code

def file_process(filepath,outpath=None):
	with open(filepath,"r") as f:
		out=text_process(f.read(),path=filepath[:filepath.rindex("/")])
	if outpath!=None:
		with open(outpath,"w") as f:
			f.write(out)
	return out










				

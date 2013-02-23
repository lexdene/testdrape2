def markdown(templatePath,vardict):
	import os,markdown,StringIO
	filepath = 'app/template'+templatePath+'.md'
	s = StringIO.StringIO()
	markdown.markdownFromFile(filepath,s)
	return s.getvalue()

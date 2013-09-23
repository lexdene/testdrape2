''' self defined render functions '''

def markdown(template_path, _):
    ''' render markdown file '''
    import StringIO
    import markdown as md

    from drape import config

    dirpath = config.MARKDOWN_DIR
    filepath = '%s/%s.md' % (dirpath, template_path)

    output = StringIO.StringIO()
    md.markdownFromFile(filepath, output)
    ret = output.getvalue().decode('utf-8')
    return ret

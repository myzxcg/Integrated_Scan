#!/usr/bin/env python
# _*_coding:utf-8 _*_
html_general = """
<html>
<head>
<title>Integrated_Scan Result</title>
<meta http-equiv="Content-Type" content="text/html; charset=utf-8" />
<style>
    body {width:960px; margin:auto; margin-top:10px; background:rgb(200,200,200);}
    p {color: #666;}
    h2 {color:#002E8C; font-size: 1em; padding-top:5px;}
    ul li {
    word-wrap: break-word;
    white-space: -moz-pre-wrap;
    white-space: pre-wrap;
    margin-bottom:10px;
    }
</style>
</head>
<body>
<h2>If you have any questions about the tool, you can submit an issue on github.</b>
If you think this tool is good, you can give me a star on github.</h2>
<h2>Github: https://github.com/myzxcg/Integrated_Scan.</h2>
${content1}
</body>
</html>
"""
html_host = """
<h2>[${status}] <a href="http://${url}" target="_blank">${url}</a></h2>
<ul>
ip:${content2}
</ul>
"""
html_ip="""
<a href='http://${ip}' target="_blank">${ip}</a>&nbsp;&nbsp;
"""
html = {
    'general': html_general,
    'host': html_host,
    'ip': html_ip
}

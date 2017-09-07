#!/usr/bin/python3.6

import sys
import json
from jinja2 import Environment, PackageLoader, select_autoescape
import argparse 
import re
from bs4 import BeautifulSoup
from subprocess import call

parser = argparse.ArgumentParser()
parser.add_argument(
    'configfile',
    help = 'A path to a configuration file, in the json format',
)

def parse_config(configfile):
    def nested_get(dic, keys,default=None):
        for key in keys[:-1]:
            dic = dic.setdefault(key, {})
        return dic.setdefault(keys[-1], default)

    def nested_set(dic, keys, value):
        for key in keys[:-1]:
            dic = dic.setdefault(key, {})
        dic[keys[-1]] = value

    def set_vars_recur(d, depth=0):
        if depth >= max_depth:
            raise Exception('Recursion exceeded max_depth value when parsing json config')
        items = [*d.items()]
        for k, v in items:
            if isinstance(v,dict):
                set_vars_recur(v, depth+1)
            elif isinstance(v,str):
                match = re.search('\{\{(.*?)\}\}',v)
                if match:
                    attributes = re.findall(r'\[(.*?)\]',match.group(1))
                    new_value = nested_get(data,attributes)
                    d[k] = new_value 

    with open(configfile) as fh:
        content = fh.read()
    data = json.loads(content)
    if 'program' not in data or data['program'] != 'cvgen':
        raise Exception('This is not a valid configuration file')
    
    max_depth = 10
    set_vars_recur(data)
    return data


def get_environment():
    return Environment(
        loader = PackageLoader('layouts', config['general']['style']),
        autoescape = select_autoescape(['html', 'xml']),
    )


def render_block(name, section):
    type = section['type']
    block_template = env.get_template('{}.html'.format(type))
    return block_template.render(block_name = name, general = config['general'], **section["data"], )
    

def render():
    pages = []
    blocks = []
   
    try:
        headerfile = config['general']['header']
        header_template = env.get_template(headerfile)
        header_html = header_template.render(**config)
    except Exception as e:
        print("Could not locate header='{}'".format(e))
        header_html = ''

    try:
        footerfile = config['general']['footer']
        footer_template = env.get_template(footerfile)
        footer_html = footer_template.render(**config)
    except Exception as e:
        print("Could not locate footer='{}'".format(e))
        footer_html = ''

    page_size_template = env.get_template('css/paper_size.css')
    css = [ page_size_template.render(**config['general']['paper_size']) ]
    for filepath in config['css_files']:
        css_template =  env.get_template(filepath)
        css.append(css_template.render(**config))


    pages = []
    for name,page_data in config['pages'].items():
        page = []
        for name, section in page_data['blocks'].items():
            page.append(render_block(name, section))
        pages.append(page)

    base_template = env.get_template('base.html')
    output_html = base_template.render(
        page_renders = pages,
        css_renders = css,
        header=header_html,
        footer=footer_html,
        **config
    )
    
    output_html = BeautifulSoup(output_html, 'html.parser').prettify()

    with open('output/{}.html'.format(config['general']['title']), 'w') as fh:
       fh.write(output_html) 

def convert():
    call([
        './wkhtmltopdf',
        '--page-size','A4',
        '--margin-top','0mm',
        '--margin-right','0mm',
        '--margin-bottom','0mm',
        '--margin-left','0mm',
        '--encoding','UTF-8',
        '--print-media-type',
        '--no-outline',
        '--disable-smart-shrinking',
        '--title',config['general']['title'],
        'output/{}.html'.format(config['general']['title']),
        'output/{}.pdf'.format(config['general']['title'])
    ])

if __name__ == '__main__':
    args = parser.parse_args() 
    config = parse_config(args.configfile)
    env = get_environment()
    render()
    convert()

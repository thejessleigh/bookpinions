from jinja2 import Environment, PackageLoader, select_autoescape

# set up template environment
template_env = Environment(
    loader=PackageLoader('bookpinions', 'templates'),
    autoescape=select_autoescape(['html', 'xml'])
)

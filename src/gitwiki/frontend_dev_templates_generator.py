import os

from gitwiki.breadcrumbrenderer import BreadcrumbRenderer
from gitwiki.pagerenderer import PageRenderer

if __name__ == "__main__":
    base_folder = os.path.dirname(os.path.realpath(__file__))
    samples_folder = os.path.join(base_folder, 'sample-markdown-files')

    rendered_samples_folder = os.path.join(base_folder, '../../static/sample-templates')

    page_renderer = PageRenderer(base_url='/pages/', base_pages_path='pages')
    html_toc, html_content = page_renderer.render_page(os.path.join(samples_folder, 'sample-content.md'))
    with open(os.path.join(rendered_samples_folder, 'content.html'), 'w') as f:
        f.write(html_content)
    with open(os.path.join(rendered_samples_folder, 'table_of_content.html'), 'w') as f:
        f.write(html_toc)

    breadcrumb_renderer = BreadcrumbRenderer(base_url='/pages/')
    breadcrumb_content = breadcrumb_renderer.render_path(['path 1', 'path 2', 'path 3'])
    with open(os.path.join(rendered_samples_folder, 'breadcrumb.html'), 'w') as f:
        f.write(breadcrumb_content)

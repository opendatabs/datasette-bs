from datasette import hookimpl


@hookimpl
def extra_css_urls(template, database, table, columns, view_name, request, datasette):
    return ["/bs/datatools.css"]

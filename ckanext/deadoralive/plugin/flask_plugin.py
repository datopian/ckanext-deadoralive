from flask import Blueprint

import ckan.plugins as plugins

import ckanext.deadoralive.plugin.plugin_functions as deadoralive_plugin

deadoralive = Blueprint(u'deadoralive', __name__)


class MixinPlugin(plugins.SingletonPlugin):
    plugins.implements(plugins.IBlueprint)

    def get_blueprint(self):
        return [deadoralive]


deadoralive.add_url_rule(
    u'/deadoralive/organization/broken_links',
    view_func=deadoralive_plugin.broken_links_by_organization,
    methods=['GET', 'POST']
)
deadoralive.add_url_rule(
    u'/ckan-admin/broken_links',
    view_func=deadoralive_plugin.broken_links_by_email,
    methods=['GET', 'POST']
)
deadoralive.add_url_rule(
    u'/deadoralive/get_resources_to_check',
    view_func=deadoralive_plugin.get_resources_to_check,
    methods=['GET', 'POST']
)
deadoralive.add_url_rule(
    u'/deadoralive/get_url_for_resource_id',
    view_func=deadoralive_plugin.get_resource_id_for_url,
    methods=['GET', 'POST']
)
deadoralive.add_url_rule(
    u'/deadoralive/upsert',
    view_func=deadoralive_plugin.upsert,
    methods=['GET', 'POST']
)

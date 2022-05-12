"""The deadoralive plugin."""

import ckan.plugins as plugins
import deadoralive.plugin.plugin_functions as deadoralive_plugin


class MixinPlugin(plugins.SingletonPlugin):
    plugins.implements(plugins.IRoutes, inherit=True)

    # IRoutes

    def before_map(self, map_):
        map_.connect("deadoralive_broken_links_by_organization",
                     "/deadoralive/organization/broken_links/",
                     controller="deadoralive_plugin",
                     action="broken_links_by_organization")
        map_.connect("deadoralive_broken_links_by_email",
                     "/ckan-admin/broken_links",
                     controller="deadoralive_plugin",
                     action="broken_links_by_email",
                     ckan_icon="link")

        # Make some of this plugin's custom action functions also available at
        # custom URLs. This is to support deadoralive's non-CKAN specific API.
        map_.connect(
            "/deadoralive/get_resources_to_check",
            controller="deadoralive_plugin",
            action="get_resources_to_check")
        map_.connect(
            "/deadoralive/get_url_for_resource_id",
            controller="deadoralive_plugin",
            action="get_resource_id_for_url")
        map_.connect(
            "/deadoralive/upsert",
            controller="deadoralive_plugin",
            action="upsert")

        return map_

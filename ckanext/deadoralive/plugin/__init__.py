"""The deadoralive plugin."""

# TODO: Backwards compatibility for Python 2 and CKAN 2.8 and lower
# if p.toolkit.check_ckan_version(min_version='2.9.0'):
#    from ckanext.deadoralive.plugin.flask_plugin import MixinPlugin
#else:
from ckanext.deadoralive.plugin.flask_plugin import MixinPlugin

import ckan.plugins as plugins
import ckan.plugins.toolkit as toolkit

import ckanext.deadoralive.model.results as results
import ckanext.deadoralive.config as config
import ckanext.deadoralive.logic.action.get as get
import ckanext.deadoralive.logic.action.update as update
import ckanext.deadoralive.helpers as helpers
import ckanext.deadoralive.logic.auth.update
import ckanext.deadoralive.logic.auth.get
import logging as log

log = log.getLogger(__name__)


class DeadOrAlivePlugin(MixinPlugin, plugins.SingletonPlugin):
    plugins.implements(plugins.IConfigurable)
    plugins.implements(plugins.IConfigurer)
    plugins.implements(plugins.IActions)
    plugins.implements(plugins.ITemplateHelpers)
    plugins.implements(plugins.IRoutes, inherit=True)
    plugins.implements(plugins.IAuthFunctions)

    # IConfigurable

    def configure(self, config_):
        results.create_database_table()
        for key, value in config_.items():
            if 'datajson' in key:
                log.error("{} = {}".format(key, value))


        # Update the class variables for the config settings with the values
        # from the config file, *if* they're in the config file.
        config.recheck_resources_after = toolkit.asint(config_.get(
            "ckanext.deadoralive.recheck_resources_after",
            config.recheck_resources_after))
        config.resend_pending_resources_after = toolkit.asint(
            config_.get(
                "ckanext.deadoralive.resend_pending_resources_after",
                config.resend_pending_resources_after))
        config.broken_resource_min_fails = toolkit.asint(
            config_.get(
                "ckanext.deadoralive.broken_resource_min_fails",
                config.broken_resource_min_fails))
        config.broken_resource_min_hours = toolkit.asint(
            config_.get(
                "ckanext.deadoralive.broken_resource_min_hours",
                config.broken_resource_min_hours))
        config.authorized_users = toolkit.aslist(
            config_.get(
                "ckanext.deadoralive.authorized_users",
                config.authorized_users))

    # IConfigurer

    def update_config(self, config_):
        toolkit.add_template_directory(config_, '../templates')
        toolkit.add_resource('../theme/resources', 'deadoralive')

        if toolkit.check_ckan_version(max_version='2.2.999'):
            # Add CKAN version 2.2 support templates.
            toolkit.add_template_directory(config_, '2.2_templates')

    # IActions

    def get_actions(self):
        return {
            "ckanext_deadoralive_get_resources_to_check":
                get.get_resources_to_check,
            "ckanext_deadoralive_upsert": update.upsert,
            "ckanext_deadoralive_get": get.get,
            "ckanext_deadoralive_broken_links_by_organization":
                get.broken_links_by_organization,
            "ckanext_deadoralive_broken_links_by_email":
                get.broken_links_by_email,
        }

    # ITemplateHelpers

    def get_helpers(self):
        return {
            "ckanext_deadoralive_get": helpers.get_results,
        }

    # IAuthFunctions

    def get_auth_functions(self):
        return {
            "ckanext_deadoralive_upsert":
                ckanext.deadoralive.logic.auth.update.upsert,
            "ckanext_deadoralive_get_resources_to_check":
                ckanext.deadoralive.logic.auth.get.get_resources_to_check,
            "ckanext_deadoralive_get":
                ckanext.deadoralive.logic.auth.get.get,
            "ckanext_deadoralive_broken_links_by_organization":
                ckanext.deadoralive.logic.auth.get.broken_links_by_organization,
            "ckanext_deadoralive_broken_links_by_email":
                ckanext.deadoralive.logic.auth.get.broken_links_by_email,
        }

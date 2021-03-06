import ckan.plugins as plugins
import ckan.plugins.toolkit as toolkit

from routes.mapper import SubMapper

# Custom helper
from ckanext.ifpb_theme import helpers as h

from ckanext.ifpb_theme.logic.auth import create as auth_create
from ckanext.ifpb_theme.logic.auth import update as auth_update
from ckanext.ifpb_theme.logic.auth import delete as auth_delete
from ckanext.ifpb_theme.logic.action import create as action_create
from ckanext.ifpb_theme.logic.action import get as action_get
from ckanext.ifpb_theme.logic.action import update as action_update
from ckanext.ifpb_theme.logic.action import delete as action_delete


class Ifpb_ThemePlugin(plugins.SingletonPlugin):
    plugins.implements(plugins.IConfigurer)
    plugins.implements(plugins.ITemplateHelpers)
    plugins.implements(plugins.IRoutes)
    plugins.implements(plugins.IAuthFunctions)
    plugins.implements(plugins.IActions)

    def update_config(self, config_):
    	toolkit.add_template_directory(config_, 'templates')
    	toolkit.add_public_directory(config_, 'public')
    	toolkit.add_resource('fanstatic', 'ifpb_theme')

	# Registro dos helpers
    # =======================================================
    def get_helpers(self):
        '''Register all functions
        '''
        
        # Template helper function names should begin with the name of the
        # extension they belong to, to avoid clashing with functions from
        # other extensions.
        return {
            # Homepage
            'count_organizations': h.organization.count_organizations
        }

    # Mapeamento das URLs
    # =======================================================                
    def before_map(self, map):
        return map

    def after_map(self, map):
        # App
        map.redirect('/app', '/apps')
        map.redirect('/app/edit', '/apps')
        with SubMapper(map, controller='ckanext.ifpb_theme.controllers.app:AppController') as m:
            m.connect('app_show', '/apps', action='show')
            m.connect('app_new', '/app/new', action='new')
            m.connect('app_edit', '/app/edit/{id}', action='edit',
                  ckan_icon='pencil-square-o')
            m.connect('app_action', '/app/{action}/{id}',
                  requirements=dict(action='|'.join([
                      'edit',
                      'delete',
                  ])))

                    
        return map

    # Definir autorization
    # =======================================================                
    def get_auth_functions(self):
        return {
            'app_create': auth_create.app_create,
            'app_update': auth_update.app_update,
            'app_delete': auth_delete.app_delete
            }

    # Definir novas actions
    # ========================================================
    def get_actions(self):
        return {'app_create': action_create.app_create,
                'app_list': action_get.app_list,
                'app_update': action_update.app_update,
                'app_show': action_get.app_show,
                'app_delete': action_delete.app_delete}
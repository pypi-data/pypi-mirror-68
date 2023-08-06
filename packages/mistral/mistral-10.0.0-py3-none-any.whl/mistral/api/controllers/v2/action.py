# Copyright 2014 - Mirantis, Inc.
# Copyright 2015 Huawei Technologies Co., Ltd.
# Copyright 2020 Nokia Software.
#
#    Licensed under the Apache License, Version 2.0 (the "License");
#    you may not use this file except in compliance with the License.
#    You may obtain a copy of the License at
#
#        http://www.apache.org/licenses/LICENSE-2.0
#
#    Unless required by applicable law or agreed to in writing, software
#    distributed under the License is distributed on an "AS IS" BASIS,
#    WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#    See the License for the specific language governing permissions and
#    limitations under the License.

from oslo_log import log as logging
import pecan
from pecan import hooks
from pecan import rest
from wsme import types as wtypes
import wsmeext.pecan as wsme_pecan

from mistral.api import access_control as acl
from mistral.api.controllers.v2 import resources
from mistral.api.controllers.v2 import types
from mistral.api.controllers.v2 import validation
from mistral.api.hooks import content_type as ct_hook
from mistral import context
from mistral.db.v2 import api as db_api
from mistral import exceptions as exc
from mistral.lang import parser as spec_parser
from mistral.services import actions
from mistral.utils import filter_utils
from mistral.utils import rest_utils

LOG = logging.getLogger(__name__)


class ActionsController(rest.RestController, hooks.HookController):
    # TODO(nmakhotkin): Have a discussion with pecan/WSME folks in order
    # to have requests and response of different content types. Then
    # delete ContentTypeHook.
    __hooks__ = [ct_hook.ContentTypeHook("application/json", ['POST', 'PUT'])]

    validate = validation.SpecValidationController(
        spec_parser.get_action_list_spec_from_yaml)

    @rest_utils.wrap_wsme_controller_exception
    @wsme_pecan.wsexpose(resources.Action, wtypes.text, wtypes.text)
    def get(self, identifier, namespace=''):
        """Return the named action.

        :param identifier: ID or name of the Action to get.
        :param namespace: The namespace of the action.
        """

        acl.enforce('actions:get', context.ctx())

        LOG.debug("Fetch action [identifier=%s]", identifier)

        # Use retries to prevent possible failures.
        db_model = rest_utils.rest_retry_on_db_error(
            db_api.get_action_definition
        )(identifier, namespace=namespace)

        return resources.Action.from_db_model(db_model)

    @rest_utils.wrap_pecan_controller_exception
    @pecan.expose(content_type="text/plain")
    def put(self, identifier=None, namespace=''):
        """Update one or more actions.

        :param identifier: Optional. If provided, it's UUID or name of an
            action. Only one action can be updated with identifier param.
        :param namespace: Optional. If provided, it's the namespace that
            the action is under.

        NOTE: This text is allowed to have definitions
            of multiple actions. In this case they all will be updated.
        """
        acl.enforce('actions:update', context.ctx())

        definition = pecan.request.text

        LOG.debug("Update action(s) [definition=%s]", definition)

        namespace = namespace or ''
        scope = pecan.request.GET.get('scope', 'private')
        resources.Action.validate_scope(scope)
        if scope == 'public':
            acl.enforce('actions:publicize', context.ctx())

        @rest_utils.rest_retry_on_db_error
        def _update_actions():
            with db_api.transaction():
                return actions.update_actions(
                    definition,
                    scope=scope,
                    identifier=identifier,
                    namespace=namespace
                )

        db_acts = _update_actions()

        action_list = [
            resources.Action.from_db_model(db_act) for db_act in db_acts
        ]

        return resources.Actions(actions=action_list).to_json()

    @rest_utils.wrap_pecan_controller_exception
    @pecan.expose(content_type="text/plain")
    def post(self, namespace=''):
        """Create a new action.

        :param namespace: Optional. The namespace to create the ad-hoc action
            in. actions with the same name can be added to a given
            project if they are in two different namespaces.
            (default namespace is '')

        NOTE: This text is allowed to have definitions
            of multiple actions. In this case they all will be created.
        """
        acl.enforce('actions:create', context.ctx())
        namespace = namespace or ''

        definition = pecan.request.text
        scope = pecan.request.GET.get('scope', 'private')
        pecan.response.status = 201

        resources.Action.validate_scope(scope)
        if scope == 'public':
            acl.enforce('actions:publicize', context.ctx())

        LOG.debug("Create action(s) [definition=%s]", definition)

        @rest_utils.rest_retry_on_db_error
        def _create_action_definitions():
            with db_api.transaction():
                return actions.create_actions(definition,
                                              scope=scope,
                                              namespace=namespace)

        db_acts = _create_action_definitions()

        action_list = [
            resources.Action.from_db_model(db_act) for db_act in db_acts
        ]

        return resources.Actions(actions=action_list).to_json()

    @rest_utils.wrap_wsme_controller_exception
    @wsme_pecan.wsexpose(None, wtypes.text, wtypes.text, status_code=204)
    def delete(self, identifier, namespace=''):
        """Delete the named action.

        :param identifier: Name or UUID of the action to delete.
        :param namespace: The namespace of which the action is in.
        """
        acl.enforce('actions:delete', context.ctx())
        LOG.debug("Delete action [identifier=%s]", identifier)

        @rest_utils.rest_retry_on_db_error
        def _delete_action_definition():
            with db_api.transaction():
                db_model = db_api.get_action_definition(identifier,
                                                        namespace=namespace)

                if db_model.is_system:
                    msg = "Attempt to delete a system action: %s" % identifier
                    raise exc.DataAccessException(msg)
                db_api.delete_action_definition(identifier,
                                                namespace=namespace)

        _delete_action_definition()

    @rest_utils.wrap_wsme_controller_exception
    @wsme_pecan.wsexpose(resources.Actions, types.uuid, int, types.uniquelist,
                         types.list, types.uniquelist, wtypes.text,
                         wtypes.text, resources.SCOPE_TYPES, wtypes.text,
                         wtypes.text, wtypes.text, wtypes.text,
                         wtypes.text, wtypes.text, wtypes.text)
    def get_all(self, marker=None, limit=None, sort_keys='name',
                sort_dirs='asc', fields='', created_at=None,
                name=None, scope=None, tags=None,
                updated_at=None, description=None, definition=None,
                is_system=None, input=None, namespace=''):
        """Return all actions.

        :param marker: Optional. Pagination marker for large data sets.
        :param limit: Optional. Maximum number of resources to return in a
                      single result. Default value is None for backward
                      compatibility.
        :param sort_keys: Optional. Columns to sort results by.
                          Default: name.
        :param sort_dirs: Optional. Directions to sort corresponding to
                          sort_keys, "asc" or "desc" can be chosen.
                          Default: asc.
        :param fields: Optional. A specified list of fields of the resource to
                       be returned. 'id' will be included automatically in
                       fields if it's provided, since it will be used when
                       constructing 'next' link.
        :param name: Optional. Keep only resources with a specific name.
        :param scope: Optional. Keep only resources with a specific scope.
        :param definition: Optional. Keep only resources with a specific
                           definition.
        :param is_system: Optional. Keep only system actions or ad-hoc
                          actions (if False).
        :param input: Optional. Keep only resources with a specific input.
        :param description: Optional. Keep only resources with a specific
                            description.
        :param tags: Optional. Keep only resources containing specific tags.
        :param created_at: Optional. Keep only resources created at a specific
                           time and date.
        :param updated_at: Optional. Keep only resources with specific latest
                           update time and date.
        :param namespace: Optional. The namespace of the action.
        """
        acl.enforce('actions:list', context.ctx())

        filters = filter_utils.create_filters_from_request_params(
            created_at=created_at,
            name=name,
            scope=scope,
            tags=tags,
            updated_at=updated_at,
            description=description,
            definition=definition,
            is_system=is_system,
            input=input,
            namespace=namespace
        )

        LOG.debug("Fetch actions. marker=%s, limit=%s, sort_keys=%s, "
                  "sort_dirs=%s, filters=%s", marker, limit, sort_keys,
                  sort_dirs, filters)

        return rest_utils.get_all(
            resources.Actions,
            resources.Action,
            db_api.get_action_definitions,
            db_api.get_action_definition_by_id,
            marker=marker,
            limit=limit,
            sort_keys=sort_keys,
            sort_dirs=sort_dirs,
            fields=fields,
            **filters
        )

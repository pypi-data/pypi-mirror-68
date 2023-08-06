# Copyright 2014 - Mirantis, Inc.
# Copyright 2014 - StackStorm, Inc.
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
from stevedore import extension

from mistral.actions import action_factory
from mistral.db.v2 import api as db_api
from mistral import exceptions as exc
from mistral.services import actions
from mistral_lib import utils
from mistral_lib.utils import inspect_utils as i_utils


# TODO(rakhmerov): Make methods more consistent and granular.

LOG = logging.getLogger(__name__)

ACTIONS_PATH = 'resources/actions'


def register_preinstalled_actions():
    action_paths = utils.get_file_list(ACTIONS_PATH)

    for action_path in action_paths:
        action_definition = open(action_path).read()
        actions.create_or_update_actions(
            action_definition,
            scope='public'
        )


def get_registered_actions(**kwargs):
    return db_api.get_action_definitions(**kwargs)


def register_action_class(name, action_class_str, attributes,
                          description=None, input_str=None, namespace=''):
    values = {
        'name': name,
        'action_class': action_class_str,
        'attributes': attributes,
        'description': description,
        'input': input_str,
        'is_system': True,
        'scope': 'public',
        'namespace': namespace
    }

    try:
        LOG.debug("Registering action in DB: %s", name)

        db_api.create_action_definition(values)
    except exc.DBDuplicateEntryError:
        LOG.debug("Action %s already exists in DB.", name)


def _clear_system_action_db():
    db_api.delete_action_definitions(is_system=True)


def sync_db():
    with db_api.transaction():
        _clear_system_action_db()
        register_action_classes()
        register_preinstalled_actions()


def _register_dynamic_action_classes(namespace=''):
    extensions = extension.ExtensionManager(
        namespace='mistral.generators',
        invoke_on_load=True
    )

    for ext in extensions:
        for generator in ext.obj:
            _register_actions(generator, namespace)


def _register_actions(generator, namespace):
    module = generator.base_action_class.__module__
    class_name = generator.base_action_class.__name__
    action_class_str = "%s.%s" % (module, class_name)

    for action in generator.create_actions():
        attrs = i_utils.get_public_fields(action['class'])

        register_action_class(
            action['name'],
            action_class_str,
            attrs,
            action['description'],
            action['arg_list'],
            namespace=namespace
        )


def register_action_classes(namespace=''):
    mgr = extension.ExtensionManager(
        namespace='mistral.actions',
        invoke_on_load=False
    )
    for name in mgr.names():
        action_class_str = mgr[name].entry_point_target.replace(':', '.')
        action_class = mgr[name].plugin
        description = i_utils.get_docstring(action_class)
        input_str = i_utils.get_arg_list_as_str(action_class.__init__)

        attrs = i_utils.get_public_fields(mgr[name].plugin)

        register_action_class(
            name,
            action_class_str,
            attrs,
            description=description,
            input_str=input_str,
            namespace=namespace
        )

    _register_dynamic_action_classes(namespace=namespace)


def get_action_db(action_name, namespace=''):
    return db_api.load_action_definition(action_name, namespace=namespace)


def get_action_class(action_full_name, namespace=''):
    """Finds action class by full action name (i.e. 'namespace.action_name').

    :param action_full_name: Full action name (that includes namespace).
    :return: Action class or None if not found.
    """
    action_db = get_action_db(action_full_name, namespace)

    if action_db:
        return action_factory.construct_action_class(
            action_db.action_class,
            action_db.attributes
        )

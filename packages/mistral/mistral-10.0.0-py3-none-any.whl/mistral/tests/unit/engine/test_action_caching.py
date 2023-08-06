# Copyright 2017 - Nokia Networks.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#        http://www.apache.org/licenses/LICENSE-2.0
#
#    Unless required by applicable law or agreed to in writing, software
#    distributed under the License is distributed on an "AS IS" BASIS,
#    WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#    See the License for the specific language governing permissions and
#    limitations under the License.

from unittest import mock

import cachetools
from oslo_config import cfg

from mistral.db.v2 import api as db_api
from mistral.services import actions as action_service
from mistral.services import workflows as wf_service
from mistral.tests.unit.engine import base

# Use the set_default method to set value otherwise in certain test cases
# the change in value is not permanent.
cfg.CONF.set_default('auth_enable', False, group='pecan')


class LookupUtilsTest(base.EngineTestCase):
    ACTION = """---
        version: '2.0'

        action1:
          base: std.echo output='Hi'
          output:
            result: $
        """

    WF_TEXT = """---
        version: '2.0'

        wf:
          tasks:
            task1:
              action: action1
              on-success: join_task

            task2:
              action: action1
              on-success: join_task

            join_task:
              join: all
              on-success: task4

            task4:
              action: action1
              pause-before: true
        """

    def test_action_definition_cache_ttl(self):
        namespace = 'test_namespace'
        wf_service.create_workflows(self.WF_TEXT, namespace=namespace)

        # Create an action.
        db_actions = action_service.create_actions(self.ACTION,
                                                   namespace=namespace)

        self.assertEqual(1, len(db_actions))
        self._assert_single_item(db_actions,
                                 name='action1',
                                 namespace=namespace)

        # Explicitly mark the action to be deleted after the test execution.
        self.addCleanup(db_api.delete_action_definitions,
                        name='action1',
                        namespace=namespace)

        # Reinitialise the cache with reduced action_definition_cache_time
        # to make sure the test environment is under control.
        new_cache = cachetools.TTLCache(
            maxsize=1000,
            ttl=50  # 50 seconds
        )
        cache_patch = mock.patch.object(
            db_api, '_ACTION_DEF_CACHE', new_cache)
        cache_patch.start()
        self.addCleanup(cache_patch.stop)

        # Start workflow.
        wf_ex = self.engine.start_workflow('wf', wf_namespace=namespace)

        self.await_workflow_paused(wf_ex.id)

        # Check that 'action1' 'echo' and 'noop' are cached.
        self.assertEqual(5, len(db_api._ACTION_DEF_CACHE))
        self.assertIn('action1:test_namespace', db_api._ACTION_DEF_CACHE)
        self.assertIn('std.noop:test_namespace', db_api._ACTION_DEF_CACHE)
        self.assertIn('std.echo:test_namespace', db_api._ACTION_DEF_CACHE)
        self.assertIn('std.noop', db_api._ACTION_DEF_CACHE)
        self.assertIn('std.echo', db_api._ACTION_DEF_CACHE)

        # Simulate cache expiry
        new_cache.clear()

        # Wait some time until cache expires
        self._await(
            lambda: len(db_api._ACTION_DEF_CACHE) == 0,
            fail_message="No triggers were found"
        )

        self.assertEqual(0, len(db_api._ACTION_DEF_CACHE))

        self.engine.resume_workflow(wf_ex.id)

        self.await_workflow_success(wf_ex.id)

        # Check all actions are cached again.
        self.assertEqual(3, len(db_api._ACTION_DEF_CACHE))
        self.assertIn('action1:test_namespace', db_api._ACTION_DEF_CACHE)
        self.assertIn('std.echo', db_api._ACTION_DEF_CACHE)
        self.assertIn('std.echo:test_namespace', db_api._ACTION_DEF_CACHE)

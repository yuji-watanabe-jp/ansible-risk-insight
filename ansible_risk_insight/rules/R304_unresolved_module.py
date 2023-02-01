# -*- mode:python; coding:utf-8 -*-

# Copyright (c) 2022 IBM Corp. All rights reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     https://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from dataclasses import dataclass
from ansible_risk_insight.models import AnsibleRunContext, ExecutableType as ActionType, RunTargetType
from ansible_risk_insight.rules.base import Rule, Severity, Tag, RuleResult


@dataclass
class UnresolvedModuleRuleResult(RuleResult):
    pass


@dataclass
class UnresolvedModuleRule(Rule):
    rule_id: str = "R304"
    description: str = "Unresolved module is found"
    enabled: bool = True
    name: str = "UnresolvedModule"
    version: str = "v0.0.1"
    severity: Severity = Severity.LOW
    tags: tuple = (Tag.DEPENDENCY)

    result_type: type = UnresolvedModuleRuleResult

    def match(self, ctx: AnsibleRunContext) -> bool:
        return ctx.current.type == RunTargetType.Task

    def check(self, ctx: AnsibleRunContext):
        task = ctx.current

        result = task.action_type == ActionType.MODULE_TYPE and task.spec.action and not task.resolved_action
        detail = {
            "module": task.spec.action,
        }

        rule_result = self.create_result(result=result, detail=detail, task=task)
        return rule_result
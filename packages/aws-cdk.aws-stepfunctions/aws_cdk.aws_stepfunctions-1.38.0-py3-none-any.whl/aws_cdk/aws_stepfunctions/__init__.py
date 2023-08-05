"""
## AWS Step Functions Construct Library

<!--BEGIN STABILITY BANNER-->---


![cfn-resources: Stable](https://img.shields.io/badge/cfn--resources-stable-success.svg?style=for-the-badge)

> All classes with the `Cfn` prefix in this module ([CFN Resources](https://docs.aws.amazon.com/cdk/latest/guide/constructs.html#constructs_lib)) are always stable and safe to use.

![cdk-constructs: Experimental](https://img.shields.io/badge/cdk--constructs-experimental-important.svg?style=for-the-badge)

> The APIs of higher level constructs in this module are experimental and under active development. They are subject to non-backward compatible changes or removal in any future version. These are not subject to the [Semantic Versioning](https://semver.org/) model and breaking changes will be announced in the release notes. This means that while you may use them, you may need to update your source code when upgrading to a newer version of this package.

---
<!--END STABILITY BANNER-->

The `@aws-cdk/aws-stepfunctions` package contains constructs for building
serverless workflows using objects. Use this in conjunction with the
`@aws-cdk/aws-stepfunctions-tasks` package, which contains classes used
to call other AWS services.

Defining a workflow looks like this (for the [Step Functions Job Poller
example](https://docs.aws.amazon.com/step-functions/latest/dg/job-status-poller-sample.html)):

### TypeScript example

```python
# Example automatically generated without compilation. See https://github.com/aws/jsii/issues/826
import aws_cdk.aws_stepfunctions as sfn
import aws_cdk.aws_stepfunctions_tasks as tasks
import aws_cdk.aws_lambda as lambda

submit_lambda = lambda.Function(self, "SubmitLambda", ...)
get_status_lambda = lambda.Function(self, "CheckLambda", ...)

submit_job = sfn.Task(self, "Submit Job",
    task=tasks.RunLambdaTask(submit_lambda),
    # Lambda's result is in the attribute `Payload`
    output_path="$.Payload"
)

wait_x = sfn.Wait(self, "Wait X Seconds",
    time=sfn.WaitTime.seconds_path("$.waitSeconds")
)

get_status = sfn.Task(self, "Get Job Status",
    task=tasks.RunLambdaTask(get_status_lambda),
    # Pass just the field named "guid" into the Lambda, put the
    # Lambda's result in a field called "status" in the response
    input_path="$.guid",
    output_path="$.Payload"
)

job_failed = sfn.Fail(self, "Job Failed",
    cause="AWS Batch Job Failed",
    error="DescribeJob returned FAILED"
)

final_status = sfn.Task(self, "Get Final Job Status",
    task=tasks.RunLambdaTask(get_status_lambda),
    # Use "guid" field as input
    input_path="$.guid",
    output_path="$.Payload"
)

definition = submit_job.next(wait_x).next(get_status).next(sfn.Choice(self, "Job Complete?").when(sfn.Condition.string_equals("$.status", "FAILED"), job_failed).when(sfn.Condition.string_equals("$.status", "SUCCEEDED"), final_status).otherwise(wait_x))

sfn.StateMachine(self, "StateMachine",
    definition=definition,
    timeout=Duration.minutes(5)
)
```

You can find more sample snippets and learn more about the service integrations
in the `@aws-cdk/aws-stepfunctions-tasks` package.

## State Machine

A `stepfunctions.StateMachine` is a resource that takes a state machine
definition. The definition is specified by its start state, and encompasses
all states reachable from the start state:

```python
# Example automatically generated without compilation. See https://github.com/aws/jsii/issues/826
start_state = stepfunctions.Pass(self, "StartState")

stepfunctions.StateMachine(self, "StateMachine",
    definition=start_state
)
```

State machines execute using an IAM Role, which will automatically have all
permissions added that are required to make all state machine tasks execute
properly (for example, permissions to invoke any Lambda functions you add to
your workflow). A role will be created by default, but you can supply an
existing one as well.

## Amazon States Language

This library comes with a set of classes that model the [Amazon States
Language](https://states-language.net/spec.html). The following State classes
are supported:

* [`Task`](#task)
* [`Pass`](#pass)
* [`Wait`](#wait)
* [`Choice`](#choice)
* [`Parallel`](#parallel)
* [`Succeed`](#succeed)
* [`Fail`](#fail)
* [`Map`](#map)
* [`Custom State`](#custom-state)

An arbitrary JSON object (specified at execution start) is passed from state to
state and transformed during the execution of the workflow. For more
information, see the States Language spec.

### Task

A `Task` represents some work that needs to be done. The exact work to be
done is determine by a class that implements `IStepFunctionsTask`, a collection
of which can be found in the `@aws-cdk/aws-stepfunctions-tasks` module.

The tasks in the `@aws-cdk/aws-stepfunctions-tasks` module support the
[service integration pattern](https://docs.aws.amazon.com/step-functions/latest/dg/connect-to-resource.html) that integrates Step Functions with services
directly in the Amazon States language.

### Pass

A `Pass` state does no work, but it can optionally transform the execution's
JSON state.

```python
# Example automatically generated without compilation. See https://github.com/aws/jsii/issues/826
# Makes the current JSON state { ..., "subObject": { "hello": "world" } }
pass = stepfunctions.Pass(self, "Add Hello World",
    result={"hello": "world"},
    result_path="$.subObject"
)

# Set the next state
pass.next(next_state)
```

### Wait

A `Wait` state waits for a given number of seconds, or until the current time
hits a particular time. The time to wait may be taken from the execution's JSON
state.

```python
# Example automatically generated without compilation. See https://github.com/aws/jsii/issues/826
# Wait until it's the time mentioned in the the state object's "triggerTime"
# field.
wait = stepfunctions.Wait(self, "Wait For Trigger Time",
    time=stepfunctions.WaitTime.timestamp_path("$.triggerTime")
)

# Set the next state
wait.next(start_the_work)
```

### Choice

A `Choice` state can take a different path through the workflow based on the
values in the execution's JSON state:

```python
# Example automatically generated without compilation. See https://github.com/aws/jsii/issues/826
choice = stepfunctions.Choice(self, "Did it work?")

# Add conditions with .when()
choice.when(stepfunctions.Condition.string_equal("$.status", "SUCCESS"), success_state)
choice.when(stepfunctions.Condition.number_greater_than("$.attempts", 5), failure_state)

# Use .otherwise() to indicate what should be done if none of the conditions match
choice.otherwise(try_again_state)
```

If you want to temporarily branch your workflow based on a condition, but have
all branches come together and continuing as one (similar to how an `if ... then ... else` works in a programming language), use the `.afterwards()` method:

```python
# Example automatically generated without compilation. See https://github.com/aws/jsii/issues/826
choice = stepfunctions.Choice(self, "What color is it?")
choice.when(stepfunctions.Condition.string_equal("$.color", "BLUE"), handle_blue_item)
choice.when(stepfunctions.Condition.string_equal("$.color", "RED"), handle_red_item)
choice.otherwise(handle_other_item_color)

# Use .afterwards() to join all possible paths back together and continue
choice.afterwards().next(ship_the_item)
```

If your `Choice` doesn't have an `otherwise()` and none of the conditions match
the JSON state, a `NoChoiceMatched` error will be thrown. Wrap the state machine
in a `Parallel` state if you want to catch and recover from this.

### Parallel

A `Parallel` state executes one or more subworkflows in parallel. It can also
be used to catch and recover from errors in subworkflows.

```python
# Example automatically generated without compilation. See https://github.com/aws/jsii/issues/826
parallel = stepfunctions.Parallel(self, "Do the work in parallel")

# Add branches to be executed in parallel
parallel.branch(ship_item)
parallel.branch(send_invoice)
parallel.branch(restock)

# Retry the whole workflow if something goes wrong
parallel.add_retry(max_attempts=1)

# How to recover from errors
parallel.add_catch(send_failure_notification)

# What to do in case everything succeeded
parallel.next(close_order)
```

### Succeed

Reaching a `Succeed` state terminates the state machine execution with a
succesful status.

```python
# Example automatically generated without compilation. See https://github.com/aws/jsii/issues/826
success = stepfunctions.Succeed(self, "We did it!")
```

### Fail

Reaching a `Fail` state terminates the state machine execution with a
failure status. The fail state should report the reason for the failure.
Failures can be caught by encompassing `Parallel` states.

```python
# Example automatically generated without compilation. See https://github.com/aws/jsii/issues/826
success = stepfunctions.Fail(self, "Fail",
    error="WorkflowFailure",
    cause="Something went wrong"
)
```

### Map

A `Map` state can be used to run a set of steps for each element of an input array.
A `Map` state will execute the same steps for multiple entries of an array in the state input.

While the `Parallel` state executes multiple branches of steps using the same input, a `Map` state will
execute the same steps for multiple entries of an array in the state input.

```python
# Example automatically generated without compilation. See https://github.com/aws/jsii/issues/826
map = stepfunctions.Map(self, "Map State",
    max_concurrency=1,
    items_path=stepfunctions.Data.string_at("$.inputForMap")
)
map.iterator(stepfunctions.Pass(self, "Pass State"))
```

### Custom State

It's possible that the high-level constructs for the states or `stepfunctions-tasks` do not have
the states or service integrations you are looking for. The primary reasons for this lack of
functionality are:

* A [service integration](https://docs.aws.amazon.com/step-functions/latest/dg/concepts-service-integrations.html) is available through Amazon States Langauge, but not available as construct
  classes in the CDK.
* The state or state properties are available through Step Functions, but are not configurable
  through constructs

If a feature is not available, a `CustomState` can be used to supply any Amazon States Language
JSON-based object as the state definition.

[Code Snippets](https://docs.aws.amazon.com/step-functions/latest/dg/tutorial-code-snippet.html#tutorial-code-snippet-1) are available and can be plugged in as the state definition.

Custom states can be chained together with any of the other states to create your state machine
definition. You will also need to provide any permissions that are required to the `role` that
the State Machine uses.

The following example uses the `DynamoDB` service integration to insert data into a DynamoDB table.

```python
# Example automatically generated without compilation. See https://github.com/aws/jsii/issues/826
import aws_cdk.aws_dynamodb as ddb
import aws_cdk.core as cdk
import aws_cdk.aws_stepfunctions as sfn

# create a table
table = ddb.Table(self, "montable",
    partition_key=Attribute(
        name="id",
        type=ddb.AttributeType.STRING
    )
)

final_status = sfn.Pass(stack, "final step")

# States language JSON to put an item into DynamoDB
# snippet generated from https://docs.aws.amazon.com/step-functions/latest/dg/tutorial-code-snippet.html#tutorial-code-snippet-1
state_json = {
    "Type": "Task",
    "Resource": "arn:aws:states:::dynamodb:putItem",
    "Parameters": {
        "TableName": table.table_name,
        "Item": {
            "id": {
                "S": "MyEntry"
            }
        }
    },
    "ResultPath": null
}

# custom state which represents a task to insert data into DynamoDB
custom = sfn.CustomState(self, "my custom task",
    state_json=state_json
)

chain = sfn.Chain.start(custom).next(final_status)

sm = sfn.StateMachine(self, "StateMachine",
    definition=chain,
    timeout=cdk.Duration.seconds(30)
)

# don't forget permissions. You need to assign them
table.grant_write_data(sm.role)
```

## Task Chaining

To make defining work flows as convenient (and readable in a top-to-bottom way)
as writing regular programs, it is possible to chain most methods invocations.
In particular, the `.next()` method can be repeated. The result of a series of
`.next()` calls is called a **Chain**, and can be used when defining the jump
targets of `Choice.on` or `Parallel.branch`:

```python
# Example automatically generated without compilation. See https://github.com/aws/jsii/issues/826
definition = step1.next(step2).next(choice.when(condition1, step3.next(step4).next(step5)).otherwise(step6).afterwards()).next(parallel.branch(step7.next(step8)).branch(step9.next(step10))).next(finish)

stepfunctions.StateMachine(self, "StateMachine",
    definition=definition
)
```

If you don't like the visual look of starting a chain directly off the first
step, you can use `Chain.start`:

```python
# Example automatically generated without compilation. See https://github.com/aws/jsii/issues/826
definition = stepfunctions.Chain.start(step1).next(step2).next(step3)
```

## State Machine Fragments

It is possible to define reusable (or abstracted) mini-state machines by
defining a construct that implements `IChainable`, which requires you to define
two fields:

* `startState: State`, representing the entry point into this state machine.
* `endStates: INextable[]`, representing the (one or more) states that outgoing
  transitions will be added to if you chain onto the fragment.

Since states will be named after their construct IDs, you may need to prefix the
IDs of states if you plan to instantiate the same state machine fragment
multiples times (otherwise all states in every instantiation would have the same
name).

The class `StateMachineFragment` contains some helper functions (like
`prefixStates()`) to make it easier for you to do this. If you define your state
machine as a subclass of this, it will be convenient to use:

```python
# Example automatically generated without compilation. See https://github.com/aws/jsii/issues/826
class MyJob(stepfunctions.StateMachineFragment):

    def __init__(self, parent, id, *, jobFlavor):
        super().__init__(parent, id)

        first = stepfunctions.Task(self, "First", ...)
        # ...
        last = stepfunctions.Task(self, "Last", ...)

        self.start_state = first
        self.end_states = [last]

# Do 3 different variants of MyJob in parallel
stepfunctions.Parallel(self, "All jobs").branch(MyJob(self, "Quick", job_flavor="quick").prefix_states()).branch(MyJob(self, "Medium", job_flavor="medium").prefix_states()).branch(MyJob(self, "Slow", job_flavor="slow").prefix_states())
```

A few utility functions are available to parse state machine fragments.

* `State.findReachableStates`: Retrieve the list of states reachable from a given state.
* `State.findReachableEndStates`: Retrieve the list of end or terminal states reachable from a given state.

## Activity

**Activities** represent work that is done on some non-Lambda worker pool. The
Step Functions workflow will submit work to this Activity, and a worker pool
that you run yourself, probably on EC2, will pull jobs from the Activity and
submit the results of individual jobs back.

You need the ARN to do so, so if you use Activities be sure to pass the Activity
ARN into your worker pool:

```python
# Example automatically generated without compilation. See https://github.com/aws/jsii/issues/826
activity = stepfunctions.Activity(self, "Activity")

# Read this CloudFormation Output from your application and use it to poll for work on
# the activity.
cdk.CfnOutput(self, "ActivityArn", value=activity.activity_arn)
```

## Metrics

`Task` object expose various metrics on the execution of that particular task. For example,
to create an alarm on a particular task failing:

```python
# Example automatically generated without compilation. See https://github.com/aws/jsii/issues/826
cloudwatch.Alarm(self, "TaskAlarm",
    metric=task.metric_failed(),
    threshold=1,
    evaluation_periods=1
)
```

There are also metrics on the complete state machine:

```python
# Example automatically generated without compilation. See https://github.com/aws/jsii/issues/826
cloudwatch.Alarm(self, "StateMachineAlarm",
    metric=state_machine.metric_failed(),
    threshold=1,
    evaluation_periods=1
)
```

And there are metrics on the capacity of all state machines in your account:

```python
# Example automatically generated without compilation. See https://github.com/aws/jsii/issues/826
cloudwatch.Alarm(self, "ThrottledAlarm",
    metric=StateTransitionMetrics.metric_throttled_events(),
    threshold=10,
    evaluation_periods=2
)
```

## Logging

Enable logging to CloudWatch by passing a logging configuration with a
destination LogGroup:

```python
# Example automatically generated without compilation. See https://github.com/aws/jsii/issues/826
log_group = logs.LogGroup(stack, "MyLogGroup")

stepfunctions.StateMachine(stack, "MyStateMachine",
    definition=stepfunctions.Chain.start(stepfunctions.Pass(stack, "Pass")),
    logs={
        "destinations": log_group,
        "level": stepfunctions.LogLevel.ALL
    }
)
```

## Future work

Contributions welcome:

* [ ] A single `LambdaTask` class that is both a `Lambda` and a `Task` in one
  might make for a nice API.
* [ ] Expression parser for Conditions.
* [ ] Simulate state machines in unit tests.
"""
import abc
import builtins
import datetime
import enum
import typing

import jsii
import jsii.compat
import publication

import aws_cdk.aws_cloudwatch
import aws_cdk.aws_events
import aws_cdk.aws_iam
import aws_cdk.aws_logs
import aws_cdk.core
import constructs

from ._jsii import *


@jsii.data_type(jsii_type="@aws-cdk/aws-stepfunctions.ActivityProps", jsii_struct_bases=[], name_mapping={'activity_name': 'activityName'})
class ActivityProps():
    def __init__(self, *, activity_name: typing.Optional[str]=None) -> None:
        """Properties for defining a new Step Functions Activity.

        :param activity_name: The name for this activity. Default: - If not supplied, a name is generated

        stability
        :stability: experimental
        """
        self._values = {
        }
        if activity_name is not None: self._values["activity_name"] = activity_name

    @builtins.property
    def activity_name(self) -> typing.Optional[str]:
        """The name for this activity.

        default
        :default: - If not supplied, a name is generated

        stability
        :stability: experimental
        """
        return self._values.get('activity_name')

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return 'ActivityProps(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


@jsii.data_type(jsii_type="@aws-cdk/aws-stepfunctions.AfterwardsOptions", jsii_struct_bases=[], name_mapping={'include_error_handlers': 'includeErrorHandlers', 'include_otherwise': 'includeOtherwise'})
class AfterwardsOptions():
    def __init__(self, *, include_error_handlers: typing.Optional[bool]=None, include_otherwise: typing.Optional[bool]=None) -> None:
        """Options for selecting the choice paths.

        :param include_error_handlers: Whether to include error handling states. If this is true, all states which are error handlers (added through 'onError') and states reachable via error handlers will be included as well. Default: false
        :param include_otherwise: Whether to include the default/otherwise transition for the current Choice state. If this is true and the current Choice does not have a default outgoing transition, one will be added included when .next() is called on the chain. Default: false

        stability
        :stability: experimental
        """
        self._values = {
        }
        if include_error_handlers is not None: self._values["include_error_handlers"] = include_error_handlers
        if include_otherwise is not None: self._values["include_otherwise"] = include_otherwise

    @builtins.property
    def include_error_handlers(self) -> typing.Optional[bool]:
        """Whether to include error handling states.

        If this is true, all states which are error handlers (added through 'onError')
        and states reachable via error handlers will be included as well.

        default
        :default: false

        stability
        :stability: experimental
        """
        return self._values.get('include_error_handlers')

    @builtins.property
    def include_otherwise(self) -> typing.Optional[bool]:
        """Whether to include the default/otherwise transition for the current Choice state.

        If this is true and the current Choice does not have a default outgoing
        transition, one will be added included when .next() is called on the chain.

        default
        :default: false

        stability
        :stability: experimental
        """
        return self._values.get('include_otherwise')

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return 'AfterwardsOptions(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


@jsii.data_type(jsii_type="@aws-cdk/aws-stepfunctions.CatchProps", jsii_struct_bases=[], name_mapping={'errors': 'errors', 'result_path': 'resultPath'})
class CatchProps():
    def __init__(self, *, errors: typing.Optional[typing.List[str]]=None, result_path: typing.Optional[str]=None) -> None:
        """Error handler details.

        :param errors: Errors to recover from by going to the given state. A list of error strings to retry, which can be either predefined errors (for example Errors.NoChoiceMatched) or a self-defined error. Default: All errors
        :param result_path: JSONPath expression to indicate where to inject the error data. May also be the special value DISCARD, which will cause the error data to be discarded. Default: $

        stability
        :stability: experimental
        """
        self._values = {
        }
        if errors is not None: self._values["errors"] = errors
        if result_path is not None: self._values["result_path"] = result_path

    @builtins.property
    def errors(self) -> typing.Optional[typing.List[str]]:
        """Errors to recover from by going to the given state.

        A list of error strings to retry, which can be either predefined errors
        (for example Errors.NoChoiceMatched) or a self-defined error.

        default
        :default: All errors

        stability
        :stability: experimental
        """
        return self._values.get('errors')

    @builtins.property
    def result_path(self) -> typing.Optional[str]:
        """JSONPath expression to indicate where to inject the error data.

        May also be the special value DISCARD, which will cause the error
        data to be discarded.

        default
        :default: $

        stability
        :stability: experimental
        """
        return self._values.get('result_path')

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return 'CatchProps(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


@jsii.implements(aws_cdk.core.IInspectable)
class CfnActivity(aws_cdk.core.CfnResource, metaclass=jsii.JSIIMeta, jsii_type="@aws-cdk/aws-stepfunctions.CfnActivity"):
    """A CloudFormation ``AWS::StepFunctions::Activity``.

    see
    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-stepfunctions-activity.html
    cloudformationResource:
    :cloudformationResource:: AWS::StepFunctions::Activity
    """
    def __init__(self, scope: aws_cdk.core.Construct, id: str, *, name: str, tags: typing.Optional[typing.List["TagsEntryProperty"]]=None) -> None:
        """Create a new ``AWS::StepFunctions::Activity``.

        :param scope: - scope in which this resource is defined.
        :param id: - scoped id of the resource.
        :param name: ``AWS::StepFunctions::Activity.Name``.
        :param tags: ``AWS::StepFunctions::Activity.Tags``.
        """
        props = CfnActivityProps(name=name, tags=tags)

        jsii.create(CfnActivity, self, [scope, id, props])

    @jsii.member(jsii_name="inspect")
    def inspect(self, inspector: aws_cdk.core.TreeInspector) -> None:
        """Examines the CloudFormation resource and discloses attributes.

        :param inspector: - tree inspector to collect and process attributes.

        stability
        :stability: experimental
        """
        return jsii.invoke(self, "inspect", [inspector])

    @jsii.member(jsii_name="renderProperties")
    def _render_properties(self, props: typing.Mapping[str, typing.Any]) -> typing.Mapping[str, typing.Any]:
        """
        :param props: -
        """
        return jsii.invoke(self, "renderProperties", [props])

    @jsii.python.classproperty
    @jsii.member(jsii_name="CFN_RESOURCE_TYPE_NAME")
    def CFN_RESOURCE_TYPE_NAME(cls) -> str:
        """The CloudFormation resource type name for this resource class."""
        return jsii.sget(cls, "CFN_RESOURCE_TYPE_NAME")

    @builtins.property
    @jsii.member(jsii_name="attrName")
    def attr_name(self) -> str:
        """
        cloudformationAttribute:
        :cloudformationAttribute:: Name
        """
        return jsii.get(self, "attrName")

    @builtins.property
    @jsii.member(jsii_name="cfnProperties")
    def _cfn_properties(self) -> typing.Mapping[str, typing.Any]:
        return jsii.get(self, "cfnProperties")

    @builtins.property
    @jsii.member(jsii_name="tags")
    def tags(self) -> aws_cdk.core.TagManager:
        """``AWS::StepFunctions::Activity.Tags``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-stepfunctions-activity.html#cfn-stepfunctions-activity-tags
        """
        return jsii.get(self, "tags")

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> str:
        """``AWS::StepFunctions::Activity.Name``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-stepfunctions-activity.html#cfn-stepfunctions-activity-name
        """
        return jsii.get(self, "name")

    @name.setter
    def name(self, value: str):
        jsii.set(self, "name", value)

    @jsii.data_type(jsii_type="@aws-cdk/aws-stepfunctions.CfnActivity.TagsEntryProperty", jsii_struct_bases=[], name_mapping={'key': 'key', 'value': 'value'})
    class TagsEntryProperty():
        def __init__(self, *, key: str, value: str) -> None:
            """
            :param key: ``CfnActivity.TagsEntryProperty.Key``.
            :param value: ``CfnActivity.TagsEntryProperty.Value``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-stepfunctions-activity-tagsentry.html
            """
            self._values = {
                'key': key,
                'value': value,
            }

        @builtins.property
        def key(self) -> str:
            """``CfnActivity.TagsEntryProperty.Key``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-stepfunctions-activity-tagsentry.html#cfn-stepfunctions-activity-tagsentry-key
            """
            return self._values.get('key')

        @builtins.property
        def value(self) -> str:
            """``CfnActivity.TagsEntryProperty.Value``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-stepfunctions-activity-tagsentry.html#cfn-stepfunctions-activity-tagsentry-value
            """
            return self._values.get('value')

        def __eq__(self, rhs) -> bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs) -> bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return 'TagsEntryProperty(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())



@jsii.data_type(jsii_type="@aws-cdk/aws-stepfunctions.CfnActivityProps", jsii_struct_bases=[], name_mapping={'name': 'name', 'tags': 'tags'})
class CfnActivityProps():
    def __init__(self, *, name: str, tags: typing.Optional[typing.List["CfnActivity.TagsEntryProperty"]]=None) -> None:
        """Properties for defining a ``AWS::StepFunctions::Activity``.

        :param name: ``AWS::StepFunctions::Activity.Name``.
        :param tags: ``AWS::StepFunctions::Activity.Tags``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-stepfunctions-activity.html
        """
        self._values = {
            'name': name,
        }
        if tags is not None: self._values["tags"] = tags

    @builtins.property
    def name(self) -> str:
        """``AWS::StepFunctions::Activity.Name``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-stepfunctions-activity.html#cfn-stepfunctions-activity-name
        """
        return self._values.get('name')

    @builtins.property
    def tags(self) -> typing.Optional[typing.List["CfnActivity.TagsEntryProperty"]]:
        """``AWS::StepFunctions::Activity.Tags``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-stepfunctions-activity.html#cfn-stepfunctions-activity-tags
        """
        return self._values.get('tags')

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return 'CfnActivityProps(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


@jsii.implements(aws_cdk.core.IInspectable)
class CfnStateMachine(aws_cdk.core.CfnResource, metaclass=jsii.JSIIMeta, jsii_type="@aws-cdk/aws-stepfunctions.CfnStateMachine"):
    """A CloudFormation ``AWS::StepFunctions::StateMachine``.

    see
    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-stepfunctions-statemachine.html
    cloudformationResource:
    :cloudformationResource:: AWS::StepFunctions::StateMachine
    """
    def __init__(self, scope: aws_cdk.core.Construct, id: str, *, definition_string: str, role_arn: str, logging_configuration: typing.Optional[typing.Union[typing.Optional["LoggingConfigurationProperty"], typing.Optional[aws_cdk.core.IResolvable]]]=None, state_machine_name: typing.Optional[str]=None, state_machine_type: typing.Optional[str]=None, tags: typing.Optional[typing.List["TagsEntryProperty"]]=None) -> None:
        """Create a new ``AWS::StepFunctions::StateMachine``.

        :param scope: - scope in which this resource is defined.
        :param id: - scoped id of the resource.
        :param definition_string: ``AWS::StepFunctions::StateMachine.DefinitionString``.
        :param role_arn: ``AWS::StepFunctions::StateMachine.RoleArn``.
        :param logging_configuration: ``AWS::StepFunctions::StateMachine.LoggingConfiguration``.
        :param state_machine_name: ``AWS::StepFunctions::StateMachine.StateMachineName``.
        :param state_machine_type: ``AWS::StepFunctions::StateMachine.StateMachineType``.
        :param tags: ``AWS::StepFunctions::StateMachine.Tags``.
        """
        props = CfnStateMachineProps(definition_string=definition_string, role_arn=role_arn, logging_configuration=logging_configuration, state_machine_name=state_machine_name, state_machine_type=state_machine_type, tags=tags)

        jsii.create(CfnStateMachine, self, [scope, id, props])

    @jsii.member(jsii_name="inspect")
    def inspect(self, inspector: aws_cdk.core.TreeInspector) -> None:
        """Examines the CloudFormation resource and discloses attributes.

        :param inspector: - tree inspector to collect and process attributes.

        stability
        :stability: experimental
        """
        return jsii.invoke(self, "inspect", [inspector])

    @jsii.member(jsii_name="renderProperties")
    def _render_properties(self, props: typing.Mapping[str, typing.Any]) -> typing.Mapping[str, typing.Any]:
        """
        :param props: -
        """
        return jsii.invoke(self, "renderProperties", [props])

    @jsii.python.classproperty
    @jsii.member(jsii_name="CFN_RESOURCE_TYPE_NAME")
    def CFN_RESOURCE_TYPE_NAME(cls) -> str:
        """The CloudFormation resource type name for this resource class."""
        return jsii.sget(cls, "CFN_RESOURCE_TYPE_NAME")

    @builtins.property
    @jsii.member(jsii_name="attrName")
    def attr_name(self) -> str:
        """
        cloudformationAttribute:
        :cloudformationAttribute:: Name
        """
        return jsii.get(self, "attrName")

    @builtins.property
    @jsii.member(jsii_name="cfnProperties")
    def _cfn_properties(self) -> typing.Mapping[str, typing.Any]:
        return jsii.get(self, "cfnProperties")

    @builtins.property
    @jsii.member(jsii_name="tags")
    def tags(self) -> aws_cdk.core.TagManager:
        """``AWS::StepFunctions::StateMachine.Tags``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-stepfunctions-statemachine.html#cfn-stepfunctions-statemachine-tags
        """
        return jsii.get(self, "tags")

    @builtins.property
    @jsii.member(jsii_name="definitionString")
    def definition_string(self) -> str:
        """``AWS::StepFunctions::StateMachine.DefinitionString``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-stepfunctions-statemachine.html#cfn-stepfunctions-statemachine-definitionstring
        """
        return jsii.get(self, "definitionString")

    @definition_string.setter
    def definition_string(self, value: str):
        jsii.set(self, "definitionString", value)

    @builtins.property
    @jsii.member(jsii_name="roleArn")
    def role_arn(self) -> str:
        """``AWS::StepFunctions::StateMachine.RoleArn``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-stepfunctions-statemachine.html#cfn-stepfunctions-statemachine-rolearn
        """
        return jsii.get(self, "roleArn")

    @role_arn.setter
    def role_arn(self, value: str):
        jsii.set(self, "roleArn", value)

    @builtins.property
    @jsii.member(jsii_name="loggingConfiguration")
    def logging_configuration(self) -> typing.Optional[typing.Union[typing.Optional["LoggingConfigurationProperty"], typing.Optional[aws_cdk.core.IResolvable]]]:
        """``AWS::StepFunctions::StateMachine.LoggingConfiguration``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-stepfunctions-statemachine.html#cfn-stepfunctions-statemachine-loggingconfiguration
        """
        return jsii.get(self, "loggingConfiguration")

    @logging_configuration.setter
    def logging_configuration(self, value: typing.Optional[typing.Union[typing.Optional["LoggingConfigurationProperty"], typing.Optional[aws_cdk.core.IResolvable]]]):
        jsii.set(self, "loggingConfiguration", value)

    @builtins.property
    @jsii.member(jsii_name="stateMachineName")
    def state_machine_name(self) -> typing.Optional[str]:
        """``AWS::StepFunctions::StateMachine.StateMachineName``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-stepfunctions-statemachine.html#cfn-stepfunctions-statemachine-statemachinename
        """
        return jsii.get(self, "stateMachineName")

    @state_machine_name.setter
    def state_machine_name(self, value: typing.Optional[str]):
        jsii.set(self, "stateMachineName", value)

    @builtins.property
    @jsii.member(jsii_name="stateMachineType")
    def state_machine_type(self) -> typing.Optional[str]:
        """``AWS::StepFunctions::StateMachine.StateMachineType``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-stepfunctions-statemachine.html#cfn-stepfunctions-statemachine-statemachinetype
        """
        return jsii.get(self, "stateMachineType")

    @state_machine_type.setter
    def state_machine_type(self, value: typing.Optional[str]):
        jsii.set(self, "stateMachineType", value)

    @jsii.data_type(jsii_type="@aws-cdk/aws-stepfunctions.CfnStateMachine.CloudWatchLogsLogGroupProperty", jsii_struct_bases=[], name_mapping={'log_group_arn': 'logGroupArn'})
    class CloudWatchLogsLogGroupProperty():
        def __init__(self, *, log_group_arn: str) -> None:
            """
            :param log_group_arn: ``CfnStateMachine.CloudWatchLogsLogGroupProperty.LogGroupArn``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-stepfunctions-statemachine-logdestination-cloudwatchlogsloggroup.html
            """
            self._values = {
                'log_group_arn': log_group_arn,
            }

        @builtins.property
        def log_group_arn(self) -> str:
            """``CfnStateMachine.CloudWatchLogsLogGroupProperty.LogGroupArn``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-stepfunctions-statemachine-logdestination-cloudwatchlogsloggroup.html#cfn-stepfunctions-statemachine-logdestination-cloudwatchlogsloggroup-loggrouparn
            """
            return self._values.get('log_group_arn')

        def __eq__(self, rhs) -> bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs) -> bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return 'CloudWatchLogsLogGroupProperty(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


    @jsii.data_type(jsii_type="@aws-cdk/aws-stepfunctions.CfnStateMachine.LogDestinationProperty", jsii_struct_bases=[], name_mapping={'cloud_watch_logs_log_group': 'cloudWatchLogsLogGroup'})
    class LogDestinationProperty():
        def __init__(self, *, cloud_watch_logs_log_group: typing.Optional[typing.Union[typing.Optional[aws_cdk.core.IResolvable], typing.Optional["CfnStateMachine.CloudWatchLogsLogGroupProperty"]]]=None) -> None:
            """
            :param cloud_watch_logs_log_group: ``CfnStateMachine.LogDestinationProperty.CloudWatchLogsLogGroup``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-stepfunctions-statemachine-logdestination.html
            """
            self._values = {
            }
            if cloud_watch_logs_log_group is not None: self._values["cloud_watch_logs_log_group"] = cloud_watch_logs_log_group

        @builtins.property
        def cloud_watch_logs_log_group(self) -> typing.Optional[typing.Union[typing.Optional[aws_cdk.core.IResolvable], typing.Optional["CfnStateMachine.CloudWatchLogsLogGroupProperty"]]]:
            """``CfnStateMachine.LogDestinationProperty.CloudWatchLogsLogGroup``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-stepfunctions-statemachine-logdestination.html#cfn-stepfunctions-statemachine-logdestination-cloudwatchlogsloggroup
            """
            return self._values.get('cloud_watch_logs_log_group')

        def __eq__(self, rhs) -> bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs) -> bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return 'LogDestinationProperty(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


    @jsii.data_type(jsii_type="@aws-cdk/aws-stepfunctions.CfnStateMachine.LoggingConfigurationProperty", jsii_struct_bases=[], name_mapping={'destinations': 'destinations', 'include_execution_data': 'includeExecutionData', 'level': 'level'})
    class LoggingConfigurationProperty():
        def __init__(self, *, destinations: typing.Optional[typing.Union[typing.Optional[aws_cdk.core.IResolvable], typing.Optional[typing.List[typing.Union[aws_cdk.core.IResolvable, "CfnStateMachine.LogDestinationProperty"]]]]]=None, include_execution_data: typing.Optional[typing.Union[typing.Optional[bool], typing.Optional[aws_cdk.core.IResolvable]]]=None, level: typing.Optional[str]=None) -> None:
            """
            :param destinations: ``CfnStateMachine.LoggingConfigurationProperty.Destinations``.
            :param include_execution_data: ``CfnStateMachine.LoggingConfigurationProperty.IncludeExecutionData``.
            :param level: ``CfnStateMachine.LoggingConfigurationProperty.Level``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-stepfunctions-statemachine-loggingconfiguration.html
            """
            self._values = {
            }
            if destinations is not None: self._values["destinations"] = destinations
            if include_execution_data is not None: self._values["include_execution_data"] = include_execution_data
            if level is not None: self._values["level"] = level

        @builtins.property
        def destinations(self) -> typing.Optional[typing.Union[typing.Optional[aws_cdk.core.IResolvable], typing.Optional[typing.List[typing.Union[aws_cdk.core.IResolvable, "CfnStateMachine.LogDestinationProperty"]]]]]:
            """``CfnStateMachine.LoggingConfigurationProperty.Destinations``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-stepfunctions-statemachine-loggingconfiguration.html#cfn-stepfunctions-statemachine-loggingconfiguration-destinations
            """
            return self._values.get('destinations')

        @builtins.property
        def include_execution_data(self) -> typing.Optional[typing.Union[typing.Optional[bool], typing.Optional[aws_cdk.core.IResolvable]]]:
            """``CfnStateMachine.LoggingConfigurationProperty.IncludeExecutionData``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-stepfunctions-statemachine-loggingconfiguration.html#cfn-stepfunctions-statemachine-loggingconfiguration-includeexecutiondata
            """
            return self._values.get('include_execution_data')

        @builtins.property
        def level(self) -> typing.Optional[str]:
            """``CfnStateMachine.LoggingConfigurationProperty.Level``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-stepfunctions-statemachine-loggingconfiguration.html#cfn-stepfunctions-statemachine-loggingconfiguration-level
            """
            return self._values.get('level')

        def __eq__(self, rhs) -> bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs) -> bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return 'LoggingConfigurationProperty(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


    @jsii.data_type(jsii_type="@aws-cdk/aws-stepfunctions.CfnStateMachine.TagsEntryProperty", jsii_struct_bases=[], name_mapping={'key': 'key', 'value': 'value'})
    class TagsEntryProperty():
        def __init__(self, *, key: str, value: str) -> None:
            """
            :param key: ``CfnStateMachine.TagsEntryProperty.Key``.
            :param value: ``CfnStateMachine.TagsEntryProperty.Value``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-stepfunctions-statemachine-tagsentry.html
            """
            self._values = {
                'key': key,
                'value': value,
            }

        @builtins.property
        def key(self) -> str:
            """``CfnStateMachine.TagsEntryProperty.Key``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-stepfunctions-statemachine-tagsentry.html#cfn-stepfunctions-statemachine-tagsentry-key
            """
            return self._values.get('key')

        @builtins.property
        def value(self) -> str:
            """``CfnStateMachine.TagsEntryProperty.Value``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-stepfunctions-statemachine-tagsentry.html#cfn-stepfunctions-statemachine-tagsentry-value
            """
            return self._values.get('value')

        def __eq__(self, rhs) -> bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs) -> bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return 'TagsEntryProperty(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())



@jsii.data_type(jsii_type="@aws-cdk/aws-stepfunctions.CfnStateMachineProps", jsii_struct_bases=[], name_mapping={'definition_string': 'definitionString', 'role_arn': 'roleArn', 'logging_configuration': 'loggingConfiguration', 'state_machine_name': 'stateMachineName', 'state_machine_type': 'stateMachineType', 'tags': 'tags'})
class CfnStateMachineProps():
    def __init__(self, *, definition_string: str, role_arn: str, logging_configuration: typing.Optional[typing.Union[typing.Optional["CfnStateMachine.LoggingConfigurationProperty"], typing.Optional[aws_cdk.core.IResolvable]]]=None, state_machine_name: typing.Optional[str]=None, state_machine_type: typing.Optional[str]=None, tags: typing.Optional[typing.List["CfnStateMachine.TagsEntryProperty"]]=None) -> None:
        """Properties for defining a ``AWS::StepFunctions::StateMachine``.

        :param definition_string: ``AWS::StepFunctions::StateMachine.DefinitionString``.
        :param role_arn: ``AWS::StepFunctions::StateMachine.RoleArn``.
        :param logging_configuration: ``AWS::StepFunctions::StateMachine.LoggingConfiguration``.
        :param state_machine_name: ``AWS::StepFunctions::StateMachine.StateMachineName``.
        :param state_machine_type: ``AWS::StepFunctions::StateMachine.StateMachineType``.
        :param tags: ``AWS::StepFunctions::StateMachine.Tags``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-stepfunctions-statemachine.html
        """
        self._values = {
            'definition_string': definition_string,
            'role_arn': role_arn,
        }
        if logging_configuration is not None: self._values["logging_configuration"] = logging_configuration
        if state_machine_name is not None: self._values["state_machine_name"] = state_machine_name
        if state_machine_type is not None: self._values["state_machine_type"] = state_machine_type
        if tags is not None: self._values["tags"] = tags

    @builtins.property
    def definition_string(self) -> str:
        """``AWS::StepFunctions::StateMachine.DefinitionString``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-stepfunctions-statemachine.html#cfn-stepfunctions-statemachine-definitionstring
        """
        return self._values.get('definition_string')

    @builtins.property
    def role_arn(self) -> str:
        """``AWS::StepFunctions::StateMachine.RoleArn``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-stepfunctions-statemachine.html#cfn-stepfunctions-statemachine-rolearn
        """
        return self._values.get('role_arn')

    @builtins.property
    def logging_configuration(self) -> typing.Optional[typing.Union[typing.Optional["CfnStateMachine.LoggingConfigurationProperty"], typing.Optional[aws_cdk.core.IResolvable]]]:
        """``AWS::StepFunctions::StateMachine.LoggingConfiguration``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-stepfunctions-statemachine.html#cfn-stepfunctions-statemachine-loggingconfiguration
        """
        return self._values.get('logging_configuration')

    @builtins.property
    def state_machine_name(self) -> typing.Optional[str]:
        """``AWS::StepFunctions::StateMachine.StateMachineName``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-stepfunctions-statemachine.html#cfn-stepfunctions-statemachine-statemachinename
        """
        return self._values.get('state_machine_name')

    @builtins.property
    def state_machine_type(self) -> typing.Optional[str]:
        """``AWS::StepFunctions::StateMachine.StateMachineType``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-stepfunctions-statemachine.html#cfn-stepfunctions-statemachine-statemachinetype
        """
        return self._values.get('state_machine_type')

    @builtins.property
    def tags(self) -> typing.Optional[typing.List["CfnStateMachine.TagsEntryProperty"]]:
        """``AWS::StepFunctions::StateMachine.Tags``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-stepfunctions-statemachine.html#cfn-stepfunctions-statemachine-tags
        """
        return self._values.get('tags')

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return 'CfnStateMachineProps(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


@jsii.data_type(jsii_type="@aws-cdk/aws-stepfunctions.ChoiceProps", jsii_struct_bases=[], name_mapping={'comment': 'comment', 'input_path': 'inputPath', 'output_path': 'outputPath'})
class ChoiceProps():
    def __init__(self, *, comment: typing.Optional[str]=None, input_path: typing.Optional[str]=None, output_path: typing.Optional[str]=None) -> None:
        """Properties for defining a Choice state.

        :param comment: An optional description for this state. Default: No comment
        :param input_path: JSONPath expression to select part of the state to be the input to this state. May also be the special value DISCARD, which will cause the effective input to be the empty object {}. Default: $
        :param output_path: JSONPath expression to select part of the state to be the output to this state. May also be the special value DISCARD, which will cause the effective output to be the empty object {}. Default: $

        stability
        :stability: experimental
        """
        self._values = {
        }
        if comment is not None: self._values["comment"] = comment
        if input_path is not None: self._values["input_path"] = input_path
        if output_path is not None: self._values["output_path"] = output_path

    @builtins.property
    def comment(self) -> typing.Optional[str]:
        """An optional description for this state.

        default
        :default: No comment

        stability
        :stability: experimental
        """
        return self._values.get('comment')

    @builtins.property
    def input_path(self) -> typing.Optional[str]:
        """JSONPath expression to select part of the state to be the input to this state.

        May also be the special value DISCARD, which will cause the effective
        input to be the empty object {}.

        default
        :default: $

        stability
        :stability: experimental
        """
        return self._values.get('input_path')

    @builtins.property
    def output_path(self) -> typing.Optional[str]:
        """JSONPath expression to select part of the state to be the output to this state.

        May also be the special value DISCARD, which will cause the effective
        output to be the empty object {}.

        default
        :default: $

        stability
        :stability: experimental
        """
        return self._values.get('output_path')

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return 'ChoiceProps(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


class Condition(metaclass=jsii.JSIIAbstractClass, jsii_type="@aws-cdk/aws-stepfunctions.Condition"):
    """A Condition for use in a Choice state branch.

    stability
    :stability: experimental
    """
    @builtins.staticmethod
    def __jsii_proxy_class__():
        return _ConditionProxy

    def __init__(self) -> None:
        jsii.create(Condition, self, [])

    @jsii.member(jsii_name="and")
    @builtins.classmethod
    def and_(cls, *conditions: "Condition") -> "Condition":
        """Combine two or more conditions with a logical AND.

        :param conditions: -

        stability
        :stability: experimental
        """
        return jsii.sinvoke(cls, "and", [*conditions])

    @jsii.member(jsii_name="booleanEquals")
    @builtins.classmethod
    def boolean_equals(cls, variable: str, value: bool) -> "Condition":
        """Matches if a boolean field has the given value.

        :param variable: -
        :param value: -

        stability
        :stability: experimental
        """
        return jsii.sinvoke(cls, "booleanEquals", [variable, value])

    @jsii.member(jsii_name="not")
    @builtins.classmethod
    def not_(cls, condition: "Condition") -> "Condition":
        """Negate a condition.

        :param condition: -

        stability
        :stability: experimental
        """
        return jsii.sinvoke(cls, "not", [condition])

    @jsii.member(jsii_name="numberEquals")
    @builtins.classmethod
    def number_equals(cls, variable: str, value: jsii.Number) -> "Condition":
        """Matches if a numeric field has the given value.

        :param variable: -
        :param value: -

        stability
        :stability: experimental
        """
        return jsii.sinvoke(cls, "numberEquals", [variable, value])

    @jsii.member(jsii_name="numberGreaterThan")
    @builtins.classmethod
    def number_greater_than(cls, variable: str, value: jsii.Number) -> "Condition":
        """Matches if a numeric field is greater than the given value.

        :param variable: -
        :param value: -

        stability
        :stability: experimental
        """
        return jsii.sinvoke(cls, "numberGreaterThan", [variable, value])

    @jsii.member(jsii_name="numberGreaterThanEquals")
    @builtins.classmethod
    def number_greater_than_equals(cls, variable: str, value: jsii.Number) -> "Condition":
        """Matches if a numeric field is greater than or equal to the given value.

        :param variable: -
        :param value: -

        stability
        :stability: experimental
        """
        return jsii.sinvoke(cls, "numberGreaterThanEquals", [variable, value])

    @jsii.member(jsii_name="numberLessThan")
    @builtins.classmethod
    def number_less_than(cls, variable: str, value: jsii.Number) -> "Condition":
        """Matches if a numeric field is less than the given value.

        :param variable: -
        :param value: -

        stability
        :stability: experimental
        """
        return jsii.sinvoke(cls, "numberLessThan", [variable, value])

    @jsii.member(jsii_name="numberLessThanEquals")
    @builtins.classmethod
    def number_less_than_equals(cls, variable: str, value: jsii.Number) -> "Condition":
        """Matches if a numeric field is less than or equal to the given value.

        :param variable: -
        :param value: -

        stability
        :stability: experimental
        """
        return jsii.sinvoke(cls, "numberLessThanEquals", [variable, value])

    @jsii.member(jsii_name="or")
    @builtins.classmethod
    def or_(cls, *conditions: "Condition") -> "Condition":
        """Combine two or more conditions with a logical OR.

        :param conditions: -

        stability
        :stability: experimental
        """
        return jsii.sinvoke(cls, "or", [*conditions])

    @jsii.member(jsii_name="stringEquals")
    @builtins.classmethod
    def string_equals(cls, variable: str, value: str) -> "Condition":
        """Matches if a string field has the given value.

        :param variable: -
        :param value: -

        stability
        :stability: experimental
        """
        return jsii.sinvoke(cls, "stringEquals", [variable, value])

    @jsii.member(jsii_name="stringGreaterThan")
    @builtins.classmethod
    def string_greater_than(cls, variable: str, value: str) -> "Condition":
        """Matches if a string field sorts after a given value.

        :param variable: -
        :param value: -

        stability
        :stability: experimental
        """
        return jsii.sinvoke(cls, "stringGreaterThan", [variable, value])

    @jsii.member(jsii_name="stringGreaterThanEquals")
    @builtins.classmethod
    def string_greater_than_equals(cls, variable: str, value: str) -> "Condition":
        """Matches if a string field sorts after or equal to a given value.

        :param variable: -
        :param value: -

        stability
        :stability: experimental
        """
        return jsii.sinvoke(cls, "stringGreaterThanEquals", [variable, value])

    @jsii.member(jsii_name="stringLessThan")
    @builtins.classmethod
    def string_less_than(cls, variable: str, value: str) -> "Condition":
        """Matches if a string field sorts before a given value.

        :param variable: -
        :param value: -

        stability
        :stability: experimental
        """
        return jsii.sinvoke(cls, "stringLessThan", [variable, value])

    @jsii.member(jsii_name="stringLessThanEquals")
    @builtins.classmethod
    def string_less_than_equals(cls, variable: str, value: str) -> "Condition":
        """Matches if a string field sorts equal to or before a given value.

        :param variable: -
        :param value: -

        stability
        :stability: experimental
        """
        return jsii.sinvoke(cls, "stringLessThanEquals", [variable, value])

    @jsii.member(jsii_name="timestampEquals")
    @builtins.classmethod
    def timestamp_equals(cls, variable: str, value: str) -> "Condition":
        """Matches if a timestamp field is the same time as the given timestamp.

        :param variable: -
        :param value: -

        stability
        :stability: experimental
        """
        return jsii.sinvoke(cls, "timestampEquals", [variable, value])

    @jsii.member(jsii_name="timestampGreaterThan")
    @builtins.classmethod
    def timestamp_greater_than(cls, variable: str, value: str) -> "Condition":
        """Matches if a timestamp field is after the given timestamp.

        :param variable: -
        :param value: -

        stability
        :stability: experimental
        """
        return jsii.sinvoke(cls, "timestampGreaterThan", [variable, value])

    @jsii.member(jsii_name="timestampGreaterThanEquals")
    @builtins.classmethod
    def timestamp_greater_than_equals(cls, variable: str, value: str) -> "Condition":
        """Matches if a timestamp field is after or equal to the given timestamp.

        :param variable: -
        :param value: -

        stability
        :stability: experimental
        """
        return jsii.sinvoke(cls, "timestampGreaterThanEquals", [variable, value])

    @jsii.member(jsii_name="timestampLessThan")
    @builtins.classmethod
    def timestamp_less_than(cls, variable: str, value: str) -> "Condition":
        """Matches if a timestamp field is before the given timestamp.

        :param variable: -
        :param value: -

        stability
        :stability: experimental
        """
        return jsii.sinvoke(cls, "timestampLessThan", [variable, value])

    @jsii.member(jsii_name="timestampLessThanEquals")
    @builtins.classmethod
    def timestamp_less_than_equals(cls, variable: str, value: str) -> "Condition":
        """Matches if a timestamp field is before or equal to the given timestamp.

        :param variable: -
        :param value: -

        stability
        :stability: experimental
        """
        return jsii.sinvoke(cls, "timestampLessThanEquals", [variable, value])

    @jsii.member(jsii_name="renderCondition")
    @abc.abstractmethod
    def render_condition(self) -> typing.Any:
        """Render Amazon States Language JSON for the condition.

        stability
        :stability: experimental
        """
        ...


class _ConditionProxy(Condition):
    @jsii.member(jsii_name="renderCondition")
    def render_condition(self) -> typing.Any:
        """Render Amazon States Language JSON for the condition.

        stability
        :stability: experimental
        """
        return jsii.invoke(self, "renderCondition", [])


class Context(metaclass=jsii.JSIIMeta, jsii_type="@aws-cdk/aws-stepfunctions.Context"):
    """Extract a field from the State Machine Context data.

    see
    :see: https://docs.aws.amazon.com/step-functions/latest/dg/connect-to-resource.html#wait-token-contextobject
    stability
    :stability: experimental
    """
    @jsii.member(jsii_name="numberAt")
    @builtins.classmethod
    def number_at(cls, path: str) -> jsii.Number:
        """Instead of using a literal number, get the value from a JSON path.

        :param path: -

        stability
        :stability: experimental
        """
        return jsii.sinvoke(cls, "numberAt", [path])

    @jsii.member(jsii_name="stringAt")
    @builtins.classmethod
    def string_at(cls, path: str) -> str:
        """Instead of using a literal string, get the value from a JSON path.

        :param path: -

        stability
        :stability: experimental
        """
        return jsii.sinvoke(cls, "stringAt", [path])

    @jsii.python.classproperty
    @jsii.member(jsii_name="entireContext")
    def entire_context(cls) -> str:
        """Use the entire context data structure.

        Will be an object at invocation time, but is represented in the CDK
        application as a string.

        stability
        :stability: experimental
        """
        return jsii.sget(cls, "entireContext")

    @jsii.python.classproperty
    @jsii.member(jsii_name="taskToken")
    def task_token(cls) -> str:
        """Return the Task Token field.

        External actions will need this token to report step completion
        back to StepFunctions using the ``SendTaskSuccess`` or ``SendTaskFailure``
        calls.

        stability
        :stability: experimental
        """
        return jsii.sget(cls, "taskToken")


@jsii.data_type(jsii_type="@aws-cdk/aws-stepfunctions.CustomStateProps", jsii_struct_bases=[], name_mapping={'state_json': 'stateJson'})
class CustomStateProps():
    def __init__(self, *, state_json: typing.Mapping[str, typing.Any]) -> None:
        """Properties for defining a custom state definition.

        :param state_json: Amazon States Language (JSON-based) definition of the state.

        stability
        :stability: experimental
        """
        self._values = {
            'state_json': state_json,
        }

    @builtins.property
    def state_json(self) -> typing.Mapping[str, typing.Any]:
        """Amazon States Language (JSON-based) definition of the state.

        see
        :see: https://docs.aws.amazon.com/step-functions/latest/dg/concepts-amazon-states-language.html
        stability
        :stability: experimental
        """
        return self._values.get('state_json')

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return 'CustomStateProps(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


class Data(metaclass=jsii.JSIIMeta, jsii_type="@aws-cdk/aws-stepfunctions.Data"):
    """Extract a field from the State Machine data that gets passed around between states.

    stability
    :stability: experimental
    """
    @jsii.member(jsii_name="isJsonPathString")
    @builtins.classmethod
    def is_json_path_string(cls, value: str) -> bool:
        """Determines if the indicated string is an encoded JSON path.

        :param value: string to be evaluated.

        stability
        :stability: experimental
        """
        return jsii.sinvoke(cls, "isJsonPathString", [value])

    @jsii.member(jsii_name="listAt")
    @builtins.classmethod
    def list_at(cls, path: str) -> typing.List[str]:
        """Instead of using a literal string list, get the value from a JSON path.

        :param path: -

        stability
        :stability: experimental
        """
        return jsii.sinvoke(cls, "listAt", [path])

    @jsii.member(jsii_name="numberAt")
    @builtins.classmethod
    def number_at(cls, path: str) -> jsii.Number:
        """Instead of using a literal number, get the value from a JSON path.

        :param path: -

        stability
        :stability: experimental
        """
        return jsii.sinvoke(cls, "numberAt", [path])

    @jsii.member(jsii_name="stringAt")
    @builtins.classmethod
    def string_at(cls, path: str) -> str:
        """Instead of using a literal string, get the value from a JSON path.

        :param path: -

        stability
        :stability: experimental
        """
        return jsii.sinvoke(cls, "stringAt", [path])

    @jsii.python.classproperty
    @jsii.member(jsii_name="entirePayload")
    def entire_payload(cls) -> str:
        """Use the entire data structure.

        Will be an object at invocation time, but is represented in the CDK
        application as a string.

        stability
        :stability: experimental
        """
        return jsii.sget(cls, "entirePayload")


class Errors(metaclass=jsii.JSIIMeta, jsii_type="@aws-cdk/aws-stepfunctions.Errors"):
    """Predefined error strings Error names in Amazon States Language - https://states-language.net/spec.html#appendix-a Error handling in Step Functions - https://docs.aws.amazon.com/step-functions/latest/dg/concepts-error-handling.html.

    stability
    :stability: experimental
    """
    def __init__(self) -> None:
        jsii.create(Errors, self, [])

    @jsii.python.classproperty
    @jsii.member(jsii_name="ALL")
    def ALL(cls) -> str:
        """Matches any Error.

        stability
        :stability: experimental
        """
        return jsii.sget(cls, "ALL")

    @jsii.python.classproperty
    @jsii.member(jsii_name="BRANCH_FAILED")
    def BRANCH_FAILED(cls) -> str:
        """A branch of a Parallel state failed.

        stability
        :stability: experimental
        """
        return jsii.sget(cls, "BRANCH_FAILED")

    @jsii.python.classproperty
    @jsii.member(jsii_name="NO_CHOICE_MATCHED")
    def NO_CHOICE_MATCHED(cls) -> str:
        """A Choice state failed to find a match for the condition field extracted from its input.

        stability
        :stability: experimental
        """
        return jsii.sget(cls, "NO_CHOICE_MATCHED")

    @jsii.python.classproperty
    @jsii.member(jsii_name="PARAMETER_PATH_FAILURE")
    def PARAMETER_PATH_FAILURE(cls) -> str:
        """Within a state’s “Parameters” field, the attempt to replace a field whose name ends in “.$” using a Path failed.

        stability
        :stability: experimental
        """
        return jsii.sget(cls, "PARAMETER_PATH_FAILURE")

    @jsii.python.classproperty
    @jsii.member(jsii_name="PERMISSIONS")
    def PERMISSIONS(cls) -> str:
        """A Task State failed because it had insufficient privileges to execute the specified code.

        stability
        :stability: experimental
        """
        return jsii.sget(cls, "PERMISSIONS")

    @jsii.python.classproperty
    @jsii.member(jsii_name="RESULT_PATH_MATCH_FAILURE")
    def RESULT_PATH_MATCH_FAILURE(cls) -> str:
        """A Task State’s “ResultPath” field cannot be applied to the input the state received.

        stability
        :stability: experimental
        """
        return jsii.sget(cls, "RESULT_PATH_MATCH_FAILURE")

    @jsii.python.classproperty
    @jsii.member(jsii_name="TASKS_FAILED")
    def TASKS_FAILED(cls) -> str:
        """A Task State failed during the execution.

        stability
        :stability: experimental
        """
        return jsii.sget(cls, "TASKS_FAILED")

    @jsii.python.classproperty
    @jsii.member(jsii_name="TIMEOUT")
    def TIMEOUT(cls) -> str:
        """A Task State either ran longer than the “TimeoutSeconds” value, or failed to heartbeat for a time longer than the “HeartbeatSeconds” value.

        stability
        :stability: experimental
        """
        return jsii.sget(cls, "TIMEOUT")


@jsii.data_type(jsii_type="@aws-cdk/aws-stepfunctions.FailProps", jsii_struct_bases=[], name_mapping={'cause': 'cause', 'comment': 'comment', 'error': 'error'})
class FailProps():
    def __init__(self, *, cause: typing.Optional[str]=None, comment: typing.Optional[str]=None, error: typing.Optional[str]=None) -> None:
        """Properties for defining a Fail state.

        :param cause: A description for the cause of the failure. Default: No description
        :param comment: An optional description for this state. Default: No comment
        :param error: Error code used to represent this failure. Default: No error code

        stability
        :stability: experimental
        """
        self._values = {
        }
        if cause is not None: self._values["cause"] = cause
        if comment is not None: self._values["comment"] = comment
        if error is not None: self._values["error"] = error

    @builtins.property
    def cause(self) -> typing.Optional[str]:
        """A description for the cause of the failure.

        default
        :default: No description

        stability
        :stability: experimental
        """
        return self._values.get('cause')

    @builtins.property
    def comment(self) -> typing.Optional[str]:
        """An optional description for this state.

        default
        :default: No comment

        stability
        :stability: experimental
        """
        return self._values.get('comment')

    @builtins.property
    def error(self) -> typing.Optional[str]:
        """Error code used to represent this failure.

        default
        :default: No error code

        stability
        :stability: experimental
        """
        return self._values.get('error')

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return 'FailProps(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


class FieldUtils(metaclass=jsii.JSIIMeta, jsii_type="@aws-cdk/aws-stepfunctions.FieldUtils"):
    """Helper functions to work with structures containing fields.

    stability
    :stability: experimental
    """
    @jsii.member(jsii_name="containsTaskToken")
    @builtins.classmethod
    def contains_task_token(cls, obj: typing.Optional[typing.Mapping[str, typing.Any]]=None) -> bool:
        """Returns whether the given task structure contains the TaskToken field anywhere.

        The field is considered included if the field itself or one of its containing
        fields occurs anywhere in the payload.

        :param obj: -

        stability
        :stability: experimental
        """
        return jsii.sinvoke(cls, "containsTaskToken", [obj])

    @jsii.member(jsii_name="findReferencedPaths")
    @builtins.classmethod
    def find_referenced_paths(cls, obj: typing.Optional[typing.Mapping[str, typing.Any]]=None) -> typing.List[str]:
        """Return all JSON paths used in the given structure.

        :param obj: -

        stability
        :stability: experimental
        """
        return jsii.sinvoke(cls, "findReferencedPaths", [obj])

    @jsii.member(jsii_name="renderObject")
    @builtins.classmethod
    def render_object(cls, obj: typing.Optional[typing.Mapping[str, typing.Any]]=None) -> typing.Optional[typing.Mapping[str, typing.Any]]:
        """Render a JSON structure containing fields to the right StepFunctions structure.

        :param obj: -

        stability
        :stability: experimental
        """
        return jsii.sinvoke(cls, "renderObject", [obj])


@jsii.data_type(jsii_type="@aws-cdk/aws-stepfunctions.FindStateOptions", jsii_struct_bases=[], name_mapping={'include_error_handlers': 'includeErrorHandlers'})
class FindStateOptions():
    def __init__(self, *, include_error_handlers: typing.Optional[bool]=None) -> None:
        """Options for finding reachable states.

        :param include_error_handlers: Whether or not to follow error-handling transitions. Default: false

        stability
        :stability: experimental
        """
        self._values = {
        }
        if include_error_handlers is not None: self._values["include_error_handlers"] = include_error_handlers

    @builtins.property
    def include_error_handlers(self) -> typing.Optional[bool]:
        """Whether or not to follow error-handling transitions.

        default
        :default: false

        stability
        :stability: experimental
        """
        return self._values.get('include_error_handlers')

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return 'FindStateOptions(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


@jsii.interface(jsii_type="@aws-cdk/aws-stepfunctions.IActivity")
class IActivity(aws_cdk.core.IResource, jsii.compat.Protocol):
    """Represents a Step Functions Activity https://docs.aws.amazon.com/step-functions/latest/dg/concepts-activities.html.

    stability
    :stability: experimental
    """
    @builtins.staticmethod
    def __jsii_proxy_class__():
        return _IActivityProxy

    @builtins.property
    @jsii.member(jsii_name="activityArn")
    def activity_arn(self) -> str:
        """The ARN of the activity.

        stability
        :stability: experimental
        attribute:
        :attribute:: true
        """
        ...

    @builtins.property
    @jsii.member(jsii_name="activityName")
    def activity_name(self) -> str:
        """The name of the activity.

        stability
        :stability: experimental
        attribute:
        :attribute:: true
        """
        ...


class _IActivityProxy(jsii.proxy_for(aws_cdk.core.IResource)):
    """Represents a Step Functions Activity https://docs.aws.amazon.com/step-functions/latest/dg/concepts-activities.html.

    stability
    :stability: experimental
    """
    __jsii_type__ = "@aws-cdk/aws-stepfunctions.IActivity"
    @builtins.property
    @jsii.member(jsii_name="activityArn")
    def activity_arn(self) -> str:
        """The ARN of the activity.

        stability
        :stability: experimental
        attribute:
        :attribute:: true
        """
        return jsii.get(self, "activityArn")

    @builtins.property
    @jsii.member(jsii_name="activityName")
    def activity_name(self) -> str:
        """The name of the activity.

        stability
        :stability: experimental
        attribute:
        :attribute:: true
        """
        return jsii.get(self, "activityName")


@jsii.interface(jsii_type="@aws-cdk/aws-stepfunctions.IChainable")
class IChainable(jsii.compat.Protocol):
    """Interface for objects that can be used in a Chain.

    stability
    :stability: experimental
    """
    @builtins.staticmethod
    def __jsii_proxy_class__():
        return _IChainableProxy

    @builtins.property
    @jsii.member(jsii_name="endStates")
    def end_states(self) -> typing.List["INextable"]:
        """The chainable end state(s) of this chainable.

        stability
        :stability: experimental
        """
        ...

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> str:
        """Descriptive identifier for this chainable.

        stability
        :stability: experimental
        """
        ...

    @builtins.property
    @jsii.member(jsii_name="startState")
    def start_state(self) -> "State":
        """The start state of this chainable.

        stability
        :stability: experimental
        """
        ...


class _IChainableProxy():
    """Interface for objects that can be used in a Chain.

    stability
    :stability: experimental
    """
    __jsii_type__ = "@aws-cdk/aws-stepfunctions.IChainable"
    @builtins.property
    @jsii.member(jsii_name="endStates")
    def end_states(self) -> typing.List["INextable"]:
        """The chainable end state(s) of this chainable.

        stability
        :stability: experimental
        """
        return jsii.get(self, "endStates")

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> str:
        """Descriptive identifier for this chainable.

        stability
        :stability: experimental
        """
        return jsii.get(self, "id")

    @builtins.property
    @jsii.member(jsii_name="startState")
    def start_state(self) -> "State":
        """The start state of this chainable.

        stability
        :stability: experimental
        """
        return jsii.get(self, "startState")


@jsii.interface(jsii_type="@aws-cdk/aws-stepfunctions.INextable")
class INextable(jsii.compat.Protocol):
    """Interface for states that can have 'next' states.

    stability
    :stability: experimental
    """
    @builtins.staticmethod
    def __jsii_proxy_class__():
        return _INextableProxy

    @jsii.member(jsii_name="next")
    def next(self, state: "IChainable") -> "Chain":
        """Go to the indicated state after this state.

        :param state: -

        return
        :return: The chain of states built up

        stability
        :stability: experimental
        """
        ...


class _INextableProxy():
    """Interface for states that can have 'next' states.

    stability
    :stability: experimental
    """
    __jsii_type__ = "@aws-cdk/aws-stepfunctions.INextable"
    @jsii.member(jsii_name="next")
    def next(self, state: "IChainable") -> "Chain":
        """Go to the indicated state after this state.

        :param state: -

        return
        :return: The chain of states built up

        stability
        :stability: experimental
        """
        return jsii.invoke(self, "next", [state])


@jsii.interface(jsii_type="@aws-cdk/aws-stepfunctions.IStateMachine")
class IStateMachine(aws_cdk.core.IResource, jsii.compat.Protocol):
    """A State Machine.

    stability
    :stability: experimental
    """
    @builtins.staticmethod
    def __jsii_proxy_class__():
        return _IStateMachineProxy

    @builtins.property
    @jsii.member(jsii_name="stateMachineArn")
    def state_machine_arn(self) -> str:
        """The ARN of the state machine.

        stability
        :stability: experimental
        attribute:
        :attribute:: true
        """
        ...

    @jsii.member(jsii_name="grantStartExecution")
    def grant_start_execution(self, identity: aws_cdk.aws_iam.IGrantable) -> aws_cdk.aws_iam.Grant:
        """Grant the given identity permissions to start an execution of this state machine.

        :param identity: The principal.

        stability
        :stability: experimental
        """
        ...


class _IStateMachineProxy(jsii.proxy_for(aws_cdk.core.IResource)):
    """A State Machine.

    stability
    :stability: experimental
    """
    __jsii_type__ = "@aws-cdk/aws-stepfunctions.IStateMachine"
    @builtins.property
    @jsii.member(jsii_name="stateMachineArn")
    def state_machine_arn(self) -> str:
        """The ARN of the state machine.

        stability
        :stability: experimental
        attribute:
        :attribute:: true
        """
        return jsii.get(self, "stateMachineArn")

    @jsii.member(jsii_name="grantStartExecution")
    def grant_start_execution(self, identity: aws_cdk.aws_iam.IGrantable) -> aws_cdk.aws_iam.Grant:
        """Grant the given identity permissions to start an execution of this state machine.

        :param identity: The principal.

        stability
        :stability: experimental
        """
        return jsii.invoke(self, "grantStartExecution", [identity])


@jsii.interface(jsii_type="@aws-cdk/aws-stepfunctions.IStepFunctionsTask")
class IStepFunctionsTask(jsii.compat.Protocol):
    """Interface for resources that can be used as tasks.

    stability
    :stability: experimental
    """
    @builtins.staticmethod
    def __jsii_proxy_class__():
        return _IStepFunctionsTaskProxy

    @jsii.member(jsii_name="bind")
    def bind(self, task: "Task") -> "StepFunctionsTaskConfig":
        """Called when the task object is used in a workflow.

        :param task: -

        stability
        :stability: experimental
        """
        ...


class _IStepFunctionsTaskProxy():
    """Interface for resources that can be used as tasks.

    stability
    :stability: experimental
    """
    __jsii_type__ = "@aws-cdk/aws-stepfunctions.IStepFunctionsTask"
    @jsii.member(jsii_name="bind")
    def bind(self, task: "Task") -> "StepFunctionsTaskConfig":
        """Called when the task object is used in a workflow.

        :param task: -

        stability
        :stability: experimental
        """
        return jsii.invoke(self, "bind", [task])


@jsii.enum(jsii_type="@aws-cdk/aws-stepfunctions.InputType")
class InputType(enum.Enum):
    """The type of task input.

    stability
    :stability: experimental
    """
    TEXT = "TEXT"
    """Use a literal string This might be a JSON-encoded object, or just text.

    valid JSON text: standalone, quote-delimited strings; objects; arrays; numbers; Boolean values; and null.

    example: ``literal string``
    example: {"json": "encoded"}

    stability
    :stability: experimental
    """
    OBJECT = "OBJECT"
    """Use an object which may contain Data and Context fields as object values, if desired.

    example:
    {
    literal: 'literal',
    SomeInput: sfn.Data.stringAt('$.someField')
    }

    see
    :see: https://docs.aws.amazon.com/step-functions/latest/dg/input-output-contextobject.html
    stability
    :stability: experimental
    """

@jsii.enum(jsii_type="@aws-cdk/aws-stepfunctions.LogLevel")
class LogLevel(enum.Enum):
    """Defines which category of execution history events are logged.

    default
    :default: ERROR

    see
    :see: https://docs.aws.amazon.com/step-functions/latest/dg/cloudwatch-log-level.html
    stability
    :stability: experimental
    """
    OFF = "OFF"
    """No Logging.

    stability
    :stability: experimental
    """
    ALL = "ALL"
    """Log everything.

    stability
    :stability: experimental
    """
    ERROR = "ERROR"
    """Log all errors.

    stability
    :stability: experimental
    """
    FATAL = "FATAL"
    """Log fatal errors.

    stability
    :stability: experimental
    """

@jsii.data_type(jsii_type="@aws-cdk/aws-stepfunctions.LogOptions", jsii_struct_bases=[], name_mapping={'destination': 'destination', 'include_execution_data': 'includeExecutionData', 'level': 'level'})
class LogOptions():
    def __init__(self, *, destination: aws_cdk.aws_logs.ILogGroup, include_execution_data: typing.Optional[bool]=None, level: typing.Optional["LogLevel"]=None) -> None:
        """Defines what execution history events are logged and where they are logged.

        :param destination: The log group where the execution history events will be logged.
        :param include_execution_data: Determines whether execution data is included in your log. Default: true
        :param level: Defines which category of execution history events are logged. Default: ERROR

        stability
        :stability: experimental
        """
        self._values = {
            'destination': destination,
        }
        if include_execution_data is not None: self._values["include_execution_data"] = include_execution_data
        if level is not None: self._values["level"] = level

    @builtins.property
    def destination(self) -> aws_cdk.aws_logs.ILogGroup:
        """The log group where the execution history events will be logged.

        stability
        :stability: experimental
        """
        return self._values.get('destination')

    @builtins.property
    def include_execution_data(self) -> typing.Optional[bool]:
        """Determines whether execution data is included in your log.

        default
        :default: true

        stability
        :stability: experimental
        """
        return self._values.get('include_execution_data')

    @builtins.property
    def level(self) -> typing.Optional["LogLevel"]:
        """Defines which category of execution history events are logged.

        default
        :default: ERROR

        stability
        :stability: experimental
        """
        return self._values.get('level')

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return 'LogOptions(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


@jsii.data_type(jsii_type="@aws-cdk/aws-stepfunctions.MapProps", jsii_struct_bases=[], name_mapping={'comment': 'comment', 'input_path': 'inputPath', 'items_path': 'itemsPath', 'max_concurrency': 'maxConcurrency', 'output_path': 'outputPath', 'parameters': 'parameters', 'result_path': 'resultPath'})
class MapProps():
    def __init__(self, *, comment: typing.Optional[str]=None, input_path: typing.Optional[str]=None, items_path: typing.Optional[str]=None, max_concurrency: typing.Optional[jsii.Number]=None, output_path: typing.Optional[str]=None, parameters: typing.Optional[typing.Mapping[str, typing.Any]]=None, result_path: typing.Optional[str]=None) -> None:
        """Properties for defining a Map state.

        :param comment: An optional description for this state. Default: No comment
        :param input_path: JSONPath expression to select part of the state to be the input to this state. May also be the special value DISCARD, which will cause the effective input to be the empty object {}. Default: $
        :param items_path: JSONPath expression to select the array to iterate over. Default: $
        :param max_concurrency: MaxConcurrency. An upper bound on the number of iterations you want running at once. Default: - full concurrency
        :param output_path: JSONPath expression to select part of the state to be the output to this state. May also be the special value DISCARD, which will cause the effective output to be the empty object {}. Default: $
        :param parameters: The JSON that you want to override your default iteration input. Default: $
        :param result_path: JSONPath expression to indicate where to inject the state's output. May also be the special value DISCARD, which will cause the state's input to become its output. Default: $

        stability
        :stability: experimental
        """
        self._values = {
        }
        if comment is not None: self._values["comment"] = comment
        if input_path is not None: self._values["input_path"] = input_path
        if items_path is not None: self._values["items_path"] = items_path
        if max_concurrency is not None: self._values["max_concurrency"] = max_concurrency
        if output_path is not None: self._values["output_path"] = output_path
        if parameters is not None: self._values["parameters"] = parameters
        if result_path is not None: self._values["result_path"] = result_path

    @builtins.property
    def comment(self) -> typing.Optional[str]:
        """An optional description for this state.

        default
        :default: No comment

        stability
        :stability: experimental
        """
        return self._values.get('comment')

    @builtins.property
    def input_path(self) -> typing.Optional[str]:
        """JSONPath expression to select part of the state to be the input to this state.

        May also be the special value DISCARD, which will cause the effective
        input to be the empty object {}.

        default
        :default: $

        stability
        :stability: experimental
        """
        return self._values.get('input_path')

    @builtins.property
    def items_path(self) -> typing.Optional[str]:
        """JSONPath expression to select the array to iterate over.

        default
        :default: $

        stability
        :stability: experimental
        """
        return self._values.get('items_path')

    @builtins.property
    def max_concurrency(self) -> typing.Optional[jsii.Number]:
        """MaxConcurrency.

        An upper bound on the number of iterations you want running at once.

        default
        :default: - full concurrency

        stability
        :stability: experimental
        """
        return self._values.get('max_concurrency')

    @builtins.property
    def output_path(self) -> typing.Optional[str]:
        """JSONPath expression to select part of the state to be the output to this state.

        May also be the special value DISCARD, which will cause the effective
        output to be the empty object {}.

        default
        :default: $

        stability
        :stability: experimental
        """
        return self._values.get('output_path')

    @builtins.property
    def parameters(self) -> typing.Optional[typing.Mapping[str, typing.Any]]:
        """The JSON that you want to override your default iteration input.

        default
        :default: $

        stability
        :stability: experimental
        """
        return self._values.get('parameters')

    @builtins.property
    def result_path(self) -> typing.Optional[str]:
        """JSONPath expression to indicate where to inject the state's output.

        May also be the special value DISCARD, which will cause the state's
        input to become its output.

        default
        :default: $

        stability
        :stability: experimental
        """
        return self._values.get('result_path')

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return 'MapProps(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


@jsii.data_type(jsii_type="@aws-cdk/aws-stepfunctions.ParallelProps", jsii_struct_bases=[], name_mapping={'comment': 'comment', 'input_path': 'inputPath', 'output_path': 'outputPath', 'result_path': 'resultPath'})
class ParallelProps():
    def __init__(self, *, comment: typing.Optional[str]=None, input_path: typing.Optional[str]=None, output_path: typing.Optional[str]=None, result_path: typing.Optional[str]=None) -> None:
        """Properties for defining a Parallel state.

        :param comment: An optional description for this state. Default: No comment
        :param input_path: JSONPath expression to select part of the state to be the input to this state. May also be the special value DISCARD, which will cause the effective input to be the empty object {}. Default: $
        :param output_path: JSONPath expression to select part of the state to be the output to this state. May also be the special value DISCARD, which will cause the effective output to be the empty object {}. Default: $
        :param result_path: JSONPath expression to indicate where to inject the state's output. May also be the special value DISCARD, which will cause the state's input to become its output. Default: $

        stability
        :stability: experimental
        """
        self._values = {
        }
        if comment is not None: self._values["comment"] = comment
        if input_path is not None: self._values["input_path"] = input_path
        if output_path is not None: self._values["output_path"] = output_path
        if result_path is not None: self._values["result_path"] = result_path

    @builtins.property
    def comment(self) -> typing.Optional[str]:
        """An optional description for this state.

        default
        :default: No comment

        stability
        :stability: experimental
        """
        return self._values.get('comment')

    @builtins.property
    def input_path(self) -> typing.Optional[str]:
        """JSONPath expression to select part of the state to be the input to this state.

        May also be the special value DISCARD, which will cause the effective
        input to be the empty object {}.

        default
        :default: $

        stability
        :stability: experimental
        """
        return self._values.get('input_path')

    @builtins.property
    def output_path(self) -> typing.Optional[str]:
        """JSONPath expression to select part of the state to be the output to this state.

        May also be the special value DISCARD, which will cause the effective
        output to be the empty object {}.

        default
        :default: $

        stability
        :stability: experimental
        """
        return self._values.get('output_path')

    @builtins.property
    def result_path(self) -> typing.Optional[str]:
        """JSONPath expression to indicate where to inject the state's output.

        May also be the special value DISCARD, which will cause the state's
        input to become its output.

        default
        :default: $

        stability
        :stability: experimental
        """
        return self._values.get('result_path')

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return 'ParallelProps(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


@jsii.data_type(jsii_type="@aws-cdk/aws-stepfunctions.PassProps", jsii_struct_bases=[], name_mapping={'comment': 'comment', 'input_path': 'inputPath', 'output_path': 'outputPath', 'parameters': 'parameters', 'result': 'result', 'result_path': 'resultPath'})
class PassProps():
    def __init__(self, *, comment: typing.Optional[str]=None, input_path: typing.Optional[str]=None, output_path: typing.Optional[str]=None, parameters: typing.Optional[typing.Mapping[str, typing.Any]]=None, result: typing.Optional["Result"]=None, result_path: typing.Optional[str]=None) -> None:
        """Properties for defining a Pass state.

        :param comment: An optional description for this state. Default: No comment
        :param input_path: JSONPath expression to select part of the state to be the input to this state. May also be the special value DISCARD, which will cause the effective input to be the empty object {}. Default: $
        :param output_path: JSONPath expression to select part of the state to be the output to this state. May also be the special value DISCARD, which will cause the effective output to be the empty object {}. Default: $
        :param parameters: Parameters pass a collection of key-value pairs, either static values or JSONPath expressions that select from the input. Default: No parameters
        :param result: If given, treat as the result of this operation. Can be used to inject or replace the current execution state. Default: No injected result
        :param result_path: JSONPath expression to indicate where to inject the state's output. May also be the special value DISCARD, which will cause the state's input to become its output. Default: $

        stability
        :stability: experimental
        """
        self._values = {
        }
        if comment is not None: self._values["comment"] = comment
        if input_path is not None: self._values["input_path"] = input_path
        if output_path is not None: self._values["output_path"] = output_path
        if parameters is not None: self._values["parameters"] = parameters
        if result is not None: self._values["result"] = result
        if result_path is not None: self._values["result_path"] = result_path

    @builtins.property
    def comment(self) -> typing.Optional[str]:
        """An optional description for this state.

        default
        :default: No comment

        stability
        :stability: experimental
        """
        return self._values.get('comment')

    @builtins.property
    def input_path(self) -> typing.Optional[str]:
        """JSONPath expression to select part of the state to be the input to this state.

        May also be the special value DISCARD, which will cause the effective
        input to be the empty object {}.

        default
        :default: $

        stability
        :stability: experimental
        """
        return self._values.get('input_path')

    @builtins.property
    def output_path(self) -> typing.Optional[str]:
        """JSONPath expression to select part of the state to be the output to this state.

        May also be the special value DISCARD, which will cause the effective
        output to be the empty object {}.

        default
        :default: $

        stability
        :stability: experimental
        """
        return self._values.get('output_path')

    @builtins.property
    def parameters(self) -> typing.Optional[typing.Mapping[str, typing.Any]]:
        """Parameters pass a collection of key-value pairs, either static values or JSONPath expressions that select from the input.

        default
        :default: No parameters

        see
        :see: https://docs.aws.amazon.com/step-functions/latest/dg/input-output-inputpath-params.html#input-output-parameters
        stability
        :stability: experimental
        """
        return self._values.get('parameters')

    @builtins.property
    def result(self) -> typing.Optional["Result"]:
        """If given, treat as the result of this operation.

        Can be used to inject or replace the current execution state.

        default
        :default: No injected result

        stability
        :stability: experimental
        """
        return self._values.get('result')

    @builtins.property
    def result_path(self) -> typing.Optional[str]:
        """JSONPath expression to indicate where to inject the state's output.

        May also be the special value DISCARD, which will cause the state's
        input to become its output.

        default
        :default: $

        stability
        :stability: experimental
        """
        return self._values.get('result_path')

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return 'PassProps(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


class Result(metaclass=jsii.JSIIMeta, jsii_type="@aws-cdk/aws-stepfunctions.Result"):
    """The result of a Pass operation.

    stability
    :stability: experimental
    """
    def __init__(self, value: typing.Any) -> None:
        """
        :param value: result of the Pass operation.

        stability
        :stability: experimental
        """
        jsii.create(Result, self, [value])

    @jsii.member(jsii_name="fromArray")
    @builtins.classmethod
    def from_array(cls, value: typing.List[typing.Any]) -> "Result":
        """The result of the operation is an array.

        :param value: -

        stability
        :stability: experimental
        """
        return jsii.sinvoke(cls, "fromArray", [value])

    @jsii.member(jsii_name="fromBoolean")
    @builtins.classmethod
    def from_boolean(cls, value: bool) -> "Result":
        """The result of the operation is a boolean.

        :param value: -

        stability
        :stability: experimental
        """
        return jsii.sinvoke(cls, "fromBoolean", [value])

    @jsii.member(jsii_name="fromNumber")
    @builtins.classmethod
    def from_number(cls, value: jsii.Number) -> "Result":
        """The result of the operation is a number.

        :param value: -

        stability
        :stability: experimental
        """
        return jsii.sinvoke(cls, "fromNumber", [value])

    @jsii.member(jsii_name="fromObject")
    @builtins.classmethod
    def from_object(cls, value: typing.Mapping[str, typing.Any]) -> "Result":
        """The result of the operation is an object.

        :param value: -

        stability
        :stability: experimental
        """
        return jsii.sinvoke(cls, "fromObject", [value])

    @jsii.member(jsii_name="fromString")
    @builtins.classmethod
    def from_string(cls, value: str) -> "Result":
        """The result of the operation is a string.

        :param value: -

        stability
        :stability: experimental
        """
        return jsii.sinvoke(cls, "fromString", [value])

    @builtins.property
    @jsii.member(jsii_name="value")
    def value(self) -> typing.Any:
        """result of the Pass operation.

        stability
        :stability: experimental
        """
        return jsii.get(self, "value")


@jsii.data_type(jsii_type="@aws-cdk/aws-stepfunctions.RetryProps", jsii_struct_bases=[], name_mapping={'backoff_rate': 'backoffRate', 'errors': 'errors', 'interval': 'interval', 'max_attempts': 'maxAttempts'})
class RetryProps():
    def __init__(self, *, backoff_rate: typing.Optional[jsii.Number]=None, errors: typing.Optional[typing.List[str]]=None, interval: typing.Optional[aws_cdk.core.Duration]=None, max_attempts: typing.Optional[jsii.Number]=None) -> None:
        """Retry details.

        :param backoff_rate: Multiplication for how much longer the wait interval gets on every retry. Default: 2
        :param errors: Errors to retry. A list of error strings to retry, which can be either predefined errors (for example Errors.NoChoiceMatched) or a self-defined error. Default: All errors
        :param interval: How many seconds to wait initially before retrying. Default: Duration.seconds(1)
        :param max_attempts: How many times to retry this particular error. May be 0 to disable retry for specific errors (in case you have a catch-all retry policy). Default: 3

        stability
        :stability: experimental
        """
        self._values = {
        }
        if backoff_rate is not None: self._values["backoff_rate"] = backoff_rate
        if errors is not None: self._values["errors"] = errors
        if interval is not None: self._values["interval"] = interval
        if max_attempts is not None: self._values["max_attempts"] = max_attempts

    @builtins.property
    def backoff_rate(self) -> typing.Optional[jsii.Number]:
        """Multiplication for how much longer the wait interval gets on every retry.

        default
        :default: 2

        stability
        :stability: experimental
        """
        return self._values.get('backoff_rate')

    @builtins.property
    def errors(self) -> typing.Optional[typing.List[str]]:
        """Errors to retry.

        A list of error strings to retry, which can be either predefined errors
        (for example Errors.NoChoiceMatched) or a self-defined error.

        default
        :default: All errors

        stability
        :stability: experimental
        """
        return self._values.get('errors')

    @builtins.property
    def interval(self) -> typing.Optional[aws_cdk.core.Duration]:
        """How many seconds to wait initially before retrying.

        default
        :default: Duration.seconds(1)

        stability
        :stability: experimental
        """
        return self._values.get('interval')

    @builtins.property
    def max_attempts(self) -> typing.Optional[jsii.Number]:
        """How many times to retry this particular error.

        May be 0 to disable retry for specific errors (in case you have
        a catch-all retry policy).

        default
        :default: 3

        stability
        :stability: experimental
        """
        return self._values.get('max_attempts')

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return 'RetryProps(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


@jsii.enum(jsii_type="@aws-cdk/aws-stepfunctions.ServiceIntegrationPattern")
class ServiceIntegrationPattern(enum.Enum):
    """Three ways to call an integrated service: Request Response, Run a Job and Wait for a Callback with Task Token.

    default
    :default: FIRE_AND_FORGET

    see
    :see:

    https://docs.aws.amazon.com/step-functions/latest/dg/connect-to-resource.html

    Here, they are named as FIRE_AND_FORGET, SYNC and WAIT_FOR_TASK_TOKEN respectly.
    stability
    :stability: experimental
    """
    FIRE_AND_FORGET = "FIRE_AND_FORGET"
    """Call a service and progress to the next state immediately after the API call completes.

    stability
    :stability: experimental
    """
    SYNC = "SYNC"
    """Call a service and wait for a job to complete.

    stability
    :stability: experimental
    """
    WAIT_FOR_TASK_TOKEN = "WAIT_FOR_TASK_TOKEN"
    """Call a service with a task token and wait until that token is returned by SendTaskSuccess/SendTaskFailure with paylaod.

    stability
    :stability: experimental
    """

@jsii.data_type(jsii_type="@aws-cdk/aws-stepfunctions.SingleStateOptions", jsii_struct_bases=[ParallelProps], name_mapping={'comment': 'comment', 'input_path': 'inputPath', 'output_path': 'outputPath', 'result_path': 'resultPath', 'prefix_states': 'prefixStates', 'state_id': 'stateId'})
class SingleStateOptions(ParallelProps):
    def __init__(self, *, comment: typing.Optional[str]=None, input_path: typing.Optional[str]=None, output_path: typing.Optional[str]=None, result_path: typing.Optional[str]=None, prefix_states: typing.Optional[str]=None, state_id: typing.Optional[str]=None) -> None:
        """Options for creating a single state.

        :param comment: An optional description for this state. Default: No comment
        :param input_path: JSONPath expression to select part of the state to be the input to this state. May also be the special value DISCARD, which will cause the effective input to be the empty object {}. Default: $
        :param output_path: JSONPath expression to select part of the state to be the output to this state. May also be the special value DISCARD, which will cause the effective output to be the empty object {}. Default: $
        :param result_path: JSONPath expression to indicate where to inject the state's output. May also be the special value DISCARD, which will cause the state's input to become its output. Default: $
        :param prefix_states: String to prefix all stateIds in the state machine with. Default: stateId
        :param state_id: ID of newly created containing state. Default: Construct ID of the StateMachineFragment

        stability
        :stability: experimental
        """
        self._values = {
        }
        if comment is not None: self._values["comment"] = comment
        if input_path is not None: self._values["input_path"] = input_path
        if output_path is not None: self._values["output_path"] = output_path
        if result_path is not None: self._values["result_path"] = result_path
        if prefix_states is not None: self._values["prefix_states"] = prefix_states
        if state_id is not None: self._values["state_id"] = state_id

    @builtins.property
    def comment(self) -> typing.Optional[str]:
        """An optional description for this state.

        default
        :default: No comment

        stability
        :stability: experimental
        """
        return self._values.get('comment')

    @builtins.property
    def input_path(self) -> typing.Optional[str]:
        """JSONPath expression to select part of the state to be the input to this state.

        May also be the special value DISCARD, which will cause the effective
        input to be the empty object {}.

        default
        :default: $

        stability
        :stability: experimental
        """
        return self._values.get('input_path')

    @builtins.property
    def output_path(self) -> typing.Optional[str]:
        """JSONPath expression to select part of the state to be the output to this state.

        May also be the special value DISCARD, which will cause the effective
        output to be the empty object {}.

        default
        :default: $

        stability
        :stability: experimental
        """
        return self._values.get('output_path')

    @builtins.property
    def result_path(self) -> typing.Optional[str]:
        """JSONPath expression to indicate where to inject the state's output.

        May also be the special value DISCARD, which will cause the state's
        input to become its output.

        default
        :default: $

        stability
        :stability: experimental
        """
        return self._values.get('result_path')

    @builtins.property
    def prefix_states(self) -> typing.Optional[str]:
        """String to prefix all stateIds in the state machine with.

        default
        :default: stateId

        stability
        :stability: experimental
        """
        return self._values.get('prefix_states')

    @builtins.property
    def state_id(self) -> typing.Optional[str]:
        """ID of newly created containing state.

        default
        :default: Construct ID of the StateMachineFragment

        stability
        :stability: experimental
        """
        return self._values.get('state_id')

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return 'SingleStateOptions(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


@jsii.implements(IChainable)
class State(aws_cdk.core.Construct, metaclass=jsii.JSIIAbstractClass, jsii_type="@aws-cdk/aws-stepfunctions.State"):
    """Base class for all other state classes.

    stability
    :stability: experimental
    """
    @builtins.staticmethod
    def __jsii_proxy_class__():
        return _StateProxy

    def __init__(self, scope: aws_cdk.core.Construct, id: str, *, comment: typing.Optional[str]=None, input_path: typing.Optional[str]=None, output_path: typing.Optional[str]=None, parameters: typing.Optional[typing.Mapping[str, typing.Any]]=None, result_path: typing.Optional[str]=None) -> None:
        """
        :param scope: -
        :param id: -
        :param comment: A comment describing this state. Default: No comment
        :param input_path: JSONPath expression to select part of the state to be the input to this state. May also be the special value DISCARD, which will cause the effective input to be the empty object {}. Default: $
        :param output_path: JSONPath expression to select part of the state to be the output to this state. May also be the special value DISCARD, which will cause the effective output to be the empty object {}. Default: $
        :param parameters: Parameters pass a collection of key-value pairs, either static values or JSONPath expressions that select from the input. Default: No parameters
        :param result_path: JSONPath expression to indicate where to inject the state's output. May also be the special value DISCARD, which will cause the state's input to become its output. Default: $

        stability
        :stability: experimental
        """
        props = StateProps(comment=comment, input_path=input_path, output_path=output_path, parameters=parameters, result_path=result_path)

        jsii.create(State, self, [scope, id, props])

    @jsii.member(jsii_name="filterNextables")
    @builtins.classmethod
    def filter_nextables(cls, states: typing.List["State"]) -> typing.List["INextable"]:
        """Return only the states that allow chaining from an array of states.

        :param states: -

        stability
        :stability: experimental
        """
        return jsii.sinvoke(cls, "filterNextables", [states])

    @jsii.member(jsii_name="findReachableEndStates")
    @builtins.classmethod
    def find_reachable_end_states(cls, start: "State", *, include_error_handlers: typing.Optional[bool]=None) -> typing.List["State"]:
        """Find the set of end states states reachable through transitions from the given start state.

        :param start: -
        :param include_error_handlers: Whether or not to follow error-handling transitions. Default: false

        stability
        :stability: experimental
        """
        options = FindStateOptions(include_error_handlers=include_error_handlers)

        return jsii.sinvoke(cls, "findReachableEndStates", [start, options])

    @jsii.member(jsii_name="findReachableStates")
    @builtins.classmethod
    def find_reachable_states(cls, start: "State", *, include_error_handlers: typing.Optional[bool]=None) -> typing.List["State"]:
        """Find the set of states reachable through transitions from the given start state.

        This does not retrieve states from within sub-graphs, such as states within a Parallel state's branch.

        :param start: -
        :param include_error_handlers: Whether or not to follow error-handling transitions. Default: false

        stability
        :stability: experimental
        """
        options = FindStateOptions(include_error_handlers=include_error_handlers)

        return jsii.sinvoke(cls, "findReachableStates", [start, options])

    @jsii.member(jsii_name="prefixStates")
    @builtins.classmethod
    def prefix_states(cls, root: aws_cdk.core.IConstruct, prefix: str) -> None:
        """Add a prefix to the stateId of all States found in a construct tree.

        :param root: -
        :param prefix: -

        stability
        :stability: experimental
        """
        return jsii.sinvoke(cls, "prefixStates", [root, prefix])

    @jsii.member(jsii_name="addBranch")
    def _add_branch(self, branch: "StateGraph") -> None:
        """Add a paralle branch to this state.

        :param branch: -

        stability
        :stability: experimental
        """
        return jsii.invoke(self, "addBranch", [branch])

    @jsii.member(jsii_name="addChoice")
    def _add_choice(self, condition: "Condition", next: "State") -> None:
        """Add a choice branch to this state.

        :param condition: -
        :param next: -

        stability
        :stability: experimental
        """
        return jsii.invoke(self, "addChoice", [condition, next])

    @jsii.member(jsii_name="addIterator")
    def _add_iterator(self, iteration: "StateGraph") -> None:
        """Add a map iterator to this state.

        :param iteration: -

        stability
        :stability: experimental
        """
        return jsii.invoke(self, "addIterator", [iteration])

    @jsii.member(jsii_name="addPrefix")
    def add_prefix(self, x: str) -> None:
        """Add a prefix to the stateId of this state.

        :param x: -

        stability
        :stability: experimental
        """
        return jsii.invoke(self, "addPrefix", [x])

    @jsii.member(jsii_name="bindToGraph")
    def bind_to_graph(self, graph: "StateGraph") -> None:
        """Register this state as part of the given graph.

        Don't call this. It will be called automatically when you work
        with states normally.

        :param graph: -

        stability
        :stability: experimental
        """
        return jsii.invoke(self, "bindToGraph", [graph])

    @jsii.member(jsii_name="makeDefault")
    def _make_default(self, def_: "State") -> None:
        """Make the indicated state the default choice transition of this state.

        :param def_: -

        stability
        :stability: experimental
        """
        return jsii.invoke(self, "makeDefault", [def_])

    @jsii.member(jsii_name="makeNext")
    def _make_next(self, next: "State") -> None:
        """Make the indicated state the default transition of this state.

        :param next: -

        stability
        :stability: experimental
        """
        return jsii.invoke(self, "makeNext", [next])

    @jsii.member(jsii_name="renderBranches")
    def _render_branches(self) -> typing.Any:
        """Render parallel branches in ASL JSON format.

        stability
        :stability: experimental
        """
        return jsii.invoke(self, "renderBranches", [])

    @jsii.member(jsii_name="renderChoices")
    def _render_choices(self) -> typing.Any:
        """Render the choices in ASL JSON format.

        stability
        :stability: experimental
        """
        return jsii.invoke(self, "renderChoices", [])

    @jsii.member(jsii_name="renderInputOutput")
    def _render_input_output(self) -> typing.Any:
        """Render InputPath/Parameters/OutputPath in ASL JSON format.

        stability
        :stability: experimental
        """
        return jsii.invoke(self, "renderInputOutput", [])

    @jsii.member(jsii_name="renderIterator")
    def _render_iterator(self) -> typing.Any:
        """Render map iterator in ASL JSON format.

        stability
        :stability: experimental
        """
        return jsii.invoke(self, "renderIterator", [])

    @jsii.member(jsii_name="renderNextEnd")
    def _render_next_end(self) -> typing.Any:
        """Render the default next state in ASL JSON format.

        stability
        :stability: experimental
        """
        return jsii.invoke(self, "renderNextEnd", [])

    @jsii.member(jsii_name="renderRetryCatch")
    def _render_retry_catch(self) -> typing.Any:
        """Render error recovery options in ASL JSON format.

        stability
        :stability: experimental
        """
        return jsii.invoke(self, "renderRetryCatch", [])

    @jsii.member(jsii_name="toStateJson")
    @abc.abstractmethod
    def to_state_json(self) -> typing.Mapping[typing.Any, typing.Any]:
        """Render the state as JSON.

        stability
        :stability: experimental
        """
        ...

    @jsii.member(jsii_name="whenBoundToGraph")
    def _when_bound_to_graph(self, graph: "StateGraph") -> None:
        """Called whenever this state is bound to a graph.

        Can be overridden by subclasses.

        :param graph: -

        stability
        :stability: experimental
        """
        return jsii.invoke(self, "whenBoundToGraph", [graph])

    @builtins.property
    @jsii.member(jsii_name="branches")
    def _branches(self) -> typing.List["StateGraph"]:
        """
        stability
        :stability: experimental
        """
        return jsii.get(self, "branches")

    @builtins.property
    @jsii.member(jsii_name="endStates")
    @abc.abstractmethod
    def end_states(self) -> typing.List["INextable"]:
        """Continuable states of this Chainable.

        stability
        :stability: experimental
        """
        ...

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> str:
        """Descriptive identifier for this chainable.

        stability
        :stability: experimental
        """
        return jsii.get(self, "id")

    @builtins.property
    @jsii.member(jsii_name="startState")
    def start_state(self) -> "State":
        """First state of this Chainable.

        stability
        :stability: experimental
        """
        return jsii.get(self, "startState")

    @builtins.property
    @jsii.member(jsii_name="stateId")
    def state_id(self) -> str:
        """Tokenized string that evaluates to the state's ID.

        stability
        :stability: experimental
        """
        return jsii.get(self, "stateId")

    @builtins.property
    @jsii.member(jsii_name="comment")
    def _comment(self) -> typing.Optional[str]:
        """
        stability
        :stability: experimental
        """
        return jsii.get(self, "comment")

    @builtins.property
    @jsii.member(jsii_name="inputPath")
    def _input_path(self) -> typing.Optional[str]:
        """
        stability
        :stability: experimental
        """
        return jsii.get(self, "inputPath")

    @builtins.property
    @jsii.member(jsii_name="outputPath")
    def _output_path(self) -> typing.Optional[str]:
        """
        stability
        :stability: experimental
        """
        return jsii.get(self, "outputPath")

    @builtins.property
    @jsii.member(jsii_name="parameters")
    def _parameters(self) -> typing.Optional[typing.Mapping[typing.Any, typing.Any]]:
        """
        stability
        :stability: experimental
        """
        return jsii.get(self, "parameters")

    @builtins.property
    @jsii.member(jsii_name="resultPath")
    def _result_path(self) -> typing.Optional[str]:
        """
        stability
        :stability: experimental
        """
        return jsii.get(self, "resultPath")

    @builtins.property
    @jsii.member(jsii_name="defaultChoice")
    def _default_choice(self) -> typing.Optional["State"]:
        """
        stability
        :stability: experimental
        """
        return jsii.get(self, "defaultChoice")

    @_default_choice.setter
    def _default_choice(self, value: typing.Optional["State"]):
        jsii.set(self, "defaultChoice", value)

    @builtins.property
    @jsii.member(jsii_name="iteration")
    def _iteration(self) -> typing.Optional["StateGraph"]:
        """
        stability
        :stability: experimental
        """
        return jsii.get(self, "iteration")

    @_iteration.setter
    def _iteration(self, value: typing.Optional["StateGraph"]):
        jsii.set(self, "iteration", value)


class _StateProxy(State):
    @jsii.member(jsii_name="toStateJson")
    def to_state_json(self) -> typing.Mapping[typing.Any, typing.Any]:
        """Render the state as JSON.

        stability
        :stability: experimental
        """
        return jsii.invoke(self, "toStateJson", [])

    @builtins.property
    @jsii.member(jsii_name="endStates")
    def end_states(self) -> typing.List["INextable"]:
        """Continuable states of this Chainable.

        stability
        :stability: experimental
        """
        return jsii.get(self, "endStates")


class StateGraph(metaclass=jsii.JSIIMeta, jsii_type="@aws-cdk/aws-stepfunctions.StateGraph"):
    """A collection of connected states.

    A StateGraph is used to keep track of all states that are connected (have
    transitions between them). It does not include the substatemachines in
    a Parallel's branches: those are their own StateGraphs, but the graphs
    themselves have a hierarchical relationship as well.

    By assigning states to a definitive StateGraph, we verify that no state
    machines are constructed. In particular:

    - Every state object can only ever be in 1 StateGraph, and not inadvertently
      be used in two graphs.
    - Every stateId must be unique across all states in the entire state
      machine.

    All policy statements in all states in all substatemachines are bubbled so
    that the top-level StateMachine instantiation can read them all and add
    them to the IAM Role.

    You do not need to instantiate this class; it is used internally.

    stability
    :stability: experimental
    """
    def __init__(self, start_state: "State", graph_description: str) -> None:
        """
        :param start_state: state that gets executed when the state machine is launched.
        :param graph_description: description of the state machine.

        stability
        :stability: experimental
        """
        jsii.create(StateGraph, self, [start_state, graph_description])

    @jsii.member(jsii_name="registerPolicyStatement")
    def register_policy_statement(self, statement: aws_cdk.aws_iam.PolicyStatement) -> None:
        """Register a Policy Statement used by states in this graph.

        :param statement: -

        stability
        :stability: experimental
        """
        return jsii.invoke(self, "registerPolicyStatement", [statement])

    @jsii.member(jsii_name="registerState")
    def register_state(self, state: "State") -> None:
        """Register a state as part of this graph.

        Called by State.bindToGraph().

        :param state: -

        stability
        :stability: experimental
        """
        return jsii.invoke(self, "registerState", [state])

    @jsii.member(jsii_name="registerSuperGraph")
    def register_super_graph(self, graph: "StateGraph") -> None:
        """Register this graph as a child of the given graph.

        Resource changes will be bubbled up to the given graph.

        :param graph: -

        stability
        :stability: experimental
        """
        return jsii.invoke(self, "registerSuperGraph", [graph])

    @jsii.member(jsii_name="toGraphJson")
    def to_graph_json(self) -> typing.Mapping[typing.Any, typing.Any]:
        """Return the Amazon States Language JSON for this graph.

        stability
        :stability: experimental
        """
        return jsii.invoke(self, "toGraphJson", [])

    @jsii.member(jsii_name="toString")
    def to_string(self) -> str:
        """Return a string description of this graph.

        stability
        :stability: experimental
        """
        return jsii.invoke(self, "toString", [])

    @builtins.property
    @jsii.member(jsii_name="policyStatements")
    def policy_statements(self) -> typing.List[aws_cdk.aws_iam.PolicyStatement]:
        """The accumulated policy statements.

        stability
        :stability: experimental
        """
        return jsii.get(self, "policyStatements")

    @builtins.property
    @jsii.member(jsii_name="startState")
    def start_state(self) -> "State":
        """state that gets executed when the state machine is launched.

        stability
        :stability: experimental
        """
        return jsii.get(self, "startState")

    @builtins.property
    @jsii.member(jsii_name="timeout")
    def timeout(self) -> typing.Optional[aws_cdk.core.Duration]:
        """Set a timeout to render into the graph JSON.

        Read/write. Only makes sense on the top-level graph, subgraphs
        do not support this feature.

        default
        :default: No timeout

        stability
        :stability: experimental
        """
        return jsii.get(self, "timeout")

    @timeout.setter
    def timeout(self, value: typing.Optional[aws_cdk.core.Duration]):
        jsii.set(self, "timeout", value)


@jsii.implements(IStateMachine)
class StateMachine(aws_cdk.core.Resource, metaclass=jsii.JSIIMeta, jsii_type="@aws-cdk/aws-stepfunctions.StateMachine"):
    """Define a StepFunctions State Machine.

    stability
    :stability: experimental
    """
    def __init__(self, scope: aws_cdk.core.Construct, id: str, *, definition: "IChainable", logs: typing.Optional["LogOptions"]=None, role: typing.Optional[aws_cdk.aws_iam.IRole]=None, state_machine_name: typing.Optional[str]=None, state_machine_type: typing.Optional["StateMachineType"]=None, timeout: typing.Optional[aws_cdk.core.Duration]=None) -> None:
        """
        :param scope: -
        :param id: -
        :param definition: Definition for this state machine.
        :param logs: Defines what execution history events are logged and where they are logged. Default: No logging
        :param role: The execution role for the state machine service. Default: A role is automatically created
        :param state_machine_name: A name for the state machine. Default: A name is automatically generated
        :param state_machine_type: Type of the state machine. Default: StateMachineType.STANDARD
        :param timeout: Maximum run time for this state machine. Default: No timeout

        stability
        :stability: experimental
        """
        props = StateMachineProps(definition=definition, logs=logs, role=role, state_machine_name=state_machine_name, state_machine_type=state_machine_type, timeout=timeout)

        jsii.create(StateMachine, self, [scope, id, props])

    @jsii.member(jsii_name="fromStateMachineArn")
    @builtins.classmethod
    def from_state_machine_arn(cls, scope: aws_cdk.core.Construct, id: str, state_machine_arn: str) -> "IStateMachine":
        """Import a state machine.

        :param scope: -
        :param id: -
        :param state_machine_arn: -

        stability
        :stability: experimental
        """
        return jsii.sinvoke(cls, "fromStateMachineArn", [scope, id, state_machine_arn])

    @jsii.member(jsii_name="addToRolePolicy")
    def add_to_role_policy(self, statement: aws_cdk.aws_iam.PolicyStatement) -> None:
        """Add the given statement to the role's policy.

        :param statement: -

        stability
        :stability: experimental
        """
        return jsii.invoke(self, "addToRolePolicy", [statement])

    @jsii.member(jsii_name="grantStartExecution")
    def grant_start_execution(self, identity: aws_cdk.aws_iam.IGrantable) -> aws_cdk.aws_iam.Grant:
        """Grant the given identity permissions to start an execution of this state machine.

        :param identity: -

        stability
        :stability: experimental
        """
        return jsii.invoke(self, "grantStartExecution", [identity])

    @jsii.member(jsii_name="metric")
    def metric(self, metric_name: str, *, account: typing.Optional[str]=None, color: typing.Optional[str]=None, dimensions: typing.Optional[typing.Mapping[str, typing.Any]]=None, label: typing.Optional[str]=None, period: typing.Optional[aws_cdk.core.Duration]=None, region: typing.Optional[str]=None, statistic: typing.Optional[str]=None, unit: typing.Optional[aws_cdk.aws_cloudwatch.Unit]=None) -> aws_cdk.aws_cloudwatch.Metric:
        """Return the given named metric for this State Machine's executions.

        :param metric_name: -
        :param account: Account which this metric comes from. Default: - Deployment account.
        :param color: The hex color code, prefixed with '#' (e.g. '#00ff00'), to use when this metric is rendered on a graph. The ``Color`` class has a set of standard colors that can be used here. Default: - Automatic color
        :param dimensions: Dimensions of the metric. Default: - No dimensions.
        :param label: Label for this metric when added to a Graph in a Dashboard. Default: - No label
        :param period: The period over which the specified statistic is applied. Default: Duration.minutes(5)
        :param region: Region which this metric comes from. Default: - Deployment region.
        :param statistic: What function to use for aggregating. Can be one of the following: - "Minimum" | "min" - "Maximum" | "max" - "Average" | "avg" - "Sum" | "sum" - "SampleCount | "n" - "pNN.NN" Default: Average
        :param unit: Unit used to filter the metric stream. Only refer to datums emitted to the metric stream with the given unit and ignore all others. Only useful when datums are being emitted to the same metric stream under different units. The default is to use all matric datums in the stream, regardless of unit, which is recommended in nearly all cases. CloudWatch does not honor this property for graphs. Default: - All metric datums in the given metric stream

        default
        :default: sum over 5 minutes

        stability
        :stability: experimental
        """
        props = aws_cdk.aws_cloudwatch.MetricOptions(account=account, color=color, dimensions=dimensions, label=label, period=period, region=region, statistic=statistic, unit=unit)

        return jsii.invoke(self, "metric", [metric_name, props])

    @jsii.member(jsii_name="metricAborted")
    def metric_aborted(self, *, account: typing.Optional[str]=None, color: typing.Optional[str]=None, dimensions: typing.Optional[typing.Mapping[str, typing.Any]]=None, label: typing.Optional[str]=None, period: typing.Optional[aws_cdk.core.Duration]=None, region: typing.Optional[str]=None, statistic: typing.Optional[str]=None, unit: typing.Optional[aws_cdk.aws_cloudwatch.Unit]=None) -> aws_cdk.aws_cloudwatch.Metric:
        """Metric for the number of executions that were aborted.

        :param account: Account which this metric comes from. Default: - Deployment account.
        :param color: The hex color code, prefixed with '#' (e.g. '#00ff00'), to use when this metric is rendered on a graph. The ``Color`` class has a set of standard colors that can be used here. Default: - Automatic color
        :param dimensions: Dimensions of the metric. Default: - No dimensions.
        :param label: Label for this metric when added to a Graph in a Dashboard. Default: - No label
        :param period: The period over which the specified statistic is applied. Default: Duration.minutes(5)
        :param region: Region which this metric comes from. Default: - Deployment region.
        :param statistic: What function to use for aggregating. Can be one of the following: - "Minimum" | "min" - "Maximum" | "max" - "Average" | "avg" - "Sum" | "sum" - "SampleCount | "n" - "pNN.NN" Default: Average
        :param unit: Unit used to filter the metric stream. Only refer to datums emitted to the metric stream with the given unit and ignore all others. Only useful when datums are being emitted to the same metric stream under different units. The default is to use all matric datums in the stream, regardless of unit, which is recommended in nearly all cases. CloudWatch does not honor this property for graphs. Default: - All metric datums in the given metric stream

        default
        :default: sum over 5 minutes

        stability
        :stability: experimental
        """
        props = aws_cdk.aws_cloudwatch.MetricOptions(account=account, color=color, dimensions=dimensions, label=label, period=period, region=region, statistic=statistic, unit=unit)

        return jsii.invoke(self, "metricAborted", [props])

    @jsii.member(jsii_name="metricFailed")
    def metric_failed(self, *, account: typing.Optional[str]=None, color: typing.Optional[str]=None, dimensions: typing.Optional[typing.Mapping[str, typing.Any]]=None, label: typing.Optional[str]=None, period: typing.Optional[aws_cdk.core.Duration]=None, region: typing.Optional[str]=None, statistic: typing.Optional[str]=None, unit: typing.Optional[aws_cdk.aws_cloudwatch.Unit]=None) -> aws_cdk.aws_cloudwatch.Metric:
        """Metric for the number of executions that failed.

        :param account: Account which this metric comes from. Default: - Deployment account.
        :param color: The hex color code, prefixed with '#' (e.g. '#00ff00'), to use when this metric is rendered on a graph. The ``Color`` class has a set of standard colors that can be used here. Default: - Automatic color
        :param dimensions: Dimensions of the metric. Default: - No dimensions.
        :param label: Label for this metric when added to a Graph in a Dashboard. Default: - No label
        :param period: The period over which the specified statistic is applied. Default: Duration.minutes(5)
        :param region: Region which this metric comes from. Default: - Deployment region.
        :param statistic: What function to use for aggregating. Can be one of the following: - "Minimum" | "min" - "Maximum" | "max" - "Average" | "avg" - "Sum" | "sum" - "SampleCount | "n" - "pNN.NN" Default: Average
        :param unit: Unit used to filter the metric stream. Only refer to datums emitted to the metric stream with the given unit and ignore all others. Only useful when datums are being emitted to the same metric stream under different units. The default is to use all matric datums in the stream, regardless of unit, which is recommended in nearly all cases. CloudWatch does not honor this property for graphs. Default: - All metric datums in the given metric stream

        default
        :default: sum over 5 minutes

        stability
        :stability: experimental
        """
        props = aws_cdk.aws_cloudwatch.MetricOptions(account=account, color=color, dimensions=dimensions, label=label, period=period, region=region, statistic=statistic, unit=unit)

        return jsii.invoke(self, "metricFailed", [props])

    @jsii.member(jsii_name="metricStarted")
    def metric_started(self, *, account: typing.Optional[str]=None, color: typing.Optional[str]=None, dimensions: typing.Optional[typing.Mapping[str, typing.Any]]=None, label: typing.Optional[str]=None, period: typing.Optional[aws_cdk.core.Duration]=None, region: typing.Optional[str]=None, statistic: typing.Optional[str]=None, unit: typing.Optional[aws_cdk.aws_cloudwatch.Unit]=None) -> aws_cdk.aws_cloudwatch.Metric:
        """Metric for the number of executions that were started.

        :param account: Account which this metric comes from. Default: - Deployment account.
        :param color: The hex color code, prefixed with '#' (e.g. '#00ff00'), to use when this metric is rendered on a graph. The ``Color`` class has a set of standard colors that can be used here. Default: - Automatic color
        :param dimensions: Dimensions of the metric. Default: - No dimensions.
        :param label: Label for this metric when added to a Graph in a Dashboard. Default: - No label
        :param period: The period over which the specified statistic is applied. Default: Duration.minutes(5)
        :param region: Region which this metric comes from. Default: - Deployment region.
        :param statistic: What function to use for aggregating. Can be one of the following: - "Minimum" | "min" - "Maximum" | "max" - "Average" | "avg" - "Sum" | "sum" - "SampleCount | "n" - "pNN.NN" Default: Average
        :param unit: Unit used to filter the metric stream. Only refer to datums emitted to the metric stream with the given unit and ignore all others. Only useful when datums are being emitted to the same metric stream under different units. The default is to use all matric datums in the stream, regardless of unit, which is recommended in nearly all cases. CloudWatch does not honor this property for graphs. Default: - All metric datums in the given metric stream

        default
        :default: sum over 5 minutes

        stability
        :stability: experimental
        """
        props = aws_cdk.aws_cloudwatch.MetricOptions(account=account, color=color, dimensions=dimensions, label=label, period=period, region=region, statistic=statistic, unit=unit)

        return jsii.invoke(self, "metricStarted", [props])

    @jsii.member(jsii_name="metricSucceeded")
    def metric_succeeded(self, *, account: typing.Optional[str]=None, color: typing.Optional[str]=None, dimensions: typing.Optional[typing.Mapping[str, typing.Any]]=None, label: typing.Optional[str]=None, period: typing.Optional[aws_cdk.core.Duration]=None, region: typing.Optional[str]=None, statistic: typing.Optional[str]=None, unit: typing.Optional[aws_cdk.aws_cloudwatch.Unit]=None) -> aws_cdk.aws_cloudwatch.Metric:
        """Metric for the number of executions that succeeded.

        :param account: Account which this metric comes from. Default: - Deployment account.
        :param color: The hex color code, prefixed with '#' (e.g. '#00ff00'), to use when this metric is rendered on a graph. The ``Color`` class has a set of standard colors that can be used here. Default: - Automatic color
        :param dimensions: Dimensions of the metric. Default: - No dimensions.
        :param label: Label for this metric when added to a Graph in a Dashboard. Default: - No label
        :param period: The period over which the specified statistic is applied. Default: Duration.minutes(5)
        :param region: Region which this metric comes from. Default: - Deployment region.
        :param statistic: What function to use for aggregating. Can be one of the following: - "Minimum" | "min" - "Maximum" | "max" - "Average" | "avg" - "Sum" | "sum" - "SampleCount | "n" - "pNN.NN" Default: Average
        :param unit: Unit used to filter the metric stream. Only refer to datums emitted to the metric stream with the given unit and ignore all others. Only useful when datums are being emitted to the same metric stream under different units. The default is to use all matric datums in the stream, regardless of unit, which is recommended in nearly all cases. CloudWatch does not honor this property for graphs. Default: - All metric datums in the given metric stream

        default
        :default: sum over 5 minutes

        stability
        :stability: experimental
        """
        props = aws_cdk.aws_cloudwatch.MetricOptions(account=account, color=color, dimensions=dimensions, label=label, period=period, region=region, statistic=statistic, unit=unit)

        return jsii.invoke(self, "metricSucceeded", [props])

    @jsii.member(jsii_name="metricThrottled")
    def metric_throttled(self, *, account: typing.Optional[str]=None, color: typing.Optional[str]=None, dimensions: typing.Optional[typing.Mapping[str, typing.Any]]=None, label: typing.Optional[str]=None, period: typing.Optional[aws_cdk.core.Duration]=None, region: typing.Optional[str]=None, statistic: typing.Optional[str]=None, unit: typing.Optional[aws_cdk.aws_cloudwatch.Unit]=None) -> aws_cdk.aws_cloudwatch.Metric:
        """Metric for the number of executions that were throttled.

        :param account: Account which this metric comes from. Default: - Deployment account.
        :param color: The hex color code, prefixed with '#' (e.g. '#00ff00'), to use when this metric is rendered on a graph. The ``Color`` class has a set of standard colors that can be used here. Default: - Automatic color
        :param dimensions: Dimensions of the metric. Default: - No dimensions.
        :param label: Label for this metric when added to a Graph in a Dashboard. Default: - No label
        :param period: The period over which the specified statistic is applied. Default: Duration.minutes(5)
        :param region: Region which this metric comes from. Default: - Deployment region.
        :param statistic: What function to use for aggregating. Can be one of the following: - "Minimum" | "min" - "Maximum" | "max" - "Average" | "avg" - "Sum" | "sum" - "SampleCount | "n" - "pNN.NN" Default: Average
        :param unit: Unit used to filter the metric stream. Only refer to datums emitted to the metric stream with the given unit and ignore all others. Only useful when datums are being emitted to the same metric stream under different units. The default is to use all matric datums in the stream, regardless of unit, which is recommended in nearly all cases. CloudWatch does not honor this property for graphs. Default: - All metric datums in the given metric stream

        default
        :default: sum over 5 minutes

        stability
        :stability: experimental
        """
        props = aws_cdk.aws_cloudwatch.MetricOptions(account=account, color=color, dimensions=dimensions, label=label, period=period, region=region, statistic=statistic, unit=unit)

        return jsii.invoke(self, "metricThrottled", [props])

    @jsii.member(jsii_name="metricTime")
    def metric_time(self, *, account: typing.Optional[str]=None, color: typing.Optional[str]=None, dimensions: typing.Optional[typing.Mapping[str, typing.Any]]=None, label: typing.Optional[str]=None, period: typing.Optional[aws_cdk.core.Duration]=None, region: typing.Optional[str]=None, statistic: typing.Optional[str]=None, unit: typing.Optional[aws_cdk.aws_cloudwatch.Unit]=None) -> aws_cdk.aws_cloudwatch.Metric:
        """Metric for the interval, in milliseconds, between the time the execution starts and the time it closes.

        :param account: Account which this metric comes from. Default: - Deployment account.
        :param color: The hex color code, prefixed with '#' (e.g. '#00ff00'), to use when this metric is rendered on a graph. The ``Color`` class has a set of standard colors that can be used here. Default: - Automatic color
        :param dimensions: Dimensions of the metric. Default: - No dimensions.
        :param label: Label for this metric when added to a Graph in a Dashboard. Default: - No label
        :param period: The period over which the specified statistic is applied. Default: Duration.minutes(5)
        :param region: Region which this metric comes from. Default: - Deployment region.
        :param statistic: What function to use for aggregating. Can be one of the following: - "Minimum" | "min" - "Maximum" | "max" - "Average" | "avg" - "Sum" | "sum" - "SampleCount | "n" - "pNN.NN" Default: Average
        :param unit: Unit used to filter the metric stream. Only refer to datums emitted to the metric stream with the given unit and ignore all others. Only useful when datums are being emitted to the same metric stream under different units. The default is to use all matric datums in the stream, regardless of unit, which is recommended in nearly all cases. CloudWatch does not honor this property for graphs. Default: - All metric datums in the given metric stream

        default
        :default: sum over 5 minutes

        stability
        :stability: experimental
        """
        props = aws_cdk.aws_cloudwatch.MetricOptions(account=account, color=color, dimensions=dimensions, label=label, period=period, region=region, statistic=statistic, unit=unit)

        return jsii.invoke(self, "metricTime", [props])

    @jsii.member(jsii_name="metricTimedOut")
    def metric_timed_out(self, *, account: typing.Optional[str]=None, color: typing.Optional[str]=None, dimensions: typing.Optional[typing.Mapping[str, typing.Any]]=None, label: typing.Optional[str]=None, period: typing.Optional[aws_cdk.core.Duration]=None, region: typing.Optional[str]=None, statistic: typing.Optional[str]=None, unit: typing.Optional[aws_cdk.aws_cloudwatch.Unit]=None) -> aws_cdk.aws_cloudwatch.Metric:
        """Metric for the number of executions that succeeded.

        :param account: Account which this metric comes from. Default: - Deployment account.
        :param color: The hex color code, prefixed with '#' (e.g. '#00ff00'), to use when this metric is rendered on a graph. The ``Color`` class has a set of standard colors that can be used here. Default: - Automatic color
        :param dimensions: Dimensions of the metric. Default: - No dimensions.
        :param label: Label for this metric when added to a Graph in a Dashboard. Default: - No label
        :param period: The period over which the specified statistic is applied. Default: Duration.minutes(5)
        :param region: Region which this metric comes from. Default: - Deployment region.
        :param statistic: What function to use for aggregating. Can be one of the following: - "Minimum" | "min" - "Maximum" | "max" - "Average" | "avg" - "Sum" | "sum" - "SampleCount | "n" - "pNN.NN" Default: Average
        :param unit: Unit used to filter the metric stream. Only refer to datums emitted to the metric stream with the given unit and ignore all others. Only useful when datums are being emitted to the same metric stream under different units. The default is to use all matric datums in the stream, regardless of unit, which is recommended in nearly all cases. CloudWatch does not honor this property for graphs. Default: - All metric datums in the given metric stream

        default
        :default: sum over 5 minutes

        stability
        :stability: experimental
        """
        props = aws_cdk.aws_cloudwatch.MetricOptions(account=account, color=color, dimensions=dimensions, label=label, period=period, region=region, statistic=statistic, unit=unit)

        return jsii.invoke(self, "metricTimedOut", [props])

    @builtins.property
    @jsii.member(jsii_name="role")
    def role(self) -> aws_cdk.aws_iam.IRole:
        """Execution role of this state machine.

        stability
        :stability: experimental
        """
        return jsii.get(self, "role")

    @builtins.property
    @jsii.member(jsii_name="stateMachineArn")
    def state_machine_arn(self) -> str:
        """The ARN of the state machine.

        stability
        :stability: experimental
        """
        return jsii.get(self, "stateMachineArn")

    @builtins.property
    @jsii.member(jsii_name="stateMachineName")
    def state_machine_name(self) -> str:
        """The name of the state machine.

        stability
        :stability: experimental
        attribute:
        :attribute:: true
        """
        return jsii.get(self, "stateMachineName")

    @builtins.property
    @jsii.member(jsii_name="stateMachineType")
    def state_machine_type(self) -> "StateMachineType":
        """Type of the state machine.

        stability
        :stability: experimental
        attribute:
        :attribute:: true
        """
        return jsii.get(self, "stateMachineType")


@jsii.implements(IChainable)
class StateMachineFragment(aws_cdk.core.Construct, metaclass=jsii.JSIIAbstractClass, jsii_type="@aws-cdk/aws-stepfunctions.StateMachineFragment"):
    """Base class for reusable state machine fragments.

    stability
    :stability: experimental
    """
    @builtins.staticmethod
    def __jsii_proxy_class__():
        return _StateMachineFragmentProxy

    def __init__(self, scope: aws_cdk.core.Construct, id: str) -> None:
        """
        :param scope: -
        :param id: -
        """
        jsii.create(StateMachineFragment, self, [scope, id])

    @jsii.member(jsii_name="next")
    def next(self, next: "IChainable") -> "Chain":
        """Continue normal execution with the given state.

        :param next: -

        stability
        :stability: experimental
        """
        return jsii.invoke(self, "next", [next])

    @jsii.member(jsii_name="prefixStates")
    def prefix_states(self, prefix: typing.Optional[str]=None) -> "StateMachineFragment":
        """Prefix the IDs of all states in this state machine fragment.

        Use this to avoid multiple copies of the state machine all having the
        same state IDs.

        :param prefix: The prefix to add. Will use construct ID by default.

        stability
        :stability: experimental
        """
        return jsii.invoke(self, "prefixStates", [prefix])

    @jsii.member(jsii_name="toSingleState")
    def to_single_state(self, *, prefix_states: typing.Optional[str]=None, state_id: typing.Optional[str]=None, comment: typing.Optional[str]=None, input_path: typing.Optional[str]=None, output_path: typing.Optional[str]=None, result_path: typing.Optional[str]=None) -> "Parallel":
        """Wrap all states in this state machine fragment up into a single state.

        This can be used to add retry or error handling onto this state
        machine fragment.

        Be aware that this changes the result of the inner state machine
        to be an array with the result of the state machine in it. Adjust
        your paths accordingly. For example, change 'outputPath' to
        '$[0]'.

        :param prefix_states: String to prefix all stateIds in the state machine with. Default: stateId
        :param state_id: ID of newly created containing state. Default: Construct ID of the StateMachineFragment
        :param comment: An optional description for this state. Default: No comment
        :param input_path: JSONPath expression to select part of the state to be the input to this state. May also be the special value DISCARD, which will cause the effective input to be the empty object {}. Default: $
        :param output_path: JSONPath expression to select part of the state to be the output to this state. May also be the special value DISCARD, which will cause the effective output to be the empty object {}. Default: $
        :param result_path: JSONPath expression to indicate where to inject the state's output. May also be the special value DISCARD, which will cause the state's input to become its output. Default: $

        stability
        :stability: experimental
        """
        options = SingleStateOptions(prefix_states=prefix_states, state_id=state_id, comment=comment, input_path=input_path, output_path=output_path, result_path=result_path)

        return jsii.invoke(self, "toSingleState", [options])

    @builtins.property
    @jsii.member(jsii_name="endStates")
    @abc.abstractmethod
    def end_states(self) -> typing.List["INextable"]:
        """The states to chain onto if this fragment is used.

        stability
        :stability: experimental
        """
        ...

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> str:
        """Descriptive identifier for this chainable.

        stability
        :stability: experimental
        """
        return jsii.get(self, "id")

    @builtins.property
    @jsii.member(jsii_name="startState")
    @abc.abstractmethod
    def start_state(self) -> "State":
        """The start state of this state machine fragment.

        stability
        :stability: experimental
        """
        ...


class _StateMachineFragmentProxy(StateMachineFragment):
    @builtins.property
    @jsii.member(jsii_name="endStates")
    def end_states(self) -> typing.List["INextable"]:
        """The states to chain onto if this fragment is used.

        stability
        :stability: experimental
        """
        return jsii.get(self, "endStates")

    @builtins.property
    @jsii.member(jsii_name="startState")
    def start_state(self) -> "State":
        """The start state of this state machine fragment.

        stability
        :stability: experimental
        """
        return jsii.get(self, "startState")


@jsii.data_type(jsii_type="@aws-cdk/aws-stepfunctions.StateMachineProps", jsii_struct_bases=[], name_mapping={'definition': 'definition', 'logs': 'logs', 'role': 'role', 'state_machine_name': 'stateMachineName', 'state_machine_type': 'stateMachineType', 'timeout': 'timeout'})
class StateMachineProps():
    def __init__(self, *, definition: "IChainable", logs: typing.Optional["LogOptions"]=None, role: typing.Optional[aws_cdk.aws_iam.IRole]=None, state_machine_name: typing.Optional[str]=None, state_machine_type: typing.Optional["StateMachineType"]=None, timeout: typing.Optional[aws_cdk.core.Duration]=None) -> None:
        """Properties for defining a State Machine.

        :param definition: Definition for this state machine.
        :param logs: Defines what execution history events are logged and where they are logged. Default: No logging
        :param role: The execution role for the state machine service. Default: A role is automatically created
        :param state_machine_name: A name for the state machine. Default: A name is automatically generated
        :param state_machine_type: Type of the state machine. Default: StateMachineType.STANDARD
        :param timeout: Maximum run time for this state machine. Default: No timeout

        stability
        :stability: experimental
        """
        if isinstance(logs, dict): logs = LogOptions(**logs)
        self._values = {
            'definition': definition,
        }
        if logs is not None: self._values["logs"] = logs
        if role is not None: self._values["role"] = role
        if state_machine_name is not None: self._values["state_machine_name"] = state_machine_name
        if state_machine_type is not None: self._values["state_machine_type"] = state_machine_type
        if timeout is not None: self._values["timeout"] = timeout

    @builtins.property
    def definition(self) -> "IChainable":
        """Definition for this state machine.

        stability
        :stability: experimental
        """
        return self._values.get('definition')

    @builtins.property
    def logs(self) -> typing.Optional["LogOptions"]:
        """Defines what execution history events are logged and where they are logged.

        default
        :default: No logging

        stability
        :stability: experimental
        """
        return self._values.get('logs')

    @builtins.property
    def role(self) -> typing.Optional[aws_cdk.aws_iam.IRole]:
        """The execution role for the state machine service.

        default
        :default: A role is automatically created

        stability
        :stability: experimental
        """
        return self._values.get('role')

    @builtins.property
    def state_machine_name(self) -> typing.Optional[str]:
        """A name for the state machine.

        default
        :default: A name is automatically generated

        stability
        :stability: experimental
        """
        return self._values.get('state_machine_name')

    @builtins.property
    def state_machine_type(self) -> typing.Optional["StateMachineType"]:
        """Type of the state machine.

        default
        :default: StateMachineType.STANDARD

        stability
        :stability: experimental
        """
        return self._values.get('state_machine_type')

    @builtins.property
    def timeout(self) -> typing.Optional[aws_cdk.core.Duration]:
        """Maximum run time for this state machine.

        default
        :default: No timeout

        stability
        :stability: experimental
        """
        return self._values.get('timeout')

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return 'StateMachineProps(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


@jsii.enum(jsii_type="@aws-cdk/aws-stepfunctions.StateMachineType")
class StateMachineType(enum.Enum):
    """Two types of state machines are available in AWS Step Functions: EXPRESS AND STANDARD.

    default
    :default: STANDARD

    see
    :see: https://docs.aws.amazon.com/step-functions/latest/dg/concepts-standard-vs-express.html
    stability
    :stability: experimental
    """
    EXPRESS = "EXPRESS"
    """Express Workflows are ideal for high-volume, event processing workloads.

    stability
    :stability: experimental
    """
    STANDARD = "STANDARD"
    """Standard Workflows are ideal for long-running, durable, and auditable workflows.

    stability
    :stability: experimental
    """

@jsii.data_type(jsii_type="@aws-cdk/aws-stepfunctions.StateProps", jsii_struct_bases=[], name_mapping={'comment': 'comment', 'input_path': 'inputPath', 'output_path': 'outputPath', 'parameters': 'parameters', 'result_path': 'resultPath'})
class StateProps():
    def __init__(self, *, comment: typing.Optional[str]=None, input_path: typing.Optional[str]=None, output_path: typing.Optional[str]=None, parameters: typing.Optional[typing.Mapping[str, typing.Any]]=None, result_path: typing.Optional[str]=None) -> None:
        """Properties shared by all states.

        :param comment: A comment describing this state. Default: No comment
        :param input_path: JSONPath expression to select part of the state to be the input to this state. May also be the special value DISCARD, which will cause the effective input to be the empty object {}. Default: $
        :param output_path: JSONPath expression to select part of the state to be the output to this state. May also be the special value DISCARD, which will cause the effective output to be the empty object {}. Default: $
        :param parameters: Parameters pass a collection of key-value pairs, either static values or JSONPath expressions that select from the input. Default: No parameters
        :param result_path: JSONPath expression to indicate where to inject the state's output. May also be the special value DISCARD, which will cause the state's input to become its output. Default: $

        stability
        :stability: experimental
        """
        self._values = {
        }
        if comment is not None: self._values["comment"] = comment
        if input_path is not None: self._values["input_path"] = input_path
        if output_path is not None: self._values["output_path"] = output_path
        if parameters is not None: self._values["parameters"] = parameters
        if result_path is not None: self._values["result_path"] = result_path

    @builtins.property
    def comment(self) -> typing.Optional[str]:
        """A comment describing this state.

        default
        :default: No comment

        stability
        :stability: experimental
        """
        return self._values.get('comment')

    @builtins.property
    def input_path(self) -> typing.Optional[str]:
        """JSONPath expression to select part of the state to be the input to this state.

        May also be the special value DISCARD, which will cause the effective
        input to be the empty object {}.

        default
        :default: $

        stability
        :stability: experimental
        """
        return self._values.get('input_path')

    @builtins.property
    def output_path(self) -> typing.Optional[str]:
        """JSONPath expression to select part of the state to be the output to this state.

        May also be the special value DISCARD, which will cause the effective
        output to be the empty object {}.

        default
        :default: $

        stability
        :stability: experimental
        """
        return self._values.get('output_path')

    @builtins.property
    def parameters(self) -> typing.Optional[typing.Mapping[str, typing.Any]]:
        """Parameters pass a collection of key-value pairs, either static values or JSONPath expressions that select from the input.

        default
        :default: No parameters

        see
        :see: https://docs.aws.amazon.com/step-functions/latest/dg/input-output-inputpath-params.html#input-output-parameters
        stability
        :stability: experimental
        """
        return self._values.get('parameters')

    @builtins.property
    def result_path(self) -> typing.Optional[str]:
        """JSONPath expression to indicate where to inject the state's output.

        May also be the special value DISCARD, which will cause the state's
        input to become its output.

        default
        :default: $

        stability
        :stability: experimental
        """
        return self._values.get('result_path')

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return 'StateProps(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


class StateTransitionMetric(metaclass=jsii.JSIIMeta, jsii_type="@aws-cdk/aws-stepfunctions.StateTransitionMetric"):
    """Metrics on the rate limiting performed on state machine execution.

    These rate limits are shared across all state machines.

    stability
    :stability: experimental
    """
    def __init__(self) -> None:
        jsii.create(StateTransitionMetric, self, [])

    @jsii.member(jsii_name="metric")
    @builtins.classmethod
    def metric(cls, metric_name: str, *, account: typing.Optional[str]=None, color: typing.Optional[str]=None, dimensions: typing.Optional[typing.Mapping[str, typing.Any]]=None, label: typing.Optional[str]=None, period: typing.Optional[aws_cdk.core.Duration]=None, region: typing.Optional[str]=None, statistic: typing.Optional[str]=None, unit: typing.Optional[aws_cdk.aws_cloudwatch.Unit]=None) -> aws_cdk.aws_cloudwatch.Metric:
        """Return the given named metric for the service's state transition metrics.

        :param metric_name: -
        :param account: Account which this metric comes from. Default: - Deployment account.
        :param color: The hex color code, prefixed with '#' (e.g. '#00ff00'), to use when this metric is rendered on a graph. The ``Color`` class has a set of standard colors that can be used here. Default: - Automatic color
        :param dimensions: Dimensions of the metric. Default: - No dimensions.
        :param label: Label for this metric when added to a Graph in a Dashboard. Default: - No label
        :param period: The period over which the specified statistic is applied. Default: Duration.minutes(5)
        :param region: Region which this metric comes from. Default: - Deployment region.
        :param statistic: What function to use for aggregating. Can be one of the following: - "Minimum" | "min" - "Maximum" | "max" - "Average" | "avg" - "Sum" | "sum" - "SampleCount | "n" - "pNN.NN" Default: Average
        :param unit: Unit used to filter the metric stream. Only refer to datums emitted to the metric stream with the given unit and ignore all others. Only useful when datums are being emitted to the same metric stream under different units. The default is to use all matric datums in the stream, regardless of unit, which is recommended in nearly all cases. CloudWatch does not honor this property for graphs. Default: - All metric datums in the given metric stream

        default
        :default: average over 5 minutes

        stability
        :stability: experimental
        """
        props = aws_cdk.aws_cloudwatch.MetricOptions(account=account, color=color, dimensions=dimensions, label=label, period=period, region=region, statistic=statistic, unit=unit)

        return jsii.sinvoke(cls, "metric", [metric_name, props])

    @jsii.member(jsii_name="metricConsumedCapacity")
    @builtins.classmethod
    def metric_consumed_capacity(cls, *, account: typing.Optional[str]=None, color: typing.Optional[str]=None, dimensions: typing.Optional[typing.Mapping[str, typing.Any]]=None, label: typing.Optional[str]=None, period: typing.Optional[aws_cdk.core.Duration]=None, region: typing.Optional[str]=None, statistic: typing.Optional[str]=None, unit: typing.Optional[aws_cdk.aws_cloudwatch.Unit]=None) -> aws_cdk.aws_cloudwatch.Metric:
        """Metric for the number of available state transitions per second.

        :param account: Account which this metric comes from. Default: - Deployment account.
        :param color: The hex color code, prefixed with '#' (e.g. '#00ff00'), to use when this metric is rendered on a graph. The ``Color`` class has a set of standard colors that can be used here. Default: - Automatic color
        :param dimensions: Dimensions of the metric. Default: - No dimensions.
        :param label: Label for this metric when added to a Graph in a Dashboard. Default: - No label
        :param period: The period over which the specified statistic is applied. Default: Duration.minutes(5)
        :param region: Region which this metric comes from. Default: - Deployment region.
        :param statistic: What function to use for aggregating. Can be one of the following: - "Minimum" | "min" - "Maximum" | "max" - "Average" | "avg" - "Sum" | "sum" - "SampleCount | "n" - "pNN.NN" Default: Average
        :param unit: Unit used to filter the metric stream. Only refer to datums emitted to the metric stream with the given unit and ignore all others. Only useful when datums are being emitted to the same metric stream under different units. The default is to use all matric datums in the stream, regardless of unit, which is recommended in nearly all cases. CloudWatch does not honor this property for graphs. Default: - All metric datums in the given metric stream

        default
        :default: average over 5 minutes

        stability
        :stability: experimental
        """
        props = aws_cdk.aws_cloudwatch.MetricOptions(account=account, color=color, dimensions=dimensions, label=label, period=period, region=region, statistic=statistic, unit=unit)

        return jsii.sinvoke(cls, "metricConsumedCapacity", [props])

    @jsii.member(jsii_name="metricProvisionedBucketSize")
    @builtins.classmethod
    def metric_provisioned_bucket_size(cls, *, account: typing.Optional[str]=None, color: typing.Optional[str]=None, dimensions: typing.Optional[typing.Mapping[str, typing.Any]]=None, label: typing.Optional[str]=None, period: typing.Optional[aws_cdk.core.Duration]=None, region: typing.Optional[str]=None, statistic: typing.Optional[str]=None, unit: typing.Optional[aws_cdk.aws_cloudwatch.Unit]=None) -> aws_cdk.aws_cloudwatch.Metric:
        """Metric for the number of available state transitions.

        :param account: Account which this metric comes from. Default: - Deployment account.
        :param color: The hex color code, prefixed with '#' (e.g. '#00ff00'), to use when this metric is rendered on a graph. The ``Color`` class has a set of standard colors that can be used here. Default: - Automatic color
        :param dimensions: Dimensions of the metric. Default: - No dimensions.
        :param label: Label for this metric when added to a Graph in a Dashboard. Default: - No label
        :param period: The period over which the specified statistic is applied. Default: Duration.minutes(5)
        :param region: Region which this metric comes from. Default: - Deployment region.
        :param statistic: What function to use for aggregating. Can be one of the following: - "Minimum" | "min" - "Maximum" | "max" - "Average" | "avg" - "Sum" | "sum" - "SampleCount | "n" - "pNN.NN" Default: Average
        :param unit: Unit used to filter the metric stream. Only refer to datums emitted to the metric stream with the given unit and ignore all others. Only useful when datums are being emitted to the same metric stream under different units. The default is to use all matric datums in the stream, regardless of unit, which is recommended in nearly all cases. CloudWatch does not honor this property for graphs. Default: - All metric datums in the given metric stream

        default
        :default: average over 5 minutes

        stability
        :stability: experimental
        """
        props = aws_cdk.aws_cloudwatch.MetricOptions(account=account, color=color, dimensions=dimensions, label=label, period=period, region=region, statistic=statistic, unit=unit)

        return jsii.sinvoke(cls, "metricProvisionedBucketSize", [props])

    @jsii.member(jsii_name="metricProvisionedRefillRate")
    @builtins.classmethod
    def metric_provisioned_refill_rate(cls, *, account: typing.Optional[str]=None, color: typing.Optional[str]=None, dimensions: typing.Optional[typing.Mapping[str, typing.Any]]=None, label: typing.Optional[str]=None, period: typing.Optional[aws_cdk.core.Duration]=None, region: typing.Optional[str]=None, statistic: typing.Optional[str]=None, unit: typing.Optional[aws_cdk.aws_cloudwatch.Unit]=None) -> aws_cdk.aws_cloudwatch.Metric:
        """Metric for the provisioned steady-state execution rate.

        :param account: Account which this metric comes from. Default: - Deployment account.
        :param color: The hex color code, prefixed with '#' (e.g. '#00ff00'), to use when this metric is rendered on a graph. The ``Color`` class has a set of standard colors that can be used here. Default: - Automatic color
        :param dimensions: Dimensions of the metric. Default: - No dimensions.
        :param label: Label for this metric when added to a Graph in a Dashboard. Default: - No label
        :param period: The period over which the specified statistic is applied. Default: Duration.minutes(5)
        :param region: Region which this metric comes from. Default: - Deployment region.
        :param statistic: What function to use for aggregating. Can be one of the following: - "Minimum" | "min" - "Maximum" | "max" - "Average" | "avg" - "Sum" | "sum" - "SampleCount | "n" - "pNN.NN" Default: Average
        :param unit: Unit used to filter the metric stream. Only refer to datums emitted to the metric stream with the given unit and ignore all others. Only useful when datums are being emitted to the same metric stream under different units. The default is to use all matric datums in the stream, regardless of unit, which is recommended in nearly all cases. CloudWatch does not honor this property for graphs. Default: - All metric datums in the given metric stream

        default
        :default: average over 5 minutes

        stability
        :stability: experimental
        """
        props = aws_cdk.aws_cloudwatch.MetricOptions(account=account, color=color, dimensions=dimensions, label=label, period=period, region=region, statistic=statistic, unit=unit)

        return jsii.sinvoke(cls, "metricProvisionedRefillRate", [props])

    @jsii.member(jsii_name="metricThrottledEvents")
    @builtins.classmethod
    def metric_throttled_events(cls, *, account: typing.Optional[str]=None, color: typing.Optional[str]=None, dimensions: typing.Optional[typing.Mapping[str, typing.Any]]=None, label: typing.Optional[str]=None, period: typing.Optional[aws_cdk.core.Duration]=None, region: typing.Optional[str]=None, statistic: typing.Optional[str]=None, unit: typing.Optional[aws_cdk.aws_cloudwatch.Unit]=None) -> aws_cdk.aws_cloudwatch.Metric:
        """Metric for the number of throttled state transitions.

        :param account: Account which this metric comes from. Default: - Deployment account.
        :param color: The hex color code, prefixed with '#' (e.g. '#00ff00'), to use when this metric is rendered on a graph. The ``Color`` class has a set of standard colors that can be used here. Default: - Automatic color
        :param dimensions: Dimensions of the metric. Default: - No dimensions.
        :param label: Label for this metric when added to a Graph in a Dashboard. Default: - No label
        :param period: The period over which the specified statistic is applied. Default: Duration.minutes(5)
        :param region: Region which this metric comes from. Default: - Deployment region.
        :param statistic: What function to use for aggregating. Can be one of the following: - "Minimum" | "min" - "Maximum" | "max" - "Average" | "avg" - "Sum" | "sum" - "SampleCount | "n" - "pNN.NN" Default: Average
        :param unit: Unit used to filter the metric stream. Only refer to datums emitted to the metric stream with the given unit and ignore all others. Only useful when datums are being emitted to the same metric stream under different units. The default is to use all matric datums in the stream, regardless of unit, which is recommended in nearly all cases. CloudWatch does not honor this property for graphs. Default: - All metric datums in the given metric stream

        default
        :default: sum over 5 minutes

        stability
        :stability: experimental
        """
        props = aws_cdk.aws_cloudwatch.MetricOptions(account=account, color=color, dimensions=dimensions, label=label, period=period, region=region, statistic=statistic, unit=unit)

        return jsii.sinvoke(cls, "metricThrottledEvents", [props])


@jsii.data_type(jsii_type="@aws-cdk/aws-stepfunctions.StepFunctionsTaskConfig", jsii_struct_bases=[], name_mapping={'resource_arn': 'resourceArn', 'heartbeat': 'heartbeat', 'metric_dimensions': 'metricDimensions', 'metric_prefix_plural': 'metricPrefixPlural', 'metric_prefix_singular': 'metricPrefixSingular', 'parameters': 'parameters', 'policy_statements': 'policyStatements'})
class StepFunctionsTaskConfig():
    def __init__(self, *, resource_arn: str, heartbeat: typing.Optional[aws_cdk.core.Duration]=None, metric_dimensions: typing.Optional[typing.Mapping[str, typing.Any]]=None, metric_prefix_plural: typing.Optional[str]=None, metric_prefix_singular: typing.Optional[str]=None, parameters: typing.Optional[typing.Mapping[str, typing.Any]]=None, policy_statements: typing.Optional[typing.List[aws_cdk.aws_iam.PolicyStatement]]=None) -> None:
        """Properties that define what kind of task should be created.

        :param resource_arn: The resource that represents the work to be executed. Either the ARN of a Lambda Function or Activity, or a special ARN.
        :param heartbeat: Maximum time between heart beats. If the time between heart beats takes longer than this, a 'Timeout' error is raised. This is only relevant when using an Activity type as resource. Default: No heart beat timeout
        :param metric_dimensions: The dimensions to attach to metrics. Default: No metrics
        :param metric_prefix_plural: Prefix for plural metric names of activity actions. Default: No such metrics
        :param metric_prefix_singular: Prefix for singular metric names of activity actions. Default: No such metrics
        :param parameters: Parameters pass a collection of key-value pairs, either static values or JSONPath expressions that select from the input. The meaning of these parameters is task-dependent. Its values will be merged with the ``parameters`` property which is configured directly on the Task state. Default: No parameters
        :param policy_statements: Additional policy statements to add to the execution role. Default: No policy roles

        stability
        :stability: experimental
        """
        self._values = {
            'resource_arn': resource_arn,
        }
        if heartbeat is not None: self._values["heartbeat"] = heartbeat
        if metric_dimensions is not None: self._values["metric_dimensions"] = metric_dimensions
        if metric_prefix_plural is not None: self._values["metric_prefix_plural"] = metric_prefix_plural
        if metric_prefix_singular is not None: self._values["metric_prefix_singular"] = metric_prefix_singular
        if parameters is not None: self._values["parameters"] = parameters
        if policy_statements is not None: self._values["policy_statements"] = policy_statements

    @builtins.property
    def resource_arn(self) -> str:
        """The resource that represents the work to be executed.

        Either the ARN of a Lambda Function or Activity, or a special
        ARN.

        stability
        :stability: experimental
        """
        return self._values.get('resource_arn')

    @builtins.property
    def heartbeat(self) -> typing.Optional[aws_cdk.core.Duration]:
        """Maximum time between heart beats.

        If the time between heart beats takes longer than this, a 'Timeout' error is raised.

        This is only relevant when using an Activity type as resource.

        default
        :default: No heart beat timeout

        stability
        :stability: experimental
        """
        return self._values.get('heartbeat')

    @builtins.property
    def metric_dimensions(self) -> typing.Optional[typing.Mapping[str, typing.Any]]:
        """The dimensions to attach to metrics.

        default
        :default: No metrics

        stability
        :stability: experimental
        """
        return self._values.get('metric_dimensions')

    @builtins.property
    def metric_prefix_plural(self) -> typing.Optional[str]:
        """Prefix for plural metric names of activity actions.

        default
        :default: No such metrics

        stability
        :stability: experimental
        """
        return self._values.get('metric_prefix_plural')

    @builtins.property
    def metric_prefix_singular(self) -> typing.Optional[str]:
        """Prefix for singular metric names of activity actions.

        default
        :default: No such metrics

        stability
        :stability: experimental
        """
        return self._values.get('metric_prefix_singular')

    @builtins.property
    def parameters(self) -> typing.Optional[typing.Mapping[str, typing.Any]]:
        """Parameters pass a collection of key-value pairs, either static values or JSONPath expressions that select from the input.

        The meaning of these parameters is task-dependent.

        Its values will be merged with the ``parameters`` property which is configured directly
        on the Task state.

        default
        :default: No parameters

        see
        :see: https://docs.aws.amazon.com/step-functions/latest/dg/input-output-inputpath-params.html#input-output-parameters
        stability
        :stability: experimental
        """
        return self._values.get('parameters')

    @builtins.property
    def policy_statements(self) -> typing.Optional[typing.List[aws_cdk.aws_iam.PolicyStatement]]:
        """Additional policy statements to add to the execution role.

        default
        :default: No policy roles

        stability
        :stability: experimental
        """
        return self._values.get('policy_statements')

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return 'StepFunctionsTaskConfig(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


class Succeed(State, metaclass=jsii.JSIIMeta, jsii_type="@aws-cdk/aws-stepfunctions.Succeed"):
    """Define a Succeed state in the state machine.

    Reaching a Succeed state terminates the state execution in success.

    stability
    :stability: experimental
    """
    def __init__(self, scope: aws_cdk.core.Construct, id: str, *, comment: typing.Optional[str]=None, input_path: typing.Optional[str]=None, output_path: typing.Optional[str]=None) -> None:
        """
        :param scope: -
        :param id: -
        :param comment: An optional description for this state. Default: No comment
        :param input_path: JSONPath expression to select part of the state to be the input to this state. May also be the special value DISCARD, which will cause the effective input to be the empty object {}. Default: $
        :param output_path: JSONPath expression to select part of the state to be the output to this state. May also be the special value DISCARD, which will cause the effective output to be the empty object {}. Default: $

        stability
        :stability: experimental
        """
        props = SucceedProps(comment=comment, input_path=input_path, output_path=output_path)

        jsii.create(Succeed, self, [scope, id, props])

    @jsii.member(jsii_name="toStateJson")
    def to_state_json(self) -> typing.Mapping[typing.Any, typing.Any]:
        """Return the Amazon States Language object for this state.

        stability
        :stability: experimental
        """
        return jsii.invoke(self, "toStateJson", [])

    @builtins.property
    @jsii.member(jsii_name="endStates")
    def end_states(self) -> typing.List["INextable"]:
        """Continuable states of this Chainable.

        stability
        :stability: experimental
        """
        return jsii.get(self, "endStates")


@jsii.data_type(jsii_type="@aws-cdk/aws-stepfunctions.SucceedProps", jsii_struct_bases=[], name_mapping={'comment': 'comment', 'input_path': 'inputPath', 'output_path': 'outputPath'})
class SucceedProps():
    def __init__(self, *, comment: typing.Optional[str]=None, input_path: typing.Optional[str]=None, output_path: typing.Optional[str]=None) -> None:
        """Properties for defining a Succeed state.

        :param comment: An optional description for this state. Default: No comment
        :param input_path: JSONPath expression to select part of the state to be the input to this state. May also be the special value DISCARD, which will cause the effective input to be the empty object {}. Default: $
        :param output_path: JSONPath expression to select part of the state to be the output to this state. May also be the special value DISCARD, which will cause the effective output to be the empty object {}. Default: $

        stability
        :stability: experimental
        """
        self._values = {
        }
        if comment is not None: self._values["comment"] = comment
        if input_path is not None: self._values["input_path"] = input_path
        if output_path is not None: self._values["output_path"] = output_path

    @builtins.property
    def comment(self) -> typing.Optional[str]:
        """An optional description for this state.

        default
        :default: No comment

        stability
        :stability: experimental
        """
        return self._values.get('comment')

    @builtins.property
    def input_path(self) -> typing.Optional[str]:
        """JSONPath expression to select part of the state to be the input to this state.

        May also be the special value DISCARD, which will cause the effective
        input to be the empty object {}.

        default
        :default: $

        stability
        :stability: experimental
        """
        return self._values.get('input_path')

    @builtins.property
    def output_path(self) -> typing.Optional[str]:
        """JSONPath expression to select part of the state to be the output to this state.

        May also be the special value DISCARD, which will cause the effective
        output to be the empty object {}.

        default
        :default: $

        stability
        :stability: experimental
        """
        return self._values.get('output_path')

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return 'SucceedProps(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


@jsii.implements(INextable)
class Task(State, metaclass=jsii.JSIIMeta, jsii_type="@aws-cdk/aws-stepfunctions.Task"):
    """Define a Task state in the state machine.

    Reaching a Task state causes some work to be executed, represented by the
    Task's resource property. Task constructs represent a generic Amazon
    States Language Task.

    For some resource types, more specific subclasses of Task may be available
    which are more convenient to use.

    stability
    :stability: experimental
    """
    def __init__(self, scope: aws_cdk.core.Construct, id: str, *, task: "IStepFunctionsTask", comment: typing.Optional[str]=None, input_path: typing.Optional[str]=None, output_path: typing.Optional[str]=None, parameters: typing.Optional[typing.Mapping[str, typing.Any]]=None, result_path: typing.Optional[str]=None, timeout: typing.Optional[aws_cdk.core.Duration]=None) -> None:
        """
        :param scope: -
        :param id: -
        :param task: Actual task to be invoked in this workflow.
        :param comment: An optional description for this state. Default: No comment
        :param input_path: JSONPath expression to select part of the state to be the input to this state. May also be the special value DISCARD, which will cause the effective input to be the empty object {}. Default: $
        :param output_path: JSONPath expression to select part of the state to be the output to this state. May also be the special value DISCARD, which will cause the effective output to be the empty object {}. Default: $
        :param parameters: Parameters to invoke the task with. It is not recommended to use this field. The object that is passed in the ``task`` property will take care of returning the right values for the ``Parameters`` field in the Step Functions definition. The various classes that implement ``IStepFunctionsTask`` will take a properties which make sense for the task type. For example, for ``InvokeFunction`` the field that populates the ``parameters`` field will be called ``payload``, and for the ``PublishToTopic`` the ``parameters`` field will be populated via a combination of the referenced topic, subject and message. If passed anyway, the keys in this map will override the parameters returned by the task object. Default: - Use the parameters implied by the ``task`` property
        :param result_path: JSONPath expression to indicate where to inject the state's output. May also be the special value DISCARD, which will cause the state's input to become its output. Default: $
        :param timeout: Maximum run time of this state. If the state takes longer than this amount of time to complete, a 'Timeout' error is raised. Default: 60

        stability
        :stability: experimental
        """
        props = TaskProps(task=task, comment=comment, input_path=input_path, output_path=output_path, parameters=parameters, result_path=result_path, timeout=timeout)

        jsii.create(Task, self, [scope, id, props])

    @jsii.member(jsii_name="addCatch")
    def add_catch(self, handler: "IChainable", *, errors: typing.Optional[typing.List[str]]=None, result_path: typing.Optional[str]=None) -> "Task":
        """Add a recovery handler for this state.

        When a particular error occurs, execution will continue at the error
        handler instead of failing the state machine execution.

        :param handler: -
        :param errors: Errors to recover from by going to the given state. A list of error strings to retry, which can be either predefined errors (for example Errors.NoChoiceMatched) or a self-defined error. Default: All errors
        :param result_path: JSONPath expression to indicate where to inject the error data. May also be the special value DISCARD, which will cause the error data to be discarded. Default: $

        stability
        :stability: experimental
        """
        props = CatchProps(errors=errors, result_path=result_path)

        return jsii.invoke(self, "addCatch", [handler, props])

    @jsii.member(jsii_name="addRetry")
    def add_retry(self, *, backoff_rate: typing.Optional[jsii.Number]=None, errors: typing.Optional[typing.List[str]]=None, interval: typing.Optional[aws_cdk.core.Duration]=None, max_attempts: typing.Optional[jsii.Number]=None) -> "Task":
        """Add retry configuration for this state.

        This controls if and how the execution will be retried if a particular
        error occurs.

        :param backoff_rate: Multiplication for how much longer the wait interval gets on every retry. Default: 2
        :param errors: Errors to retry. A list of error strings to retry, which can be either predefined errors (for example Errors.NoChoiceMatched) or a self-defined error. Default: All errors
        :param interval: How many seconds to wait initially before retrying. Default: Duration.seconds(1)
        :param max_attempts: How many times to retry this particular error. May be 0 to disable retry for specific errors (in case you have a catch-all retry policy). Default: 3

        stability
        :stability: experimental
        """
        props = RetryProps(backoff_rate=backoff_rate, errors=errors, interval=interval, max_attempts=max_attempts)

        return jsii.invoke(self, "addRetry", [props])

    @jsii.member(jsii_name="metric")
    def metric(self, metric_name: str, *, account: typing.Optional[str]=None, color: typing.Optional[str]=None, dimensions: typing.Optional[typing.Mapping[str, typing.Any]]=None, label: typing.Optional[str]=None, period: typing.Optional[aws_cdk.core.Duration]=None, region: typing.Optional[str]=None, statistic: typing.Optional[str]=None, unit: typing.Optional[aws_cdk.aws_cloudwatch.Unit]=None) -> aws_cdk.aws_cloudwatch.Metric:
        """Return the given named metric for this Task.

        :param metric_name: -
        :param account: Account which this metric comes from. Default: - Deployment account.
        :param color: The hex color code, prefixed with '#' (e.g. '#00ff00'), to use when this metric is rendered on a graph. The ``Color`` class has a set of standard colors that can be used here. Default: - Automatic color
        :param dimensions: Dimensions of the metric. Default: - No dimensions.
        :param label: Label for this metric when added to a Graph in a Dashboard. Default: - No label
        :param period: The period over which the specified statistic is applied. Default: Duration.minutes(5)
        :param region: Region which this metric comes from. Default: - Deployment region.
        :param statistic: What function to use for aggregating. Can be one of the following: - "Minimum" | "min" - "Maximum" | "max" - "Average" | "avg" - "Sum" | "sum" - "SampleCount | "n" - "pNN.NN" Default: Average
        :param unit: Unit used to filter the metric stream. Only refer to datums emitted to the metric stream with the given unit and ignore all others. Only useful when datums are being emitted to the same metric stream under different units. The default is to use all matric datums in the stream, regardless of unit, which is recommended in nearly all cases. CloudWatch does not honor this property for graphs. Default: - All metric datums in the given metric stream

        default
        :default: sum over 5 minutes

        stability
        :stability: experimental
        """
        props = aws_cdk.aws_cloudwatch.MetricOptions(account=account, color=color, dimensions=dimensions, label=label, period=period, region=region, statistic=statistic, unit=unit)

        return jsii.invoke(self, "metric", [metric_name, props])

    @jsii.member(jsii_name="metricFailed")
    def metric_failed(self, *, account: typing.Optional[str]=None, color: typing.Optional[str]=None, dimensions: typing.Optional[typing.Mapping[str, typing.Any]]=None, label: typing.Optional[str]=None, period: typing.Optional[aws_cdk.core.Duration]=None, region: typing.Optional[str]=None, statistic: typing.Optional[str]=None, unit: typing.Optional[aws_cdk.aws_cloudwatch.Unit]=None) -> aws_cdk.aws_cloudwatch.Metric:
        """Metric for the number of times this activity fails.

        :param account: Account which this metric comes from. Default: - Deployment account.
        :param color: The hex color code, prefixed with '#' (e.g. '#00ff00'), to use when this metric is rendered on a graph. The ``Color`` class has a set of standard colors that can be used here. Default: - Automatic color
        :param dimensions: Dimensions of the metric. Default: - No dimensions.
        :param label: Label for this metric when added to a Graph in a Dashboard. Default: - No label
        :param period: The period over which the specified statistic is applied. Default: Duration.minutes(5)
        :param region: Region which this metric comes from. Default: - Deployment region.
        :param statistic: What function to use for aggregating. Can be one of the following: - "Minimum" | "min" - "Maximum" | "max" - "Average" | "avg" - "Sum" | "sum" - "SampleCount | "n" - "pNN.NN" Default: Average
        :param unit: Unit used to filter the metric stream. Only refer to datums emitted to the metric stream with the given unit and ignore all others. Only useful when datums are being emitted to the same metric stream under different units. The default is to use all matric datums in the stream, regardless of unit, which is recommended in nearly all cases. CloudWatch does not honor this property for graphs. Default: - All metric datums in the given metric stream

        default
        :default: sum over 5 minutes

        stability
        :stability: experimental
        """
        props = aws_cdk.aws_cloudwatch.MetricOptions(account=account, color=color, dimensions=dimensions, label=label, period=period, region=region, statistic=statistic, unit=unit)

        return jsii.invoke(self, "metricFailed", [props])

    @jsii.member(jsii_name="metricHeartbeatTimedOut")
    def metric_heartbeat_timed_out(self, *, account: typing.Optional[str]=None, color: typing.Optional[str]=None, dimensions: typing.Optional[typing.Mapping[str, typing.Any]]=None, label: typing.Optional[str]=None, period: typing.Optional[aws_cdk.core.Duration]=None, region: typing.Optional[str]=None, statistic: typing.Optional[str]=None, unit: typing.Optional[aws_cdk.aws_cloudwatch.Unit]=None) -> aws_cdk.aws_cloudwatch.Metric:
        """Metric for the number of times the heartbeat times out for this activity.

        :param account: Account which this metric comes from. Default: - Deployment account.
        :param color: The hex color code, prefixed with '#' (e.g. '#00ff00'), to use when this metric is rendered on a graph. The ``Color`` class has a set of standard colors that can be used here. Default: - Automatic color
        :param dimensions: Dimensions of the metric. Default: - No dimensions.
        :param label: Label for this metric when added to a Graph in a Dashboard. Default: - No label
        :param period: The period over which the specified statistic is applied. Default: Duration.minutes(5)
        :param region: Region which this metric comes from. Default: - Deployment region.
        :param statistic: What function to use for aggregating. Can be one of the following: - "Minimum" | "min" - "Maximum" | "max" - "Average" | "avg" - "Sum" | "sum" - "SampleCount | "n" - "pNN.NN" Default: Average
        :param unit: Unit used to filter the metric stream. Only refer to datums emitted to the metric stream with the given unit and ignore all others. Only useful when datums are being emitted to the same metric stream under different units. The default is to use all matric datums in the stream, regardless of unit, which is recommended in nearly all cases. CloudWatch does not honor this property for graphs. Default: - All metric datums in the given metric stream

        default
        :default: sum over 5 minutes

        stability
        :stability: experimental
        """
        props = aws_cdk.aws_cloudwatch.MetricOptions(account=account, color=color, dimensions=dimensions, label=label, period=period, region=region, statistic=statistic, unit=unit)

        return jsii.invoke(self, "metricHeartbeatTimedOut", [props])

    @jsii.member(jsii_name="metricRunTime")
    def metric_run_time(self, *, account: typing.Optional[str]=None, color: typing.Optional[str]=None, dimensions: typing.Optional[typing.Mapping[str, typing.Any]]=None, label: typing.Optional[str]=None, period: typing.Optional[aws_cdk.core.Duration]=None, region: typing.Optional[str]=None, statistic: typing.Optional[str]=None, unit: typing.Optional[aws_cdk.aws_cloudwatch.Unit]=None) -> aws_cdk.aws_cloudwatch.Metric:
        """The interval, in milliseconds, between the time the Task starts and the time it closes.

        :param account: Account which this metric comes from. Default: - Deployment account.
        :param color: The hex color code, prefixed with '#' (e.g. '#00ff00'), to use when this metric is rendered on a graph. The ``Color`` class has a set of standard colors that can be used here. Default: - Automatic color
        :param dimensions: Dimensions of the metric. Default: - No dimensions.
        :param label: Label for this metric when added to a Graph in a Dashboard. Default: - No label
        :param period: The period over which the specified statistic is applied. Default: Duration.minutes(5)
        :param region: Region which this metric comes from. Default: - Deployment region.
        :param statistic: What function to use for aggregating. Can be one of the following: - "Minimum" | "min" - "Maximum" | "max" - "Average" | "avg" - "Sum" | "sum" - "SampleCount | "n" - "pNN.NN" Default: Average
        :param unit: Unit used to filter the metric stream. Only refer to datums emitted to the metric stream with the given unit and ignore all others. Only useful when datums are being emitted to the same metric stream under different units. The default is to use all matric datums in the stream, regardless of unit, which is recommended in nearly all cases. CloudWatch does not honor this property for graphs. Default: - All metric datums in the given metric stream

        default
        :default: average over 5 minutes

        stability
        :stability: experimental
        """
        props = aws_cdk.aws_cloudwatch.MetricOptions(account=account, color=color, dimensions=dimensions, label=label, period=period, region=region, statistic=statistic, unit=unit)

        return jsii.invoke(self, "metricRunTime", [props])

    @jsii.member(jsii_name="metricScheduled")
    def metric_scheduled(self, *, account: typing.Optional[str]=None, color: typing.Optional[str]=None, dimensions: typing.Optional[typing.Mapping[str, typing.Any]]=None, label: typing.Optional[str]=None, period: typing.Optional[aws_cdk.core.Duration]=None, region: typing.Optional[str]=None, statistic: typing.Optional[str]=None, unit: typing.Optional[aws_cdk.aws_cloudwatch.Unit]=None) -> aws_cdk.aws_cloudwatch.Metric:
        """Metric for the number of times this activity is scheduled.

        :param account: Account which this metric comes from. Default: - Deployment account.
        :param color: The hex color code, prefixed with '#' (e.g. '#00ff00'), to use when this metric is rendered on a graph. The ``Color`` class has a set of standard colors that can be used here. Default: - Automatic color
        :param dimensions: Dimensions of the metric. Default: - No dimensions.
        :param label: Label for this metric when added to a Graph in a Dashboard. Default: - No label
        :param period: The period over which the specified statistic is applied. Default: Duration.minutes(5)
        :param region: Region which this metric comes from. Default: - Deployment region.
        :param statistic: What function to use for aggregating. Can be one of the following: - "Minimum" | "min" - "Maximum" | "max" - "Average" | "avg" - "Sum" | "sum" - "SampleCount | "n" - "pNN.NN" Default: Average
        :param unit: Unit used to filter the metric stream. Only refer to datums emitted to the metric stream with the given unit and ignore all others. Only useful when datums are being emitted to the same metric stream under different units. The default is to use all matric datums in the stream, regardless of unit, which is recommended in nearly all cases. CloudWatch does not honor this property for graphs. Default: - All metric datums in the given metric stream

        default
        :default: sum over 5 minutes

        stability
        :stability: experimental
        """
        props = aws_cdk.aws_cloudwatch.MetricOptions(account=account, color=color, dimensions=dimensions, label=label, period=period, region=region, statistic=statistic, unit=unit)

        return jsii.invoke(self, "metricScheduled", [props])

    @jsii.member(jsii_name="metricScheduleTime")
    def metric_schedule_time(self, *, account: typing.Optional[str]=None, color: typing.Optional[str]=None, dimensions: typing.Optional[typing.Mapping[str, typing.Any]]=None, label: typing.Optional[str]=None, period: typing.Optional[aws_cdk.core.Duration]=None, region: typing.Optional[str]=None, statistic: typing.Optional[str]=None, unit: typing.Optional[aws_cdk.aws_cloudwatch.Unit]=None) -> aws_cdk.aws_cloudwatch.Metric:
        """The interval, in milliseconds, for which the activity stays in the schedule state.

        :param account: Account which this metric comes from. Default: - Deployment account.
        :param color: The hex color code, prefixed with '#' (e.g. '#00ff00'), to use when this metric is rendered on a graph. The ``Color`` class has a set of standard colors that can be used here. Default: - Automatic color
        :param dimensions: Dimensions of the metric. Default: - No dimensions.
        :param label: Label for this metric when added to a Graph in a Dashboard. Default: - No label
        :param period: The period over which the specified statistic is applied. Default: Duration.minutes(5)
        :param region: Region which this metric comes from. Default: - Deployment region.
        :param statistic: What function to use for aggregating. Can be one of the following: - "Minimum" | "min" - "Maximum" | "max" - "Average" | "avg" - "Sum" | "sum" - "SampleCount | "n" - "pNN.NN" Default: Average
        :param unit: Unit used to filter the metric stream. Only refer to datums emitted to the metric stream with the given unit and ignore all others. Only useful when datums are being emitted to the same metric stream under different units. The default is to use all matric datums in the stream, regardless of unit, which is recommended in nearly all cases. CloudWatch does not honor this property for graphs. Default: - All metric datums in the given metric stream

        default
        :default: average over 5 minutes

        stability
        :stability: experimental
        """
        props = aws_cdk.aws_cloudwatch.MetricOptions(account=account, color=color, dimensions=dimensions, label=label, period=period, region=region, statistic=statistic, unit=unit)

        return jsii.invoke(self, "metricScheduleTime", [props])

    @jsii.member(jsii_name="metricStarted")
    def metric_started(self, *, account: typing.Optional[str]=None, color: typing.Optional[str]=None, dimensions: typing.Optional[typing.Mapping[str, typing.Any]]=None, label: typing.Optional[str]=None, period: typing.Optional[aws_cdk.core.Duration]=None, region: typing.Optional[str]=None, statistic: typing.Optional[str]=None, unit: typing.Optional[aws_cdk.aws_cloudwatch.Unit]=None) -> aws_cdk.aws_cloudwatch.Metric:
        """Metric for the number of times this activity is started.

        :param account: Account which this metric comes from. Default: - Deployment account.
        :param color: The hex color code, prefixed with '#' (e.g. '#00ff00'), to use when this metric is rendered on a graph. The ``Color`` class has a set of standard colors that can be used here. Default: - Automatic color
        :param dimensions: Dimensions of the metric. Default: - No dimensions.
        :param label: Label for this metric when added to a Graph in a Dashboard. Default: - No label
        :param period: The period over which the specified statistic is applied. Default: Duration.minutes(5)
        :param region: Region which this metric comes from. Default: - Deployment region.
        :param statistic: What function to use for aggregating. Can be one of the following: - "Minimum" | "min" - "Maximum" | "max" - "Average" | "avg" - "Sum" | "sum" - "SampleCount | "n" - "pNN.NN" Default: Average
        :param unit: Unit used to filter the metric stream. Only refer to datums emitted to the metric stream with the given unit and ignore all others. Only useful when datums are being emitted to the same metric stream under different units. The default is to use all matric datums in the stream, regardless of unit, which is recommended in nearly all cases. CloudWatch does not honor this property for graphs. Default: - All metric datums in the given metric stream

        default
        :default: sum over 5 minutes

        stability
        :stability: experimental
        """
        props = aws_cdk.aws_cloudwatch.MetricOptions(account=account, color=color, dimensions=dimensions, label=label, period=period, region=region, statistic=statistic, unit=unit)

        return jsii.invoke(self, "metricStarted", [props])

    @jsii.member(jsii_name="metricSucceeded")
    def metric_succeeded(self, *, account: typing.Optional[str]=None, color: typing.Optional[str]=None, dimensions: typing.Optional[typing.Mapping[str, typing.Any]]=None, label: typing.Optional[str]=None, period: typing.Optional[aws_cdk.core.Duration]=None, region: typing.Optional[str]=None, statistic: typing.Optional[str]=None, unit: typing.Optional[aws_cdk.aws_cloudwatch.Unit]=None) -> aws_cdk.aws_cloudwatch.Metric:
        """Metric for the number of times this activity succeeds.

        :param account: Account which this metric comes from. Default: - Deployment account.
        :param color: The hex color code, prefixed with '#' (e.g. '#00ff00'), to use when this metric is rendered on a graph. The ``Color`` class has a set of standard colors that can be used here. Default: - Automatic color
        :param dimensions: Dimensions of the metric. Default: - No dimensions.
        :param label: Label for this metric when added to a Graph in a Dashboard. Default: - No label
        :param period: The period over which the specified statistic is applied. Default: Duration.minutes(5)
        :param region: Region which this metric comes from. Default: - Deployment region.
        :param statistic: What function to use for aggregating. Can be one of the following: - "Minimum" | "min" - "Maximum" | "max" - "Average" | "avg" - "Sum" | "sum" - "SampleCount | "n" - "pNN.NN" Default: Average
        :param unit: Unit used to filter the metric stream. Only refer to datums emitted to the metric stream with the given unit and ignore all others. Only useful when datums are being emitted to the same metric stream under different units. The default is to use all matric datums in the stream, regardless of unit, which is recommended in nearly all cases. CloudWatch does not honor this property for graphs. Default: - All metric datums in the given metric stream

        default
        :default: sum over 5 minutes

        stability
        :stability: experimental
        """
        props = aws_cdk.aws_cloudwatch.MetricOptions(account=account, color=color, dimensions=dimensions, label=label, period=period, region=region, statistic=statistic, unit=unit)

        return jsii.invoke(self, "metricSucceeded", [props])

    @jsii.member(jsii_name="metricTime")
    def metric_time(self, *, account: typing.Optional[str]=None, color: typing.Optional[str]=None, dimensions: typing.Optional[typing.Mapping[str, typing.Any]]=None, label: typing.Optional[str]=None, period: typing.Optional[aws_cdk.core.Duration]=None, region: typing.Optional[str]=None, statistic: typing.Optional[str]=None, unit: typing.Optional[aws_cdk.aws_cloudwatch.Unit]=None) -> aws_cdk.aws_cloudwatch.Metric:
        """The interval, in milliseconds, between the time the activity is scheduled and the time it closes.

        :param account: Account which this metric comes from. Default: - Deployment account.
        :param color: The hex color code, prefixed with '#' (e.g. '#00ff00'), to use when this metric is rendered on a graph. The ``Color`` class has a set of standard colors that can be used here. Default: - Automatic color
        :param dimensions: Dimensions of the metric. Default: - No dimensions.
        :param label: Label for this metric when added to a Graph in a Dashboard. Default: - No label
        :param period: The period over which the specified statistic is applied. Default: Duration.minutes(5)
        :param region: Region which this metric comes from. Default: - Deployment region.
        :param statistic: What function to use for aggregating. Can be one of the following: - "Minimum" | "min" - "Maximum" | "max" - "Average" | "avg" - "Sum" | "sum" - "SampleCount | "n" - "pNN.NN" Default: Average
        :param unit: Unit used to filter the metric stream. Only refer to datums emitted to the metric stream with the given unit and ignore all others. Only useful when datums are being emitted to the same metric stream under different units. The default is to use all matric datums in the stream, regardless of unit, which is recommended in nearly all cases. CloudWatch does not honor this property for graphs. Default: - All metric datums in the given metric stream

        default
        :default: average over 5 minutes

        stability
        :stability: experimental
        """
        props = aws_cdk.aws_cloudwatch.MetricOptions(account=account, color=color, dimensions=dimensions, label=label, period=period, region=region, statistic=statistic, unit=unit)

        return jsii.invoke(self, "metricTime", [props])

    @jsii.member(jsii_name="metricTimedOut")
    def metric_timed_out(self, *, account: typing.Optional[str]=None, color: typing.Optional[str]=None, dimensions: typing.Optional[typing.Mapping[str, typing.Any]]=None, label: typing.Optional[str]=None, period: typing.Optional[aws_cdk.core.Duration]=None, region: typing.Optional[str]=None, statistic: typing.Optional[str]=None, unit: typing.Optional[aws_cdk.aws_cloudwatch.Unit]=None) -> aws_cdk.aws_cloudwatch.Metric:
        """Metric for the number of times this activity times out.

        :param account: Account which this metric comes from. Default: - Deployment account.
        :param color: The hex color code, prefixed with '#' (e.g. '#00ff00'), to use when this metric is rendered on a graph. The ``Color`` class has a set of standard colors that can be used here. Default: - Automatic color
        :param dimensions: Dimensions of the metric. Default: - No dimensions.
        :param label: Label for this metric when added to a Graph in a Dashboard. Default: - No label
        :param period: The period over which the specified statistic is applied. Default: Duration.minutes(5)
        :param region: Region which this metric comes from. Default: - Deployment region.
        :param statistic: What function to use for aggregating. Can be one of the following: - "Minimum" | "min" - "Maximum" | "max" - "Average" | "avg" - "Sum" | "sum" - "SampleCount | "n" - "pNN.NN" Default: Average
        :param unit: Unit used to filter the metric stream. Only refer to datums emitted to the metric stream with the given unit and ignore all others. Only useful when datums are being emitted to the same metric stream under different units. The default is to use all matric datums in the stream, regardless of unit, which is recommended in nearly all cases. CloudWatch does not honor this property for graphs. Default: - All metric datums in the given metric stream

        default
        :default: sum over 5 minutes

        stability
        :stability: experimental
        """
        props = aws_cdk.aws_cloudwatch.MetricOptions(account=account, color=color, dimensions=dimensions, label=label, period=period, region=region, statistic=statistic, unit=unit)

        return jsii.invoke(self, "metricTimedOut", [props])

    @jsii.member(jsii_name="next")
    def next(self, next: "IChainable") -> "Chain":
        """Continue normal execution with the given state.

        :param next: -

        stability
        :stability: experimental
        """
        return jsii.invoke(self, "next", [next])

    @jsii.member(jsii_name="toStateJson")
    def to_state_json(self) -> typing.Mapping[typing.Any, typing.Any]:
        """Return the Amazon States Language object for this state.

        stability
        :stability: experimental
        """
        return jsii.invoke(self, "toStateJson", [])

    @jsii.member(jsii_name="whenBoundToGraph")
    def _when_bound_to_graph(self, graph: "StateGraph") -> None:
        """Called whenever this state is bound to a graph.

        Can be overridden by subclasses.

        :param graph: -

        stability
        :stability: experimental
        """
        return jsii.invoke(self, "whenBoundToGraph", [graph])

    @builtins.property
    @jsii.member(jsii_name="endStates")
    def end_states(self) -> typing.List["INextable"]:
        """Continuable states of this Chainable.

        stability
        :stability: experimental
        """
        return jsii.get(self, "endStates")


class TaskInput(metaclass=jsii.JSIIMeta, jsii_type="@aws-cdk/aws-stepfunctions.TaskInput"):
    """Type union for task classes that accept multiple types of payload.

    stability
    :stability: experimental
    """
    @jsii.member(jsii_name="fromContextAt")
    @builtins.classmethod
    def from_context_at(cls, path: str) -> "TaskInput":
        """Use a part of the task context as task input.

        Use this when you want to use a subobject or string from
        the current task context as complete payload
        to a task.

        :param path: -

        stability
        :stability: experimental
        """
        return jsii.sinvoke(cls, "fromContextAt", [path])

    @jsii.member(jsii_name="fromDataAt")
    @builtins.classmethod
    def from_data_at(cls, path: str) -> "TaskInput":
        """Use a part of the execution data as task input.

        Use this when you want to use a subobject or string from
        the current state machine execution as complete payload
        to a task.

        :param path: -

        stability
        :stability: experimental
        """
        return jsii.sinvoke(cls, "fromDataAt", [path])

    @jsii.member(jsii_name="fromObject")
    @builtins.classmethod
    def from_object(cls, obj: typing.Mapping[str, typing.Any]) -> "TaskInput":
        """Use an object as task input.

        This object may contain Data and Context fields
        as object values, if desired.

        :param obj: -

        stability
        :stability: experimental
        """
        return jsii.sinvoke(cls, "fromObject", [obj])

    @jsii.member(jsii_name="fromText")
    @builtins.classmethod
    def from_text(cls, text: str) -> "TaskInput":
        """Use a literal string as task input.

        This might be a JSON-encoded object, or just a text.

        :param text: -

        stability
        :stability: experimental
        """
        return jsii.sinvoke(cls, "fromText", [text])

    @builtins.property
    @jsii.member(jsii_name="type")
    def type(self) -> "InputType":
        """type of task input.

        stability
        :stability: experimental
        """
        return jsii.get(self, "type")

    @builtins.property
    @jsii.member(jsii_name="value")
    def value(self) -> typing.Any:
        """payload for the corresponding input type.

        It can be a JSON-encoded object, context, data, etc.

        stability
        :stability: experimental
        """
        return jsii.get(self, "value")


@jsii.data_type(jsii_type="@aws-cdk/aws-stepfunctions.TaskProps", jsii_struct_bases=[], name_mapping={'task': 'task', 'comment': 'comment', 'input_path': 'inputPath', 'output_path': 'outputPath', 'parameters': 'parameters', 'result_path': 'resultPath', 'timeout': 'timeout'})
class TaskProps():
    def __init__(self, *, task: "IStepFunctionsTask", comment: typing.Optional[str]=None, input_path: typing.Optional[str]=None, output_path: typing.Optional[str]=None, parameters: typing.Optional[typing.Mapping[str, typing.Any]]=None, result_path: typing.Optional[str]=None, timeout: typing.Optional[aws_cdk.core.Duration]=None) -> None:
        """Props that are common to all tasks.

        :param task: Actual task to be invoked in this workflow.
        :param comment: An optional description for this state. Default: No comment
        :param input_path: JSONPath expression to select part of the state to be the input to this state. May also be the special value DISCARD, which will cause the effective input to be the empty object {}. Default: $
        :param output_path: JSONPath expression to select part of the state to be the output to this state. May also be the special value DISCARD, which will cause the effective output to be the empty object {}. Default: $
        :param parameters: Parameters to invoke the task with. It is not recommended to use this field. The object that is passed in the ``task`` property will take care of returning the right values for the ``Parameters`` field in the Step Functions definition. The various classes that implement ``IStepFunctionsTask`` will take a properties which make sense for the task type. For example, for ``InvokeFunction`` the field that populates the ``parameters`` field will be called ``payload``, and for the ``PublishToTopic`` the ``parameters`` field will be populated via a combination of the referenced topic, subject and message. If passed anyway, the keys in this map will override the parameters returned by the task object. Default: - Use the parameters implied by the ``task`` property
        :param result_path: JSONPath expression to indicate where to inject the state's output. May also be the special value DISCARD, which will cause the state's input to become its output. Default: $
        :param timeout: Maximum run time of this state. If the state takes longer than this amount of time to complete, a 'Timeout' error is raised. Default: 60

        stability
        :stability: experimental
        """
        self._values = {
            'task': task,
        }
        if comment is not None: self._values["comment"] = comment
        if input_path is not None: self._values["input_path"] = input_path
        if output_path is not None: self._values["output_path"] = output_path
        if parameters is not None: self._values["parameters"] = parameters
        if result_path is not None: self._values["result_path"] = result_path
        if timeout is not None: self._values["timeout"] = timeout

    @builtins.property
    def task(self) -> "IStepFunctionsTask":
        """Actual task to be invoked in this workflow.

        stability
        :stability: experimental
        """
        return self._values.get('task')

    @builtins.property
    def comment(self) -> typing.Optional[str]:
        """An optional description for this state.

        default
        :default: No comment

        stability
        :stability: experimental
        """
        return self._values.get('comment')

    @builtins.property
    def input_path(self) -> typing.Optional[str]:
        """JSONPath expression to select part of the state to be the input to this state.

        May also be the special value DISCARD, which will cause the effective
        input to be the empty object {}.

        default
        :default: $

        stability
        :stability: experimental
        """
        return self._values.get('input_path')

    @builtins.property
    def output_path(self) -> typing.Optional[str]:
        """JSONPath expression to select part of the state to be the output to this state.

        May also be the special value DISCARD, which will cause the effective
        output to be the empty object {}.

        default
        :default: $

        stability
        :stability: experimental
        """
        return self._values.get('output_path')

    @builtins.property
    def parameters(self) -> typing.Optional[typing.Mapping[str, typing.Any]]:
        """Parameters to invoke the task with.

        It is not recommended to use this field. The object that is passed in
        the ``task`` property will take care of returning the right values for the
        ``Parameters`` field in the Step Functions definition.

        The various classes that implement ``IStepFunctionsTask`` will take a
        properties which make sense for the task type. For example, for
        ``InvokeFunction`` the field that populates the ``parameters`` field will be
        called ``payload``, and for the ``PublishToTopic`` the ``parameters`` field
        will be populated via a combination of the referenced topic, subject and
        message.

        If passed anyway, the keys in this map will override the parameters
        returned by the task object.

        default
        :default: - Use the parameters implied by the ``task`` property

        see
        :see: https://docs.aws.amazon.com/step-functions/latest/dg/input-output-inputpath-params.html#input-output-parameters
        stability
        :stability: experimental
        """
        return self._values.get('parameters')

    @builtins.property
    def result_path(self) -> typing.Optional[str]:
        """JSONPath expression to indicate where to inject the state's output.

        May also be the special value DISCARD, which will cause the state's
        input to become its output.

        default
        :default: $

        stability
        :stability: experimental
        """
        return self._values.get('result_path')

    @builtins.property
    def timeout(self) -> typing.Optional[aws_cdk.core.Duration]:
        """Maximum run time of this state.

        If the state takes longer than this amount of time to complete, a 'Timeout' error is raised.

        default
        :default: 60

        stability
        :stability: experimental
        """
        return self._values.get('timeout')

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return 'TaskProps(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


@jsii.implements(INextable)
class Wait(State, metaclass=jsii.JSIIMeta, jsii_type="@aws-cdk/aws-stepfunctions.Wait"):
    """Define a Wait state in the state machine.

    A Wait state can be used to delay execution of the state machine for a while.

    stability
    :stability: experimental
    """
    def __init__(self, scope: aws_cdk.core.Construct, id: str, *, time: "WaitTime", comment: typing.Optional[str]=None) -> None:
        """
        :param scope: -
        :param id: -
        :param time: Wait duration.
        :param comment: An optional description for this state. Default: No comment

        stability
        :stability: experimental
        """
        props = WaitProps(time=time, comment=comment)

        jsii.create(Wait, self, [scope, id, props])

    @jsii.member(jsii_name="next")
    def next(self, next: "IChainable") -> "Chain":
        """Continue normal execution with the given state.

        :param next: -

        stability
        :stability: experimental
        """
        return jsii.invoke(self, "next", [next])

    @jsii.member(jsii_name="toStateJson")
    def to_state_json(self) -> typing.Mapping[typing.Any, typing.Any]:
        """Return the Amazon States Language object for this state.

        stability
        :stability: experimental
        """
        return jsii.invoke(self, "toStateJson", [])

    @builtins.property
    @jsii.member(jsii_name="endStates")
    def end_states(self) -> typing.List["INextable"]:
        """Continuable states of this Chainable.

        stability
        :stability: experimental
        """
        return jsii.get(self, "endStates")


@jsii.data_type(jsii_type="@aws-cdk/aws-stepfunctions.WaitProps", jsii_struct_bases=[], name_mapping={'time': 'time', 'comment': 'comment'})
class WaitProps():
    def __init__(self, *, time: "WaitTime", comment: typing.Optional[str]=None) -> None:
        """Properties for defining a Wait state.

        :param time: Wait duration.
        :param comment: An optional description for this state. Default: No comment

        stability
        :stability: experimental
        """
        self._values = {
            'time': time,
        }
        if comment is not None: self._values["comment"] = comment

    @builtins.property
    def time(self) -> "WaitTime":
        """Wait duration.

        stability
        :stability: experimental
        """
        return self._values.get('time')

    @builtins.property
    def comment(self) -> typing.Optional[str]:
        """An optional description for this state.

        default
        :default: No comment

        stability
        :stability: experimental
        """
        return self._values.get('comment')

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return 'WaitProps(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


class WaitTime(metaclass=jsii.JSIIMeta, jsii_type="@aws-cdk/aws-stepfunctions.WaitTime"):
    """Represents the Wait state which delays a state machine from continuing for a specified time.

    see
    :see: https://docs.aws.amazon.com/step-functions/latest/dg/amazon-states-language-wait-state.html
    stability
    :stability: experimental
    """
    @jsii.member(jsii_name="duration")
    @builtins.classmethod
    def duration(cls, duration: aws_cdk.core.Duration) -> "WaitTime":
        """Wait a fixed amount of time.

        :param duration: -

        stability
        :stability: experimental
        """
        return jsii.sinvoke(cls, "duration", [duration])

    @jsii.member(jsii_name="secondsPath")
    @builtins.classmethod
    def seconds_path(cls, path: str) -> "WaitTime":
        """Wait for a number of seconds stored in the state object.

        :param path: -

        stability
        :stability: experimental

        Example::

            # Example automatically generated without compilation. See https://github.com/aws/jsii/issues/826
            $.wait_seconds
        """
        return jsii.sinvoke(cls, "secondsPath", [path])

    @jsii.member(jsii_name="timestamp")
    @builtins.classmethod
    def timestamp(cls, timestamp: str) -> "WaitTime":
        """Wait until the given ISO8601 timestamp.

        :param timestamp: -

        stability
        :stability: experimental

        Example::

            # Example automatically generated without compilation. See https://github.com/aws/jsii/issues/826
            2016 - 03 - 14T01:5900Z
        """
        return jsii.sinvoke(cls, "timestamp", [timestamp])

    @jsii.member(jsii_name="timestampPath")
    @builtins.classmethod
    def timestamp_path(cls, path: str) -> "WaitTime":
        """Wait until a timestamp found in the state object.

        :param path: -

        stability
        :stability: experimental

        Example::

            # Example automatically generated without compilation. See https://github.com/aws/jsii/issues/826
            $.wait_timestamp
        """
        return jsii.sinvoke(cls, "timestampPath", [path])


@jsii.implements(IActivity)
class Activity(aws_cdk.core.Resource, metaclass=jsii.JSIIMeta, jsii_type="@aws-cdk/aws-stepfunctions.Activity"):
    """Define a new Step Functions Activity.

    stability
    :stability: experimental
    """
    def __init__(self, scope: aws_cdk.core.Construct, id: str, *, activity_name: typing.Optional[str]=None) -> None:
        """
        :param scope: -
        :param id: -
        :param activity_name: The name for this activity. Default: - If not supplied, a name is generated

        stability
        :stability: experimental
        """
        props = ActivityProps(activity_name=activity_name)

        jsii.create(Activity, self, [scope, id, props])

    @jsii.member(jsii_name="fromActivityArn")
    @builtins.classmethod
    def from_activity_arn(cls, scope: aws_cdk.core.Construct, id: str, activity_arn: str) -> "IActivity":
        """Construct an Activity from an existing Activity ARN.

        :param scope: -
        :param id: -
        :param activity_arn: -

        stability
        :stability: experimental
        """
        return jsii.sinvoke(cls, "fromActivityArn", [scope, id, activity_arn])

    @jsii.member(jsii_name="fromActivityName")
    @builtins.classmethod
    def from_activity_name(cls, scope: aws_cdk.core.Construct, id: str, activity_name: str) -> "IActivity":
        """Construct an Activity from an existing Activity Name.

        :param scope: -
        :param id: -
        :param activity_name: -

        stability
        :stability: experimental
        """
        return jsii.sinvoke(cls, "fromActivityName", [scope, id, activity_name])

    @jsii.member(jsii_name="metric")
    def metric(self, metric_name: str, *, account: typing.Optional[str]=None, color: typing.Optional[str]=None, dimensions: typing.Optional[typing.Mapping[str, typing.Any]]=None, label: typing.Optional[str]=None, period: typing.Optional[aws_cdk.core.Duration]=None, region: typing.Optional[str]=None, statistic: typing.Optional[str]=None, unit: typing.Optional[aws_cdk.aws_cloudwatch.Unit]=None) -> aws_cdk.aws_cloudwatch.Metric:
        """Return the given named metric for this Activity.

        :param metric_name: -
        :param account: Account which this metric comes from. Default: - Deployment account.
        :param color: The hex color code, prefixed with '#' (e.g. '#00ff00'), to use when this metric is rendered on a graph. The ``Color`` class has a set of standard colors that can be used here. Default: - Automatic color
        :param dimensions: Dimensions of the metric. Default: - No dimensions.
        :param label: Label for this metric when added to a Graph in a Dashboard. Default: - No label
        :param period: The period over which the specified statistic is applied. Default: Duration.minutes(5)
        :param region: Region which this metric comes from. Default: - Deployment region.
        :param statistic: What function to use for aggregating. Can be one of the following: - "Minimum" | "min" - "Maximum" | "max" - "Average" | "avg" - "Sum" | "sum" - "SampleCount | "n" - "pNN.NN" Default: Average
        :param unit: Unit used to filter the metric stream. Only refer to datums emitted to the metric stream with the given unit and ignore all others. Only useful when datums are being emitted to the same metric stream under different units. The default is to use all matric datums in the stream, regardless of unit, which is recommended in nearly all cases. CloudWatch does not honor this property for graphs. Default: - All metric datums in the given metric stream

        default
        :default: sum over 5 minutes

        stability
        :stability: experimental
        """
        props = aws_cdk.aws_cloudwatch.MetricOptions(account=account, color=color, dimensions=dimensions, label=label, period=period, region=region, statistic=statistic, unit=unit)

        return jsii.invoke(self, "metric", [metric_name, props])

    @jsii.member(jsii_name="metricFailed")
    def metric_failed(self, *, account: typing.Optional[str]=None, color: typing.Optional[str]=None, dimensions: typing.Optional[typing.Mapping[str, typing.Any]]=None, label: typing.Optional[str]=None, period: typing.Optional[aws_cdk.core.Duration]=None, region: typing.Optional[str]=None, statistic: typing.Optional[str]=None, unit: typing.Optional[aws_cdk.aws_cloudwatch.Unit]=None) -> aws_cdk.aws_cloudwatch.Metric:
        """Metric for the number of times this activity fails.

        :param account: Account which this metric comes from. Default: - Deployment account.
        :param color: The hex color code, prefixed with '#' (e.g. '#00ff00'), to use when this metric is rendered on a graph. The ``Color`` class has a set of standard colors that can be used here. Default: - Automatic color
        :param dimensions: Dimensions of the metric. Default: - No dimensions.
        :param label: Label for this metric when added to a Graph in a Dashboard. Default: - No label
        :param period: The period over which the specified statistic is applied. Default: Duration.minutes(5)
        :param region: Region which this metric comes from. Default: - Deployment region.
        :param statistic: What function to use for aggregating. Can be one of the following: - "Minimum" | "min" - "Maximum" | "max" - "Average" | "avg" - "Sum" | "sum" - "SampleCount | "n" - "pNN.NN" Default: Average
        :param unit: Unit used to filter the metric stream. Only refer to datums emitted to the metric stream with the given unit and ignore all others. Only useful when datums are being emitted to the same metric stream under different units. The default is to use all matric datums in the stream, regardless of unit, which is recommended in nearly all cases. CloudWatch does not honor this property for graphs. Default: - All metric datums in the given metric stream

        default
        :default: sum over 5 minutes

        stability
        :stability: experimental
        """
        props = aws_cdk.aws_cloudwatch.MetricOptions(account=account, color=color, dimensions=dimensions, label=label, period=period, region=region, statistic=statistic, unit=unit)

        return jsii.invoke(self, "metricFailed", [props])

    @jsii.member(jsii_name="metricHeartbeatTimedOut")
    def metric_heartbeat_timed_out(self, *, account: typing.Optional[str]=None, color: typing.Optional[str]=None, dimensions: typing.Optional[typing.Mapping[str, typing.Any]]=None, label: typing.Optional[str]=None, period: typing.Optional[aws_cdk.core.Duration]=None, region: typing.Optional[str]=None, statistic: typing.Optional[str]=None, unit: typing.Optional[aws_cdk.aws_cloudwatch.Unit]=None) -> aws_cdk.aws_cloudwatch.Metric:
        """Metric for the number of times the heartbeat times out for this activity.

        :param account: Account which this metric comes from. Default: - Deployment account.
        :param color: The hex color code, prefixed with '#' (e.g. '#00ff00'), to use when this metric is rendered on a graph. The ``Color`` class has a set of standard colors that can be used here. Default: - Automatic color
        :param dimensions: Dimensions of the metric. Default: - No dimensions.
        :param label: Label for this metric when added to a Graph in a Dashboard. Default: - No label
        :param period: The period over which the specified statistic is applied. Default: Duration.minutes(5)
        :param region: Region which this metric comes from. Default: - Deployment region.
        :param statistic: What function to use for aggregating. Can be one of the following: - "Minimum" | "min" - "Maximum" | "max" - "Average" | "avg" - "Sum" | "sum" - "SampleCount | "n" - "pNN.NN" Default: Average
        :param unit: Unit used to filter the metric stream. Only refer to datums emitted to the metric stream with the given unit and ignore all others. Only useful when datums are being emitted to the same metric stream under different units. The default is to use all matric datums in the stream, regardless of unit, which is recommended in nearly all cases. CloudWatch does not honor this property for graphs. Default: - All metric datums in the given metric stream

        default
        :default: sum over 5 minutes

        stability
        :stability: experimental
        """
        props = aws_cdk.aws_cloudwatch.MetricOptions(account=account, color=color, dimensions=dimensions, label=label, period=period, region=region, statistic=statistic, unit=unit)

        return jsii.invoke(self, "metricHeartbeatTimedOut", [props])

    @jsii.member(jsii_name="metricRunTime")
    def metric_run_time(self, *, account: typing.Optional[str]=None, color: typing.Optional[str]=None, dimensions: typing.Optional[typing.Mapping[str, typing.Any]]=None, label: typing.Optional[str]=None, period: typing.Optional[aws_cdk.core.Duration]=None, region: typing.Optional[str]=None, statistic: typing.Optional[str]=None, unit: typing.Optional[aws_cdk.aws_cloudwatch.Unit]=None) -> aws_cdk.aws_cloudwatch.Metric:
        """The interval, in milliseconds, between the time the activity starts and the time it closes.

        :param account: Account which this metric comes from. Default: - Deployment account.
        :param color: The hex color code, prefixed with '#' (e.g. '#00ff00'), to use when this metric is rendered on a graph. The ``Color`` class has a set of standard colors that can be used here. Default: - Automatic color
        :param dimensions: Dimensions of the metric. Default: - No dimensions.
        :param label: Label for this metric when added to a Graph in a Dashboard. Default: - No label
        :param period: The period over which the specified statistic is applied. Default: Duration.minutes(5)
        :param region: Region which this metric comes from. Default: - Deployment region.
        :param statistic: What function to use for aggregating. Can be one of the following: - "Minimum" | "min" - "Maximum" | "max" - "Average" | "avg" - "Sum" | "sum" - "SampleCount | "n" - "pNN.NN" Default: Average
        :param unit: Unit used to filter the metric stream. Only refer to datums emitted to the metric stream with the given unit and ignore all others. Only useful when datums are being emitted to the same metric stream under different units. The default is to use all matric datums in the stream, regardless of unit, which is recommended in nearly all cases. CloudWatch does not honor this property for graphs. Default: - All metric datums in the given metric stream

        default
        :default: average over 5 minutes

        stability
        :stability: experimental
        """
        props = aws_cdk.aws_cloudwatch.MetricOptions(account=account, color=color, dimensions=dimensions, label=label, period=period, region=region, statistic=statistic, unit=unit)

        return jsii.invoke(self, "metricRunTime", [props])

    @jsii.member(jsii_name="metricScheduled")
    def metric_scheduled(self, *, account: typing.Optional[str]=None, color: typing.Optional[str]=None, dimensions: typing.Optional[typing.Mapping[str, typing.Any]]=None, label: typing.Optional[str]=None, period: typing.Optional[aws_cdk.core.Duration]=None, region: typing.Optional[str]=None, statistic: typing.Optional[str]=None, unit: typing.Optional[aws_cdk.aws_cloudwatch.Unit]=None) -> aws_cdk.aws_cloudwatch.Metric:
        """Metric for the number of times this activity is scheduled.

        :param account: Account which this metric comes from. Default: - Deployment account.
        :param color: The hex color code, prefixed with '#' (e.g. '#00ff00'), to use when this metric is rendered on a graph. The ``Color`` class has a set of standard colors that can be used here. Default: - Automatic color
        :param dimensions: Dimensions of the metric. Default: - No dimensions.
        :param label: Label for this metric when added to a Graph in a Dashboard. Default: - No label
        :param period: The period over which the specified statistic is applied. Default: Duration.minutes(5)
        :param region: Region which this metric comes from. Default: - Deployment region.
        :param statistic: What function to use for aggregating. Can be one of the following: - "Minimum" | "min" - "Maximum" | "max" - "Average" | "avg" - "Sum" | "sum" - "SampleCount | "n" - "pNN.NN" Default: Average
        :param unit: Unit used to filter the metric stream. Only refer to datums emitted to the metric stream with the given unit and ignore all others. Only useful when datums are being emitted to the same metric stream under different units. The default is to use all matric datums in the stream, regardless of unit, which is recommended in nearly all cases. CloudWatch does not honor this property for graphs. Default: - All metric datums in the given metric stream

        default
        :default: sum over 5 minutes

        stability
        :stability: experimental
        """
        props = aws_cdk.aws_cloudwatch.MetricOptions(account=account, color=color, dimensions=dimensions, label=label, period=period, region=region, statistic=statistic, unit=unit)

        return jsii.invoke(self, "metricScheduled", [props])

    @jsii.member(jsii_name="metricScheduleTime")
    def metric_schedule_time(self, *, account: typing.Optional[str]=None, color: typing.Optional[str]=None, dimensions: typing.Optional[typing.Mapping[str, typing.Any]]=None, label: typing.Optional[str]=None, period: typing.Optional[aws_cdk.core.Duration]=None, region: typing.Optional[str]=None, statistic: typing.Optional[str]=None, unit: typing.Optional[aws_cdk.aws_cloudwatch.Unit]=None) -> aws_cdk.aws_cloudwatch.Metric:
        """The interval, in milliseconds, for which the activity stays in the schedule state.

        :param account: Account which this metric comes from. Default: - Deployment account.
        :param color: The hex color code, prefixed with '#' (e.g. '#00ff00'), to use when this metric is rendered on a graph. The ``Color`` class has a set of standard colors that can be used here. Default: - Automatic color
        :param dimensions: Dimensions of the metric. Default: - No dimensions.
        :param label: Label for this metric when added to a Graph in a Dashboard. Default: - No label
        :param period: The period over which the specified statistic is applied. Default: Duration.minutes(5)
        :param region: Region which this metric comes from. Default: - Deployment region.
        :param statistic: What function to use for aggregating. Can be one of the following: - "Minimum" | "min" - "Maximum" | "max" - "Average" | "avg" - "Sum" | "sum" - "SampleCount | "n" - "pNN.NN" Default: Average
        :param unit: Unit used to filter the metric stream. Only refer to datums emitted to the metric stream with the given unit and ignore all others. Only useful when datums are being emitted to the same metric stream under different units. The default is to use all matric datums in the stream, regardless of unit, which is recommended in nearly all cases. CloudWatch does not honor this property for graphs. Default: - All metric datums in the given metric stream

        default
        :default: average over 5 minutes

        stability
        :stability: experimental
        """
        props = aws_cdk.aws_cloudwatch.MetricOptions(account=account, color=color, dimensions=dimensions, label=label, period=period, region=region, statistic=statistic, unit=unit)

        return jsii.invoke(self, "metricScheduleTime", [props])

    @jsii.member(jsii_name="metricStarted")
    def metric_started(self, *, account: typing.Optional[str]=None, color: typing.Optional[str]=None, dimensions: typing.Optional[typing.Mapping[str, typing.Any]]=None, label: typing.Optional[str]=None, period: typing.Optional[aws_cdk.core.Duration]=None, region: typing.Optional[str]=None, statistic: typing.Optional[str]=None, unit: typing.Optional[aws_cdk.aws_cloudwatch.Unit]=None) -> aws_cdk.aws_cloudwatch.Metric:
        """Metric for the number of times this activity is started.

        :param account: Account which this metric comes from. Default: - Deployment account.
        :param color: The hex color code, prefixed with '#' (e.g. '#00ff00'), to use when this metric is rendered on a graph. The ``Color`` class has a set of standard colors that can be used here. Default: - Automatic color
        :param dimensions: Dimensions of the metric. Default: - No dimensions.
        :param label: Label for this metric when added to a Graph in a Dashboard. Default: - No label
        :param period: The period over which the specified statistic is applied. Default: Duration.minutes(5)
        :param region: Region which this metric comes from. Default: - Deployment region.
        :param statistic: What function to use for aggregating. Can be one of the following: - "Minimum" | "min" - "Maximum" | "max" - "Average" | "avg" - "Sum" | "sum" - "SampleCount | "n" - "pNN.NN" Default: Average
        :param unit: Unit used to filter the metric stream. Only refer to datums emitted to the metric stream with the given unit and ignore all others. Only useful when datums are being emitted to the same metric stream under different units. The default is to use all matric datums in the stream, regardless of unit, which is recommended in nearly all cases. CloudWatch does not honor this property for graphs. Default: - All metric datums in the given metric stream

        default
        :default: sum over 5 minutes

        stability
        :stability: experimental
        """
        props = aws_cdk.aws_cloudwatch.MetricOptions(account=account, color=color, dimensions=dimensions, label=label, period=period, region=region, statistic=statistic, unit=unit)

        return jsii.invoke(self, "metricStarted", [props])

    @jsii.member(jsii_name="metricSucceeded")
    def metric_succeeded(self, *, account: typing.Optional[str]=None, color: typing.Optional[str]=None, dimensions: typing.Optional[typing.Mapping[str, typing.Any]]=None, label: typing.Optional[str]=None, period: typing.Optional[aws_cdk.core.Duration]=None, region: typing.Optional[str]=None, statistic: typing.Optional[str]=None, unit: typing.Optional[aws_cdk.aws_cloudwatch.Unit]=None) -> aws_cdk.aws_cloudwatch.Metric:
        """Metric for the number of times this activity succeeds.

        :param account: Account which this metric comes from. Default: - Deployment account.
        :param color: The hex color code, prefixed with '#' (e.g. '#00ff00'), to use when this metric is rendered on a graph. The ``Color`` class has a set of standard colors that can be used here. Default: - Automatic color
        :param dimensions: Dimensions of the metric. Default: - No dimensions.
        :param label: Label for this metric when added to a Graph in a Dashboard. Default: - No label
        :param period: The period over which the specified statistic is applied. Default: Duration.minutes(5)
        :param region: Region which this metric comes from. Default: - Deployment region.
        :param statistic: What function to use for aggregating. Can be one of the following: - "Minimum" | "min" - "Maximum" | "max" - "Average" | "avg" - "Sum" | "sum" - "SampleCount | "n" - "pNN.NN" Default: Average
        :param unit: Unit used to filter the metric stream. Only refer to datums emitted to the metric stream with the given unit and ignore all others. Only useful when datums are being emitted to the same metric stream under different units. The default is to use all matric datums in the stream, regardless of unit, which is recommended in nearly all cases. CloudWatch does not honor this property for graphs. Default: - All metric datums in the given metric stream

        default
        :default: sum over 5 minutes

        stability
        :stability: experimental
        """
        props = aws_cdk.aws_cloudwatch.MetricOptions(account=account, color=color, dimensions=dimensions, label=label, period=period, region=region, statistic=statistic, unit=unit)

        return jsii.invoke(self, "metricSucceeded", [props])

    @jsii.member(jsii_name="metricTime")
    def metric_time(self, *, account: typing.Optional[str]=None, color: typing.Optional[str]=None, dimensions: typing.Optional[typing.Mapping[str, typing.Any]]=None, label: typing.Optional[str]=None, period: typing.Optional[aws_cdk.core.Duration]=None, region: typing.Optional[str]=None, statistic: typing.Optional[str]=None, unit: typing.Optional[aws_cdk.aws_cloudwatch.Unit]=None) -> aws_cdk.aws_cloudwatch.Metric:
        """The interval, in milliseconds, between the time the activity is scheduled and the time it closes.

        :param account: Account which this metric comes from. Default: - Deployment account.
        :param color: The hex color code, prefixed with '#' (e.g. '#00ff00'), to use when this metric is rendered on a graph. The ``Color`` class has a set of standard colors that can be used here. Default: - Automatic color
        :param dimensions: Dimensions of the metric. Default: - No dimensions.
        :param label: Label for this metric when added to a Graph in a Dashboard. Default: - No label
        :param period: The period over which the specified statistic is applied. Default: Duration.minutes(5)
        :param region: Region which this metric comes from. Default: - Deployment region.
        :param statistic: What function to use for aggregating. Can be one of the following: - "Minimum" | "min" - "Maximum" | "max" - "Average" | "avg" - "Sum" | "sum" - "SampleCount | "n" - "pNN.NN" Default: Average
        :param unit: Unit used to filter the metric stream. Only refer to datums emitted to the metric stream with the given unit and ignore all others. Only useful when datums are being emitted to the same metric stream under different units. The default is to use all matric datums in the stream, regardless of unit, which is recommended in nearly all cases. CloudWatch does not honor this property for graphs. Default: - All metric datums in the given metric stream

        default
        :default: average over 5 minutes

        stability
        :stability: experimental
        """
        props = aws_cdk.aws_cloudwatch.MetricOptions(account=account, color=color, dimensions=dimensions, label=label, period=period, region=region, statistic=statistic, unit=unit)

        return jsii.invoke(self, "metricTime", [props])

    @jsii.member(jsii_name="metricTimedOut")
    def metric_timed_out(self, *, account: typing.Optional[str]=None, color: typing.Optional[str]=None, dimensions: typing.Optional[typing.Mapping[str, typing.Any]]=None, label: typing.Optional[str]=None, period: typing.Optional[aws_cdk.core.Duration]=None, region: typing.Optional[str]=None, statistic: typing.Optional[str]=None, unit: typing.Optional[aws_cdk.aws_cloudwatch.Unit]=None) -> aws_cdk.aws_cloudwatch.Metric:
        """Metric for the number of times this activity times out.

        :param account: Account which this metric comes from. Default: - Deployment account.
        :param color: The hex color code, prefixed with '#' (e.g. '#00ff00'), to use when this metric is rendered on a graph. The ``Color`` class has a set of standard colors that can be used here. Default: - Automatic color
        :param dimensions: Dimensions of the metric. Default: - No dimensions.
        :param label: Label for this metric when added to a Graph in a Dashboard. Default: - No label
        :param period: The period over which the specified statistic is applied. Default: Duration.minutes(5)
        :param region: Region which this metric comes from. Default: - Deployment region.
        :param statistic: What function to use for aggregating. Can be one of the following: - "Minimum" | "min" - "Maximum" | "max" - "Average" | "avg" - "Sum" | "sum" - "SampleCount | "n" - "pNN.NN" Default: Average
        :param unit: Unit used to filter the metric stream. Only refer to datums emitted to the metric stream with the given unit and ignore all others. Only useful when datums are being emitted to the same metric stream under different units. The default is to use all matric datums in the stream, regardless of unit, which is recommended in nearly all cases. CloudWatch does not honor this property for graphs. Default: - All metric datums in the given metric stream

        default
        :default: sum over 5 minutes

        stability
        :stability: experimental
        """
        props = aws_cdk.aws_cloudwatch.MetricOptions(account=account, color=color, dimensions=dimensions, label=label, period=period, region=region, statistic=statistic, unit=unit)

        return jsii.invoke(self, "metricTimedOut", [props])

    @builtins.property
    @jsii.member(jsii_name="activityArn")
    def activity_arn(self) -> str:
        """The ARN of the activity.

        stability
        :stability: experimental
        attribute:
        :attribute:: true
        """
        return jsii.get(self, "activityArn")

    @builtins.property
    @jsii.member(jsii_name="activityName")
    def activity_name(self) -> str:
        """The name of the activity.

        stability
        :stability: experimental
        attribute:
        :attribute:: true
        """
        return jsii.get(self, "activityName")


@jsii.implements(IChainable)
class Chain(metaclass=jsii.JSIIMeta, jsii_type="@aws-cdk/aws-stepfunctions.Chain"):
    """A collection of states to chain onto.

    A Chain has a start and zero or more chainable ends. If there are
    zero ends, calling next() on the Chain will fail.

    stability
    :stability: experimental
    """
    @jsii.member(jsii_name="custom")
    @builtins.classmethod
    def custom(cls, start_state: "State", end_states: typing.List["INextable"], last_added: "IChainable") -> "Chain":
        """Make a Chain with specific start and end states, and a last-added Chainable.

        :param start_state: -
        :param end_states: -
        :param last_added: -

        stability
        :stability: experimental
        """
        return jsii.sinvoke(cls, "custom", [start_state, end_states, last_added])

    @jsii.member(jsii_name="sequence")
    @builtins.classmethod
    def sequence(cls, start: "IChainable", next: "IChainable") -> "Chain":
        """Make a Chain with the start from one chain and the ends from another.

        :param start: -
        :param next: -

        stability
        :stability: experimental
        """
        return jsii.sinvoke(cls, "sequence", [start, next])

    @jsii.member(jsii_name="start")
    @builtins.classmethod
    def start(cls, state: "IChainable") -> "Chain":
        """Begin a new Chain from one chainable.

        :param state: -

        stability
        :stability: experimental
        """
        return jsii.sinvoke(cls, "start", [state])

    @jsii.member(jsii_name="next")
    def next(self, next: "IChainable") -> "Chain":
        """Continue normal execution with the given state.

        :param next: -

        stability
        :stability: experimental
        """
        return jsii.invoke(self, "next", [next])

    @jsii.member(jsii_name="toSingleState")
    def to_single_state(self, id: str, *, comment: typing.Optional[str]=None, input_path: typing.Optional[str]=None, output_path: typing.Optional[str]=None, result_path: typing.Optional[str]=None) -> "Parallel":
        """Return a single state that encompasses all states in the chain.

        This can be used to add error handling to a sequence of states.

        Be aware that this changes the result of the inner state machine
        to be an array with the result of the state machine in it. Adjust
        your paths accordingly. For example, change 'outputPath' to
        '$[0]'.

        :param id: -
        :param comment: An optional description for this state. Default: No comment
        :param input_path: JSONPath expression to select part of the state to be the input to this state. May also be the special value DISCARD, which will cause the effective input to be the empty object {}. Default: $
        :param output_path: JSONPath expression to select part of the state to be the output to this state. May also be the special value DISCARD, which will cause the effective output to be the empty object {}. Default: $
        :param result_path: JSONPath expression to indicate where to inject the state's output. May also be the special value DISCARD, which will cause the state's input to become its output. Default: $

        stability
        :stability: experimental
        """
        props = ParallelProps(comment=comment, input_path=input_path, output_path=output_path, result_path=result_path)

        return jsii.invoke(self, "toSingleState", [id, props])

    @builtins.property
    @jsii.member(jsii_name="endStates")
    def end_states(self) -> typing.List["INextable"]:
        """The chainable end state(s) of this chain.

        stability
        :stability: experimental
        """
        return jsii.get(self, "endStates")

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> str:
        """Identify this Chain.

        stability
        :stability: experimental
        """
        return jsii.get(self, "id")

    @builtins.property
    @jsii.member(jsii_name="startState")
    def start_state(self) -> "State":
        """The start state of this chain.

        stability
        :stability: experimental
        """
        return jsii.get(self, "startState")


class Choice(State, metaclass=jsii.JSIIMeta, jsii_type="@aws-cdk/aws-stepfunctions.Choice"):
    """Define a Choice in the state machine.

    A choice state can be used to make decisions based on the execution
    state.

    stability
    :stability: experimental
    """
    def __init__(self, scope: aws_cdk.core.Construct, id: str, *, comment: typing.Optional[str]=None, input_path: typing.Optional[str]=None, output_path: typing.Optional[str]=None) -> None:
        """
        :param scope: -
        :param id: -
        :param comment: An optional description for this state. Default: No comment
        :param input_path: JSONPath expression to select part of the state to be the input to this state. May also be the special value DISCARD, which will cause the effective input to be the empty object {}. Default: $
        :param output_path: JSONPath expression to select part of the state to be the output to this state. May also be the special value DISCARD, which will cause the effective output to be the empty object {}. Default: $

        stability
        :stability: experimental
        """
        props = ChoiceProps(comment=comment, input_path=input_path, output_path=output_path)

        jsii.create(Choice, self, [scope, id, props])

    @jsii.member(jsii_name="afterwards")
    def afterwards(self, *, include_error_handlers: typing.Optional[bool]=None, include_otherwise: typing.Optional[bool]=None) -> "Chain":
        """Return a Chain that contains all reachable end states from this Choice.

        Use this to combine all possible choice paths back.

        :param include_error_handlers: Whether to include error handling states. If this is true, all states which are error handlers (added through 'onError') and states reachable via error handlers will be included as well. Default: false
        :param include_otherwise: Whether to include the default/otherwise transition for the current Choice state. If this is true and the current Choice does not have a default outgoing transition, one will be added included when .next() is called on the chain. Default: false

        stability
        :stability: experimental
        """
        options = AfterwardsOptions(include_error_handlers=include_error_handlers, include_otherwise=include_otherwise)

        return jsii.invoke(self, "afterwards", [options])

    @jsii.member(jsii_name="otherwise")
    def otherwise(self, def_: "IChainable") -> "Choice":
        """If none of the given conditions match, continue execution with the given state.

        If no conditions match and no otherwise() has been given, an execution
        error will be raised.

        :param def_: -

        stability
        :stability: experimental
        """
        return jsii.invoke(self, "otherwise", [def_])

    @jsii.member(jsii_name="toStateJson")
    def to_state_json(self) -> typing.Mapping[typing.Any, typing.Any]:
        """Return the Amazon States Language object for this state.

        stability
        :stability: experimental
        """
        return jsii.invoke(self, "toStateJson", [])

    @jsii.member(jsii_name="when")
    def when(self, condition: "Condition", next: "IChainable") -> "Choice":
        """If the given condition matches, continue execution with the given state.

        :param condition: -
        :param next: -

        stability
        :stability: experimental
        """
        return jsii.invoke(self, "when", [condition, next])

    @builtins.property
    @jsii.member(jsii_name="endStates")
    def end_states(self) -> typing.List["INextable"]:
        """Continuable states of this Chainable.

        stability
        :stability: experimental
        """
        return jsii.get(self, "endStates")


@jsii.implements(IChainable, INextable)
class CustomState(State, metaclass=jsii.JSIIMeta, jsii_type="@aws-cdk/aws-stepfunctions.CustomState"):
    """State defined by supplying Amazon States Language (ASL) in the state machine.

    stability
    :stability: experimental
    """
    def __init__(self, scope: aws_cdk.core.Construct, id: str, *, state_json: typing.Mapping[str, typing.Any]) -> None:
        """
        :param scope: -
        :param id: -
        :param state_json: Amazon States Language (JSON-based) definition of the state.

        stability
        :stability: experimental
        """
        props = CustomStateProps(state_json=state_json)

        jsii.create(CustomState, self, [scope, id, props])

    @jsii.member(jsii_name="next")
    def next(self, next: "IChainable") -> "Chain":
        """Continue normal execution with the given state.

        :param next: -

        stability
        :stability: experimental
        """
        return jsii.invoke(self, "next", [next])

    @jsii.member(jsii_name="toStateJson")
    def to_state_json(self) -> typing.Mapping[typing.Any, typing.Any]:
        """Returns the Amazon States Language object for this state.

        stability
        :stability: experimental
        """
        return jsii.invoke(self, "toStateJson", [])

    @builtins.property
    @jsii.member(jsii_name="endStates")
    def end_states(self) -> typing.List["INextable"]:
        """Continuable states of this Chainable.

        stability
        :stability: experimental
        """
        return jsii.get(self, "endStates")


class Fail(State, metaclass=jsii.JSIIMeta, jsii_type="@aws-cdk/aws-stepfunctions.Fail"):
    """Define a Fail state in the state machine.

    Reaching a Fail state terminates the state execution in failure.

    stability
    :stability: experimental
    """
    def __init__(self, scope: aws_cdk.core.Construct, id: str, *, cause: typing.Optional[str]=None, comment: typing.Optional[str]=None, error: typing.Optional[str]=None) -> None:
        """
        :param scope: -
        :param id: -
        :param cause: A description for the cause of the failure. Default: No description
        :param comment: An optional description for this state. Default: No comment
        :param error: Error code used to represent this failure. Default: No error code

        stability
        :stability: experimental
        """
        props = FailProps(cause=cause, comment=comment, error=error)

        jsii.create(Fail, self, [scope, id, props])

    @jsii.member(jsii_name="toStateJson")
    def to_state_json(self) -> typing.Mapping[typing.Any, typing.Any]:
        """Return the Amazon States Language object for this state.

        stability
        :stability: experimental
        """
        return jsii.invoke(self, "toStateJson", [])

    @builtins.property
    @jsii.member(jsii_name="endStates")
    def end_states(self) -> typing.List["INextable"]:
        """Continuable states of this Chainable.

        stability
        :stability: experimental
        """
        return jsii.get(self, "endStates")


@jsii.implements(INextable)
class Map(State, metaclass=jsii.JSIIMeta, jsii_type="@aws-cdk/aws-stepfunctions.Map"):
    """Define a Map state in the state machine.

    A ``Map`` state can be used to run a set of steps for each element of an input array.
    A Map state will execute the same steps for multiple entries of an array in the state input.

    While the Parallel state executes multiple branches of steps using the same input, a Map state
    will execute the same steps for multiple entries of an array in the state input.

    see
    :see: https://docs.aws.amazon.com/step-functions/latest/dg/amazon-states-language-map-state.html
    stability
    :stability: experimental
    """
    def __init__(self, scope: aws_cdk.core.Construct, id: str, *, comment: typing.Optional[str]=None, input_path: typing.Optional[str]=None, items_path: typing.Optional[str]=None, max_concurrency: typing.Optional[jsii.Number]=None, output_path: typing.Optional[str]=None, parameters: typing.Optional[typing.Mapping[str, typing.Any]]=None, result_path: typing.Optional[str]=None) -> None:
        """
        :param scope: -
        :param id: -
        :param comment: An optional description for this state. Default: No comment
        :param input_path: JSONPath expression to select part of the state to be the input to this state. May also be the special value DISCARD, which will cause the effective input to be the empty object {}. Default: $
        :param items_path: JSONPath expression to select the array to iterate over. Default: $
        :param max_concurrency: MaxConcurrency. An upper bound on the number of iterations you want running at once. Default: - full concurrency
        :param output_path: JSONPath expression to select part of the state to be the output to this state. May also be the special value DISCARD, which will cause the effective output to be the empty object {}. Default: $
        :param parameters: The JSON that you want to override your default iteration input. Default: $
        :param result_path: JSONPath expression to indicate where to inject the state's output. May also be the special value DISCARD, which will cause the state's input to become its output. Default: $

        stability
        :stability: experimental
        """
        props = MapProps(comment=comment, input_path=input_path, items_path=items_path, max_concurrency=max_concurrency, output_path=output_path, parameters=parameters, result_path=result_path)

        jsii.create(Map, self, [scope, id, props])

    @jsii.member(jsii_name="addCatch")
    def add_catch(self, handler: "IChainable", *, errors: typing.Optional[typing.List[str]]=None, result_path: typing.Optional[str]=None) -> "Map":
        """Add a recovery handler for this state.

        When a particular error occurs, execution will continue at the error
        handler instead of failing the state machine execution.

        :param handler: -
        :param errors: Errors to recover from by going to the given state. A list of error strings to retry, which can be either predefined errors (for example Errors.NoChoiceMatched) or a self-defined error. Default: All errors
        :param result_path: JSONPath expression to indicate where to inject the error data. May also be the special value DISCARD, which will cause the error data to be discarded. Default: $

        stability
        :stability: experimental
        """
        props = CatchProps(errors=errors, result_path=result_path)

        return jsii.invoke(self, "addCatch", [handler, props])

    @jsii.member(jsii_name="addRetry")
    def add_retry(self, *, backoff_rate: typing.Optional[jsii.Number]=None, errors: typing.Optional[typing.List[str]]=None, interval: typing.Optional[aws_cdk.core.Duration]=None, max_attempts: typing.Optional[jsii.Number]=None) -> "Map":
        """Add retry configuration for this state.

        This controls if and how the execution will be retried if a particular
        error occurs.

        :param backoff_rate: Multiplication for how much longer the wait interval gets on every retry. Default: 2
        :param errors: Errors to retry. A list of error strings to retry, which can be either predefined errors (for example Errors.NoChoiceMatched) or a self-defined error. Default: All errors
        :param interval: How many seconds to wait initially before retrying. Default: Duration.seconds(1)
        :param max_attempts: How many times to retry this particular error. May be 0 to disable retry for specific errors (in case you have a catch-all retry policy). Default: 3

        stability
        :stability: experimental
        """
        props = RetryProps(backoff_rate=backoff_rate, errors=errors, interval=interval, max_attempts=max_attempts)

        return jsii.invoke(self, "addRetry", [props])

    @jsii.member(jsii_name="iterator")
    def iterator(self, iterator: "IChainable") -> "Map":
        """Define iterator state machine in Map.

        :param iterator: -

        stability
        :stability: experimental
        """
        return jsii.invoke(self, "iterator", [iterator])

    @jsii.member(jsii_name="next")
    def next(self, next: "IChainable") -> "Chain":
        """Continue normal execution with the given state.

        :param next: -

        stability
        :stability: experimental
        """
        return jsii.invoke(self, "next", [next])

    @jsii.member(jsii_name="toStateJson")
    def to_state_json(self) -> typing.Mapping[typing.Any, typing.Any]:
        """Return the Amazon States Language object for this state.

        stability
        :stability: experimental
        """
        return jsii.invoke(self, "toStateJson", [])

    @jsii.member(jsii_name="validate")
    def _validate(self) -> typing.List[str]:
        """Validate this state.

        stability
        :stability: experimental
        """
        return jsii.invoke(self, "validate", [])

    @builtins.property
    @jsii.member(jsii_name="endStates")
    def end_states(self) -> typing.List["INextable"]:
        """Continuable states of this Chainable.

        stability
        :stability: experimental
        """
        return jsii.get(self, "endStates")


@jsii.implements(INextable)
class Parallel(State, metaclass=jsii.JSIIMeta, jsii_type="@aws-cdk/aws-stepfunctions.Parallel"):
    """Define a Parallel state in the state machine.

    A Parallel state can be used to run one or more state machines at the same
    time.

    The Result of a Parallel state is an array of the results of its substatemachines.

    stability
    :stability: experimental
    """
    def __init__(self, scope: aws_cdk.core.Construct, id: str, *, comment: typing.Optional[str]=None, input_path: typing.Optional[str]=None, output_path: typing.Optional[str]=None, result_path: typing.Optional[str]=None) -> None:
        """
        :param scope: -
        :param id: -
        :param comment: An optional description for this state. Default: No comment
        :param input_path: JSONPath expression to select part of the state to be the input to this state. May also be the special value DISCARD, which will cause the effective input to be the empty object {}. Default: $
        :param output_path: JSONPath expression to select part of the state to be the output to this state. May also be the special value DISCARD, which will cause the effective output to be the empty object {}. Default: $
        :param result_path: JSONPath expression to indicate where to inject the state's output. May also be the special value DISCARD, which will cause the state's input to become its output. Default: $

        stability
        :stability: experimental
        """
        props = ParallelProps(comment=comment, input_path=input_path, output_path=output_path, result_path=result_path)

        jsii.create(Parallel, self, [scope, id, props])

    @jsii.member(jsii_name="addCatch")
    def add_catch(self, handler: "IChainable", *, errors: typing.Optional[typing.List[str]]=None, result_path: typing.Optional[str]=None) -> "Parallel":
        """Add a recovery handler for this state.

        When a particular error occurs, execution will continue at the error
        handler instead of failing the state machine execution.

        :param handler: -
        :param errors: Errors to recover from by going to the given state. A list of error strings to retry, which can be either predefined errors (for example Errors.NoChoiceMatched) or a self-defined error. Default: All errors
        :param result_path: JSONPath expression to indicate where to inject the error data. May also be the special value DISCARD, which will cause the error data to be discarded. Default: $

        stability
        :stability: experimental
        """
        props = CatchProps(errors=errors, result_path=result_path)

        return jsii.invoke(self, "addCatch", [handler, props])

    @jsii.member(jsii_name="addRetry")
    def add_retry(self, *, backoff_rate: typing.Optional[jsii.Number]=None, errors: typing.Optional[typing.List[str]]=None, interval: typing.Optional[aws_cdk.core.Duration]=None, max_attempts: typing.Optional[jsii.Number]=None) -> "Parallel":
        """Add retry configuration for this state.

        This controls if and how the execution will be retried if a particular
        error occurs.

        :param backoff_rate: Multiplication for how much longer the wait interval gets on every retry. Default: 2
        :param errors: Errors to retry. A list of error strings to retry, which can be either predefined errors (for example Errors.NoChoiceMatched) or a self-defined error. Default: All errors
        :param interval: How many seconds to wait initially before retrying. Default: Duration.seconds(1)
        :param max_attempts: How many times to retry this particular error. May be 0 to disable retry for specific errors (in case you have a catch-all retry policy). Default: 3

        stability
        :stability: experimental
        """
        props = RetryProps(backoff_rate=backoff_rate, errors=errors, interval=interval, max_attempts=max_attempts)

        return jsii.invoke(self, "addRetry", [props])

    @jsii.member(jsii_name="branch")
    def branch(self, *branches: "IChainable") -> "Parallel":
        """Define one or more branches to run in parallel.

        :param branches: -

        stability
        :stability: experimental
        """
        return jsii.invoke(self, "branch", [*branches])

    @jsii.member(jsii_name="next")
    def next(self, next: "IChainable") -> "Chain":
        """Continue normal execution with the given state.

        :param next: -

        stability
        :stability: experimental
        """
        return jsii.invoke(self, "next", [next])

    @jsii.member(jsii_name="toStateJson")
    def to_state_json(self) -> typing.Mapping[typing.Any, typing.Any]:
        """Return the Amazon States Language object for this state.

        stability
        :stability: experimental
        """
        return jsii.invoke(self, "toStateJson", [])

    @jsii.member(jsii_name="validate")
    def _validate(self) -> typing.List[str]:
        """Validate this state.

        stability
        :stability: experimental
        """
        return jsii.invoke(self, "validate", [])

    @builtins.property
    @jsii.member(jsii_name="endStates")
    def end_states(self) -> typing.List["INextable"]:
        """Continuable states of this Chainable.

        stability
        :stability: experimental
        """
        return jsii.get(self, "endStates")


@jsii.implements(INextable)
class Pass(State, metaclass=jsii.JSIIMeta, jsii_type="@aws-cdk/aws-stepfunctions.Pass"):
    """Define a Pass in the state machine.

    A Pass state can be used to transform the current exeuction's state.

    stability
    :stability: experimental
    """
    def __init__(self, scope: aws_cdk.core.Construct, id: str, *, comment: typing.Optional[str]=None, input_path: typing.Optional[str]=None, output_path: typing.Optional[str]=None, parameters: typing.Optional[typing.Mapping[str, typing.Any]]=None, result: typing.Optional["Result"]=None, result_path: typing.Optional[str]=None) -> None:
        """
        :param scope: -
        :param id: -
        :param comment: An optional description for this state. Default: No comment
        :param input_path: JSONPath expression to select part of the state to be the input to this state. May also be the special value DISCARD, which will cause the effective input to be the empty object {}. Default: $
        :param output_path: JSONPath expression to select part of the state to be the output to this state. May also be the special value DISCARD, which will cause the effective output to be the empty object {}. Default: $
        :param parameters: Parameters pass a collection of key-value pairs, either static values or JSONPath expressions that select from the input. Default: No parameters
        :param result: If given, treat as the result of this operation. Can be used to inject or replace the current execution state. Default: No injected result
        :param result_path: JSONPath expression to indicate where to inject the state's output. May also be the special value DISCARD, which will cause the state's input to become its output. Default: $

        stability
        :stability: experimental
        """
        props = PassProps(comment=comment, input_path=input_path, output_path=output_path, parameters=parameters, result=result, result_path=result_path)

        jsii.create(Pass, self, [scope, id, props])

    @jsii.member(jsii_name="next")
    def next(self, next: "IChainable") -> "Chain":
        """Continue normal execution with the given state.

        :param next: -

        stability
        :stability: experimental
        """
        return jsii.invoke(self, "next", [next])

    @jsii.member(jsii_name="toStateJson")
    def to_state_json(self) -> typing.Mapping[typing.Any, typing.Any]:
        """Return the Amazon States Language object for this state.

        stability
        :stability: experimental
        """
        return jsii.invoke(self, "toStateJson", [])

    @builtins.property
    @jsii.member(jsii_name="endStates")
    def end_states(self) -> typing.List["INextable"]:
        """Continuable states of this Chainable.

        stability
        :stability: experimental
        """
        return jsii.get(self, "endStates")


__all__ = [
    "Activity",
    "ActivityProps",
    "AfterwardsOptions",
    "CatchProps",
    "CfnActivity",
    "CfnActivityProps",
    "CfnStateMachine",
    "CfnStateMachineProps",
    "Chain",
    "Choice",
    "ChoiceProps",
    "Condition",
    "Context",
    "CustomState",
    "CustomStateProps",
    "Data",
    "Errors",
    "Fail",
    "FailProps",
    "FieldUtils",
    "FindStateOptions",
    "IActivity",
    "IChainable",
    "INextable",
    "IStateMachine",
    "IStepFunctionsTask",
    "InputType",
    "LogLevel",
    "LogOptions",
    "Map",
    "MapProps",
    "Parallel",
    "ParallelProps",
    "Pass",
    "PassProps",
    "Result",
    "RetryProps",
    "ServiceIntegrationPattern",
    "SingleStateOptions",
    "State",
    "StateGraph",
    "StateMachine",
    "StateMachineFragment",
    "StateMachineProps",
    "StateMachineType",
    "StateProps",
    "StateTransitionMetric",
    "StepFunctionsTaskConfig",
    "Succeed",
    "SucceedProps",
    "Task",
    "TaskInput",
    "TaskProps",
    "Wait",
    "WaitProps",
    "WaitTime",
]

publication.publish()

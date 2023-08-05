"""
# CDK Lambda Power Tuner

This is simply a CDK wrapper for the SAM/SAR application - [aws-lambda-power-tuning](https://github.com/alexcasalboni/aws-lambda-power-tuning)

> Note this is an alpha module, it needs thoroughly tested before being production recommended

All of the lambda logic is cloned on build from that source repo with only the stepfunction definition being defined in this project.

This enables you to now do this:

![snippet](https://raw.githubusercontent.com/nideveloper/cdk-lambda-powertuner/master/img/snippet.png)

## Deploying the state machine

Import it into any CDK stack and then `cdk deploy`

## Running The Tuner

This is the same as [here](https://github.com/alexcasalboni/aws-lambda-power-tuning#how-to-execute-the-state-machine-web-console)

## Differences from [aws-lambda-power-tuning](https://github.com/alexcasalboni/aws-lambda-power-tuning)

Since this uses AWS CDK to build and deploy the step function, we need to play by the rules of CDK.

The method of integrating Lambda functions as a step into your workflow via ARN has been deprecated by the team.
They have chosen to support integrating via function name. For reference see [issue](https://github.com/aws/aws-cdk/issues/7709)

This means that the payloads coming back from the Lambda functions contain an extra abstraction layer of data not present in the SAR application.

To make this work without rewriting the Lambda functions so that I can always pull the latest code on every build I
had to introduce adapters between the step function Lambda tasks to strip out this abstraction layer. This is their only purpose

![stepfunction flow](https://raw.githubusercontent.com/nideveloper/cdk-lambda-powertuner/master/img/stepfunctions_graph.png)
"""
import abc
import builtins
import datetime
import enum
import typing

import jsii
import jsii.compat
import publication

import aws_cdk.aws_iam
import aws_cdk.aws_lambda
import aws_cdk.aws_stepfunctions
import aws_cdk.aws_stepfunctions_tasks
import aws_cdk.core
import constructs

from ._jsii import *


class LambdaPowerTuner(aws_cdk.core.Construct, metaclass=jsii.JSIIMeta, jsii_type="cdk-lambda-powertuner.LambdaPowerTuner"):
    """
    stability
    :stability: experimental
    """
    def __init__(self, scope: aws_cdk.core.Construct, id: str, *, lambda_resource: str, power_values: typing.Optional[typing.List[jsii.Number]]=None, visualization_url: typing.Optional[str]=None) -> None:
        """
        :param scope: -
        :param id: -
        :param lambda_resource: 
        :param power_values: 
        :param visualization_url: 

        stability
        :stability: experimental
        """
        config = LambdaPowerTunerConfig(lambda_resource=lambda_resource, power_values=power_values, visualization_url=visualization_url)

        jsii.create(LambdaPowerTuner, self, [scope, id, config])

    @jsii.member(jsii_name="createLambda")
    def create_lambda(self, scope: aws_cdk.core.Construct, id: str, handler: str, env: typing.Any, timeout: typing.Optional[jsii.Number]=None) -> aws_cdk.aws_lambda.Function:
        """All the lambdas have the same config, so this method saves typing.

        :param scope: -
        :param id: -
        :param handler: -
        :param env: -
        :param timeout: -

        stability
        :stability: experimental
        """
        return jsii.invoke(self, "createLambda", [scope, id, handler, env, timeout])


@jsii.data_type(jsii_type="cdk-lambda-powertuner.LambdaPowerTunerConfig", jsii_struct_bases=[], name_mapping={'lambda_resource': 'lambdaResource', 'power_values': 'powerValues', 'visualization_url': 'visualizationURL'})
class LambdaPowerTunerConfig():
    def __init__(self, *, lambda_resource: str, power_values: typing.Optional[typing.List[jsii.Number]]=None, visualization_url: typing.Optional[str]=None) -> None:
        """
        :param lambda_resource: 
        :param power_values: 
        :param visualization_url: 

        stability
        :stability: experimental
        """
        self._values = {
            'lambda_resource': lambda_resource,
        }
        if power_values is not None: self._values["power_values"] = power_values
        if visualization_url is not None: self._values["visualization_url"] = visualization_url

    @builtins.property
    def lambda_resource(self) -> str:
        """
        stability
        :stability: experimental
        """
        return self._values.get('lambda_resource')

    @builtins.property
    def power_values(self) -> typing.Optional[typing.List[jsii.Number]]:
        """
        stability
        :stability: experimental
        """
        return self._values.get('power_values')

    @builtins.property
    def visualization_url(self) -> typing.Optional[str]:
        """
        stability
        :stability: experimental
        """
        return self._values.get('visualization_url')

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return 'LambdaPowerTunerConfig(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


__all__ = [
    "LambdaPowerTuner",
    "LambdaPowerTunerConfig",
]

publication.publish()

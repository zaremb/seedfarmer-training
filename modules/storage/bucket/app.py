#!/usr/bin/env python3
import os

import aws_cdk as cdk
from aws_cdk import CfnOutput
from stack import Stack

deployment_name = os.getenv("TRAINING_DEPLOYMENT_NAME", "")
module_name = os.getenv("TRAINING_MODULE_NAME", "")

environment = cdk.Environment(
    account=os.environ["CDK_DEFAULT_ACCOUNT"],
    region=os.environ["CDK_DEFAULT_REGION"],
)

app = cdk.App()
stack = Stack(
    scope=app,
    id=f"training-{deployment_name}-{module_name}",
    deployment_name=deployment_name,
    module_name=module_name,
    env=environment,
)

CfnOutput(
    scope=stack,
    id="metadata",
    value=stack.to_json_string({"bucket": stack.bucket.bucket_name}),
)

app.synth()

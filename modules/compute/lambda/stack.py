import os

import cdk_nag
from aws_cdk import Aspects, Aws, Stack
from aws_cdk import aws_lambda as _lambda
from aws_cdk import aws_s3 as s3
from constructs import Construct


class Stack(Stack):
    def __init__(
        self,
        scope: Construct,
        id: str,
        deployment_name: str,
        module_name: str,
        bucket_name: str,
        **kwargs,
    ) -> None:
        super().__init__(
            scope,
            id,
            description=f"Lambda {deployment_name=} {module_name=}",
            **kwargs,
        )
        bucket = s3.Bucket.from_bucket_name(self, "Bucket", bucket_name)
        lambda_src_code_path = os.path.join(os.path.dirname(__file__), "lambda-handler")
        self.lambda_function = _lambda.Function(
            self,
            "Function",
            runtime=_lambda.Runtime.PYTHON_3_10,
            handler="handler.lambda_handler",
            code=_lambda.Code.from_asset(lambda_src_code_path),
            environment={
                "BUCKET_NAME": bucket_name,
            },
            layers=[
                _lambda.LayerVersion.from_layer_version_arn(
                    self,
                    "powertools-layer",
                    # Official AWS powertools layer per https://awslabs.github.io/aws-lambda-powertools-python/2.10.0/
                    f"arn:aws:lambda:{Aws.REGION}:017000801446:layer:AWSLambdaPowertoolsPythonV2:24",
                )
            ],
        )
        bucket.grant_read(self.lambda_function)
        cdk_nag.NagSuppressions.add_resource_suppressions(
            self.lambda_function.role,
            [
                cdk_nag.NagPackSuppression(
                    id="AwsSolutions-IAM4",
                    reason="Lambda basic execution role allowing for cloudwatch logs",
                ),
            ],
        )
        cdk_nag.NagSuppressions.add_stack_suppressions(
            self,
            [
                cdk_nag.NagPackSuppression(
                    id="AwsSolutions-IAM5",
                    reason="This role has tailored policy to read S3 bucket, which"
                    "includes wildcards after GetBucket, GetObject, and List",
                ),
            ],
        )

        Aspects.of(self).add(cdk_nag.AwsSolutionsChecks())

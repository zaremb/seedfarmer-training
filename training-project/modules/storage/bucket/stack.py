import cdk_nag
from aws_cdk import Aspects, RemovalPolicy, Stack
from aws_cdk import aws_s3 as s3
from constructs import Construct


class Stack(Stack):
    def __init__(
        self,
        scope: Construct,
        id: str,
        deployment_name: str,
        module_name: str,
        **kwargs,
    ) -> None:
        super().__init__(
            scope,
            id,
            description=f"S3 bucket {deployment_name=} {module_name=}",
            **kwargs,
        )
        # Create S3 bucket
        self.bucket = s3.Bucket(
            self,
            "bucket",
            server_access_logs_prefix="logs",
            encryption=s3.BucketEncryption.S3_MANAGED,
            enforce_ssl=True,
            versioned=True,
            removal_policy=RemovalPolicy.RETAIN,
            block_public_access=s3.BlockPublicAccess.BLOCK_ALL,
        )
        Aspects.of(self).add(cdk_nag.AwsSolutionsChecks())

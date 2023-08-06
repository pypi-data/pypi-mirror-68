## AWS CloudTrail Construct Library

<!--BEGIN STABILITY BANNER-->---


![cfn-resources: Stable](https://img.shields.io/badge/cfn--resources-stable-success.svg?style=for-the-badge)

> All classes with the `Cfn` prefix in this module ([CFN Resources](https://docs.aws.amazon.com/cdk/latest/guide/constructs.html#constructs_lib)) are always stable and safe to use.

![cdk-constructs: Experimental](https://img.shields.io/badge/cdk--constructs-experimental-important.svg?style=for-the-badge)

> The APIs of higher level constructs in this module are experimental and under active development. They are subject to non-backward compatible changes or removal in any future version. These are not subject to the [Semantic Versioning](https://semver.org/) model and breaking changes will be announced in the release notes. This means that while you may use them, you may need to update your source code when upgrading to a newer version of this package.

---
<!--END STABILITY BANNER-->

Add a CloudTrail construct - for ease of setting up CloudTrail logging in your account

Example usage:

```python
# Example automatically generated without compilation. See https://github.com/aws/jsii/issues/826
import aws_cdk.aws_cloudtrail as cloudtrail

trail = cloudtrail.Trail(self, "CloudTrail")
```

You can instantiate the CloudTrail construct with no arguments - this will by default:

* Create a new S3 Bucket and associated Policy that allows CloudTrail to write to it
* Create a CloudTrail with the following configuration:

  * Logging Enabled
  * Log file validation enabled
  * Multi Region set to true
  * Global Service Events set to true
  * The created S3 bucket
  * CloudWatch Logging Disabled
  * No SNS configuartion
  * No tags
  * No fixed name

You can override any of these properties using the `CloudTrailProps` configuraiton object.

For example, to log to CloudWatch Logs

```python
# Example automatically generated without compilation. See https://github.com/aws/jsii/issues/826
import aws_cdk.aws_cloudtrail as cloudtrail

trail = cloudtrail.Trail(self, "CloudTrail",
    send_to_cloud_watch_logs=True
)
```

This creates the same setup as above - but also logs events to a created CloudWatch Log stream.
By default, the created log group has a retention period of 365 Days, but this is also configurable.

For using CloudTrail event selector to log specific S3 events,
you can use the `CloudTrailProps` configuration object.
Example:

```python
# Example automatically generated without compilation. See https://github.com/aws/jsii/issues/826
import aws_cdk.aws_cloudtrail as cloudtrail

trail = cloudtrail.Trail(self, "MyAmazingCloudTrail")

# Adds an event selector to the bucket magic-bucket.
# By default, this includes management events and all operations (Read + Write)
trail.add_s3_event_selector(["arn:aws:s3:::magic-bucket/"])

# Adds an event selector to the bucket foo, with a specific configuration
trail.add_s3_event_selector(["arn:aws:s3:::foo/"],
    include_management_events=False,
    read_write_type=ReadWriteType.ALL
)
```

For using CloudTrail event selector to log events about Lambda
functions, you can use `addLambdaEventSelector`.

```python
# Example automatically generated without compilation. See https://github.com/aws/jsii/issues/826
import aws_cdk.aws_cloudtrail as cloudtrail
import aws_cdk.aws_lambda as lambda

trail = cloudtrail.Trail(self, "MyAmazingCloudTrail")
lambda_function = lambda.Function(stack, "AnAmazingFunction",
    runtime=lambda.Runtime.NODEJS_10_X,
    handler="hello.handler",
    code=lambda.Code.from_asset("lambda")
)

# Add an event selector to log data events for all functions in the account.
trail.add_lambda_event_selector(["arn:aws:lambda"])

# Add an event selector to log data events for the provided Lambda functions.
trail.add_lambda_event_selector([lambda_function.function_arn])
```

# CDK Apex Cname - Route53

A CDK utility construct to allowing setting an domain apex (in Route53) to resolve to a cname record of a resource
not in Route 53.

## Usage

### Typescript

First install the package

```
npm install cdk-apex-cname
```

Then you can use the Apex CNAME in your code:

```python
# Example automatically generated without compilation. See https://github.com/aws/jsii/issues/826
from cdk_apex_cname import CdkApexCname

CdkApexCname(self, "CdkApexCname",
    apex_name="apex.com",
    record_name="cname.example.com",
    hosted_zone_id="ZONE1234",
    apex_cname_rule_cron="cron(0 * ? * * *)"
)
```

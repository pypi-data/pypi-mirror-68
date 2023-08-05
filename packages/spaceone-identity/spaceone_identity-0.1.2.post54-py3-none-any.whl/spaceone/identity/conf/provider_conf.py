DEFAULT_PROVIDERS = [{
    'provider': 'aws',
    'name': 'AWS',
    'template': {
        'service_account': {
            'schema': {
                'type': 'object',
                'properties': {
                    'account_id': {
                        'title': 'Account ID',
                        'type': 'string',
                        'minLength': 4
                    }
                },
                'required': ['account_id']
            }
        }
    },
    'capability': {
        'supported_schema': ['aws_access_key', 'aws_assume_role']
    },
    'tags': {
        'color': '#FF9900',
        'icon': 'https://assets-console-cloudone-stg.s3.ap-northeast-2.amazonaws.com/console-assets/icons/aws.svg',
        'external_link_template': 'https://{{data.account_id}}.signin.aws.amazon.com/console',
        'creation_help': '<h2>Finding Your AWS Account ID</h2>'
                         'You can find your account ID in the AWS Management Console, or using the AWS CLI or AWS API.'
                         '<h3>Finding your account ID (Console)</h3>'
                         'In the navigation bar, choose **Support**, and then **Support Center**. '
                         'Your currently signed-in 12-digit account number (ID) appears in the **Support Center** title bar.'
                         '<h3>Finding your account ID (AWS CLI)</h3>'
                         'To view your user ID, account ID, and your user ARN:'
                         '* [aws sts get-caller-identity](https://docs.aws.amazon.com/IAM/latest/UserGuide/console_account-alias.html)'
                         '<h3>Finding your account ID (AWS API)</h3>'
                         'To view your user ID, account ID, and your user ARN:'
                         '* [GetCallerIdentity](https://docs.aws.amazon.com/STS/latest/APIReference/API_GetCallerIdentity.html)'
                         '<h3>References</h3>'
                         '* [AWS Guide](https://docs.aws.amazon.com/IAM/latest/UserGuide/console_account-alias.html)'''
    }
}, {
    'provider': 'google_cloud',
    'name': 'Google Cloud',
    'template': {
        'service_account': {
            'schema': {
                'type': 'object',
                'properties': {
                    'sa_name': {
                        'title': 'Service Account',
                        'type': 'string',
                        'minLength': 4
                    },
                    'project_id': {
                        'title': 'Project ID',
                        'type': 'string',
                        'minLength': 4
                    }
                },
                'required': ['sa_name', 'project_id']
            }
        }
    },
    'capability': {
        'supported_schema': ['google_api_key', 'google_oauth2.0_client']
    },
    'tags': {
        'color': '#4285F4',
        'icon': 'https://assets-console-cloudone-stg.s3.ap-northeast-2.amazonaws.com/console-assets/icons/google_cloud.svg'
    }
}, {
    'provider': 'azure',
    'name': 'Microsoft Azure',
    'template': {
        'service_account': {
            'schema': {
                'type': 'object',
                'properties': {
                    'tenant_id': {
                        'title': 'Tenant ID',
                        'type': 'string',
                        'minLength': 4
                    },
                    'subscription_id': {
                        'title': 'Subscription ID',
                        'type': 'string',
                        'minLength': 4
                    }
                },
                'required': ['tenant_id', 'subscription_id']
            }
        }
    },
    'capability': {
        'supported_schema': ['azure_client_secret']
    },
    'tags': {
        'color': '#00BCF2',
        'icon': 'https://assets-console-cloudone-stg.s3.ap-northeast-2.amazonaws.com/console-assets/icons/azure.svg'
    }
}]

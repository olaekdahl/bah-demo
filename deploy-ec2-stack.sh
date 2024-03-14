#!/bin/bash

# Replace these variables accordingly
STACK_NAME="script-deploy"
GITHUB_REPO="olaekdahl/bah-demo"

# Deploy stack
aws cloudformation create-stack --stack-name $STACK_NAME --template-body file://ec2_docker.yaml --parameters ParameterKey=ImageId,ParameterValue=ami-0440d3b780d96b29d
# Wait for the stack to be created
aws cloudformation wait stack-create-complete --stack-name $STACK_NAME

# Fetch the public DNS of the EC2 instance from CloudFormation outputs
EC2_DNS_NAME=$(aws cloudformation describe-stacks --stack-name $STACK_NAME --query "Stacks[0].Outputs[?OutputKey=='InstancePublicDNS'].OutputValue" --output text)

if [ -n "$EC2_DNS_NAME" ]; then
    echo "Updating GitHub repository secret EC2_HOST with value: $EC2_DNS_NAME"

    # Update the GitHub secret
    gh secret set EC2_HOST -b"$EC2_DNS_NAME" -r $GITHUB_REPO

    echo "GitHub secret EC2_HOST updated successfully."
else
    echo "Failed to retrieve EC2 instance DNS name from CloudFormation stack outputs."
fi
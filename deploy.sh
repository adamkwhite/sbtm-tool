#!/bin/bash

# SBTM Tool AWS Deployment Script
set -e

# Configuration
AWS_REGION=${AWS_REGION:-us-east-1}
AWS_ACCOUNT_ID=$(aws sts get-caller-identity --query Account --output text)
ECR_REPOSITORY="sbtm-tool"
IMAGE_TAG=${IMAGE_TAG:-latest}

echo "🚀 Starting SBTM Tool deployment to AWS..."
echo "Region: $AWS_REGION"
echo "Account: $AWS_ACCOUNT_ID"

# Step 1: Create ECR repository if it doesn't exist
echo "📦 Setting up ECR repository..."
aws ecr describe-repositories --repository-names $ECR_REPOSITORY --region $AWS_REGION 2>/dev/null || \
aws ecr create-repository --repository-name $ECR_REPOSITORY --region $AWS_REGION

# Step 2: Get ECR login token
echo "🔐 Logging into ECR..."
aws ecr get-login-password --region $AWS_REGION | docker login --username AWS --password-stdin $AWS_ACCOUNT_ID.dkr.ecr.$AWS_REGION.amazonaws.com

# Step 3: Build Docker image
echo "🏗️ Building Docker image..."
docker build -t $ECR_REPOSITORY:$IMAGE_TAG .

# Step 4: Tag and push image
echo "📤 Pushing image to ECR..."
docker tag $ECR_REPOSITORY:$IMAGE_TAG $AWS_ACCOUNT_ID.dkr.ecr.$AWS_REGION.amazonaws.com/$ECR_REPOSITORY:$IMAGE_TAG
docker push $AWS_ACCOUNT_ID.dkr.ecr.$AWS_REGION.amazonaws.com/$ECR_REPOSITORY:$IMAGE_TAG

# Step 5: Deploy CloudFormation stack
echo "☁️ Deploying CloudFormation stack..."
read -s -p "Enter database password: " DB_PASSWORD
echo

aws cloudformation deploy \
  --template-file aws/cloudformation.yaml \
  --stack-name sbtm-tool-stack \
  --parameter-overrides \
    VpcId=$(aws ec2 describe-vpcs --filters "Name=is-default,Values=true" --query "Vpcs[0].VpcId" --output text) \
    SubnetIds=$(aws ec2 describe-subnets --filters "Name=vpc-id,Values=$(aws ec2 describe-vpcs --filters "Name=is-default,Values=true" --query "Vpcs[0].VpcId" --output text)" --query "Subnets[0:2].SubnetId" --output text | tr '\t' ',') \
    DBPassword=$DB_PASSWORD \
  --capabilities CAPABILITY_IAM \
  --region $AWS_REGION

# Step 6: Get deployment info
echo "📋 Getting deployment information..."
LOAD_BALANCER_URL=$(aws cloudformation describe-stacks --stack-name sbtm-tool-stack --query "Stacks[0].Outputs[?OutputKey=='LoadBalancerURL'].OutputValue" --output text --region $AWS_REGION)

echo ""
echo "✅ Deployment completed successfully!"
echo ""
echo "🌐 Application URL: $LOAD_BALANCER_URL"
echo "📊 Health Check: $LOAD_BALANCER_URL/health"
echo ""
echo "⏰ Note: It may take 2-3 minutes for the service to become healthy."
echo ""
echo "🔧 To update the application:"
echo "   1. Make your changes"
echo "   2. Run: ./deploy.sh"
echo ""
echo "🗑️ To cleanup:"
echo "   aws cloudformation delete-stack --stack-name sbtm-tool-stack --region $AWS_REGION"
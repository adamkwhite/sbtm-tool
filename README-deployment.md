# SBTM Tool - AWS Deployment Guide

## Quick Start

Deploy the SBTM tool to AWS with one command:

```bash
./deploy.sh
```

## What Gets Deployed

### Infrastructure (via CloudFormation)
- **ECS Fargate Cluster** - Serverless container hosting
- **Application Load Balancer** - Public access with health checks
- **RDS PostgreSQL** - Managed database (db.t3.micro)
- **ECR Repository** - Container image storage
- **VPC Security Groups** - Network security
- **CloudWatch Logs** - Application logging
- **Secrets Manager** - Secure database credentials

### Estimated Monthly Cost
- **ECS Fargate**: ~$15/month (256 CPU, 512MB RAM)
- **RDS PostgreSQL**: ~$15/month (db.t3.micro)
- **Application Load Balancer**: ~$22/month
- **Total**: ~$52/month for production deployment

## Prerequisites

1. **AWS CLI configured** with appropriate permissions
2. **Docker** installed and running
3. **VPC with public subnets** (uses default VPC by default)

Required AWS permissions:
- ECS, ECR, RDS, CloudFormation
- EC2 (VPC, Security Groups, Load Balancer)
- IAM, Secrets Manager, CloudWatch

## Deployment Steps

1. **Clone and prepare**:
   ```bash
   cd sbtm-tool
   ./deploy.sh
   ```

2. **Enter database password** when prompted

3. **Wait for deployment** (~10-15 minutes)

4. **Access application** at the provided Load Balancer URL

## Configuration

### Environment Variables
- `ENVIRONMENT=production` - Disables debug logging
- `DATABASE_URL` - PostgreSQL connection (from Secrets Manager)
- `HOST=0.0.0.0` - Bind to all interfaces
- `PORT=8080` - Application port

### Database
- **Engine**: PostgreSQL 15.4
- **Instance**: db.t3.micro (1 vCPU, 1GB RAM)
- **Storage**: 20GB GP2
- **Backup**: 7-day retention

## Monitoring

### Health Check
- **Endpoint**: `/health`
- **Interval**: 30 seconds
- **Timeout**: 5 seconds

### Logs
- **CloudWatch Log Group**: `/ecs/sbtm-tool`
- **Retention**: 7 days

### Metrics
Monitor via AWS CloudWatch:
- ECS service health
- RDS performance
- Load balancer requests

## Maintenance

### Updates
```bash
# Make changes to code
./deploy.sh  # Rebuilds and redeploys
```

### Database Access
```bash
# Get database endpoint
aws cloudformation describe-stacks --stack-name sbtm-tool-stack \
  --query "Stacks[0].Outputs[?OutputKey=='DatabaseEndpoint'].OutputValue" --output text

# Connect via psql (from within VPC)
psql postgresql://sbtm:PASSWORD@ENDPOINT:5432/sbtm
```

### Cleanup
```bash
# Delete entire stack
aws cloudformation delete-stack --stack-name sbtm-tool-stack
```

## Troubleshooting

### Service Not Starting
1. Check ECS service events in AWS Console
2. View CloudWatch logs: `/ecs/sbtm-tool`
3. Verify database connectivity

### Load Balancer 503 Errors
1. Check ECS service health
2. Verify security group rules
3. Check target group health

### Database Connection Issues
1. Verify RDS instance is running
2. Check security group allows port 5432
3. Verify Secrets Manager secret

## Security Features

- **No public database access** - RDS in private subnets
- **Secrets Management** - Database credentials in AWS Secrets Manager
- **Security Groups** - Least privilege network access
- **Container Security** - Non-root user, minimal base image
- **HTTPS Ready** - Load balancer supports SSL termination

## Scaling Options

### Horizontal Scaling
```bash
# Increase ECS service desired count
aws ecs update-service --cluster sbtm-cluster --service sbtm-service --desired-count 3
```

### Vertical Scaling
Update CloudFormation template:
- Increase ECS task CPU/memory
- Upgrade RDS instance class

### Auto Scaling
Add CloudWatch alarms and ECS auto scaling policies for production workloads.
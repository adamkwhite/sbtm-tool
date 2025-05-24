# SBTM Tool - AWS Console Deployment (No CLI Required)

Deploy your SBTM tool to AWS using only the web console - no CLI installation needed!

## Option 1: AWS App Runner (Easiest - 5 minutes)

### Step 1: Create GitHub Repository
1. Go to [GitHub](https://github.com) and create a new repository called `sbtm-tool`
2. Upload all your SBTM tool files to this repository
3. Make the repository public (or private with GitHub connection)

### Step 2: Deploy with App Runner
1. Go to [AWS App Runner Console](https://console.aws.amazon.com/apprunner)
2. Click **"Create service"**
3. **Source**: Choose **"Source code repository"**
4. **Connect to GitHub**: Link your GitHub account
5. **Repository**: Select your `sbtm-tool` repository
6. **Branch**: `main` or `master`
7. **Build settings**: 
   - **Runtime**: Python 3
   - **Build command**: `pip install -r requirements.txt`
   - **Start command**: `python main.py`
8. **Service settings**:
   - **Service name**: `sbtm-tool`
   - **Port**: `8080`
9. **Environment variables**:
   ```
   ENVIRONMENT=production
   HOST=0.0.0.0
   PORT=8080
   DATABASE_URL=sqlite:///sbtm.db
   ```
10. Click **"Create & deploy"**

**Cost**: ~$25/month | **Time**: 5-10 minutes | **Database**: SQLite (file-based)

---

## Option 2: Elastic Beanstalk (Most Complete)

### Step 1: Prepare Application Package
1. Create a ZIP file with these files:
   ```
   sbtm-tool.zip
   ├── main.py
   ├── requirements.txt
   ├── database/
   ├── views/
   └── Dockerfile (optional)
   ```

### Step 2: Deploy to Elastic Beanstalk
1. Go to [AWS Elastic Beanstalk Console](https://console.aws.amazon.com/elasticbeanstalk)
2. Click **"Create application"**
3. **Application information**:
   - **Application name**: `SBTM-Tool`
   - **Platform**: Python 3.11
   - **Platform branch**: Python 3.11 running on 64bit Amazon Linux 2023
4. **Application code**: Upload your ZIP file
5. **Configuration presets**: Single instance (free tier eligible)
6. **Service access**: Create new service role
7. **Environment variables** (in Configuration > Software):
   ```
   ENVIRONMENT=production
   HOST=0.0.0.0
   PORT=8000
   ```
8. Click **"Create application"**

**Cost**: Free tier eligible | **Time**: 10-15 minutes | **Database**: SQLite initially

---

## Option 3: EC2 Instance (Traditional)

### Step 1: Launch EC2 Instance
1. Go to [EC2 Console](https://console.aws.amazon.com/ec2)
2. Click **"Launch Instance"**
3. **Name**: `SBTM-Tool-Server`
4. **AMI**: Amazon Linux 2023
5. **Instance type**: t3.micro (free tier)
6. **Key pair**: Create or select existing
7. **Security group**: Create new with these rules:
   - SSH (22) from your IP
   - HTTP (80) from anywhere
   - Custom TCP (8080) from anywhere
8. Click **"Launch instance"**

### Step 2: Connect and Deploy
1. Wait for instance to be running
2. Click **"Connect"** > **"EC2 Instance Connect"**
3. Run these commands:
   ```bash
   # Install Python and Git
   sudo yum update -y
   sudo yum install -y python3 python3-pip git
   
   # Clone your code (upload to GitHub first)
   git clone https://github.com/YOUR_USERNAME/sbtm-tool.git
   cd sbtm-tool
   
   # Install dependencies
   pip3 install -r requirements.txt
   
   # Run application
   python3 main.py
   ```
4. Access via: `http://YOUR_EC2_PUBLIC_IP:8080`

**Cost**: Free tier eligible | **Time**: 15-20 minutes | **Database**: SQLite

---

## Option 4: Railway.app (External - Easiest)

### Simple Alternative Outside AWS
1. Go to [Railway.app](https://railway.app)
2. Sign up with GitHub
3. Click **"New Project"** > **"Deploy from GitHub repo"**
4. Select your SBTM tool repository
5. Railway auto-detects Python and deploys!
6. Add environment variables in dashboard:
   ```
   ENVIRONMENT=production
   ```

**Cost**: Free tier available | **Time**: 2 minutes | **Database**: SQLite

---

## Recommended Approach

For **quick testing**: Use **Railway.app** (2 minutes, free)
For **AWS deployment**: Use **App Runner** (5 minutes, ~$25/month)
For **production**: Use **Elastic Beanstalk** (most features)

## Adding PostgreSQL Database Later

Once deployed, you can add a managed database:

### For App Runner/Beanstalk:
1. Go to [RDS Console](https://console.aws.amazon.com/rds)
2. Click **"Create database"**
3. Choose **PostgreSQL**
4. Select **Free tier** template
5. Set database name: `sbtm`
6. Note the endpoint URL
7. Update your app's `DATABASE_URL` environment variable

**All methods get your SBTM tool running without installing anything locally!**

Which option would you prefer to try first?
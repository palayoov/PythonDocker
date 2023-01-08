## Script to validate S3 access from AWS Fargate container

Steps to run this process:
1. Build Docker image using supplied Dockerfile
   2. 
2. Push Image to ECR
3. Create ECS Cluster and task definition in the .aws folder
4. Start a Task
5. Validate output in logs and check S3 bucket
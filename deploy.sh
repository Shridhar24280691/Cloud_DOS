#!/bin/bash

APP_NAME="car_detailing_app"
GROUP_NAME="car_detailing_group"
BUCKET="car-detailing-artifacts-844028821119"

echo "Zipping application..."
zip -r deploy.zip . -x "*.git*" "*.md" "*.zip" "__pycache__/*" "*.sqlite3" "env/*"

echo "Uploading to S3..."
aws s3 cp deploy.zip s3://$BUCKET/deploy.zip

echo "Creating CodeDeploy deployment..."
aws deploy create-deployment \
  --application-name $APP_NAME \
  --deployment-group-name $GROUP_NAME \
  --s3-location bucket=$BUCKET,key=deploy.zip,bundleType=zip

echo "Deployment triggered!"


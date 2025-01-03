source $(pwd)/.env

# Set the current project
gcloud config set project $PROJECT_ID

## Add permissions to the service account to deploy the cloud run function
export SVC_ACCOUNT_EMAIL=$SVC_ACCOUNT@$PROJECT_ID.iam.gserviceaccount.com

# Allow service account to run and manage Cloud Build jobs
gcloud projects add-iam-policy-binding $PROJECT_ID \
  --member="serviceAccount:$SVC_ACCOUNT_EMAIL" \
  --role="roles/cloudbuild.builds.editor"

# Allow service account access to logs
gcloud projects add-iam-policy-binding $PROJECT_ID \
  --member="serviceAccount:$SVC_ACCOUNT_EMAIL" \
  --role="roles/logging.viewer"

# Allow this service account to deploy
gcloud iam service-accounts add-iam-policy-binding $SVC_ACCOUNT_EMAIL \
  --member="serviceAccount:$SVC_ACCOUNT_EMAIL" \
  --role="roles/iam.serviceAccountUser"

gcloud projects add-iam-policy-binding $PROJECT_ID \
  --member="serviceAccount:$SVC_ACCOUNT_EMAIL" \
  --role=roles/run.admin

gcloud projects add-iam-policy-binding $PROJECT_ID \
  --member="serviceAccount:$SVC_ACCOUNT_EMAIL" \
  --role=roles/cloudfunctions.admin

echo "Deploying Cloud Run function $FUNCTION_NAME in $REGION"
gcloud functions deploy $FUNCTION_NAME \
	--gen2     \
	--runtime=python312     \
	--run-service-account=$SVC_ACCOUNT_EMAIL \
	--region=$REGION     \
	--source=.     \
	--entry-point=get_website_articles     \
	--trigger-http     \
    --max-instances 5 \
	--allow-unauthenticated \
	--env-vars-file .env.yaml \
	--memory=1024Mi

FUNCTION_URI=$(gcloud functions describe $FUNCTION_NAME --gen2 --region $REGION --format "value(serviceConfig.uri)")
echo "Url for $FUNCTION_NAME: $FUNCTION_URI"
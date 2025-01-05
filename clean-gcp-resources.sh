source $(pwd)/.env

# Set the current project
gcloud config set project $PROJECT_ID

# Specify email for the service principal account
export SVC_ACCOUNT_EMAIL=$SVC_ACCOUNT@$PROJECT_ID.iam.gserviceaccount.com

# Delete the service account created for application
gcloud iam service-accounts delete $SVC_ACCOUNT_EMAIL --quiet

# Delete the service account created for invoking the cloud run function
gcloud iam service-accounts delete $SVC_INVOKER_ACCOUNT_EMAIL --quiet

# Delete the workflow
gcloud workflows delete $NEWS_DOWNLOAD_WORKFLOW

# Delete the deployed cloud run function
gcloud functions delete $FUNCTION_NAME --quiet

# Create storage bucket to store news articles
gcloud storage rm -r gs://$NEWS_BUCKET --quiet


# Delete the firestore database
gcloud firestore databases delete --database=$FIRESTORE_DATABASE --quiet
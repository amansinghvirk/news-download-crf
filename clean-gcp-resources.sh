source $(pwd)/.env

# Set the current project
gcloud config set project $PROJECT_ID

# Specify email for the service principal account
export SVC_ACCOUNT_EMAIL=$SVC_ACCOUNT@$PROJECT_ID.iam.gserviceaccount.com

gcloud iam service-accounts delete $SVC_ACCOUNT_EMAIL --quiet

gcloud functions delete $FUNCTION_NAME --quiet

# Create storage bucket to store news articles
gcloud storage rm -r gs://$NEWS_BUCKET --quiet
# gcloud storage buckets delete gs://$NEWS_BUCKET --quiet

# Delete the firestore database
gcloud firestore databases delete --database=$FIRESTORE_DATABASE --quiet
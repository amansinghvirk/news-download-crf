source $(pwd)/.env

# Set the current project
gcloud config set project $PROJECT_ID

# Specify email for the service principal account
export SVC_ACCOUNT_EMAIL=$SVC_ACCOUNT@$PROJECT_ID.iam.gserviceaccount.com

# Enable required APIs for the project
gcloud services enable \
  artifactregistry.googleapis.com \
  cloudfunctions.googleapis.com \
  cloudbuild.googleapis.com \
  eventarc.googleapis.com \
  run.googleapis.com \
  logging.googleapis.com \
  storage.googleapis.com \
  pubsub.googleapis.com 

# Create storage bucket to store news articles
gcloud storage buckets create gs://$NEWS_BUCKET \
    --default-storage-class=standard \
    --location=$REGION

# Create firestore database
gcloud firestore databases create \
    --database=$DATABASE_NAME \
    --location=$REGION

# Allow service account to access GCS Cloud Storage bucket
gcloud projects add-iam-policy-binding $PROJECT_ID \
  --member="serviceAccount:$SVC_ACCOUNT_EMAIL" \
  --role="roles/storage.objectUser"

# Accow service account to access Firestore database
gcloud projects add-iam-policy-binding $PROJECT_ID \
  --member="serviceAccount:$SVC_ACCOUNT_EMAIL" \
  --role="roles/datastore.user"
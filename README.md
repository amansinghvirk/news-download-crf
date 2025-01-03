# news-download-crf
Cloud run function to extract news articles from website and save as JSON to GCP cloud storage

# Prerequistes
#### Login in CLI with account which should have permissions
    - create and delete service principals
    - assign permissions to the service principals for deploy and creating resources

For application to communicate with resource will create new service principals with least privalages required only for the task.

# Intial Setup for GCP services

# Create new service principal which will be used by app
    - to create objects in cloud storage
    - create and retrieve data from Firestore database
  
## Set environment variables
```
export PROJECT_ID=existing-project-id
export SVC_ACCOUNT=replace-this-with-service-principal-name
export SVC_ACCOUNT_EMAIL=$SVC_ACCOUNT@$PROJECT_ID.iam.gserviceaccount.com
```

e.g.
```
export PROJECT_ID=prj-demo
export SVC_ACCOUNT=news-downloader-crf
export SVC_ACCOUNT_EMAIL=$SVC_ACCOUNT@$PROJECT_ID.iam.gserviceaccount.com
```

Set the current project
```
gcloud config set project $PROJECT_ID
```

## Enable the required apis

```
gcloud services enable \
  artifactregistry.googleapis.com \
  cloudfunctions.googleapis.com \
  cloudbuild.googleapis.com \
  eventarc.googleapis.com \
  run.googleapis.com \
  logging.googleapis.com \
  storage.googleapis.com \
  pubsub.googleapis.com 
```

## Create new service principal
```sh
gcloud iam service-accounts create $SVC_ACCOUNT
```

## Create credentials and download them as JSON file

Set the file where key file needs to be store, specify the path other than the project folder this should not be publicly accessed

```
export GOOGLE_APPLICATION_CREDENTIALS=path-for-the-credentials-file
```
e.g. 
```
export GOOGLE_APPLICATION_CRDENTIALS="/keys/credentials.json"
```

### Download the key file and save it to system
```
gcloud iam service-accounts keys create $GOOGLE_APPLICATION_CREDENTIALS \
    --iam-account=$SVC_ACCOUNT_EMAIL
```

# Setup Cloud Storage Bucket and Firestore Database

## Set environment variables for setup

```
export REGION=replace-with-region-name
export NEWS_BUCKET=replace-with-unique-bucket-name
export DATABASE_NAME=replace-with-firestore-database-name
```

e.g.
```
export REGION=us-central1
export NEWS_BUCKET=bucket-smart-news-2025010113
export DATABASE_NAME=smart-news-db-2025010113
```

## Create storage bucket to store news articles
```
gcloud storage buckets create gs://$NEWS_BUCKET \
    --default-storage-class=standard \
    --location=$REGION
```

## Create Firestore database to store the article as document in collection
```
gcloud firestore databases create \
    --database=$DATABASE_NAME \
    --location=$REGION
```

# Allow service account to access GCS Cloud Bucket and Firestore database
```
gcloud projects add-iam-policy-binding $PROJECT_ID \
  --member="serviceAccount:$SVC_ACCOUNT_EMAIL" \
  --role="roles/storage.objectUser"
```

```
gcloud projects add-iam-policy-binding $PROJECT_ID \
  --member="serviceAccount:$SVC_ACCOUNT_EMAIL" \
  --role="roles/datastore.user"
```

# Create environment variable file to store the variables for application

## Create .env file with following structure
```
PROJECT_ID=prj-demo
SVC_ACCOUNT=news-downloader-crf
GOOGLE_APPLICATION_CRDENTIALS="/keys/credentials.json"
REGION=us-central1
NEWS_BUCKET=bucket-smart-news-2025010113
DATABASE_NAME=smart-news-db-2025010113
```

# Stage 2: Setup environment for the application

- Create and activate Conda or virutal environment with Python 3.12
- install dependencies from requirements.txt

## Setup up project code

## Execute

## Add collection name to the .env file
COLLECTION_NAME=articles

```
python main.py --newssite 'http://cnn.com' --docs_count 5
```

# Stage 3: Setup and Test Cloud Run Funciton locally

- run function locally
```
functions-framework --target get_website_articles
```

### Test the url with test script by passing url of the cloud run function

```
python test_crf.py --crf_url http://127.0.0.1:8080
```

### Expected result
b'5 articles parsed form http://cnn.com and saved to cloud storage!'

# Stage 4: Deploy unauthenticated Cloud Run Function

### Setup environment variable for Cloud Run Function name and assign additional permissions required to the service principal

```
export FUNCTION_NAME=replace-with-cloud-run-function-name
```

e.g
```
export FUNCTION_NAME=news-downloader-crf
```

### Assign privilages to the service account

```
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
```

## Create .env.yaml file in the project folder to store the environment variables required for function to run in GCP

```.env.yaml
NEWS_BUCKET: name-of-the-cloud-bucket-created-in-previous-steps
DATABASE_NAME: name-of-the-firestore-database-created-in-previous-steps
COLLECTION_NAME: articles
```

e.g.
```
NEWS_BUCKET: bucket-smart-news-2025010113
DATABASE_NAME: smart-news-db-2025010113
COLLECTION_NAME: articles
```

## Deploy unauthenticated function to the GCP project

```
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

```

### Copy the URL of the function

### Test the url with test script by passing url of the cloud run function

```
python test_crf.py --crf_url replace-it-with-url-of-the-deployed-function
```

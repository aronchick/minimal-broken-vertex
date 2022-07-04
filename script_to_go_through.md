
Steps:

Set the project:
gcloud config set project same-project-vertex
export PROJECT_ID="minimal-vertex-tester"
export SERVICE_ACCOUNT_ID="minimal-vertex-runner-sp"
export USER_EMAIL="aronchick@busted.dev"
export BUCKET_NAME="minimal_vertex_test_bucket"
export FILE_NAME="minimal_vertex_sp_credentials"
export GOOGLE_APPLICATION_CREDENTIALS="./minimal_vertex_sp_credentials.json"

- Create Service Principal to run - https://cloud.google.com/vertex-ai/docs/pipelines/configure-project#service-account

gcloud iam service-accounts create $SERVICE_ACCOUNT_ID \
--description="Service principal for running vertex and creating pipelines/metadata" \
--display-name="$SERVICE_ACCOUNT_ID" \
--project ${PROJECT_ID}

gcloud projects add-iam-policy-binding ${PROJECT_ID} \
    --member="serviceAccount:$SERVICE_ACCOUNT_ID@$PROJECT_ID.iam.gserviceaccount.com" \
    --role=roles/storage.objectAdmin

gcloud projects add-iam-policy-binding ${PROJECT_ID} \
    --member="serviceAccount:$SERVICE_ACCOUNT_ID@$PROJECT_ID.iam.gserviceaccount.com" \
    --role=roles/aiplatform.user

gcloud projects add-iam-policy-binding ${PROJECT_ID} \
    --member="serviceAccount:$SERVICE_ACCOUNT_ID@$PROJECT_ID.iam.gserviceaccount.com" \
    --role=roles/ml.admin

gcloud projects add-iam-policy-binding ${PROJECT_ID} \
    --member="serviceAccount:$SERVICE_ACCOUNT_ID@$PROJECT_ID.iam.gserviceaccount.com" \
    --role=roles/logging.admin

gcloud projects get-iam-policy $PROJECT_ID \
    --flatten="bindings[].members" \
    --format='table(bindings.role)' \
    --filter="bindings.members:serviceAccount:$SERVICE_ACCOUNT_ID@$PROJECT_ID.iam.gserviceaccount.com"


Need to create a custom role with additional permissions
- Unfortunately need to do this in the UI
https://console.cloud.google.com/iam-admin/roles?project=same-project-vertex&authuser=1
Once you create the Service Account Name, add the additional permissions
https://console.cloud.google.com/iam-admin/roles?project=same-project-vertex&authuser=1
storage.objects.create
storage.objects.get

gcloud iam service-accounts add-iam-policy-binding \
    $SERVICE_ACCOUNT_ID@$PROJECT_ID.iam.gserviceaccount.com \
    --member="user:$USER_EMAIL" \
    --role="roles/iam.serviceAccountUser"
    --project ${PROJECT_ID}

gcloud iam service-accounts add-iam-policy-binding \
    $SERVICE_ACCOUNT_ID@$PROJECT_ID.iam.gserviceaccount.com \
    --member="user:$USER_EMAIL" \
    --role="roles/iam.serviceAccountTokenCreator" \
    --project ${PROJECT_ID}

- Create a cloud bucket
gsutil mb -p $PROJECT_ID gs://$BUCKET_NAME
- Enable APIs -


    gsutil iam ch \
    serviceAccount:$SERVICE_ACCOUNT_ID@$PROJECT_ID.iam.gserviceaccount.com:roles/storage.objectCreator,objectViewer \
    gs://$BUCKET_NAME

Download the service account credentials
https://cloud.google.com/docs/authentication/getting-started#auth-cloud-implicit-python
gcloud iam service-accounts keys create $FILE_NAME.json --iam-account=$SERVICE_ACCOUNT_ID@$PROJECT_ID.iam.gserviceaccount.com

python3 /home/daaronch/code/same-project/sameproject/ops/vertex/vertex_debugger.py deploy-vertex --compiled-pipeline-path . --project-id $PROJECT_ID --pipeline-root "gs://$PIPELINE_ROOT" --service-account $SERVICE_ACCOUNT_ID --service-account-credentials-file $GOOGLE_APPLICATION_CREDENTIALS

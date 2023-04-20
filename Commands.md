gcloud builds submit --tag gcr.io/plotlygraph/graph3 --project=plotlygraph

gcloud run deploy --image gcr.io/plotlygraph/graph3 --platform managed --project=plotlygraph --allow-unauthenticated

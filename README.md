This is an app which can provide the recent exchange rates between GBP and CAD, USD, CNY, EUR. Type the the date from 019-03-01 to 2019-03-26 and currency behind external IP, then we can get the exchange rate between GBP and other currencies. 

a. I use the data which I get from API (https://api.exchangeratesapi.io/history?base=GBP&symbols=CAD,USD,CNY,EUR&start_at=2019-03-01&end_at=2019-03-26) to transform from json format to csv format. 

b. I upload my csv file on github and edit it to fit my app. Here is the url of the file: https://gist.githubusercontent.com/qmul-wyt/322f467803982d9ae73626bffde49ad5/raw/8035dcc05fb347200bfa84dfb712fea9ad47061d/rates.csv

c. Download this csv via ‘wget’ and copy it into the Cassandra image.
#chose "europe-west2-b" and export the project name as an environment variable
gcloud config set compute/zone europe-west2-b
export PROJECT_ID="$(gcloud config get-value project -q)"
#pull the Cassandra Docker Image
docker pull cassandra:latest
#run a Cassandra instance within docker
docker run --name cassandra-test -d cassandra:latest
#Download this csv
wget -O rates.csv https://gist.githubusercontent.com/qmul-wyt/322f467803982d9ae73626bffde49ad5/raw/8035dcc05fb347200bfa84dfb712fea9ad47061d/rates.csv

d. Copy the data from the csv into the cassandra database.
#copy the data in the container
docker cp rates.csv cassandra-test:/home/rates.csv
#interact with our Cassandra
docker exec -it cassandra-test cqlsh
CREATE KEYSPACE rates WITH REPLICATION = {'class' : 'SimpleStrategy', 'replication_factor' : 1};
CREATE TABLE rates.stats (date text PRIMARY KEY,CAD float, USD float, CNY float, EUR float);
COPY rates.stats (date,CAD,USD,CNY,EUR) FROM '/home/rates.csv' WITH DELIMITER=',' AND HEADER=TRUE;

e. Run Cassandra on Kubernetes.

f. Pull data from our Cassandra database into a flask web client.
#build the image
docker build -t gcr.io/${PROJECT_ID}/rates-wyt:v1 .
#Push it to the Google Repository
docker push gcr.io/${PROJECT_ID}/rates-wyt:v1
#Run it as a service, exposing the deploment to get an external IP
kubectl run rates-wyt --image=gcr.io/${PROJECT_ID}/rates-wyt:v1 --port 8080
kubectl expose deployment rates-wyt --type=LoadBalancer --port 80 --target-port 8080
#Scale up the application
kubectl scale deployment rates-wyt --replicas=2

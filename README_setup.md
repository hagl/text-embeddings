
docker run --name elastic_7.3.1 -p 9200:9200 -p 9300:9300 -e "discovery.type=single-node" docker.elastic.co/elasticsearch/elasticsearch:7.3.1


ipython kernel install --user --name=search
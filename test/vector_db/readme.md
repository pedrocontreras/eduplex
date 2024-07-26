source: https://github.com/openai/chatgpt-retrieval-plugin/blob/main/README.md
### Choosing a Vector Database

The plugin supports several vector database providers, each with different features, performance, and pricing. Depending on which one you choose, you will need to use a different Dockerfile and set different environment variables. The following sections provide brief introductions to each vector database provider.

For more detailed instructions on setting up and using each vector database provider, please refer to the respective documentation in the `/docs/providers/<datastore_name>/setup.md` file ([folders here](/docs/providers)).

#### Pinecone

[Pinecone](https://www.pinecone.io) is a managed vector database designed for speed, scale, and rapid deployment to production. It supports hybrid search and is currently the only datastore to natively support SPLADE sparse vectors. For detailed setup instructions, refer to [`/docs/providers/pinecone/setup.md`](/docs/providers/pinecone/setup.md).

#### Weaviate

[Weaviate](https://weaviate.io/) is an open-source vector search engine built to scale seamlessly into billions of data objects. It supports hybrid search out-of-the-box, making it suitable for users who require efficient keyword searches. Weaviate can be self-hosted or managed, offering flexibility in deployment. For detailed setup instructions, refer to [`/docs/providers/weaviate/setup.md`](/docs/providers/weaviate/setup.md).

#### Zilliz

[Zilliz](https://zilliz.com) is a managed cloud-native vector database designed for billion-scale data. It offers a wide range of features, including multiple indexing algorithms, distance metrics, scalar filtering, time travel searches, rollback with snapshots, full RBAC, 99.9% uptime, separated storage and compute, and multi-language SDKs. For detailed setup instructions, refer to [`/docs/providers/zilliz/setup.md`](/docs/providers/zilliz/setup.md).

#### Milvus

[Milvus](https://milvus.io/) is an open-source, cloud-native vector database that scales to billions of vectors. It is the open-source version of Zilliz and shares many of its features, such as various indexing algorithms, distance metrics, scalar filtering, time travel searches, rollback with snapshots, multi-language SDKs, storage and compute separation, and cloud scalability. For detailed setup instructions, refer to [`/docs/providers/milvus/setup.md`](/docs/providers/milvus/setup.md).

#### Qdrant

[Qdrant](https://qdrant.tech/) is a vector database capable of storing documents and vector embeddings. It offers both self-hosted and managed [Qdrant Cloud](https://cloud.qdrant.io/) deployment options, providing flexibility for users with different requirements. For detailed setup instructions, refer to [`/docs/providers/qdrant/setup.md`](/docs/providers/qdrant/setup.md).

#### Redis

[Redis](https://redis.com/solutions/use-cases/vector-database/) is a real-time data platform suitable for a variety of use cases, including everyday applications and AI/ML workloads. It can be used as a low-latency vector engine by creating a Redis database with the [Redis Stack docker container](/examples/docker/redis/docker-compose.yml). For a hosted/managed solution, [Redis Cloud](https://app.redislabs.com/#/) is available. For detailed setup instructions, refer to [`/docs/providers/redis/setup.md`](/docs/providers/redis/setup.md).

#### LlamaIndex

[LlamaIndex](https://github.com/jerryjliu/llama_index) is a central interface to connect your LLM's with external data.
It provides a suite of in-memory indices over your unstructured and structured data for use with ChatGPT.
Unlike standard vector databases, LlamaIndex supports a wide range of indexing strategies (e.g. tree, keyword table, knowledge graph) optimized for different use-cases.
It is light-weight, easy-to-use, and requires no additional deployment.
All you need to do is specifying a few environment variables (optionally point to an existing saved Index json file).
Note that metadata filters in queries are not yet supported.
For detailed setup instructions, refer to [`/docs/providers/llama/setup.md`](/docs/providers/llama/setup.md).

#### Chroma

[Chroma](https://trychroma.com) is an AI-native open-source embedding database designed to make getting started as easy as possible. Chroma runs in-memory, or in a client-server setup. It supports metadata and keyword filtering out of the box. For detailed instructions, refer to [`/docs/providers/chroma/setup.md`](/docs/providers/chroma/setup.md).

#### Azure Cognitive Search

[Azure Cognitive Search](https://azure.microsoft.com/products/search/) is a complete retrieval cloud service that supports vector search, text search, and hybrid (vectors + text combined to yield the best of the two approaches). It also offers an [optional L2 re-ranking step](https://learn.microsoft.com/azure/search/semantic-search-overview) to further improve results quality. For detailed setup instructions, refer to [`/docs/providers/azuresearch/setup.md`](/docs/providers/azuresearch/setup.md)

#### Supabase

[Supabase](https://supabase.com/blog/openai-embeddings-postgres-vector) offers an easy and efficient way to store vectors via [pgvector](https://github.com/pgvector/pgvector) extension for Postgres Database. [You can use Supabase CLI](https://github.com/supabase/cli) to set up a whole Supabase stack locally or in the cloud or you can also use docker-compose, k8s and other options available. For a hosted/managed solution, try [Supabase.com](https://supabase.com/) and unlock the full power of Postgres with built-in authentication, storage, auto APIs, and Realtime features. For detailed setup instructions, refer to [`/docs/providers/supabase/setup.md`](/docs/providers/supabase/setup.md).

#### Postgres

[Postgres](https://www.postgresql.org) offers an easy and efficient way to store vectors via [pgvector](https://github.com/pgvector/pgvector) extension. To use pgvector, you will need to set up a PostgreSQL database with the pgvector extension enabled. For example, you can [use docker](https://www.docker.com/blog/how-to-use-the-postgres-docker-official-image/) to run locally. For a hosted/managed solution, you can use any of the cloud vendors which support [pgvector](https://github.com/pgvector/pgvector#hosted-postgres). For detailed setup instructions, refer to [`/docs/providers/postgres/setup.md`](/docs/providers/postgres/setup.md).

#### AnalyticDB

[AnalyticDB](https://www.alibabacloud.com/help/en/analyticdb-for-postgresql/latest/product-introduction-overview) is a distributed cloud-native vector database designed for storing documents and vector embeddings. It is fully compatible with PostgreSQL syntax and managed by Alibaba Cloud. AnalyticDB offers a powerful vector compute engine, processing billions of data vectors and providing features such as indexing algorithms, structured and unstructured data capabilities, real-time updates, distance metrics, scalar filtering, and time travel searches. For detailed setup instructions, refer to [`/docs/providers/analyticdb/setup.md`](/docs/providers/analyticdb/setup.md).

#### Elasticsearch

[Elasticsearch](https://www.elastic.co/guide/en/elasticsearch/reference/current/index.html) currently supports storing vectors through the `dense_vector` field type and uses them to calculate document scores. Elasticsearch 8.0 builds on this functionality to support fast, approximate nearest neighbor search (ANN). This represents a much more scalable approach, allowing vector search to run efficiently on large datasets. For detailed setup instructions, refer to [`/docs/providers/elasticsearch/setup.md`](/docs/providers/elasticsearch/setup.md).

# Database Examples

This folder contains examples for using different vector store backends with the VFN RAG system.

## Available Backends

### Azure Cosmos DB
- `azure-cosmos-create.py` - Create a vector store in Azure Cosmos DB
- `azure-cosmos-load.py` - Load and query an existing Cosmos DB vector store

### PostgreSQL with pgvector
- `postgres-create.py` - Create a vector store in PostgreSQL
- `postgres-load.py` - Load and query an existing PostgreSQL vector store

## PostgreSQL Setup with Docker

### Quick Start

1. **Start PostgreSQL with pgvector:**
   ```bash
   docker run -d \
     --name postgres-pgvector \
     -e POSTGRES_PASSWORD=password \
     -e POSTGRES_USER=postgres \
     -e POSTGRES_DB=vector_db \
     -p 5432:5432 \
     pgvector/pgvector:pg16
   ```

2. **Run the create script:**
   ```bash
   python examples/data-base/postgres-create.py
   ```

3. **Query the stored data:**
   ```bash
   python examples/data-base/postgres-load.py
   ```

### Environment Variables (Optional)

You can set these environment variables instead of using defaults:

```bash
POSTGRES_HOST=localhost
POSTGRES_PORT=5432
POSTGRES_DB=vector_db
POSTGRES_USER=postgres
POSTGRES_PASSWORD=password
```

### Docker Commands

**Stop the container:**
```bash
docker stop postgres-pgvector
```

**Start the container:**
```bash
docker start postgres-pgvector
```

**Remove the container:**
```bash
docker stop postgres-pgvector
docker rm postgres-pgvector
```

**Connect to PostgreSQL CLI:**
```bash
docker exec -it postgres-pgvector psql -U postgres -d vector_db
```

**Useful SQL queries:**
```sql
-- List all tables
\dt

-- Check vector store contents
SELECT COUNT(*) FROM public.deltares_vectors;

-- View sample data
SELECT id, node_id, LEFT(text, 100) as text_preview 
FROM public.deltares_vectors 
LIMIT 5;

-- Check table schema
\d public.deltares_vectors
```

## Switching from Local to Cloud

Once you've tested locally, switching to a cloud database is easy:

```python
# Local (Docker)
storage_context = Postgres.create(
    host="localhost",
    port=5432,
    database="vector_db",
    user="postgres",
    password="password",
    table_name="my_vectors"
)

# Cloud (Azure Database for PostgreSQL, AWS RDS, etc.)
storage_context = Postgres.create(
    host="your-cloud-host.postgres.database.azure.com",
    port=5432,
    database="production_db",
    user="admin@your-cloud-host",
    password="your-secure-password",
    table_name="my_vectors"
)
```

Or use environment variables and just change your `.env` file!

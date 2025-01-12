
# **SQS Queue Order Processing Pipeline**

## **Project Overview**
This project demonstrates a data pipeline for an  platform where order events are ingested, processed, aggregated, and cached for fast retrieval. It includes:
- **Event Ingestion**: From a simulated SQS queue.
- **Data Transformation**: Validation, aggregation, and cleanup.
- **Caching**: Redis as the caching layer for user and global statistics.
- **REST API**: Exposing endpoints for quick retrieval of stats using FastAPI.
- **Gen AI**: Integrating Gen AI for advanced data quality checks

---

## **Tools Used**
- **FastAPI**: REST API framework.
- **Redis**: In-memory data store for caching.
- **Localstack**: Simulates AWS SQS for local development.
- **Docker & Docker Compose**: Containerization and service orchestration.
- **AWS Cli**: Configuring and creating queue.

---

## **Setup Instructions**
### **Prerequisites**
1. **Docker & Docker Compose**:
   - Download from [Docker Official Website](https://www.docker.com/get-started).
2. **Python** (3.8+):
   - Download from [Python Official Website](https://www.python.org/downloads/).
3. **AWS CLI**:
   - Install using [AWS CLI Installation Guide](https://docs.aws.amazon.com/cli/latest/userguide/getting-started-install.html).

### **Steps to Set Up the Project**
1. Clone the repository:
   ```bash
   git clone https://github.com/Aftabbs/SQS-py-pipeline-DE-Assignment.git
   cd <repository-folder>
   ```

2. Start services using Docker Compose:
   ```bash
   docker-compose up
   ```

3. Populate the SQS queue with sample data:
   ```bash
   python scripts/populate_sqs.py
   ```

4. Verify worker processing:
   - Confirm worker logs for successful ingestion and Redis updates.

5. Test API Endpoints:
   - **User stats**: 
     ```bash
     curl http://localhost:8000/users/U5678/stats
     ```
   - **Global stats**:
     ```bash
     curl http://localhost:8000/stats/global
     ```


---

## **Repository Contents**
- **`scripts/`**:
  - `populate_sqs.py`: Adds sample data to SQS Queue.
- **`project/`**:
  - `api/main.py`: FastAPI application.
  - `consumer/consumer.py`: SQS consumer.
- **`enhancement/enhanced_queries.py`**:
  - Optional enhancements: Top N users, date range filters.
- **`docker-compose.yml`**: Service orchestration.

---

### **Task 3: Design Reasoning**
#### Data Models & Approach:
1. **Redis Hash for User Stats**:
   - Key: `user:<user_id>`, Fields: `order_count`, `total_spend`.
   - Efficient for individual lookups.
2. **Redis Hash for Global Stats**:
   - Key: `global:stats`, Fields: `total_orders`, `total_revenue`.
   - Simplifies global data aggregation.


---

#### Further Enhancements:
   - Horizontal scaling using multiple workers with k8s(Kubernetes).
   - Employ Redis clustering for distributed caching.
   - Utilizing Kafka for parallel processing.


---

### Design Diagram
![alt text](image.png)


### Testing Result:

#### Postman Tests

```
Data :

{
  "order_id": "ORD1237",
  "user_id": "U0001",
  "order_timestamp": "2024-12-16T13:00:00Z",
  "order_value": 2000,
  "items": [
    { "product_id": "P006", "quantity": 5, "price_per_unit": 200.00 },
    { "product_id": "P007", "quantity": 2, "price_per_unit": 500.00 }
  ],
  "shipping_address": "321 Pine St, Springfield",
  "payment_method": "CreditCard"
}

{
  "order_id": "ORD1237",
  "user_id": "U0002",
  "order_timestamp": "2024-12-16T13:00:00Z",
  "order_value": 2000,
  "items": [
    { "product_id": "P006", "quantity": 5, "price_per_unit": 200.00 },
    { "product_id": "P007", "quantity": 2, "price_per_unit": 500.00 }
  ],
  "shipping_address": "321 Pine St, Springfield",
  "payment_method": "CreditCard"
}






- invalid data


{
  "order_id": "ORD1237",
  "user_id": "U0002",
  "order_timestamp": "2024-12-16T13:00:00Z",
  "order_value": 201,
  "items": [
    { "product_id": "P006", "quantity": 5, "price_per_unit": 200.00 },
    { "product_id": "P007", "quantity": 2, "price_per_unit": 500.00 }
  ],
  "shipping_address": "321 Pine St, Springfield",
  "payment_method": "CreditCard"
}




URL : http://localhost:4566/?Action=SendMessage&QueueUrl=http://sqs.us-east-1.localhost.localstack.cloud:4566/000000000000/OrderQueue
&Content-Type=application/x-www-form-urlencoded

params

key and values
Action:SendMessage
QueueUrl:http://sqs.us-east-1.localhost.localstack.cloud:4566/000000000000/OrderQueue
Content-Type:application/x-www-form-urlencoded



Body:
key and values
MessageBody:Data
```
- 

![image-1](https://github.com/user-attachments/assets/7ecaf804-dde3-4de4-af65-514253fbc2d8)

![image-2](https://github.com/user-attachments/assets/3e4f3e8f-8151-4869-a7e1-5c12f268a554)

![image-3](https://github.com/user-attachments/assets/cd9216b1-ebe2-4ced-9824-e8089c3e24ee)

![image-4](https://github.com/user-attachments/assets/985074ee-b0bf-45d0-88ee-9057599c47dd)

![image-5](https://github.com/user-attachments/assets/ce849284-0232-45a8-bcc3-a3a2bde69f0b)

![image-6](https://github.com/user-attachments/assets/8a072b72-492f-4988-962b-c2e1e54c7757)

![image-7](https://github.com/user-attachments/assets/95ffbe2b-d5ae-42ee-a5ba-646ad4e698a8)

![image-8](https://github.com/user-attachments/assets/7635d96a-4bec-46ac-b28a-c10c8ec25c03)


- Sending and verifying the data with script.
![image-9](https://github.com/user-attachments/assets/6aefd7df-0c3e-4e93-a725-d61fe190e331)

![image-10](https://github.com/user-attachments/assets/677675eb-7ae0-4e8a-a733-0080ce137e40)

![image-11](https://github.com/user-attachments/assets/599a31fe-4b1c-4c07-9d97-2cb8bf629e85)



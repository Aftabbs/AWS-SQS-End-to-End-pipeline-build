# **Order Validation and Transformation with GenAI**

![alt text](image.png)

## **Overview**
As an additional part of this assignment i wanted to demonstrate the use of a GenAI-powered workflow to validate and transform order data. By integrating the Meta LLaMA 3.3 70B Instruct model through NVIDIA Enterprise's API, we efficiently processed and validated transactional data. The solution highlights the capabilities of GenAI in ensuring data consistency and accuracy within pipeline workflows.

---

## **Key Features**
1. **Data Validation**:
   - Ensures critical fields like `user_id`, `order_id`, and `order_value` are present and correctly typed.
   - Verifies that the `order_value` matches the sum of `(quantity × price_per_unit)` for all items in the order.
   - Identifying context relevant data artifacts(unknown/irrelevant addresses,payment method or other irrelevant typs of data)

2. **Error Identification and Fix Suggestions**:
   - Highlights any missing or inconsistent data.
   - Proposes corrections to ensure data integrity.

3. **Field Extraction**:
   - Extracts key fields such as `user_id`, `order_value`, and `order_timestamp` for downstream processing.

4. **Integration and Efficiency**:
   - Utilizes NVIDIA Enterprise's API for high-speed model execution.
   - Processes multiple transactions in bulk while storing both raw and validated results in JSON format.

---

## **Project Workflow**
1. **Input Data**:
   - Synthetic sample data of transactions containing both valid and invalid records.
   - Each transaction includes details like order ID, user ID, items, shipping address, and payment method.

2. **Validation and Transformation**:
   - Each transaction is processed through the GenAI model to validate its integrity and propose corrections if needed.
   - The raw model response is stored alongside the original transaction data.

3. **Output**:
   - A JSON file containing:
     - Original transaction data.
     - GenAI's raw validation and transformation output.

---

## **Why Use GenAI for Pipeline Workflow Validations?**
- **Scalability**: Processes large datasets with ease, making it ideal for enterprise-level operations.
- **Accuracy**: Ensures consistent and reliable validation of complex transactional data.
- **Automation**: Minimizes manual effort by identifying and correcting errors autonomously.
- **Speed And Precision**: Integrates seamlessly into pipelines, leveraging NVIDIA Enterprise's APIs for rapid execution with using meta's 3.3 llama 70b finetuned model the quality and precision remained consistent throughout .

---

## **Technologies Used**
- **Model**: Meta LLaMA 3.3 70B Instruct
- **Platform**: NVIDIA Enterprise API
- **Language**: Python
- **Output Format**: JSON

---

## **Future Scope**
- **Enhanced Validation Rules**: Incorporate domain-specific rules for more nuanced validations.
- **Visualization**: Add dashboards to monitor and analyze validation outcomes.
- **End-to-End Automation**: Integrate into CI/CD pipelines for real-time validation of transactional data.

This example showcases how GenAI can be a transformative tool in ensuring data quality and reliability in automated workflows.
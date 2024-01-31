# Hotels Data Merge
This application is designed to merge hotel data from different suppliers, clean and organize the data, and provide a unified API endpoint for querying hotels based on destination or hotel IDs.

## Deployment Instructions

### Prerequisites

- Docker and Docker Compose installed on the deployment machine.

### Deployment Steps

1. Clone the repository:

   ```bash
   git clone https://github.com/vuthanhnhan/ascenda
   cd ascenda
   docker-compose build
   docker-compose up

## Configuring Environment File

To ensure a seamless deployment, make sure to update your environment configuration. Follow the steps below:

1. Open the `.env` file in app folder.
2. Update the following key-value pairs based on your deployment environment:

   ```env
    ACME_URL = your_acme_url
    PATAGONIA_URL = your_patagonia_url
    PAPERFLIES_URL = your_paperflies_url

    DATABASE_URL=your_database_url
    DATABASE_NAME=your_database_name

## Local Routes for Testing

To facilitate testing and exploration of the latest changes locally, use the following local routes:
2. **Backend:**
   - The backend is accessible at [http://localhost/api](http://localhost/api) or [http://localhost/api](http://localhost/api)
   - To read OpenAPI docs at [http://localhost/docs](http://localhost/docs)
   - Explore API endpoints, perform requests, and interact with the backend services.

Please make sure that your Docker containers or development servers are running to access these local routes.

## Demonstration Video

For a visual walkthrough of the new features and enhancements introduced in this release, I have prepared a demonstration video.

[Watch the Demonstration Video](https://youtu.be/Ud7xk8Ji4Yk)

## Requirements
### Endpoint
The API endpoint accepts the following parameters:

- **destination_id**: Filter hotels based on the destination ID.
- **hotel_ids**: Filter hotels based on a list of hotel IDs.
Example endpoint: [http://localhost/api/hotel/?hotel_ids=f8c9&hotel_ids=SjyX&destination_id=5432](http://localhost/api/hotel/?hotel_ids=f8c9&hotel_ids=SjyX&destination_id=5432)

### Parse and Clean Dirty Data
Data Cleaning Strategies:

1. **Address, Lat, Lng:**
Utilizes the priority of sources for address, lat, and lng fields.
2. **Destination ID, Name:**
Prioritizes data based on the source.
3. **Images and Amenities:**
Combines and deduplicates images and amenities from multiple sources, ensuring uniqueness based on their properties.

### Architect of application
Preprocessing the data and store it to the Mongodb because sometime **suppliers may be not available**. This method is suitable for application that **hotel not frequently change the data**. 

Below is some advantage and disadvantage of this method:

1. **Advantages:**
- Handles **semi-structured** data effectively.
- Enables quick storage and retrieval for real-time queries.
- Provides a reliable backup in case a supplier is unavailable.

2. **Drawbacks:**
May not be up-to-date with the latest supplier data.
Operational overhead in deploying and maintaining MongoDB.

### Potential Improvements
1. **Architect improvement**

      We can stay up to date with the suppliers' data by implements one of the following methods, ranked from high to low priority:

- Establish communication with suppliers to receive webhook updates.

- Set up a cronjob to periodically check and update MongoDB data. (set suitable interval of cronjob).

- Implement logic to update MongoDB data when a request is made, comparing with supplier data. This method **take more resources and slower** if we not implement the comparison in the background and lead to high load when many people request at the same time (not recommend this method)



2. **Data Merge Improvements**

- Solve data conflict of multiple source is need to take into account
- Solve the duplicate of data in 1 source (intrasource duplicate)

3. **Performance Improvements**

- Procuring Data:
    - Asynchronous calls to suppliers for faster request processing.
    - Use MongoDB as a cache to store data during supplier unavailability.
- Delivering Data:
  - Implement a distributed system for global scalability.
  - Utilize GraphQL to optimize data retrieval by removing unnecessary fields.

### Reference for data fusion
Bleiholder, J., & Naumann, F. (2008). Data Fusion. Hasso-Plattner-Institut.

### Contributors

  - Nhan Vu Thanh

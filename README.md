# Lidar Availability Tracker

The Lidar Availability Tracker is a Django web application designed to compute the availability of Lidar devices on an hourly, daily, monthly, and campaign basis using data sourced from a JSON file stored in an S3 bucket. This tool is valuable for the continuous monitoring and analysis of Lidar device availability across various time spans.

## Features

- **Hourly Availability:** Track the availability of Lidar devices on an hourly basis.
- **Daily Availability:** Monitor Lidar device availability on a daily scale.
- **Monthly Availability:** Analyze availability trends on a monthly basis.
- **Campaign Availability:** Calculate availability for specific campaigns or periods.

## Installation

1. Clone the repository:

   ```bash
   git clone https://github.com/GharialDev/Availability.git

   cd Availability

   pip install -r requirements.txt

## Execution

Create a .env file and provide environment variables to establish a connection with S3:

AWS_ACCESS_KEY_ID=your-access-key-id
AWS_SECRET_ACCESS_KEY=your-secret-access-key
AWS_BUCKET_NAME=your-bucket-name
AWS_OBJECT_KEY=payload_data/data.json
AWS_REGION_NAME=region_name

Run the following commands to set up the database and start the server:

python manage.py migrate

python manage.py runserver




## API Reference

#### Get all campaigns

```http
  GET /api/campaign/
```

#### Get campaign details

```http
  GET /api/campaign/${id}
```

| Parameter | Type     | Description                       |
| :-------- | :------- | :-------------------------------- |
| `id`      | `string` | **Required**. Id of item to fetch |

#### Get all availabilities

```http
  GET /api/availability/
```

#### Get availability details

```http
  GET /api/availability/${id}
```

| Parameter | Type     | Description                       |
| :-------- | :------- | :-------------------------------- |
| `id`      | `string` | **Required**. Id of item to fetch |

#### Post availability calculate

```http
  POST /api/availability_calculate/
```
Payload data will be comming from AWS S3



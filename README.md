# CloudWatch Custom Metrics Pusher
This Python script enables you to push custom metrics to Amazon CloudWatch, providing insights into your system's performance. The script gathers information on running and unhealthy containers, log space capacity, and memory usage. You can specify the instance name and ID to add granularity to your metrics, making them more actionable.

## Prerequisites
- An AWS account with appropriate credentials
- Python 3.x
- boto3 Python package
- Docker

## Usage
1. Clone the repository to your local machine.

2. Install the required Python packages by running:
```sh
pip install boto3
```

3. Ensure that you have Docker installed and running on your machine.

4. Run the script using:
```sh
python cloudwatch-custom-metrics-pusher.py
```

5. The script will gather metrics on the number of running and unhealthy containers, log space capacity, and memory usage. It will also retrieve the instance name and ID.

6. The script will then push the custom metrics to Amazon CloudWatch.

## Configuration
You can customize this script to fit your specific needs by modifying the following parameters:

- `region_name`: The region where your CloudWatch instance is located.
- `Namespace`: The namespace under which you want to publish the metrics.
- `MetricName`: The name of the metric.
- `Dimensions`: Any dimensions you want to add to the metric.
- `Unit`: The unit of the metric.
- `Value`: The value of the metric.

## Troubleshooting
If you encounter any issues while using this script, please refer to the CloudWatch documentation or contact AWS support for assistance.

import urllib.request
import boto3
import time
import subprocess

def getRunningContainersCountMetric():
    cmd = 'docker ps | wc -l'
    output=subprocess.run(cmd, shell=True, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    runningContainers = int(output.stdout.decode("utf-8"))-1
    return runningContainers

def getUnhealthyContainersCountMetric():
    cmd = 'docker ps | grep unhealthy | wc -l'
    output=subprocess.run(cmd, shell=True, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    unhealthyContainers = int(output.stdout.decode("utf-8"))
    return unhealthyContainers

def getLogSpaceCapacityMetric():
    cmd = 'df -h | grep /dev/nvme0n1p1 | awk NR==1\'{print $5}\' | sed \'s/%//g\''  
    output=subprocess.run(cmd, shell=True, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    logSpaceCapacity = int(output.stdout.decode("utf-8"))
    return logSpaceCapacity

def getMemoryUsedPercentMetric():
    cmd = 'free | grep Mem | awk \'{print $3/$2 * 100.0}\''
    output=subprocess.run(cmd, shell=True, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    memUsedPercent = float(output.stdout.decode("utf-8"))
    return memUsedPercent

def publishCustomMetrics():
    runningContainersCount = getRunningContainersCountMetric()
    unhealthyContainersCount = getUnhealthyContainersCountMetric()
    logDiskAvailablePercent = getLogSpaceCapacityMetric()
    memUsedPercent = getMemoryUsedPercentMetric()
    instanceName = urllib.request.urlopen('http://169.254.169.254/latest/meta-data/tags/instance/Name').read().decode()
    instanceID = urllib.request.urlopen('http://169.254.169.254/latest/meta-data/instance-id').read().decode()
    cloudwatch = boto3.client('cloudwatch', region_name='eu-central-1')
    response = cloudwatch.put_metric_data(
        MetricData = [
            {
                'MetricName': 'RunningContainersCount',
                'Dimensions': [
                    {
                        'Name': 'InstanceName',
                        'Value': instanceName
                    },
                    {
                        'Name': 'InstanceID',
                        'Value': instanceID
                    },
                    ],
                    'Unit': 'Count',
                    'Value': runningContainersCount
            },
            {
                'MetricName': 'UnhealthyContainersCount',
                'Dimensions': [
                    {
                        'Name': 'InstanceName',
                        'Value': instanceName
                    },
                    {
                        'Name': 'InstanceID',
                        'Value': instanceID
                    },
                    ],
                    'Unit': 'Count',
                    'Value': unhealthyContainersCount
            },
            {
                'MetricName': 'LogDiskAvailablePercent',
                'Dimensions': [
                    {
                        'Name': 'InstanceName',
                        'Value': instanceName
                    },
                    {
                        'Name': 'InstanceID',
                        'Value': instanceID
                    },
                    ],
                    'Unit': 'Percent',
                    'Value': logDiskAvailablePercent
            },
            {
                'MetricName': 'MemoryUsedPercent',
                'Dimensions': [
                    {
                        'Name': 'InstanceName',
                        'Value': instanceName
                    },
                    {
                        'Name': 'InstanceID',
                        'Value': instanceID
                    },
                    ],
                    'Unit': 'Percent',
                    'Value': memUsedPercent
            }
            ],
            Namespace = 'APS-CustomMetrics')
    print(response)

publishCustomMetrics()

import boto3
import datetime
import time

# Initialize the EC2 client (make sure your AWS CLI is configured)
ec2 = boto3.client('ec2', region_name='ap-southeast-1')  # Change to your region

def terminate_idle_instances(max_runtime_hours=2):
    """
    Security Automation Script:
    1. Lists all running EC2 instances.
    2. If an instance has been running longer than 'max_runtime_hours', terminate it.
    3. Prints a log of all actions.
    """
    print(f"--- EC2 Security Guardian: Scanning for idle instances ---")
    print(f"Current Time: {datetime.datetime.now()}")

    # Describe all running instances
    try:
        response = ec2.describe_instances(Filters=[{'Name': 'instance-state-name', 'Values': ['running']}])
    except Exception as e:
        print(f"ERROR: Failed to connect to AWS. Check your credentials. Error: {e}")
        return

    instances_found = 0
    instances_terminated = 0

    for reservation in response['Reservations']:
        for instance in reservation['Instances']:
            instance_id = instance['InstanceId']
            launch_time = instance['LaunchTime']
            current_time = datetime.datetime.now(launch_time.tzinfo) # Handle timezone awareness

            runtime = (current_time - launch_time).total_seconds() / 3600.0  # Hours
            instances_found += 1

            print(f"Instance ID: {instance_id}, Launch Time: {launch_time}, Runtime: {runtime:.2f} hours")

            # If runtime exceeds the limit, TERMINATE IT
            if runtime > max_runtime_hours:
                print(f"⚠️  ALERT: Instance {instance_id} has been running for {runtime:.2f} hours (exceeds {max_runtime_hours} hour limit).")
                try:
                    ec2.terminate_instances(InstanceIds=[instance_id])
                    print(f"✅ ACTION TAKEN: Instance {instance_id} terminated successfully.")
                    instances_terminated += 1
                except Exception as e:
                    print(f"❌ ERROR: Failed to terminate {instance_id}. Error: {e}")
            else:
                print(f"✅ Instance {instance_id} is within safe limits.")

    print(f"\n--- Scan Complete ---")
    print(f"Total Running Instances Found: {instances_found}")
    print(f"Total Instances Terminated: {instances_terminated}")

if __name__ == "__main__":
    # Call the function. You can change the max_runtime_hours value.
    terminate_idle_instances(max_runtime_hours=2)
#!/usr/bin/env python
import argparse
import json
import subprocess
import sys

from operator import itemgetter
from .common import load_config


def terminate_cluster(args, confirm=False):
    args = load_config(args)
    query_command = """
    AWS_ACCESS_KEY_ID="{}" AWS_SECRET_ACCESS_KEY="{}" \
    aws ec2 describe-instances \
        --region {} \
        --filter Name=tag:cluster-name,Values={} \
        --query 'Reservations[*].Instances[*].[State.Name, InstanceId]'
    """.format(
        args["aws_access_key_id"], args["aws_secret_access_key"], args["region"], args["name"])
    result = subprocess.run(query_command, shell=True, check=True, stdout=subprocess.PIPE)
    output = result.stdout
    all_status = json.loads(output)
    if len(all_status) == 0:
        print("No cluster found with the name '{}'. Quit.".format(args["name"]))
        return
    if len(all_status) > 1:
        print("More than 1 cluster found with the name '{}'. ".format(args["name"]) +
              "They will all be terminated (if proceed).")

    total = sum([len([t for t in status if t[0] != "terminated"]) for status in all_status])
    if total == 0:
        print("No running instance found in the cluster(s) '{}'. Quit.".format(args["name"]))
        return
    if confirm:
        confirm_msg = input("Shutting down {} instances in the cluster(s) '{}'. "
                        "Are you sure? (y/N) ".format(total, args["name"]))
        if confirm_msg.strip().lower() != 'y':
            print("Operation cancelled. Nothing is changed. Quit.")
            return

    term_command = ""
    for status in all_status:
        ids = ' '.join(map(itemgetter(1), status))
        term_command += """
        AWS_ACCESS_KEY_ID="{}" AWS_SECRET_ACCESS_KEY="{}" \
            aws ec2 terminate-instances --region {} --instance-ids {};
        """.format(args["aws_access_key_id"], args["aws_secret_access_key"], args["region"], ids)
    p = subprocess.run(term_command, shell=True, check=True, stdout=subprocess.PIPE)
    for s in p.stdout.split(b"\n}"):
        if s.strip():
            output = json.loads(s + b'}')
            for instance in output["TerminatingInstances"]:
                print("{} ({})".format(instance["InstanceId"], instance["CurrentState"]["Name"]))
    print("Done.")


def main_terminate_cluster():
    parser = argparse.ArgumentParser(
        description="Terminate a cluster",
        usage="aws-jupyter config <args>",
    )
    parser.add_argument("--name",
                        required=False,
                        help="cluster name")
    parser.add_argument("--region",
                        help="Region name")
    parser.add_argument("--credential",
                        help="path to the credential file")
    args = vars(parser.parse_args(sys.argv[2:]))
    terminate_cluster(args, confirm=True)


if __name__ == '__main__':
    main_terminate_cluster()

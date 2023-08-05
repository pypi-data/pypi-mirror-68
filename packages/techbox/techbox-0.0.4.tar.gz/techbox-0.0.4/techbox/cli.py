"""Console script for techbox."""
import sys

import fire

from .cloud.aws.monitor import Billing
from .snippets import print_snippet, get_snippet
from .boto3_wrapper import Boto3Wrapper
from .git import GitProjects


class TechboxCli:

    @staticmethod
    def snippet(path, from_line, to_line):
        snippet = get_snippet(path, from_line, to_line)
        print_snippet(snippet)

    project = GitProjects()

    @staticmethod
    def aws_instances_info(fields=None):
        boto3_wrapper = Boto3Wrapper()
        if fields:
            boto3_wrapper.describe_instances_from_fields(fields)
        else:
            boto3_wrapper.describe_instances_basic()

    @staticmethod
    def aws_daily_cost():
        billing = Billing()
        print(billing.get_daily_blended_cost())

    @staticmethod
    def aws_monthly_cost():
        billing = Billing()
        print(billing.get_monthly_blended_cost())


def ep():
    fire.Fire(TechboxCli)

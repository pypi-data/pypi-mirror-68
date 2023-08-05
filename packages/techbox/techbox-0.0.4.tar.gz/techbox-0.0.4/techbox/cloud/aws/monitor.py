import datetime
import boto3


class Billing:

    def __init__(self):
        self.client = boto3.client('ce')
        self.aws_fmt = '%Y-%m-%d'

    def filter_blended_cost_amount(self, response):
        try:
            r = response['ResultsByTime'][0]['Total']['BlendedCost']['Amount']
        except KeyError:
            # !! Should be replaced by logging
            print('An error occured while processing response')
            print(response)

        return r

    def get_basic_cost(self, datetime_objects, granularity):

        dates = [date.strftime(self.aws_fmt) for date in datetime_objects]

        time_period = {'Start': dates[0], 'End': dates[1]}
        metrics = ['BlendedCost']

        response = self.client.get_cost_and_usage(
                        TimePeriod=time_period,
                        Granularity=granularity,
                        Metrics=metrics,)

        return self.filter_blended_cost_amount(response=response)

    def get_daily_blended_cost(self):
        now = datetime.datetime.now()
        yesterday = now-datetime.timedelta(days=1)

        response = self.get_basic_cost([yesterday, now], 'DAILY')
        return response

    def get_monthly_blended_cost(self):
        now = datetime.datetime.now()
        month_start = now.replace(day=1)

        response = self.get_basic_cost([month_start, now], 'MONTHLY')
        return response

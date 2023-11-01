import unittest
from unittest.mock import patch, Mock
import lambda_function.costs as costs

class TestLambdaFunction(unittest.TestCase):

    @patch('lambda_function.costs.boto3.client')
    def test_lambda_handler(self, mock_client):
        # Mock the response from the AWS Cost Explorer API
        mock_ce = Mock()
        mock_ce.get_cost_and_usage.return_value = {
            'ResultsByTime': [
                {
                    'TimePeriod': {'Start': '2023-10-29', 'End': '2023-10-30'},
                    'Total': {'BlendedCost': {'Amount': '0.92', 'Unit': 'USD'}},
                    'Groups': [],
                    'Estimated': True
                }
            ]
        }
        mock_client.side_effect = [mock_ce]

        # Mock the send_sns_message function to check if it's called
        with patch('lambda_function.costs.send_sns_message') as mock_send_sns:
            costs.lambda_handler({}, {})
            mock_send_sns.assert_called_once()
            
if __name__ == '__main__':
    unittest.main()

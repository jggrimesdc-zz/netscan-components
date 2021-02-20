""" Dummy client for boto3 """


class DummyClient(object):
    """
    A Dummy Client. All attributes/methods redirect to the `DummyClient.do_nothing` method, which
    ignores all arguments except a single keyword argument: `return_value`. If `return_value` is

    # Create a dummy client:
    # >>> from resources.dummy_boto3_client import DummyClient
    # >>> client = DummyClient('s3')

    # Call a method the client would have:
    # >>> client.upload_file('tmp/file_name.txt', 'some-bucket', 'data/file_name.txt')
    {'statusCode': 200}

    # With a return value: 
    # >>> client.list_buckets(return_value=['bucket-a','bucket-b'])
    ['bucket-a', 'bucket-b']
    """
    default_return_value = {
        'statusCode': 200
    }

    def __init__(self, client_name, *args, **kwargs):
        self.client_name = client_name

    def do_nothing(self, *args, return_value=None, return_none=False, **kwargs):
        """
        Does nothing, then returns:
            - `None` if `return_none` is True, 
            - `return_value` if `return_value` is not None
            - `DummyClient.return_value` if neither `return_none` or `return_value` are set

        To change the default return value, you can change the `default_return_value` property on 
        a client instance:

        # >>> client = DummyClient('lambda')
        # >>> client.default_return_value = True
        # >>> client.invoke_function('a')
        True
        """

        if return_none:
            return None
        elif return_value is not None:
            return return_value
        return self.default_return_value

    def __getattr__(self, attr):
        """ Overrides attribute finder to always return `DummyClient.do_nothing` """
        if attr == '__str__':
            return str(self)
        if attr == '__repr__':
            return repr(self)
        return self.do_nothing

    def __str__(self):
        return f"Dummy boto3 {self.client_type} client."

    def __repr__(self):
        return f"DummyClient({self.client_type})"

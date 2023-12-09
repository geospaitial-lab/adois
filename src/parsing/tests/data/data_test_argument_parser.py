import argparse

data_test_parse_integration = (
    (['path/to/config.yaml'],
     argparse.Namespace(path_config='path/to/config.yaml',
                        debug=False)),
    (['path/to/config.yaml', '-d'],
     argparse.Namespace(path_config='path/to/config.yaml',
                        debug=True)),
    (['path/to/config.yaml', '--debug'],
     argparse.Namespace(path_config='path/to/config.yaml',
                        debug=True)))

data_test_parse_SystemExit_integration = (
    ([],
     'the following arguments are required: path_config'),
    (['path/to/config.yaml', '-i'],
     'unrecognized arguments: -i'))

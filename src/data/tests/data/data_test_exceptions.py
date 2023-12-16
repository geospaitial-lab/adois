data_test_WMSEPSGCodeError = (
    [((0, [1]),
      r'Invalid epsg_code in the config!\n'
      'Expected 1, got 0 instead.'),
     ((0, [1, 2]),
      r'Invalid epsg_code in the config!\n'
      'Expected 1 or 2, got 0 instead.'),
     ((0, [1, 2, 3]),
      r'Invalid epsg_code in the config!\n'
      'Expected 1, 2 or 3, got 0 instead.')])

data_test_WMSLayerError = (
    [(('z', ['a']),
      r'Invalid layer in the config!\n'
      'Expected a, got z instead.'),
     (('z', ['a', 'b']),
      r'Invalid layer in the config!\n'
      'Expected a or b, got z instead.'),
     (('z', ['a', 'b', 'c']),
      r'Invalid layer in the config!\n'
      'Expected a, b or c, got z instead.')])

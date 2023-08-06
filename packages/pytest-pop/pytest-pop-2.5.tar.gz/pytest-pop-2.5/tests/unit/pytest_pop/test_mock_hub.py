def test_mock_hub(mock_hub):
    mock_hub.log.debug("item")
    mock_hub.log.debug.assert_called_once_with("item")

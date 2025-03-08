resource "aws_cloudwatch_event_rule" "lambda_parser_schedule" {
  name                = "lambda-parser-specific-times"
  description         = "Triggers Lambda functions at 4:00, 12:00, and 20:00 UTC"
  schedule_expression = "cron(0 4,12,20 * * ? *)"
}

resource "aws_cloudwatch_event_rule" "lambda_headline_collector_schedule" {
  name                = "lambda-collector-specific-times"
  description         = "Triggers Lambda functions at 4:00, 12:00, and 20:00 UTC"
  schedule_expression = "cron(5 4,12,20 * * ? *)"
}

resource "aws_cloudwatch_event_target" "cnn_parser_scheduler" {
  rule      = aws_cloudwatch_event_rule.lambda_parser_schedule.name
  target_id = aws_lambda_function.cnn_parser.id
  arn       = aws_lambda_function.cnn_parser.arn
}

resource "aws_lambda_permission" "allow_cloudwatch_cnn" {
  statement_id  = "AllowExecutionFromCloudWatch-${aws_lambda_function.cnn_parser.id}"
  action        = "lambda:InvokeFunction"
  function_name = aws_lambda_function.cnn_parser.function_name
  principal     = "events.amazonaws.com"
  source_arn    = aws_cloudwatch_event_rule.lambda_parser_schedule.arn
}

resource "aws_cloudwatch_event_target" "liga_parser_scheduler" {
  rule      = aws_cloudwatch_event_rule.lambda_parser_schedule.name
  target_id = aws_lambda_function.liga_parser.id
  arn       = aws_lambda_function.liga_parser.arn
}

resource "aws_lambda_permission" "allow_cloudwatch_liga" {
  statement_id  = "AllowExecutionFromCloudWatch-${aws_lambda_function.liga_parser.id}"
  action        = "lambda:InvokeFunction"
  function_name = aws_lambda_function.liga_parser.function_name
  principal     = "events.amazonaws.com"
  source_arn    = aws_cloudwatch_event_rule.lambda_parser_schedule.arn
}


resource "aws_cloudwatch_event_target" "headline_collector_scheduler" {
  rule      = aws_cloudwatch_event_rule.lambda_headline_collector_schedule.name
  target_id = aws_lambda_function.headline_collector.id
  arn       = aws_lambda_function.headline_collector.arn
}

resource "aws_lambda_permission" "allow_cloudwatch_headline_collector" {
  statement_id  = "AllowExecutionFromCloudWatch-${aws_lambda_function.headline_collector.id}"
  action        = "lambda:InvokeFunction"
  function_name = aws_lambda_function.headline_collector.function_name
  principal     = "events.amazonaws.com"
  source_arn    = aws_cloudwatch_event_rule.lambda_headline_collector_schedule.arn
}
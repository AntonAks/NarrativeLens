resource "aws_cloudwatch_event_rule" "lambda_schedule" {
  name                = "lambda-every-6-hours"
  description         = "Triggers multiple Lambda functions every 6 hours"
  schedule_expression = "rate(6 hours)"
}

resource "aws_cloudwatch_event_target" "cnn_parser_scheduler" {
  rule      = aws_cloudwatch_event_rule.lambda_schedule.name
  target_id = aws_lambda_function.cnn_parser.id
  arn       = aws_lambda_function.cnn_parser.arn
}

resource "aws_cloudwatch_event_target" "liga_parser_scheduler" {
  rule      = aws_cloudwatch_event_rule.lambda_schedule.name
  target_id = aws_lambda_function.liga_parser.id
  arn       = aws_lambda_function.liga_parser.arn
}

resource "aws_lambda_permission" "allow_cloudwatch_cnn" {
  statement_id  = "AllowExecutionFromCloudWatch-${aws_lambda_function.cnn_parser.id}"
  action        = "lambda:InvokeFunction"
  function_name = aws_lambda_function.cnn_parser.function_name
  principal     = "events.amazonaws.com"
  source_arn    = aws_cloudwatch_event_rule.lambda_schedule.arn
}

resource "aws_lambda_permission" "allow_cloudwatch_liga" {
  statement_id  = "AllowExecutionFromCloudWatch-${aws_lambda_function.liga_parser.id}"
  action        = "lambda:InvokeFunction"
  function_name = aws_lambda_function.liga_parser.function_name
  principal     = "events.amazonaws.com"
  source_arn    = aws_cloudwatch_event_rule.lambda_schedule.arn
}
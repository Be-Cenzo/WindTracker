resource "aws_s3_bucket" "test-bucket" {
  bucket = "mybucket"
}

resource "aws_sqs_queue" "sqs_queue" {
  name                        = "sqs_queue"
}

data "aws_iam_policy_document" "assume_role" {
  statement {
    effect = "Allow"

    principals {
      type        = "Service"
      identifiers = ["lambda.amazonaws.com"]
    }

    actions = ["sts:AssumeRole"]
  }
}

resource "aws_iam_role" "iam_for_lambda" {
  name               = "iam_for_lambda"
  assume_role_policy = data.aws_iam_policy_document.assume_role.json
}

data "archive_file" "sqsTrigger" {
  type        = "zip"
  source_file = "../functions/sqsTrigger/sqsTrigger.py"
  output_path = "../functions/sqsTrigger/sqsTrigger.zip"
}

data "archive_file" "prova" {
  type        = "zip"
  source_file = "../functions/ProvaAPI/prova.py"
  output_path = "../functions/ProvaAPI/prova.zip"
}

data "archive_file" "getSensors" {
  type        = "zip"
  source_file = "../functions/getSensors/getSensors.py"
  output_path = "../functions/getSensors/getSensors.zip"
}

data "archive_file" "getDataForSensor" {
  type        = "zip"
  source_file = "../functions/getDataForSensor/getDataForSensor.py"
  output_path = "../functions/getDataForSensor/getDataForSensor.zip"
}

data "archive_file" "sensorError" {
  type        = "zip"
  source_file = "../functions/sensorError/sensorError.py"
  output_path = "../functions/sensorError/sensorError.zip"
}

resource "aws_lambda_function" "sqsTriggerLambda" {
  # If the file is not in the current working directory you will need to include a
  # path.module in the filename.
  filename      = "../functions/sqsTrigger/sqsTrigger.zip"
  function_name = "sqsTrigger"
  role          = aws_iam_role.iam_for_lambda.arn
  handler       = "sqsTrigger.lambda_handler"

  source_code_hash = data.archive_file.sqsTrigger.output_base64sha256

  runtime = "python3.9"

}

resource "aws_lambda_function" "provaLambda" {
  filename      = "../functions/ProvaAPI/prova.zip"
  function_name = "prova"
  role          = aws_iam_role.iam_for_lambda.arn
  handler       = "prova.lambda_handler"

  source_code_hash = data.archive_file.prova.output_base64sha256

  runtime = "python3.9"

}

resource "aws_lambda_function" "getSensors" {
  filename      = "../functions/getSensors/getSensors.zip"
  function_name = "getSensors"
  role          = aws_iam_role.iam_for_lambda.arn
  handler       = "getSensors.lambda_handler"

  source_code_hash = data.archive_file.getSensors.output_base64sha256

  runtime = "python3.9"

}

resource "aws_lambda_function" "getDataForSensor" {
  filename      = "../functions/getDataForSensor/getDataForSensor.zip"
  function_name = "getDataForSensor"
  role          = aws_iam_role.iam_for_lambda.arn
  handler       = "getDataForSensor.lambda_handler"

  source_code_hash = data.archive_file.getDataForSensor.output_base64sha256

  runtime = "python3.9"

}

resource "aws_lambda_function" "sensorError" {
  filename      = "../functions/sensorError/sensorError.zip"
  function_name = "sensorError"
  role          = aws_iam_role.iam_for_lambda.arn
  handler       = "sensorError.lambda_handler"

  source_code_hash = data.archive_file.sensorError.output_base64sha256

  runtime = "python3.9"

}

resource "aws_lambda_event_source_mapping" "event_source_mapping" {
  event_source_arn = "${aws_sqs_queue.sqs_queue.arn}"
  enabled          = true
  function_name    = "${aws_lambda_function.sqsTriggerLambda.arn}"
  batch_size       = 5
}

# API Gateway
resource "aws_api_gateway_rest_api" "api" {
  name = "myapi"
}

resource "aws_api_gateway_resource" "resource" {
  path_part   = "getSensors"
  parent_id   = aws_api_gateway_rest_api.api.root_resource_id
  rest_api_id = aws_api_gateway_rest_api.api.id
}

resource "aws_api_gateway_resource" "getDataForSensorResource" {
  path_part   = "getDataForSensor"
  parent_id   = aws_api_gateway_rest_api.api.root_resource_id
  rest_api_id = aws_api_gateway_rest_api.api.id
}

resource "aws_api_gateway_method" "method" {
  rest_api_id   = aws_api_gateway_rest_api.api.id
  resource_id   = aws_api_gateway_resource.resource.id
  http_method   = "GET"
  authorization = "NONE"
}

resource "aws_api_gateway_method" "getDataForSensorMethod" {
  rest_api_id   = aws_api_gateway_rest_api.api.id
  resource_id   = aws_api_gateway_resource.getDataForSensorResource.id
  http_method   = "GET"
  authorization = "NONE"
}

resource "aws_api_gateway_integration" "integration" {
  rest_api_id             = aws_api_gateway_rest_api.api.id
  resource_id             = aws_api_gateway_resource.resource.id
  http_method             = aws_api_gateway_method.method.http_method
  integration_http_method = "POST"
  type                    = "AWS_PROXY"
  uri                     = aws_lambda_function.getSensors.invoke_arn
}

resource "aws_api_gateway_integration" "GDFSintegration" {
  rest_api_id             = aws_api_gateway_rest_api.api.id
  resource_id             = aws_api_gateway_resource.getDataForSensorResource.id
  http_method             = aws_api_gateway_method.getDataForSensorMethod.http_method
  integration_http_method = "POST"
  type                    = "AWS_PROXY"
  uri                     = aws_lambda_function.getDataForSensor.invoke_arn
}

resource "aws_api_gateway_deployment" "deploy" {
  rest_api_id = aws_api_gateway_rest_api.api.id

  triggers = {
    # NOTE: The configuration below will satisfy ordering considerations,
    #       but not pick up all future REST API changes. More advanced patterns
    #       are possible, such as using the filesha1() function against the
    #       Terraform configuration file(s) or removing the .id references to
    #       calculate a hash against whole resources. Be aware that using whole
    #       resources will show a difference after the initial implementation.
    #       It will stabilize to only change when resources change afterwards.
    redeployment = sha1(jsonencode([
      aws_api_gateway_resource.resource.id,
      aws_api_gateway_method.method.id,
      aws_api_gateway_integration.integration.id,
      aws_api_gateway_resource.getDataForSensorResource.id,
      aws_api_gateway_method.getDataForSensorMethod.id,
      aws_api_gateway_integration.GDFSintegration.id,
    ]))
  }

  lifecycle {
    create_before_destroy = true
  }
}

resource "aws_api_gateway_stage" "stage" {
  deployment_id = aws_api_gateway_deployment.deploy.id
  rest_api_id   = aws_api_gateway_rest_api.api.id
  stage_name    = "api"
}

resource "aws_sns_topic" "errors_topic" {
    name = "errors-topic"
    display_name = "errors-topic"
}

resource "aws_sns_topic_subscription" "errors_topic_email" {
    topic_arn = "${aws_sns_topic.errors_topic.arn}"
    protocol  = "email"
    endpoint  = "infra-mantainer@windtracker.com"
}

resource "aws_sns_topic_subscription" "errors_topic_lambda" {
    topic_arn = "${aws_sns_topic.errors_topic.arn}"
    protocol  = "lambda"
    endpoint  = "${aws_lambda_function.sensorError.arn}"
}

resource "aws_lambda_permission" "sensorError_permission" {
    statement_id = "AllowExecutionFromSNS"
    action = "lambda:InvokeFunction"
    function_name = "${aws_lambda_function.sensorError.arn}"
    principal = "sns.amazonaws.com"
    source_arn = "${aws_sns_topic.errors_topic.arn}"
}
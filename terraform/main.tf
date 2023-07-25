resource "aws_sqs_queue" "sqs_queue" {
  name = "sqs_queue"
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

data "archive_file" "getDataForSensor" {
  type        = "zip"
  source_file = "../functions/getDataForSensor/getDataForSensor.py"
  output_path = "../functions/getDataForSensor/getDataForSensor.zip"
}

data "archive_file" "localSearch" {
  type        = "zip"
  source_file = "../functions/localSearch/localSearch.py"
  output_path = "../functions/localSearch/localSearch.zip"
}

data "archive_file" "subscribeSensor" {
  type        = "zip"
  source_file = "../functions/subscribeSensor/subscribeSensor.py"
  output_path = "../functions/subscribeSensor/subscribeSensor.zip"
}

data "archive_file" "sensorError" {
  type        = "zip"
  source_file = "../functions/sensorError/sensorError.py"
  output_path = "../functions/sensorError/sensorError.zip"
}

data "archive_file" "fixSensor" {
  type        = "zip"
  source_file = "../functions/fixSensor/fixSensor.py"
  output_path = "../functions/fixSensor/fixSensor.zip"
}

resource "aws_lambda_function" "sqsTriggerLambda" {
  filename      = "../functions/sqsTrigger/sqsTrigger.zip"
  function_name = "sqsTrigger"
  role          = aws_iam_role.iam_for_lambda.arn
  handler       = "sqsTrigger.lambda_handler"

  source_code_hash = data.archive_file.sqsTrigger.output_base64sha256

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

resource "aws_lambda_function" "localSearch" {
  filename      = "../functions/localSearch/localSearch.zip"
  function_name = "localSearch"
  role          = aws_iam_role.iam_for_lambda.arn
  handler       = "localSearch.lambda_handler"

  source_code_hash = data.archive_file.localSearch.output_base64sha256

  runtime = "python3.9"

}

resource "aws_lambda_function" "subscribeSensor" {
  filename      = "../functions/subscribeSensor/subscribeSensor.zip"
  function_name = "subscribeSensor"
  role          = aws_iam_role.iam_for_lambda.arn
  handler       = "subscribeSensor.lambda_handler"

  source_code_hash = data.archive_file.subscribeSensor.output_base64sha256

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

resource "aws_lambda_function" "fixSensor" {
  filename      = "../functions/fixSensor/fixSensor.zip"
  function_name = "fixSensor"
  role          = aws_iam_role.iam_for_lambda.arn
  handler       = "fixSensor.lambda_handler"

  source_code_hash = data.archive_file.fixSensor.output_base64sha256

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
  name = "api"
  provisioner "local-exec" {
    command = "python rest-file.py ${self.id}"
  }
}

resource "aws_api_gateway_resource" "getDataForSensorResource" {
  path_part   = "getDataForSensor"
  parent_id   = aws_api_gateway_rest_api.api.root_resource_id
  rest_api_id = aws_api_gateway_rest_api.api.id
}

resource "aws_api_gateway_resource" "localSearchResource" {
  path_part   = "localSearch"
  parent_id   = aws_api_gateway_rest_api.api.root_resource_id
  rest_api_id = aws_api_gateway_rest_api.api.id
}

resource "aws_api_gateway_resource" "subscribeSensorResource" {
  path_part   = "subscribeSensor"
  parent_id   = aws_api_gateway_rest_api.api.root_resource_id
  rest_api_id = aws_api_gateway_rest_api.api.id
}

resource "aws_api_gateway_resource" "fixSensorResource" {
  path_part   = "fixSensor"
  parent_id   = aws_api_gateway_rest_api.api.root_resource_id
  rest_api_id = aws_api_gateway_rest_api.api.id
}

resource "aws_api_gateway_method" "getDataForSensorMethod" {
  rest_api_id   = aws_api_gateway_rest_api.api.id
  resource_id   = aws_api_gateway_resource.getDataForSensorResource.id
  http_method   = "GET"
  authorization = "NONE"
}

resource "aws_api_gateway_method" "localSearchMethod" {
  rest_api_id   = aws_api_gateway_rest_api.api.id
  resource_id   = aws_api_gateway_resource.localSearchResource.id
  http_method   = "POST"
  authorization = "NONE"
}

resource "aws_api_gateway_method" "subscribeSensorMethod" {
  rest_api_id   = aws_api_gateway_rest_api.api.id
  resource_id   = aws_api_gateway_resource.subscribeSensorResource.id
  http_method   = "POST"
  authorization = "NONE"
}

resource "aws_api_gateway_method" "fixSensorMethod" {
  rest_api_id   = aws_api_gateway_rest_api.api.id
  resource_id   = aws_api_gateway_resource.fixSensorResource.id
  http_method   = "POST"
  authorization = "NONE"
}

resource "aws_api_gateway_integration" "GDFSintegration" {
  rest_api_id             = aws_api_gateway_rest_api.api.id
  resource_id             = aws_api_gateway_resource.getDataForSensorResource.id
  http_method             = aws_api_gateway_method.getDataForSensorMethod.http_method
  integration_http_method = "POST"
  type                    = "AWS_PROXY"
  uri                     = aws_lambda_function.getDataForSensor.invoke_arn
}


resource "aws_api_gateway_integration" "LSintegration" {
  rest_api_id             = aws_api_gateway_rest_api.api.id
  resource_id             = aws_api_gateway_resource.localSearchResource.id
  http_method             = aws_api_gateway_method.localSearchMethod.http_method
  integration_http_method = "POST"
  type                    = "AWS_PROXY"
  uri                     = aws_lambda_function.localSearch.invoke_arn
}

resource "aws_api_gateway_integration" "SSintegration" {
  rest_api_id             = aws_api_gateway_rest_api.api.id
  resource_id             = aws_api_gateway_resource.subscribeSensorResource.id
  http_method             = aws_api_gateway_method.subscribeSensorMethod.http_method
  integration_http_method = "POST"
  type                    = "AWS_PROXY"
  uri                     = aws_lambda_function.subscribeSensor.invoke_arn
}

resource "aws_api_gateway_integration" "FSintegration" {
  rest_api_id             = aws_api_gateway_rest_api.api.id
  resource_id             = aws_api_gateway_resource.fixSensorResource.id
  http_method             = aws_api_gateway_method.fixSensorMethod.http_method
  integration_http_method = "POST"
  type                    = "AWS_PROXY"
  uri                     = aws_lambda_function.fixSensor.invoke_arn
}


resource "aws_api_gateway_deployment" "deploy" {
  rest_api_id = aws_api_gateway_rest_api.api.id

  triggers = {
    redeployment = sha1(jsonencode([
      aws_api_gateway_resource.getDataForSensorResource.id,
      aws_api_gateway_method.getDataForSensorMethod.id,
      aws_api_gateway_integration.GDFSintegration.id,
      aws_api_gateway_resource.localSearchResource.id,
      aws_api_gateway_method.localSearchMethod.id,
      aws_api_gateway_integration.LSintegration.id,
      aws_api_gateway_resource.subscribeSensorResource.id,
      aws_api_gateway_method.subscribeSensorMethod.id,
      aws_api_gateway_integration.SSintegration.id,
      aws_api_gateway_resource.fixSensorResource.id,
      aws_api_gateway_method.fixSensorMethod.id,
      aws_api_gateway_integration.FSintegration.id,
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

output "rest-api-id"{
    description = "rest api id"
    value = aws_api_gateway_rest_api.api.id
}
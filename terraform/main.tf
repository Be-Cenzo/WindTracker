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

resource "aws_lambda_function" "sqsTriggerLambda" {
  # If the file is not in the current working directory you will need to include a
  # path.module in the filename.
  filename      = "../functions/sqsTrigger/sqsTrigger.zip"
  function_name = "sqsTrigger"
  role          = aws_iam_role.iam_for_lambda.arn
  handler       = "sqsTrigger.lambda_handler"

  source_code_hash = data.archive_file.sqsTrigger.output_base64sha256

  runtime = "python3.10"

}

resource "aws_lambda_function" "provaLambda" {
  filename      = "../functions/ProvaAPI/prova.zip"
  function_name = "prova"
  role          = aws_iam_role.iam_for_lambda.arn
  handler       = "prova.lambda_handler"

  source_code_hash = data.archive_file.sqsTrigger.output_base64sha256

  runtime = "python3.10"

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
  path_part   = "resource"
  parent_id   = aws_api_gateway_rest_api.api.root_resource_id
  rest_api_id = aws_api_gateway_rest_api.api.id
}

resource "aws_api_gateway_method" "method" {
  rest_api_id   = aws_api_gateway_rest_api.api.id
  resource_id   = aws_api_gateway_resource.resource.id
  http_method   = "GET"
  authorization = "NONE"
}

resource "aws_api_gateway_integration" "integration" {
  rest_api_id             = aws_api_gateway_rest_api.api.id
  resource_id             = aws_api_gateway_resource.resource.id
  http_method             = aws_api_gateway_method.method.http_method
  integration_http_method = "POST"
  type                    = "AWS_PROXY"
  uri                     = aws_lambda_function.provaLambda.invoke_arn
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
# Clay Webhook API Wrapper

This Flask application serves as an API wrapper to turn any Clay Table into an API.

This will only work on Clay tables that ingest data via Webhooks and complete with the HTTP API tool in Clay.

## Setup

1. Set the `INTERNAL_API_KEY` in the Secrets tool
2. Set the `CLAY_TABLE_WEBHOOK_URL` in your environment variables.

Once your Clay Table and endpoint logic is set up, head to Deployments tab in Replit and deploy this Flask app as a production API in two clicks.

Autoscale deployment type is recommended.

## API Endpoints

### POST /clay/api-start

Initiates a Clay Webhook Table request.

Headers:
- `Authorization`: Your internal API key

Body:
- JSON payload to be sent to Clay table

### POST /clay/api-complete

Endpoint for Clay to send back the completed request data.

Headers:
- `Authorization`: Your API key

Body:
- JSON payload including `request_id` and response data

## Running the Application

To run this app in a development environment, hit the green `Run` (shortcut Cmd + Enter) button at the top of the Workspace.

You can find your development base URL in the Webview or in the Networking tab.

## Hosting the Application

To host this as a production API for your team to use, head to Replit Deployments (under Tools in Replit) and set up an Autoscale deployment in a few clicks.


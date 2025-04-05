# Social Media API Documentation

## Base URL

```
https://your-app-name.herokuapp.com/api/v1/
```

## Authentication

All authenticated endpoints require a Token in the header:

```
Authorization: Token your-auth-token
```

To obtain a token, use the login endpoint.

## Endpoints

### Authentication

#### Register

- **POST** `/accounts/register/`
- Request Body:

```json
{
  "username": "string",
  "email": "string",
  "password": "string"
}
```

#### Login

- **POST** `/accounts/login/`
- Request Body:

```json
{
  "username": "string",
  "password": "string"
}
```

- Response includes authentication token

### Posts

#### List Posts

- **GET** `/posts/`
- Query Parameters:
  - `page`: Page number for pagination
  - `search`: Search posts by content
  - `ordering`: Sort by created_at (asc/desc)

#### Create Post

- **POST** `/posts/`
- Auth Required: Yes
- Request Body:

```json
{
  "content": "string",
  "image": "file (optional)"
}
```

#### Get Post

- **GET** `/posts/{id}/`

#### Update Post

- **PUT/PATCH** `/posts/{id}/`
- Auth Required: Yes (must be post owner)

#### Delete Post

- **DELETE** `/posts/{id}/`
- Auth Required: Yes (must be post owner)

#### Like/Unlike Post

- **POST** `/posts/{id}/like/`
- **POST** `/posts/{id}/unlike/`
- Auth Required: Yes

### Comments

#### List Comments

- **GET** `/comments/`
- Query Parameters:
  - `post`: Filter by post ID
  - `page`: Page number

#### Create Comment

- **POST** `/comments/`
- Auth Required: Yes
- Request Body:

```json
{
  "post": "integer",
  "content": "string"
}
```

### Feed

#### Get User Feed

- **GET** `/feed/`
- Auth Required: Yes
- Query Parameters:
  - `page`: Page number

### Notifications

#### List Notifications

- **GET** `/notifications/`
- Auth Required: Yes
- Query Parameters:
  - `read`: Filter by read status (true/false)
  - `page`: Page number

## Error Responses

```json
{
  "detail": "Error message"
}
```

## Rate Limiting

- Authenticated requests: 1000 per hour
- Anonymous requests: 100 per hour

## Best Practices

1. Always validate response status codes
2. Include authentication token for authenticated endpoints
3. Use pagination for large datasets
4. Handle errors gracefully
5. Keep track of rate limits

## Testing

You can test the API using tools like:

- Postman
- cURL
- HTTPie

Example cURL request:

```bash
curl -H "Authorization: Token YOUR_TOKEN" https://your-app-name.herokuapp.com/api/v1/feed/
```

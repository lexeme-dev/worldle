// This file is auto-generated by @hey-api/openapi-ts

export const HTTPValidationErrorSchema = {
  properties: {
    detail: {
      items: {
        $ref: "#/components/schemas/ValidationError",
      },
      type: "array",
      title: "Detail",
    },
  },
  type: "object",
  title: "HTTPValidationError",
} as const;

export const ProxiedStreamReadSchema = {
  properties: {
    id: {
      type: "integer",
      title: "Id",
    },
    scraped_stream_id: {
      type: "integer",
      title: "Scraped Stream Id",
    },
    status: {
      type: "string",
      title: "Status",
    },
    created_at: {
      type: "string",
      format: "date-time",
      title: "Created At",
    },
    updated_at: {
      type: "string",
      format: "date-time",
      title: "Updated At",
    },
    scraped_stream: {
      $ref: "#/components/schemas/ScrapedStreamRead",
    },
  },
  type: "object",
  required: [
    "id",
    "scraped_stream_id",
    "status",
    "created_at",
    "updated_at",
    "scraped_stream",
  ],
  title: "ProxiedStreamRead",
} as const;

export const ScrapedStreamReadSchema = {
  properties: {
    id: {
      type: "integer",
      title: "Id",
    },
    third_party_id: {
      type: "integer",
      title: "Third Party Id",
    },
    id_in_third_party: {
      type: "string",
      title: "Id In Third Party",
    },
    title: {
      type: "string",
      title: "Title",
    },
    webpage_url: {
      type: "string",
      title: "Webpage Url",
    },
    last_seen_at: {
      anyOf: [
        {
          type: "string",
          format: "date-time",
        },
        {
          type: "null",
        },
      ],
      title: "Last Seen At",
    },
    created_at: {
      type: "string",
      format: "date-time",
      title: "Created At",
    },
    updated_at: {
      type: "string",
      format: "date-time",
      title: "Updated At",
    },
  },
  type: "object",
  required: [
    "id",
    "third_party_id",
    "id_in_third_party",
    "title",
    "webpage_url",
    "last_seen_at",
    "created_at",
    "updated_at",
  ],
  title: "ScrapedStreamRead",
} as const;

export const ValidationErrorSchema = {
  properties: {
    loc: {
      items: {
        anyOf: [
          {
            type: "string",
          },
          {
            type: "integer",
          },
        ],
      },
      type: "array",
      title: "Location",
    },
    msg: {
      type: "string",
      title: "Message",
    },
    type: {
      type: "string",
      title: "Error Type",
    },
  },
  type: "object",
  required: ["loc", "msg", "type"],
  title: "ValidationError",
} as const;

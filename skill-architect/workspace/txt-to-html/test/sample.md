# API仕様書

## エンドポイント一覧

| Method | Path | Description |
|--------|------|-------------|
| GET | /api/users | ユーザー一覧取得 |
| POST | /api/users | ユーザー作成 |
| PUT | /api/users/:id | ユーザー更新 |
| DELETE | /api/users/:id | ユーザー削除 |

## 認証

すべてのエンドポイントで **Bearer Token** が必要です。

> 注意: トークンの有効期限は *24時間* です。期限切れの場合は再取得してください。

## レスポンス例

```json
{
  "id": 1,
  "name": "田中太郎",
  "email": "tanaka@example.com",
  "role": "admin"
}
```

## エラーハンドリング

- `400` Bad Request — リクエストパラメータ不正
- `401` Unauthorized — 認証トークン無効
- `404` Not Found — リソースが存在しない
- `500` Internal Server Error — サーバー内部エラー

package cache

import (
	"context"
	"server-go/pkg/renderx"
)

type IApiCache interface {
	CacheApiResponse(ctx context.Context, key string, data []byte) error
	GetApiCache(ctx context.Context, key string) (*renderx.Response, error)
}

package redisc

import (
	"context"
	"encoding/json"
	"github.com/redis/go-redis/v9"
	"server-go/domain/cache"
	"server-go/pkg/renderx"
	"time"
)

const apiCacheExpired = 10 * time.Second

type ApiCache struct {
	rds *redis.Client
}

func NewApiCache(rds *redis.Client) *ApiCache {
	return &ApiCache{
		rds: rds,
	}
}

// UserRepo implements the repo.UserRepo interface
var _ cache.IApiCache = &ApiCache{}

func (cache *ApiCache) CacheApiResponse(ctx context.Context, key string, data []byte) error {
	return cache.rds.Set(ctx, key, data, apiCacheExpired).Err()
}

func (cache *ApiCache) GetApiCache(ctx context.Context, key string) (*renderx.Response, error) {
	data, err := cache.rds.Get(ctx, key).Result()
	if err != nil {
		if err == redis.Nil {
			return nil, nil
		}
		return nil, err
	}
	var resp renderx.Response
	if err = json.Unmarshal([]byte(data), &resp); err != nil {
		return nil, err
	}
	return &resp, nil
}

package redisc

import (
	"server-go/config"
	"server-go/domain/cache"

	"github.com/redis/go-redis/v9"
)

type Caches struct {
	rds      *redis.Client
	ApiCache cache.IApiCache
}

func NewCaches(redisConf *config.RedisConfig) (*Caches, error) {
	rds := redis.NewClient(&redis.Options{
		Addr:     redisConf.Addr(),
		Password: "",
		DB:       0,
	})

	return &Caches{
		rds:      rds,
		ApiCache: NewApiCache(rds),
	}, nil
}

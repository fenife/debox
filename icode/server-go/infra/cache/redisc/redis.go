package redisc

import (
	"github.com/redis/go-redis/v9"
	"server-go/config"
	"server-go/domain/cache"
)

type Caches struct {
	rds       *redis.Client
	UserCache cache.IUserCache
	ApiCache  cache.IApiCache
}

func NewCaches(redisConf *config.RedisConfig) (*Caches, error) {
	rds := redis.NewClient(&redis.Options{
		Addr:     redisConf.Addr(),
		Password: "",
		DB:       0,
	})

	return &Caches{
		rds:       rds,
		UserCache: NewUserCache(rds),
		ApiCache:  NewApiCache(rds),
	}, nil
}

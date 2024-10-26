package middleware

import (
	"bytes"
	"github.com/gin-gonic/gin"
	"server-go/domain/cache"
	"server-go/pkg/logx"
	"server-go/pkg/renderx"
)

func ApiCacheMiddleware(apiCache cache.IApiCache) gin.HandlerFunc {
	return func(c *gin.Context) {
		key := c.Request.RequestURI
		respData, err := apiCache.GetApiCache(c, key)
		if err != nil {
			logx.Ctx(c).With("error", err).Errorf("get api cache failed")
			renderx.ErrOutput(c, err)
			c.Abort()
			return
		}
		if respData != nil {
			logx.Ctx(c).With("key", key).Infof("get resp from cache")
			renderx.SuccOutput(c, respData)
			c.Abort()
			return
		}

		// 双写
		writer := &bodyLogWriter{body: bytes.NewBufferString(""), ResponseWriter: c.Writer}
		c.Writer = writer

		c.Next()

		if err := apiCache.CacheApiResponse(c, key, writer.body.Bytes()); err != nil {
			logx.Ctx(c).With("error", err).Errorf("cache resp failed")
		}
	}
}

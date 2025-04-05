package middleware

import (
	"github.com/gin-gonic/gin"
	"server-go/domain/cache"
	"server-go/internal/errorx"
	"server-go/internal/gctx"
	"server-go/pkg/logx"
	"server-go/pkg/renderx"
)

func UserAuthMiddleware(userCache cache.IUserCache) gin.HandlerFunc {
	return func(c *gin.Context) {
		userToken := c.GetHeader(gctx.HeaderKeyUserToken)
		user, err := userCache.GetUserByToken(c, userToken)
		if err != nil || !user.IsValid() {
			logx.Ctx(c).With("token", userToken, "error", err).Errorf("user auth failed")
			renderx.ErrOutput(c, errorx.UserAuthFailed)
			c.Abort()
			return
		}

		gctx.SetUserToken(c, userToken)
		gctx.SetUser(c, user)

		c.Next()
	}
}

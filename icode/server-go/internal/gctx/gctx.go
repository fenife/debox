package gctx

import (
	"context"
	"github.com/gin-gonic/gin"
	"server-go/domain/entity"
)

const (
	HeaderKeyReqId     = "X-Request-Id"
	HeaderKeyUserToken = "X-User-Token"
)

const (
	ctxKeyReqId     = "request_id"
	ctxKeyUser      = "user"
	ctxKeyUserToken = "user_token"
)

func SetReqId(ctx *gin.Context, reqId string) {
	ctx.Set(ctxKeyReqId, reqId)
}

func GetReqId(ctx context.Context) (reqId string) {
	if val := ctx.Value(ctxKeyReqId); val != nil {
		reqId, _ = val.(string)
	}
	return
}

func SetUser(ctx *gin.Context, user *entity.User) {
	ctx.Set(ctxKeyUser, user)
}

func GetUser(ctx context.Context) (user *entity.User) {
	if val := ctx.Value(ctxKeyUser); val != nil {
		user, _ = val.(*entity.User)
	}
	return
}

func SetUserToken(ctx *gin.Context, token string) {
	ctx.Set(ctxKeyUserToken, token)
}

func GetUserToken(ctx context.Context) (token string) {
	if val := ctx.Value(ctxKeyUserToken); val != nil {
		token, _ = val.(string)
	}
	return
}

package aservice

import (
	"context"
	"server-go/domain/dservice"
	"server-go/domain/entity"
)

type IUserApp interface {
	GetUserList(ctx context.Context) ([]entity.User, error)
}

type UserApp struct {
	userDomain dservice.IUserDomain
}

func NewUserApp(userDomain dservice.IUserDomain) *UserApp {
	return &UserApp{
		userDomain: userDomain,
	}
}

var _ IUserApp = &UserApp{}

func (app *UserApp) GetUserList(ctx context.Context) ([]entity.User, error) {
	return app.userDomain.GetUserList(ctx)
}

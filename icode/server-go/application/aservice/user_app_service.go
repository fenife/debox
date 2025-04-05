package aservice

import (
	"context"
	"html"
	"server-go/domain/do"
	"server-go/domain/dservice"
	"server-go/domain/entity"
)

type IUserApp interface {
	Signup(ctx context.Context, username, passwd string) (*entity.User, error)
	SignIn(ctx context.Context, username, passwd string) (user *entity.User, signin *do.UserSignInInfo, err error)
	SignOut(ctx context.Context, token string) (err error)
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

// Signup 用户注册
func (app *UserApp) Signup(ctx context.Context, username, passwd string) (*entity.User, error) {
	user := entity.User{
		Name: html.EscapeString(username),
	}
	user.PasswordHash = user.GenPasswordHash(passwd)

	return app.userDomain.Signup(ctx, &user)
}

// SignIn 用户登陆
func (app *UserApp) SignIn(ctx context.Context, username, passwd string) (
	user *entity.User, signin *do.UserSignInInfo, err error) {
	return app.userDomain.SignIn(ctx, username, passwd)
}

// SignOut 用户退出
func (app *UserApp) SignOut(ctx context.Context, token string) (err error) {
	return app.userDomain.SignOut(ctx, token)
}

func (app *UserApp) GetUserList(ctx context.Context) ([]entity.User, error) {
	return app.userDomain.GetUserList(ctx)
}

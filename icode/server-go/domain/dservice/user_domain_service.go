package dservice

import (
	"context"
	"server-go/domain/entity"
	"server-go/domain/repo"
)

type IUserDomain interface {
	GetUserList(ctx context.Context) ([]entity.User, error)
}

type UserDomain struct {
	userRepo repo.IUserRepo
}

func NewUserDomain(userRepo repo.IUserRepo) *UserDomain {
	return &UserDomain{
		userRepo: userRepo,
	}
}

var _ IUserDomain = &UserDomain{}

func (ds *UserDomain) GetUserList(ctx context.Context) ([]entity.User, error) {
	return ds.userRepo.GetUserList(ctx)
}

package repo

import (
	"context"
	"server-go/domain/entity"
)

type IUserRepo interface {
	CreateUser(ctx context.Context, user *entity.User) (*entity.User, error)
	FindByName(ctx context.Context, name string) (*entity.User, error)
	FindById(ctx context.Context, userId uint64) (*entity.User, error)
	GetUserList(ctx context.Context) ([]entity.User, error)
}
